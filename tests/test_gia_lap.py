"""Giả lập: chạy luật máy thật, không chỉ khớp chữ.

Khác mọi file test kia — mấy file đó kiểm markdown có nói đúng không. File này
kiểm luật có **chạy** đúng không: rào giờ, ngày nghỉ, gộp tin dồn, sổ nợ.
"""

from __future__ import annotations

import unittest
from datetime import datetime, time, timedelta

from sim.kenh import Tin, chia_tin, duoc_tra_loi, gop_tin_don, phieu_id, session_key
from sim.kho import Chu, Phieu, _gio, _ngay_nghi
from sim.nen import Nen, luot
from sim.nhip import ban_giao_con_treo, boot_tin_no, im_sau_gia, sau_don

T = datetime(2026, 9, 11, 10, 0)
CHU = Chu(gio_followup=(time(9), time(21)), ngay_nghi=[((1, 28), (2, 5))],
          im_sau_gia_gio=24, sau_don_gio=48, cau_mau_sau_don="nhận hàng chưa ạ")


def phieu(**tr) -> Phieu:
    return Phieu("123", tr)


class DocUserMd(unittest.TestCase):
    def test_gio(self):
        self.assertEqual(_gio("9h–21h"), (time(9), time(21)))
        self.assertEqual(_gio("09:00 - 18:30"), (time(9), time(18, 30)))
        self.assertIsNone(_gio("[CHỜ CHỦ SHOP: ví dụ 9h–21h]"))
        self.assertIsNone(_gio("tắt"))

    def test_ngay_nghi(self):
        self.assertEqual(_ngay_nghi("28/1–5/2"), [((1, 28), (2, 5))])
        self.assertEqual(_ngay_nghi("không nghỉ ngày nào"), [])
        self.assertEqual(_ngay_nghi("[CHỜ CHỦ SHOP]"), [])

    def test_khoang_vat_qua_nam_moi(self):
        c = Chu(ngay_nghi=_ngay_nghi("28/12–5/1"))
        self.assertTrue(c.dang_nghi(datetime(2026, 12, 30).date()))
        self.assertTrue(c.dang_nghi(datetime(2026, 1, 3).date()))
        self.assertFalse(c.dang_nghi(datetime(2026, 6, 1).date()))

    def test_template_giao_di_la_tat_het(self):
        """USER.md như lúc giao khách: mọi nhánh follow-up phải tắt."""
        c = Chu.doc()
        self.assertIsNone(c.im_sau_gia_gio)
        self.assertIsNone(c.sau_don_gio)
        self.assertEqual(c.cau_mau_sau_don, "")
        self.assertEqual(c.ngay_nghi, [])


class RaoFollowUp(unittest.TestCase):
    P = dict(da_bao_gia_luc="2026-09-09 10:00", followup_im="chua")

    def test_du_dieu_kien_thi_gui(self):
        self.assertTrue(im_sau_gia(phieu(**self.P), CHU, T))

    def test_ngoai_gio_khong_gui(self):
        self.assertFalse(im_sau_gia(phieu(**self.P), CHU, T.replace(hour=23)))
        self.assertFalse(im_sau_gia(phieu(**self.P), CHU, T.replace(hour=4)))

    def test_ngay_nghi_khong_gui_va_khong_gui_bu(self):
        trong_tet = datetime(2026, 1, 30, 10, 0)
        q = im_sau_gia(phieu(**self.P), CHU, trong_tet)
        self.assertFalse(q)
        self.assertIn("ngày nghỉ", q.ly_do)

    def test_chua_du_delay(self):
        self.assertFalse(im_sau_gia(phieu(**self.P), CHU, datetime(2026, 9, 9, 20)))

    def test_nhanh_da_khoa_khong_gui_lan_hai(self):
        self.assertFalse(im_sau_gia(phieu(**{**self.P, "followup_im": "da_gui"}), CHU, T))
        self.assertFalse(im_sau_gia(phieu(**{**self.P, "followup_im": "tat"}), CHU, T))

    def test_chua_bao_gia_thi_khong_co_nhanh_im(self):
        self.assertFalse(im_sau_gia(phieu(followup_im="chua"), CHU, T))

    def test_user_md_tat_thi_khong_gui(self):
        tat = Chu(gio_followup=(time(9), time(21)))
        self.assertFalse(im_sau_gia(phieu(**self.P), tat, T))


class RaoSauDon(unittest.TestCase):
    DON = dict(trang_thai_don="cho_chot", don_ghi_luc="2026-09-08 09:00", followup_don="chua")

    def test_don_that_thi_gui(self):
        self.assertTrue(sau_don(phieu(**self.DON), CHU, T))

    def test_chi_co_anh_ck_thi_khong(self):
        """Luật đắt nhất trong repo: CK không phải đơn."""
        q = sau_don(phieu(anh_thay_gi="biên lai CK", trang_thai_don="trong",
                          followup_don="chua"), CHU, T)
        self.assertFalse(q)
        self.assertIn("Ảnh CK", q.ly_do)

    def test_chua_co_cau_mau_thi_khong_bia(self):
        khong_mau = Chu(gio_followup=(time(9), time(21)), sau_don_gio=48)
        self.assertFalse(sau_don(phieu(**self.DON), khong_mau, T))

    def test_moi_trang_thai_don_that(self):
        for tt in ("cho_chot", "da_chot_chu", "dang_giao", "xong"):
            self.assertTrue(sau_don(phieu(**{**self.DON, "trang_thai_don": tt}), CHU, T), tt)
        self.assertFalse(sau_don(phieu(**{**self.DON, "trang_thai_don": "trong"}), CHU, T))


class BanGiaoHetHan(unittest.TestCase):
    BG = dict(ban_giao="dang_cho", ban_giao_luc="2026-09-09 09:00")

    def test_trong_24h_van_cho(self):
        self.assertFalse(ban_giao_con_treo(phieu(**self.BG), datetime(2026, 9, 9, 20)))

    def test_qua_24h_bao_chu_nhung_van_giu_co(self):
        q = ban_giao_con_treo(phieu(**self.BG), T)
        self.assertTrue(q)
        self.assertIn("giữ dang_cho", q.ly_do)

    def test_khong_co_ban_giao_thi_thoi(self):
        self.assertFalse(ban_giao_con_treo(phieu(ban_giao="khong"), T))


class SoTinNo(unittest.TestCase):
    def test_trong_12h_tra_khach_cu_hon_chi_bao_chu(self):
        ra = boot_tin_no([("a", T - timedelta(hours=3)), ("b", T - timedelta(hours=30))], T)
        self.assertEqual(ra, {"tra_khach": ["a"], "chi_bao_chu": ["b"]})

    def test_rong_thi_khong_lam_gi(self):
        self.assertEqual(boot_tin_no([], T), {"tra_khach": [], "chi_bao_chu": []})


class GopTinDon(unittest.TestCase):
    def test_burst_thanh_mot_cum(self):
        t = T
        tins = [Tin("1", "alo", t), Tin("1", "shop ơi", t + timedelta(milliseconds=900)),
                Tin("1", "còn hàng ko", t + timedelta(milliseconds=1700))]
        self.assertEqual(len(gop_tin_don(tins)), 1)

    def test_im_lau_thi_thanh_cum_moi(self):
        t = T
        tins = [Tin("1", "alo", t), Tin("1", "à quên", t + timedelta(seconds=30))]
        self.assertEqual(len(gop_tin_don(tins)), 2)

    def test_hai_khach_khong_gop_lan_nhau(self):
        t = T
        tins = [Tin("1", "a", t), Tin("2", "b", t + timedelta(milliseconds=100))]
        self.assertEqual(len(gop_tin_don(tins)), 2)

    def test_anh_cho_lau_hon_chu(self):
        t = T
        tins = [Tin("1", "", t, co_media=True),
                Tin("1", "", t + timedelta(milliseconds=2500), co_media=True)]
        self.assertEqual(len(gop_tin_don(tins)), 1, "nhieu anh gui lech nhau phai gop")


class NhomPhaiGoiTen(unittest.TestCase):
    def test_inbox_luon_tra(self):
        self.assertTrue(duoc_tra_loi(Tin("1", "gì đó", T)))

    def test_nhom_khong_goi_ten_thi_im(self):
        self.assertFalse(duoc_tra_loi(Tin("1", "hôm nay đẹp trời", T, nhom="g")))

    def test_nhom_goi_ten_thi_tra(self):
        self.assertTrue(duoc_tra_loi(Tin("1", "Nami ơi còn hàng không", T, nhom="g")))
        self.assertTrue(duoc_tra_loi(Tin("1", "nami oi", T, nhom="g")))

    def test_reply_tin_bot_thi_tra(self):
        self.assertTrue(duoc_tra_loi(Tin("1", "ừ", T, nhom="g"), reply_tin_bot=True))

    def test_biet_hieu(self):
        self.assertTrue(duoc_tra_loi(Tin("1", "shop ơi", T, nhom="g"), biet_hieu=("shop ơi",)))


class KhoaPhien(unittest.TestCase):
    def test_inbox_va_nhom_la_hai_phien(self):
        self.assertNotEqual(session_key(Tin("1", "x", T)),
                            session_key(Tin("1", "x", T, nhom="g")))

    def test_phieu_id_nhom_co_ca_hai(self):
        self.assertEqual(phieu_id(Tin("1", "x", T, nhom="g9")), "g9-1")

    def test_id_ban_thi_khong_tao_file(self):
        self.assertEqual(phieu_id(Tin("a/b", "x", T)), "")


class ChiaTin(unittest.TestCase):
    def test_ngan_thi_mot_tin(self):
        self.assertEqual(chia_tin("Ship 30k nha anh"), ["Ship 30k nha anh"])

    def test_khong_cat_giua_ma_don(self):
        dai = ("Ship nội thành 30k.\n\n" + "Đổi trả trong 7 ngày nếu nguyên tem. " * 15
               + "\n\nMã đơn ABC123456 anh giữ nhé.")
        ra = chia_tin(dai)
        self.assertEqual(sum("ABC123456" in x for x in ra), 1)
        self.assertLessEqual(len(ra), 3)

    def test_mot_doan_dai_van_di_nguyen_tin(self):
        mot_doan = "x" * 1500
        self.assertEqual(chia_tin(mot_doan), [mot_doan])


class NenPrompt(unittest.TestCase):
    def test_khong_co_gi_bay_hoi_lot_vao_nen(self):
        self.assertEqual(Nen.dung().soi_bay_hoi(), [])

    def test_van_tay_on_dinh_giua_hai_lan_dung(self):
        self.assertEqual(Nen.dung().van_tay(), Nen.dung().van_tay())

    def test_phieu_va_wiki_khong_duoc_vao_system(self):
        g = luot(Nen.dung(), "ship bao nhiêu", phieu="- size: M", wiki="30k")
        self.assertNotIn("size: M", g["system"][0]["text"])
        self.assertIn("size: M", g["messages"][0]["content"])

    def test_system_co_cache_control(self):
        g = luot(Nen.dung(), "alo")
        self.assertEqual(g["system"][0]["cache_control"], {"type": "ephemeral"})

    def test_nen_khong_qua_to(self):
        """Nền là tiền mỗi lượt khi cache miss. Phình quá là phải xem lại."""
        self.assertLess(Nen.dung().token_uoc(), 15000)


if __name__ == "__main__":
    unittest.main()


class LoiDaSua(unittest.TestCase):
    """Bốn lỗi tìm ra lúc soi từng dòng. Test ở đây để chúng không quay lại."""

    def test_hai_khach_xen_ke_van_gop_dung(self):
        """Shop đông thì hai khách nhắn đan nhau — gộp tuần tự sẽ cắt vụn cả hai."""
        t = T
        tins = [Tin("A", "a1", t), Tin("B", "b1", t + timedelta(milliseconds=100)),
                Tin("A", "a2", t + timedelta(milliseconds=200)),
                Tin("B", "b2", t + timedelta(milliseconds=300))]
        cum = gop_tin_don(tins)
        self.assertEqual(len(cum), 2, "moi khach mot cum")
        self.assertEqual({len(c) for c in cum}, {2})

    def test_gio_khong_nuot_phut(self):
        self.assertEqual(_gio("9h–18h30"), (time(9), time(18, 30)))
        self.assertEqual(_gio("08:15 - 17:45"), (time(8, 15), time(17, 45)))
        self.assertIsNone(_gio("24/7"), "24/7 khong phai khung gio")

    def test_doc_duoc_gio_kieu_nguoi_viet(self):
        """Bot ghi sai định dạng thì follow-up im luôn mà không báo lỗi."""
        self.assertEqual(Phieu("x", {"g": "2026-09-09 10:00"}).gio("g"),
                         datetime(2026, 9, 9, 10, 0))
        self.assertEqual(Phieu("x", {"g": "10h ngày 9/9"}).gio("g", nam_mac_dinh=2026),
                         datetime(2026, 9, 9, 10, 0))
        self.assertIsNone(Phieu("x", {"g": "hôm qua"}).gio("g"))

    def test_mau_phieu_chot_dinh_dang_gio(self):
        """Đọc cứu chỉ là lưới an toàn — template phải nói rõ định dạng."""
        from pathlib import Path
        goc = Path(__file__).resolve().parent.parent
        for f in ("memory/phieu/MAU.md", "skills/phieu/SKILL.md"):
            self.assertIn("YYYY-MM-DD HH:MM", (goc / f).read_text(encoding="utf-8"), f)

    def test_soi_bay_hoi_khong_mien_tru_qua_tay(self):
        """Miễn trừ rộng quá là kiểm cho có."""
        from sim.nen import MIEN_TRU
        n = Nen.dung()
        dong = [d for _, noi in n.manh for d in noi.split("\n")]
        bo_qua = sum(1 for d in dong if MIEN_TRU.search(d))
        self.assertLess(bo_qua / len(dong), 0.15, "mien tru qua 15% nen la kiem cho co")

    def test_soi_bay_hoi_bat_duoc_dau_thoi_gian(self):
        class NenGia(Nen):
            pass
        gia = NenGia([("gia.md", "Phiên bắt đầu lúc 14:32 ngày 2026-09-11.")])
        loi = gia.soi_bay_hoi()
        self.assertTrue(loi, "phai bat duoc dau thoi gian o nen")

    def test_soi_bay_hoi_bo_qua_khoi_code(self):
        gia = Nen([("x.md", "Mẫu:\n\n```\nupdated: 2026-09-09\n```\n\nHết.")])
        self.assertEqual(gia.soi_bay_hoi(), [], "khoi code la vi du, khong tinh")
