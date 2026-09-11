"""CLI giả lập.

    python3 -m sim.chay nen              # soi nền prompt: to bao nhiêu, có gì bay hơi lọt vào
    python3 -m sim.chay nhip             # chạy bảng tình huống rào follow-up / boot
    python3 -m sim.chay chat "alo shop"  # một lượt; --nao claude để gọi model thật
"""

from __future__ import annotations

import sys
from datetime import datetime, time, timedelta

from .kenh import Tin, chia_tin, duoc_tra_loi, gop_tin_don, phieu_id, session_key
from .kho import Chu, Phieu
from .nao import chon, co_key
from .nen import Nen, luot
from .nhip import ban_giao_con_treo, boot_tin_no, im_sau_gia, sau_don

OK, XAU = "  ok  ", " LỖI "


def lenh_nen() -> int:
    n = Nen.dung()
    print(f"Nền prompt: {len(n.manh)} file · {n.ky_tu():,} ký tự · ~{n.token_uoc():,} token")
    print(f"Vân tay: {n.van_tay()}  (đổi một ký tự ở nền là đổi vân tay = vỡ cache)\n")
    for ten, noi in n.manh:
        print(f"  {len(noi):>7,} ký tự  {ten}")
    loi = n.soi_bay_hoi()
    print()
    if loi:
        print(f"{XAU} {len(loi)} thứ bay hơi lọt vào nền:")
        for l in loi:
            print("   -", l)
        return 1
    print(f"{OK} không có dấu thời gian / id ngẫu nhiên nào ở nền")
    return 0


def lenh_nhip() -> int:
    chu_that = Chu.doc()
    chu = Chu(gio_followup=(time(9), time(21)), ngay_nghi=[((1, 28), (2, 5))],
              im_sau_gia_gio=24, sau_don_gio=48, cau_mau_sau_don="nhận hàng chưa ạ")
    t = datetime(2026, 9, 11, 10, 0)
    p_gia = Phieu("1", {"da_bao_gia_luc": "2026-09-09 10:00", "followup_im": "chua"})
    p_ck = Phieu("2", {"anh_thay_gi": "biên lai CK", "trang_thai_don": "trong",
                       "followup_don": "chua"})
    p_don = Phieu("3", {"trang_thai_don": "cho_chot", "don_ghi_luc": "2026-09-08 09:00",
                        "followup_don": "chua"})
    p_bg = Phieu("4", {"ban_giao": "dang_cho", "ban_giao_luc": "2026-09-09 09:00"})

    ca = [
        ("USER.md như template giao đi → không nhắn ai", im_sau_gia(p_gia, chu_that, t), False),
        ("im sau giá, đủ giờ, ngày thường", im_sau_gia(p_gia, chu, t), True),
        ("im sau giá, 23h đêm", im_sau_gia(p_gia, chu, t.replace(hour=23)), False),
        ("im sau giá, mùng 2 Tết", im_sau_gia(p_gia, chu, datetime(2026, 1, 30, 10)), False),
        ("im sau giá, nhánh đã khóa",
         im_sau_gia(Phieu("1", {**p_gia.truong, "followup_im": "da_gui"}), chu, t), False),
        ("CHỈ có ảnh CK → không follow-up sau đơn", sau_don(p_ck, chu, t), False),
        ("đã ghi đơn, đủ 48h", sau_don(p_don, chu, t), True),
        ("chủ chưa cho câu mẫu",
         sau_don(p_don, Chu(gio_followup=(time(9), time(21)), sau_don_gio=48), t), False),
        ("bàn giao quá 24h → báo chủ một lần", ban_giao_con_treo(p_bg, t), True),
        ("bàn giao còn trong 24h",
         ban_giao_con_treo(p_bg, datetime(2026, 9, 9, 20)), False),
    ]
    hong = 0
    for nhan, q, mong in ca:
        dat = bool(q) == mong
        hong += not dat
        print(f"{OK if dat else XAU} {nhan:44} → {'gửi' if q else 'không'}"
              f"{'' if bool(q) else '  · ' + q.ly_do}")

    no = boot_tin_no([("111", t - timedelta(hours=3)), ("222", t - timedelta(hours=30))], t)
    dat = no == {"tra_khach": ["111"], "chi_bao_chu": ["222"]}
    hong += not dat
    print(f"{OK if dat else XAU} boot: nợ 3h trả khách, nợ 30h chỉ báo chủ → {no}")
    return 1 if hong else 0


def lenh_chat(tin_chu: str, ten_nao: str) -> int:
    if ten_nao == "claude" and not co_key():
        print("Chưa có ANTHROPIC_API_KEY. Dùng --nao luat để chạy phần máy.")
        return 2
    nao, nen = chon(ten_nao), Nen.dung()
    tin = Tin("999", tin_chu, datetime.now())
    print(f"phiên : {session_key(tin)}\nphiếu : {phieu_id(tin)}\n")
    tl = nao(luot(nen, tin_chu))
    for i, phan in enumerate(chia_tin(tl.chu), 1):
        print(f"[tin {i}] {phan}")
    if tl.that:
        print(f"\ntoken vào {tl.token_vao:,} · đọc lại từ cache {tl.tu_cache:,} · ra {tl.token_ra:,}")
        if tl.tu_cache == 0:
            print(f"{XAU} lượt này không đọc được gì từ cache — lượt đầu thì bình thường, "
                  "lặp lại mà vẫn 0 là nền đang vỡ (docs/12)")
    return 0


def main(argv: list[str]) -> int:
    if not argv or argv[0] in ("-h", "--help"):
        print(__doc__)
        return 0
    lenh, con = argv[0], argv[1:]
    nao = "luat"
    if "--nao" in con:
        i = con.index("--nao")
        nao = con[i + 1]
        con = con[:i] + con[i + 2:]
    if lenh == "nen":
        return lenh_nen()
    if lenh == "nhip":
        return lenh_nhip()
    if lenh == "chat":
        return lenh_chat(" ".join(con) or "alo", nao)
    print(f"lệnh lạ: {lenh}")
    print(__doc__)
    return 2


if __name__ == "__main__":
    try:
        raise SystemExit(main(sys.argv[1:]))
    except BrokenPipeError:      # `| head` đóng ống — không phải lỗi
        sys.stderr.close()
        raise SystemExit(0)
