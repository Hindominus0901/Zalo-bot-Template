#!/usr/bin/env python3
"""Điền config OpenClaw cho shop — hỏi ba câu, không phải sửa JSON bằng tay.

    python3 scripts/dien_config.py

Hỏi: tên bot, senderId Zalo của chủ, có tiết kiệm không. Rồi:

1. Điền vào bản mẫu `config/openclaw.zalouser.example.json5`.
2. Sửa dòng **Name:** trong IDENTITY.md cho khớp (lệch tên = bot im trong nhóm).
3. Gộp vào config thật bằng `openclaw config patch` — GỘP, không ghi đè: token
   gateway và mã AI mà `openclaw onboard` đã tạo vẫn còn nguyên.
4. Chạy `openclaw config validate` và đọc cả warning — lệnh vẫn báo "valid"
   khi config sai kiểu im lặng.

Không có lệnh `openclaw` trên máy này → chỉ in file đã điền ra, để mang sang
máy Gateway.

Cờ cho người dựng / agent (bỏ qua câu hỏi):
    --ten "Nami"  --chu 1234567890123456789  --tiet-kiem
    --workspace /duong/dan  --chi-xem  --openclaw /duong/toi/openclaw
"""

from __future__ import annotations

import argparse
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
MAU = ROOT / "config" / "openclaw.zalouser.example.json5"
IDENTITY = ROOT / "IDENTITY.md"
CHO = "SENDERID_CHU"
# (chính, dự phòng, tiết kiệm) theo nhà AI. Tên ghim đủ — đừng dùng bí danh.
# Danh mục + giá: extensions/openai|anthropic/openclaw.plugin.json của OpenClaw 2026.9.4.
MO_HINH = {
    "openai": ("openai/gpt-5.6-terra", ["openai/gpt-5.4"], "openai/gpt-5.6-luna"),
    "anthropic": ("anthropic/claude-opus-5", ["anthropic/claude-sonnet-5"], "anthropic/claude-sonnet-5"),
}
NHA_AI_MAC_DINH = "openai"
MODEL_MANH, _DU_PHONG, MODEL_TIET_KIEM = MO_HINH[NHA_AI_MAC_DINH]

# Warning của `config validate` mà người không rành sẽ bỏ qua — dịch ra chữ thường.
CANH_BAO = [
    ("all DMs will be dropped", "Khách nhắn riêng sẽ RƠI HẾT — thiếu allowFrom \"*\"."),
    ("no ambient heartbeat owner", "Follow-up sẽ không chạy — thiếu agent giữ heartbeat."),
    ("Unrecognized key", "Có key sai chỗ — gateway sẽ không lên."),
]


class Loi(Exception):
    """Lỗi do người nhập — in chữ thường, không in traceback."""


def ten_hien_tai() -> str:
    m = re.search(r"\*\*Name:\*\*\s*(.+)", IDENTITY.read_text(encoding="utf-8"))
    return m.group(1).strip() if m else "Nami"


def kiem_sender(s: str) -> str:
    """senderId Zalo là một dãy số. Số điện thoại hay tên là sai — hay gặp nhất."""
    s = s.strip()
    if not s:
        return ""
    if s.startswith(("0", "+84")) and len(re.sub(r"\D", "", s)) in (10, 11):
        raise Loi(f"'{s}' trông như số điện thoại. Cần senderId — một dãy số Zalo sinh ra.\n"
                  "Cách lấy: docs/14-vps-headless.md mục 'Lấy senderId và groupId'.")
    if not re.fullmatch(r"\d{6,25}", s):
        raise Loi(f"'{s}' không phải senderId (phải là một dãy số, không chữ, không dấu cách).")
    return s


def kiem_ten(s: str) -> str:
    s = s.strip()
    if not s:
        raise Loi("Tên bot không được trống.")
    if '"' in s or "\\" in s or "\n" in s:
        raise Loi("Tên bot không được có dấu ngoặc kép hay gạch chéo.")
    return s


def dien(mau: str, ten: str, chu: str, workspace: str, model: str,
         du_phong: list[str] | None = None) -> str:
    """Thay chỗ trống trong bản mẫu. Hàm thuần — test gọi thẳng."""
    out = mau
    if chu:
        out = out.replace(CHO, chu)
    out = doi_ten_identity(out, ten)
    # Mọi chỗ — defaults VÀ từng agent. Thiếu một chỗ là agent đó chạy trong
    # <gốc>/<tên agent>: thư mục rỗng, bot không thấy sổ.
    out = out.replace('workspace: ".",', f'workspace: "{workspace}",')
    out = re.sub(r'primary:\s*"[^"]*"', f'primary: "{model}"', out, count=1)
    if du_phong is None:
        du_phong = next((dp for m, dp, _ in MO_HINH.values() if m == model), [])
    ds = ", ".join(f'"{x}"' for x in du_phong if x != model)
    out = re.sub(r'fallbacks:\s*\[[^\]]*\]', f'fallbacks: [{ds}]', out, count=1)
    return out


def doi_ten_identity(text: str, ten: str) -> str:
    return re.sub(r'identity:\s*\{\s*name:\s*"[^"]*"\s*\}', f'identity: {{ name: "{ten}" }}', text)


def sua_ten_trong_repo(ten: str) -> bool:
    """Đổi tên ở CẢ IDENTITY.md lẫn config mẫu của repo shop.

    Plugin nhận tên theo config, test so config mẫu với IDENTITY.md. Chỉ đổi một
    chỗ là tự tạo ra đúng cái lệch mà test được viết để bắt. Bản mẫu vẫn giữ
    SENDERID_CHU và workspace "." — chỉ tên đổi."""
    doi = False
    t = IDENTITY.read_text(encoding="utf-8")
    moi = re.sub(r"(\*\*Name:\*\*\s*).+", lambda m: m.group(1) + ten, t, count=1)
    if moi != t:
        IDENTITY.write_text(moi, encoding="utf-8")
        doi = True
    m = MAU.read_text(encoding="utf-8")
    m2 = doi_ten_identity(m, ten)
    if m2 != m:
        MAU.write_text(m2, encoding="utf-8")
        doi = True
    return doi


def hoi(cau: str, mac_dinh: str = "") -> str:
    """Câu hỏi in ra stderr — stdout dành cho file config (--chi-xem). In câu hỏi
    ra stdout là nó lẫn vào config, OpenClaw đọc hỏng ngay ký tự đầu."""
    goi_y = f" [{mac_dinh}]" if mac_dinh else ""
    sys.stderr.write(f"{cau}{goi_y}: ")
    sys.stderr.flush()
    try:
        tl = input().strip()
    except EOFError:
        tl = ""
    return tl or mac_dinh


def chay(oc: str, *args: str) -> subprocess.CompletedProcess:
    return subprocess.run([oc, *args], capture_output=True, text=True)


def doc_canh_bao(text: str) -> list[str]:
    return [loi for khoa, loi in CANH_BAO if khoa in text]


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="Điền config OpenClaw cho shop.")
    ap.add_argument("--ten")
    ap.add_argument("--chu", help="senderId Zalo của chủ (bỏ trống = chưa bật dạy bot)")
    ap.add_argument("--workspace", default=str(ROOT))
    ap.add_argument("--tiet-kiem", action="store_true", help="dùng model rẻ hơn của cùng nhà AI")
    ap.add_argument("--nha-ai", choices=sorted(MO_HINH), default=NHA_AI_MAC_DINH,
                    help="nhà AI của mã đã nhập (mặc định openai — GPT)")
    ap.add_argument("--chi-xem", action="store_true", help="in file đã điền, không gộp")
    ap.add_argument("--openclaw", default=shutil.which("openclaw") or "")
    a = ap.parse_args(argv)
    hoi_tuong_tac = a.ten is None and a.chu is None

    try:
        ten = kiem_ten(a.ten if a.ten is not None else
                       hoi("1. Tên bot (khách gọi tên này trong nhóm)", ten_hien_tai()))
        if a.chu is not None:
            chu = kiem_sender(a.chu)
        elif not hoi_tuong_tac:
            chu = ""   # gọi từ máy (đã có --ten): không hỏi, bỏ trống = chưa bật dạy bot
        else:
            print("2. senderId Zalo của CHỦ — để chủ dạy bot và giao việc qua Zalo.", file=sys.stderr)
            print("   Chưa có thì Enter bỏ qua: bot vẫn chạy, chỉ là chưa dạy được.", file=sys.stderr)
            chu = kiem_sender(hoi("   senderId"))
        tiet_kiem = a.tiet_kiem
        if hoi_tuong_tac and not tiet_kiem:
            tiet_kiem = hoi("3. Dùng bản tiết kiệm (rẻ ~2,5 lần, kém tinh tế hơn)? c/k", "k").lower().startswith("c")
    except Loi as e:
        print(f"\n✗ {e}", file=sys.stderr)
        return 2

    manh, du_phong, re_ = MO_HINH[a.nha_ai]
    model = re_ if tiet_kiem else manh
    du_phong = [] if tiet_kiem else du_phong
    ws = str(Path(a.workspace).resolve())
    filled = dien(MAU.read_text(encoding="utf-8"), ten, chu, ws, model, du_phong)

    if a.chi_xem:
        print(filled)
        return 0

    if sua_ten_trong_repo(ten):
        print(f"✓ Tên bot = {ten} ở IDENTITY.md và config mẫu")

    if not a.openclaw:
        ra = ROOT / "config" / "openclaw.da-dien.json5"
        ra.write_text(filled, encoding="utf-8")
        print(f"\nMáy này không có lệnh openclaw. Đã ghi {ra.relative_to(ROOT)} —")
        print("mang file đó sang máy Gateway rồi chạy:")
        print(f"  openclaw config patch --file {ra.name} && openclaw config validate")
        return 0

    with tempfile.NamedTemporaryFile("w", suffix=".json5", delete=False, encoding="utf-8") as f:
        f.write(filled)
        patch = f.name
    try:
        thu = chay(a.openclaw, "config", "patch", "--file", patch, "--dry-run")
        if thu.returncode != 0:
            print("✗ OpenClaw từ chối config này (chưa ghi gì):\n" + thu.stdout + thu.stderr, file=sys.stderr)
            return 1
        that = chay(a.openclaw, "config", "patch", "--file", patch)
        if that.returncode != 0:
            print("✗ Gộp config hỏng:\n" + that.stdout + that.stderr, file=sys.stderr)
            return 1
    finally:
        Path(patch).unlink(missing_ok=True)

    kq = chay(a.openclaw, "config", "validate")
    toan_bo = kq.stdout + kq.stderr
    print("\n" + toan_bo.strip())
    loi = doc_canh_bao(toan_bo)
    if kq.returncode != 0 or loi:
        for l in loi:
            print(f"✗ {l}", file=sys.stderr)
        return 1

    print(f"\n✓ Xong. Bot tên {ten}, model {model}.")
    if chu:
        print("✓ Chủ nhắn RIÊNG cho bot là dạy được bot và giao việc (docs/16-day-bot.md).")
    else:
        print("• Chưa bật dạy bot. Có senderId thì chạy lại: python3 scripts/dien_config.py --chu <id>")
    print("• Khởi động lại gateway để áp: openclaw gateway restart")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
