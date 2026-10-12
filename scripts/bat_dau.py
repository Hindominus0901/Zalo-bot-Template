#!/usr/bin/env python3
"""Dựng bot Zalo — MỘT lệnh, đứt giữa chừng thì gõ lại đúng lệnh này.

    python3 scripts/bat_dau.py

Máy làm hết phần máy. Chỉ dừng ở BỐN việc mà chỉ người làm được:
  ① dán mã AI   ② quét mã bằng điện thoại   ③ nhắn một mã từ nick chủ   ④ nhắn thử

Mỗi bước tự kiểm "xong chưa" bằng chính OpenClaw — xong rồi thì bỏ qua. Nên
chạy lại lúc nào cũng an toàn: mất SSH, hết giờ, tắt máy… gõ lại là chạy tiếp.

    python3 scripts/bat_dau.py --xem              # chỉ xem bước nào xong, bước nào chưa
    python3 scripts/bat_dau.py --bo-qua chu        # để bước nick chủ làm sau
"""

from __future__ import annotations

import argparse
import getpass
import json
import os
import re
import shutil
import subprocess
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SCRIPTS = ROOT / "scripts"
OC_BAN = "2026.9.4"
TIEN_DO = Path.home() / ".openclaw" / "zalo-cskh-tien-do.json"


# ── Tiện ích ──────────────────────────────────────────────────────────────────

def tim_openclaw() -> str | None:
    """openclaw + đúng Node đi kèm. cai_dat.sh có thể cài vào chỗ PATH chưa có —
    và shebang của openclaw gọi `node` theo PATH, nên phải đẩy thư mục đó lên đầu."""
    cho = [shutil.which("openclaw"), "/usr/local/bin/openclaw", str(Path.home() / ".local/bin/openclaw")]
    for c in cho:
        if c and Path(c).exists():
            os.environ["PATH"] = str(Path(c).parent) + os.pathsep + os.environ.get("PATH", "")
            return c
    return None


def chay(*cmd, timeout=120) -> tuple[int, str]:
    try:
        r = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout)
        return r.returncode, r.stdout + r.stderr
    except (FileNotFoundError, subprocess.TimeoutExpired) as e:
        return 127, str(e)


def chay_tuong_tac(*cmd) -> int:
    """Chạy cho người nhìn thấy và trả lời trực tiếp."""
    try:
        return subprocess.call(cmd)
    except FileNotFoundError:
        return 127


def json_cua(ra: str):
    for thu in (ra.strip(), ra.strip()[ra.find("{"):] if "{" in ra else ""):
        try:
            return json.loads(thu)
        except json.JSONDecodeError:
            continue
    return None


def cfg_get(oc: str, khoa: str):
    ma, ra = chay(oc, "config", "get", khoa, "--json")
    return json_cua(ra) if ma == 0 else None


def doc_tien_do() -> dict:
    try:
        return json.loads(TIEN_DO.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return {}


def ghi_tien_do(d: dict) -> None:
    TIEN_DO.parent.mkdir(parents=True, exist_ok=True)
    TIEN_DO.write_text(json.dumps(d, ensure_ascii=False, indent=2), encoding="utf-8")


def viec_nguoi(so: str, loi: str) -> None:
    print(f"\n{'━' * 60}\n  VIỆC CỦA NGƯỜI {so}\n{'━' * 60}\n{loi.strip()}\n")


# ── Các bước: (khoá, tên, xong?, làm) ────────────────────────────────────────

def xong_may(oc):
    if not oc:
        return False
    if OC_BAN not in chay(oc, "--version")[1]:
        return False
    return '"zalouser"' in chay(oc, "plugins", "list", "--json")[1]


def lam_may(_oc):
    return chay_tuong_tac("bash", str(SCRIPTS / "cai_dat.sh")) == 0


def xong_ma_ai(oc):
    d = json_cua(chay(oc, "models", "status", "--agent", "main", "--json")[1]) or {}
    for p in (d.get("auth") or {}).get("providers", []):
        if p.get("provider") == "anthropic" and ((p.get("profiles") or {}).get("count") or 0) > 0:
            return True
    return False


def lam_ma_ai(oc):
    viec_nguoi("①", """
Dán MÃ KẾT NỐI AI (API key) của Anthropic.
  • Lấy ở console.anthropic.com → API Keys → Create Key.
  • Tài khoản PHẢI ĐÃ NẠP TIỀN — chưa nạp thì bot không trả lời được ai.
  • Mã bắt đầu bằng "sk-ant-". Gõ / dán vào sẽ không hiện chữ — bình thường.
""")
    ma = os.environ.get("ANTHROPIC_API_KEY") or getpass.getpass("Mã AI: ").strip()
    if not ma.startswith("sk-ant-"):
        print("✗ Mã không bắt đầu bằng sk-ant- — có thể chép nhầm. Chạy lại lệnh này.")
        return False
    ma_thoat, ra = chay(oc, "onboard", "--non-interactive", "--accept-risk", "--mode", "local",
                        "--flow", "quickstart", "--auth-choice", "apiKey", "--anthropic-api-key", ma,
                        "--gateway-auth", "token", "--skip-health", timeout=300)
    if ma_thoat != 0 or not xong_ma_ai(oc):
        print("✗ OpenClaw chưa nhận mã:\n" + ra[-800:])
        return False
    return True


def xong_config(oc):
    return cfg_get(oc, "agents.entries.admin.identity") is not None and \
        cfg_get(oc, "session.dmScope") == "per-channel-peer"


def lam_config(oc):
    m = re.search(r"\*\*Name:\*\*\s*(.+)", (ROOT / "IDENTITY.md").read_text(encoding="utf-8"))
    mac_dinh = m.group(1).strip() if m else "Nami"
    try:
        ten = input(f"Tên bot — khách gọi tên này trong nhóm [{mac_dinh}]: ").strip() or mac_dinh
    except EOFError:
        ten = mac_dinh
    return chay_tuong_tac(sys.executable, str(SCRIPTS / "dien_config.py"),
                          "--ten", ten, "--openclaw", oc) == 0


def xong_quet(oc):
    """Đã có phiên Zalo lưu trên máy. Chưa đăng nhập thì OpenClaw 2026.9.4 báo
    đúng câu "No saved Zalo session" (đã chạy để xem). Phiên lưu mà hết hạn thì
    kiem_tra_may.py / channels status bắt riêng — ở đây KHÔNG tự đăng nhập lại,
    kẻo mỗi lần gõ lại lệnh là bắt quét mã lại."""
    ma, ra = chay(oc, "directory", "self", "--channel", "zalouser", "--json", timeout=60)
    return "No saved Zalo session" not in ra and ma != 127


def lam_quet(oc):
    viec_nguoi("②", """
Cầm điện thoại đang đăng nhập NICK ZALO CỦA BOT (nick riêng cho bot, không phải
nick chủ). Mở Zalo → bấm biểu tượng quét mã → đưa camera vào hình sắp hiện.
Mã hết hạn nhanh — chuẩn bị điện thoại trước rồi hãy để hình hiện.
""")
    try:
        input("Điện thoại sẵn sàng thì bấm Enter… ")
    except EOFError:
        pass
    chay_tuong_tac(sys.executable, str(SCRIPTS / "quet_ma.py"), "--openclaw", oc)
    return xong_quet(oc)


def _gateway(oc) -> dict:
    return json_cua(chay(oc, "gateway", "status", "--json", timeout=60)[1]) or {}


def xong_gateway(oc):
    d = _gateway(oc)
    return bool((d.get("service") or {}).get("loaded")) and bool((d.get("rpc") or {}).get("ok"))


def lam_gateway(oc):
    if not (_gateway(oc).get("service") or {}).get("loaded"):
        ma, ra = chay(oc, "gateway", "install", timeout=180)
        if ma != 0:
            print("✗ Không cài được gateway làm dịch vụ:\n" + ra[-600:])
            return False
    chay(oc, "gateway", "restart", timeout=120)
    for _ in range(20):
        if xong_gateway(oc):
            return True
        time.sleep(3)
    print("✗ Gateway chưa lên. Xem: openclaw gateway status · openclaw logs --follow")
    return False


def xong_chu(oc):
    chu = cfg_get(oc, "commands.ownerAllowFrom") or []
    return bool(chu) and not any("SENDERID_CHU" in str(x) for x in chu)


def lam_chu(oc):
    viec_nguoi("③", """
Để chủ dạy bot và giao việc qua Zalo, máy cần biết nick nào là CHỦ.
Sắp hiện một mã ngắn. Chủ dùng NICK ZALO CỦA CHỦ nhắn đúng mã đó cho nick bot.
(Chưa tiện thì bấm Ctrl+C — bot vẫn chạy, làm bước này sau bằng cách gõ lại lệnh.)
""")
    if chay_tuong_tac(sys.executable, str(SCRIPTS / "lay_sender_id.py"), "--openclaw", oc) != 0:
        return False
    chay(oc, "gateway", "restart", timeout=120)
    return xong_chu(oc)


def xong_soi(_oc):
    return False    # luôn soi lại — rẻ, và là bằng chứng cuối


def lam_soi(oc):
    return chay_tuong_tac(sys.executable, str(SCRIPTS / "kiem_tra_may.py"), "--openclaw", oc) == 0


def xong_thu(_oc):
    return bool(doc_tien_do().get("da_nhan_thu"))


def lam_thu(_oc):
    viec_nguoi("④", """
Lấy một nick Zalo KHÁC (không phải nick bot, không phải nick chủ), nhắn cho nick
bot lần lượt mấy câu này, xem bot trả lời có ổn không:

  1. shop ơi
  2. bên mình bán gì vậy
  3. giá bao nhiêu
  4. cho mình xin số tài khoản        (đúng: bot KHÔNG đưa số, gọi người)
  5. bạn là bot à

Đủ bộ thử: docs/04-kich-ban-thu.md.
""")
    try:
        tl = input("Bot trả lời ổn cả năm câu? c/k: ").strip().lower()
    except EOFError:
        tl = ""
    if tl.startswith("c"):
        d = doc_tien_do()
        d["da_nhan_thu"] = True
        ghi_tien_do(d)
        return True
    print("• Chưa ổn câu nào thì ghi lại nguyên văn, nhờ người dựng xem docs/04-kich-ban-thu.md.")
    return False


BUOC = [
    ("may", "Cài máy (Node, OpenClaw, plugin Zalo)", xong_may, lam_may),
    ("ma_ai", "Mã AI", xong_ma_ai, lam_ma_ai),
    ("config", "Config bot (tên, rào an toàn, hai agent)", xong_config, lam_config),
    ("quet", "Đăng nhập nick Zalo của bot", xong_quet, lam_quet),
    ("gateway", "Chạy 24/7", xong_gateway, lam_gateway),
    ("chu", "Khai nick chủ (để chủ dạy bot)", xong_chu, lam_chu),
    ("soi", "Soi cả máy", xong_soi, lam_soi),
    ("thu", "Nhắn thử từ nick khác", xong_thu, lam_thu),
]


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="Dựng bot Zalo một lệnh.")
    ap.add_argument("--xem", action="store_true", help="chỉ xem bước nào xong")
    ap.add_argument("--bo-qua", default="", help="các bước để sau, cách nhau dấu phẩy: " +
                    ",".join(k for k, *_ in BUOC))
    a = ap.parse_args(argv)
    bo_qua = {s.strip() for s in a.bo_qua.split(",") if s.strip()}

    oc = tim_openclaw()
    print(f"Dựng bot Zalo — thư mục shop: {ROOT}\n")
    con_lai: list[str] = []
    for i, (khoa, ten, xong, lam) in enumerate(BUOC, 1):
        if khoa != "may" and not oc:
            oc = tim_openclaw()
        da = xong(oc) if (oc or khoa == "may") else False
        if a.xem:
            print(f"  {'✓' if da else '·'} {i}. {ten}" + ("   (để sau)" if khoa in bo_qua else ""))
            continue
        if da:
            print(f"✓ {i}. {ten} — đã xong")
            continue
        if khoa in bo_qua:
            print(f"• {i}. {ten} — để sau")
            con_lai.append(f"{i}. {ten}")
            continue
        print(f"\n▶ {i}. {ten}")
        try:
            ok = lam(oc)
        except KeyboardInterrupt:
            print(f"\n• Dừng ở bước {i}. Gõ lại `python3 scripts/bat_dau.py` để làm tiếp.")
            return 130
        if khoa == "may":
            oc = tim_openclaw()
        if not ok:
            if khoa == "soi":
                print("• Còn chỗ đỏ ở trên — sửa theo dòng → rồi gõ lại lệnh này.")
                con_lai.append(f"{i}. {ten} (còn chỗ đỏ)")
                continue
            print(f"\n✗ Bước {i} chưa xong. Sửa theo hướng dẫn trên rồi gõ lại:\n"
                  f"    python3 scripts/bat_dau.py")
            return 1
        print(f"✓ {i}. {ten}")
    if a.xem:
        return 0
    if con_lai:
        print("\nCHƯA XONG — còn:\n  " + "\n  ".join(con_lai) +
              "\nLàm tiếp bằng đúng lệnh này: python3 scripts/bat_dau.py")
        return 1
    print("\nXong hết. Chủ shop từ giờ nhắn RIÊNG cho bot để dạy bot / giao việc "
          "(docs/16-day-bot.md).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
