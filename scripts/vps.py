#!/usr/bin/env python3
"""Coding agent trên máy người dựng điều khiển VPS — người dựng không gõ lệnh nào.

Chạy trên máy người dựng (Windows / Mac / Linux), không phải trên VPS. Cần Python
3.9+ và `ssh` (Windows 10/11, Mac, Linux đều có sẵn). Chỉ dùng thư viện chuẩn.

    python scripts/vps.py khoa                 # tạo chìa khoá SSH, in phần dán vào VPS
    python scripts/vps.py noi 203.0.113.5      # lưu địa chỉ VPS + thử nối
    python scripts/vps.py thu                  # thử nối lại, xem máy
    python scripts/vps.py day-len              # đẩy template lên VPS (~/zalo-bot)
    python scripts/vps.py bat-dau [--da-thu…]  # chạy bat_dau.py --tu-dong trên VPS
    python scripts/vps.py gui-ma-ai --mo       # mở Notepad cho người dán mã AI
    python scripts/vps.py gui-ma-ai --gui      # gửi mã lên VPS, xoá file trên máy này
    python scripts/vps.py lay-qr               # kéo ảnh mã đăng nhập về, mở lên màn hình
    python scripts/vps.py day-so               # đẩy sổ shop (đã phỏng vấn) lên VPS
    python scripts/vps.py keo-so               # kéo sổ trên VPS (chủ đã dạy qua Zalo) về
    python scripts/vps.py chay -- <lệnh>       # chạy một lệnh trong thư mục bot trên VPS

`bat-dau` thoát mã 3 khi tới việc của người. Dòng cuối `TRANG-THAI: {json}` nói
việc gì: ma_ai → gui-ma-ai; quet → lay-qr; chu → đọc mã cho người nhắn; thu →
đọc các câu thử. Người làm xong thì gọi lại `bat-dau`.

Địa chỉ VPS lưu ở `.vps.json` (không commit). Mã AI, ảnh QR không bao giờ in ra
màn hình, không nằm lại trên máy này.
"""

from __future__ import annotations

import argparse
import io
import json
import os
import re
import subprocess
import sys
import tarfile
import tempfile
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(Path(__file__).resolve().parent))
from dong_goi import gom, thanh_khoi  # noqa: E402

CAU_HINH = ROOT / ".vps.json"
KHOA = Path.home() / ".ssh" / "zalo_bot_ed25519"
TAM = Path(tempfile.gettempdir())
FILE_MA = TAM / "zalo-bot-ma-ai.txt"
FILE_QR = TAM / "zalo-bot-ma-dang-nhap.png"
THU_MUC_VPS = "zalo-bot"

# Không bao giờ đẩy lên: bí mật, dữ liệu sống trên máy kia, rác.
BO_THU_MUC = {".git", "__pycache__", ".ban-cu", "node_modules", ".venv", ".pytest_cache"}
BO_FILE = re.compile(r"(?:^|/)(?:\.env|\.vps\.json|secrets[^/]*|[^/]*\.(?:key|pem|pyc))$"
                     r"|^config/openclaw\.da-dien\.json5$")
GIU_TRONG_MEMORY = {"README.md", ".gitkeep", "MAU.md"}


class Loi(Exception):
    pass


# ── Cấu hình + ssh ───────────────────────────────────────────────────────────

def doc_cau_hinh() -> dict:
    try:
        return json.loads(CAU_HINH.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        raise Loi("Chưa có địa chỉ VPS. Chạy: python scripts/vps.py noi <địa-chỉ-IP>")


def ghi_cau_hinh(d: dict) -> None:
    CAU_HINH.write_text(json.dumps(d, ensure_ascii=False, indent=2), encoding="utf-8")


def lenh_ssh(ch: dict, *them: str) -> list[str]:
    return ["ssh", "-i", str(KHOA), "-p", str(ch.get("cong", 22)),
            "-o", "BatchMode=yes", "-o", "StrictHostKeyChecking=accept-new",
            "-o", "ConnectTimeout=20", "-o", "ServerAliveInterval=30",
            *them, f"{ch.get('user', 'root')}@{ch['ip']}"]


def tu_xa(ch: dict, lenh: str, *, vao: bytes | None = None, nhi_phan=False, hien=False,
          timeout: int | None = 900):
    """Chạy `lenh` trên VPS (trong thư mục bot nếu có). hien=True: in thẳng ra màn hình."""
    goc = f"cd ~/{ch.get('thu_muc', THU_MUC_VPS)} 2>/dev/null || cd ~; {lenh}"
    cmd = lenh_ssh(ch) + [goc]
    try:
        if hien:
            return subprocess.run(cmd, input=vao, timeout=timeout).returncode, b""
        r = subprocess.run(cmd, input=vao, capture_output=True, timeout=timeout)
    except FileNotFoundError:
        raise Loi("Máy này chưa có lệnh ssh. Windows: Cài đặt → Ứng dụng → Tính năng tuỳ chọn → "
                  "thêm OpenSSH Client.")
    except subprocess.TimeoutExpired:
        raise Loi("VPS không trả lời kịp — mạng chậm hoặc VPS đang tắt.")
    if r.returncode == 255:
        raise Loi(_giai_thich_ssh(r.stderr.decode("utf-8", "replace")))
    return r.returncode, (r.stdout if nhi_phan else r.stdout + r.stderr)


def _giai_thich_ssh(err: str) -> str:
    e = err.lower()
    if "permission denied" in e:
        return ("VPS chưa nhận chìa khoá của máy này. Chạy `vps.py khoa` rồi dán đúng phần nó in "
                "vào VPS (ô SSH key lúc tạo VPS, hoặc console web của nhà cung cấp).")
    if "timed out" in e or "no route" in e or "unreachable" in e:
        return "Không nối được VPS — sai địa chỉ IP, VPS đang tắt, hoặc nhà cung cấp chặn cổng 22."
    if "refused" in e:
        return "VPS từ chối kết nối ở cổng này — SSH chưa bật, hoặc sai cổng (--cong)."
    if "host key verification failed" in e or "remote host identification has changed" in e:
        return ("Dấu vân tay VPS đổi (cài lại VPS?). Nếu đúng là vừa cài lại: xoá dòng của IP này "
                "trong ~/.ssh/known_hosts rồi thử lại. Không chắc thì hỏi nhà cung cấp.")
    return "Lỗi SSH: " + err.strip()[-300:]


def mo_file(p: Path) -> bool:
    """Mở file bằng app mặc định của máy (ảnh → trình xem ảnh, .txt → Notepad/TextEdit)."""
    try:
        if sys.platform.startswith("win"):
            if p.suffix == ".txt":
                subprocess.Popen(["notepad", str(p)])
            else:
                os.startfile(str(p))  # type: ignore[attr-defined]
        elif sys.platform == "darwin":
            subprocess.Popen(["open", "-e", str(p)] if p.suffix == ".txt" else ["open", str(p)])
        else:
            subprocess.Popen(["xdg-open", str(p)], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        return True
    except OSError:
        return False


# ── Các lệnh ─────────────────────────────────────────────────────────────────

def cmd_khoa(_a) -> int:
    if not KHOA.exists():
        KHOA.parent.mkdir(parents=True, exist_ok=True)
        r = subprocess.run(["ssh-keygen", "-t", "ed25519", "-N", "", "-C", "zalo-bot",
                            "-f", str(KHOA), "-q"])
        if r.returncode != 0:
            raise Loi("Không tạo được chìa khoá (ssh-keygen lỗi).")
        print(f"✓ Đã tạo chìa khoá: {KHOA}")
    pub = Path(str(KHOA) + ".pub").read_text().strip()
    print(f"""
CHÌA KHOÁ CÔNG KHAI (dán đi đâu cũng an toàn — phần bí mật nằm lại máy này):

{pub}

Cách 1 — lúc TẠO VPS: ô "SSH key" / "SSH Keys" / "Khoá SSH" → Thêm → dán dòng trên.
Cách 2 — VPS đã tạo rồi: mở console web của nhà cung cấp (nút Console / VNC /
Terminal trên trang quản lý VPS), đăng nhập root, dán đúng MỘT dòng này rồi Enter:

mkdir -p ~/.ssh && echo '{pub}' >> ~/.ssh/authorized_keys && chmod 700 ~/.ssh && chmod 600 ~/.ssh/authorized_keys
""")
    return 0


def cmd_noi(a) -> int:
    if not re.fullmatch(r"[A-Za-z0-9.:\-]+", a.ip):
        raise Loi("Địa chỉ VPS lạ — dạng đúng như 203.0.113.5")
    ghi_cau_hinh({"ip": a.ip, "user": a.user, "cong": a.cong, "thu_muc": THU_MUC_VPS})
    return cmd_thu(a)


def cmd_thu(_a) -> int:
    ch = doc_cau_hinh()
    _, ra = tu_xa(ch, "uname -sm; . /etc/os-release 2>/dev/null && echo \"$PRETTY_NAME\"; "
                      "free -m | awk '/^Mem/ {print \"RAM \" $2 \" MB\"}'; "
                      "command -v python3 >/dev/null && python3 --version || echo 'Chưa có python3'; "
                      "id -un", timeout=60)
    print(f"✓ Nối được {ch['user']}@{ch['ip']}\n" + ra.decode("utf-8", "replace").strip())
    return 0


def _goi_template(cap_nhat: bool) -> tuple[bytes, int]:
    """tar.gz thư mục bot. cap_nhat=True: VPS đã có bot → KHÔNG đè sổ shop (chủ đã dạy qua Zalo)."""
    so_shop = set(gom(ROOT)) if cap_nhat else set()
    buf, dem = io.BytesIO(), 0
    with tarfile.open(fileobj=buf, mode="w:gz") as t:
        for p in sorted(ROOT.rglob("*")):
            rel = p.relative_to(ROOT).as_posix()
            phan = rel.split("/")
            if any(x in BO_THU_MUC for x in phan) or p.is_symlink() or not p.is_file():
                continue
            if BO_FILE.search(rel) or rel in so_shop:
                continue
            if phan[0] == "memory" and phan[-1] not in GIU_TRONG_MEMORY:
                continue                       # phiếu khách, nhật ký: dữ liệu sống trên VPS
            if rel.startswith("knowledge/raw/") and phan[-1] not in ("NGUON.md", ".gitkeep"):
                continue                       # file gốc chủ gửi: bot không cần, đừng mang đi
            t.add(p, arcname=rel)
            dem += 1
    return buf.getvalue(), dem


def cmd_day_len(_a) -> int:
    ch = doc_cau_hinh()
    ma, _ = tu_xa(ch, f"test -f ~/{ch['thu_muc']}/AGENTS.md", timeout=60)
    cap_nhat = ma == 0
    goi, dem = _goi_template(cap_nhat)
    lenh = f"mkdir -p ~/{ch['thu_muc']} && tar -xzf - -C ~/{ch['thu_muc']} && echo OK"
    ma, ra = tu_xa(ch, lenh, vao=goi, timeout=600)
    if ma != 0 or b"OK" not in ra:
        raise Loi("Đẩy lên không xong:\n" + ra.decode("utf-8", "replace")[-500:])
    print(f"✓ Đã đẩy {dem} file lên ~/{ch['thu_muc']} ({len(goi) // 1024} KB)")
    if cap_nhat:
        print("• VPS đã có bot — giữ nguyên sổ shop trên đó (chủ có thể đã dạy bot qua Zalo).")
    return 0


def cmd_bat_dau(a) -> int:
    ch = doc_cau_hinh()
    them = []
    if a.da_thu:
        them.append("--da-thu")
    if a.chu_id:
        them += ["--chu-id", a.chu_id]
    if a.ten:
        them += ["--ten", a.ten]
    if a.bo_qua:
        them += ["--bo-qua", a.bo_qua]
    an_toan = " ".join("'" + x.replace("'", "'\\''") + "'" for x in them)
    ma, _ = tu_xa(ch, f"python3 scripts/bat_dau.py --tu-dong {an_toan}", hien=True, timeout=None)
    if ma != 3 and FILE_QR.exists():
        FILE_QR.unlink()                       # đã qua bước quét — ảnh mã không còn dùng, xoá
    return ma


def cmd_gui_ma_ai(a) -> int:
    if a.mo:
        FILE_MA.write_text("Dán mã AI (bắt đầu bằng sk-ant-) vào dòng dưới, rồi Lưu (Ctrl+S) và đóng:\n\n",
                           encoding="utf-8")
        cach = "Đã mở" if mo_file(FILE_MA) else "Không tự mở được — nhờ người mở tay"
        print(f"✓ {cach} file {FILE_MA}. Người dán mã, lưu, đóng — rồi chạy: vps.py gui-ma-ai --gui")
        return 0
    if not FILE_MA.exists():
        raise Loi("Chưa có file mã — chạy gui-ma-ai --mo trước.")
    m = re.search(r"sk-ant-[A-Za-z0-9_\-]{10,}", FILE_MA.read_text(encoding="utf-8", errors="replace"))
    if not m:
        raise Loi("Trong file chưa có mã bắt đầu bằng sk-ant- — người chưa dán, hoặc chưa bấm Lưu.")
    ch = doc_cau_hinh()
    ma, ra = tu_xa(ch, "umask 077; mkdir -p ~/.openclaw && cat > ~/.openclaw/.ma-ai-tam && echo OK",
                   vao=(m.group(0) + "\n").encode(), timeout=60)
    FILE_MA.write_text("", encoding="utf-8")
    FILE_MA.unlink()
    if ma != 0 or b"OK" not in ra:
        raise Loi("Gửi mã lên VPS không xong.")
    print("✓ Đã gửi mã lên VPS (không in ra đây), đã xoá file trên máy này. Gọi lại: vps.py bat-dau")
    return 0


def cmd_lay_qr(_a) -> int:
    ch = doc_cau_hinh()
    lenh = ("f=$(grep -o 'Scan QR image: [^ ]*\\.png' ~/.openclaw/zalo-dang-nhap.log 2>/dev/null "
            "| tail -1 | cut -d' ' -f4); test -n \"$f\" && cat \"$f\"")
    ma, du = tu_xa(ch, lenh, nhi_phan=True, timeout=60)
    if ma != 0 or not du.startswith(b"\x89PNG"):
        raise Loi("Chưa có mã trên VPS — chạy vps.py bat-dau trước (nó bật đăng nhập).")
    FILE_QR.write_bytes(du)
    cach = "Đã mở mã đăng nhập trên màn hình" if mo_file(FILE_QR) else "Không tự mở được — mở tay ảnh"
    print(f"✓ {cach} ({FILE_QR}). Mã hết hạn nhanh — người quét ngay, "
          "rồi gọi lại vps.py bat-dau. Đừng gửi ảnh này cho ai.")
    return 0


def cmd_day_so(a) -> int:
    ch = doc_cau_hinh()
    moc = ch.get("dong_bo_luc")
    if moc and not a.ep:
        lenh = (f"find knowledge IDENTITY.md USER.md MEMORY.md SOUL.md skills/khai-thac skills/ghi-don "
                f"-name '*.md' ! -name INDEX.md -newermt @{int(moc)} 2>/dev/null")
        _, ra = tu_xa(ch, lenh, timeout=60)
        doi = ra.decode("utf-8", "replace").split()
        if doi:
            raise Loi("Sổ trên VPS đã đổi sau lần đồng bộ trước (chủ dạy bot qua Zalo?): "
                      + ", ".join(doi[:8]) + ". Kéo về trước: vps.py keo-so — rồi mới day-so. "
                      "Chắc chắn muốn đè: day-so --ep")
    ma, ra = tu_xa(ch, "python3 scripts/mo_goi.py && date +%s", vao=thanh_khoi(gom(ROOT)).encode(),
                   timeout=300)
    van = ra.decode("utf-8", "replace")
    print(re.sub(r"\n\d{9,11}\s*$", "", van.strip()))
    if ma != 0:
        raise Loi("VPS chưa nhận sổ.")
    _ghi_moc(ch, van)
    return 0


def cmd_keo_so(_a) -> int:
    from mo_goi import doc_khoi, ghi, kiem
    ch = doc_cau_hinh()
    ma, ra = tu_xa(ch, "python3 scripts/dong_goi.py 2>/dev/null && date +%s", timeout=120)
    van = ra.decode("utf-8", "replace")
    if ma != 0:
        raise Loi("VPS chưa gói được sổ.")
    tep = doc_khoi(van)
    kiem(tep)
    kq = ghi(ROOT, tep)
    for nhom, ds in kq.items():
        if ds:
            print(f"{nhom} ({len(ds)}): " + ", ".join(ds))
    if kq["đổi"]:
        print("• Bản cũ trên máy này của các tờ bị đổi: thư mục .ban-cu/")
    subprocess.run([sys.executable, str(ROOT / "scripts" / "lam_chi_muc.py")], cwd=ROOT)
    _ghi_moc(ch, van)
    return 0


def _ghi_moc(ch: dict, van: str) -> None:
    so = re.findall(r"^(\d{9,11})\s*$", van, re.M)
    ch["dong_bo_luc"] = int(so[-1]) if so else int(time.time())
    ghi_cau_hinh(ch)


def cmd_chay(a) -> int:
    if not a.lenh:
        raise Loi("Thiếu lệnh. Ví dụ: vps.py chay -- python3 scripts/kiem_tra_may.py")
    return tu_xa(doc_cau_hinh(), " ".join(a.lenh), hien=True, timeout=None)[0]


def main(argv: list[str] | None = None) -> int:
    for s in (sys.stdout, sys.stderr):
        try:
            s.reconfigure(encoding="utf-8")  # type: ignore[attr-defined]
        except (AttributeError, ValueError):
            pass
    ap = argparse.ArgumentParser(description="Điều khiển VPS của bot từ máy người dựng.")
    sp = ap.add_subparsers(dest="lenh_con", required=True)
    sp.add_parser("khoa").set_defaults(f=cmd_khoa)
    p = sp.add_parser("noi")
    p.add_argument("ip")
    p.add_argument("--user", default="root")
    p.add_argument("--cong", type=int, default=22)
    p.set_defaults(f=cmd_noi)
    sp.add_parser("thu").set_defaults(f=cmd_thu)
    sp.add_parser("day-len").set_defaults(f=cmd_day_len)
    p = sp.add_parser("bat-dau")
    p.add_argument("--da-thu", action="store_true")
    p.add_argument("--chu-id")
    p.add_argument("--ten")
    p.add_argument("--bo-qua")
    p.set_defaults(f=cmd_bat_dau)
    p = sp.add_parser("gui-ma-ai")
    g = p.add_mutually_exclusive_group(required=True)
    g.add_argument("--mo", action="store_true")
    g.add_argument("--gui", action="store_true")
    p.set_defaults(f=cmd_gui_ma_ai)
    sp.add_parser("lay-qr").set_defaults(f=cmd_lay_qr)
    p = sp.add_parser("day-so")
    p.add_argument("--ep", action="store_true")
    p.set_defaults(f=cmd_day_so)
    sp.add_parser("keo-so").set_defaults(f=cmd_keo_so)
    p = sp.add_parser("chay")
    p.add_argument("lenh", nargs=argparse.REMAINDER)
    p.set_defaults(f=cmd_chay)
    a = ap.parse_args(argv)
    if getattr(a, "lenh", None) and a.lenh[:1] == ["--"]:
        a.lenh = a.lenh[1:]
    try:
        return a.f(a)
    except Loi as e:
        print(f"✗ {e}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
