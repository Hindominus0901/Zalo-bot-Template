"""Lớp vui / lầy / chuyện ngoài shop, và luật nhóm.

Vẫn là khớp chữ trong repo. Xem tests/README.md.
"""

import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
VUI = "knowledge/vui-va-ngoai-le.md"


def _read(rel: str) -> str:
    return (ROOT / rel).read_text(encoding="utf-8")


class CongTacTatHai(unittest.TestCase):
    """Lầy mạnh mà không tắt đúng lúc thì tệ hơn khô khan."""

    TAT = ["Tiền", "Hàng lỗi", "bực", "gấp", "bàn giao", "Quấy rối", "buồn", "hai tin đầu"]

    def test_du_cong_tac(self):
        body = _read(VUI)
        muc = body[body.index("## Công tắc tắt"):body.index("## Chuyện ngoài shop")]
        for x in self.TAT:
            self.assertIn(x, muc, f"cong tac tat thieu: {x}")

    def test_khong_co_quan_tinh(self):
        muc = _read(VUI)
        self.assertIn("đổi theo ngay trong tin đó", muc)
        self.assertIn("coi như đang bực", muc)

    def test_soul_tro_toi_luat_day_du(self):
        soul = _read("SOUL.md")
        self.assertIn("vui-va-ngoai-le", soul)
        self.assertIn("tắt hẳn", soul.lower())


class BayNhomKhongDam(unittest.TestCase):
    NHOM = ["Y tế", "Pháp lý", "Tài chính", "Chính trị", "Tự hại", "Người lớn", "Học hộ"]

    def test_du_bay_nhom(self):
        body = _read(VUI)
        muc = body[body.index("## Không dám"):body.index("## Trong nhóm")]
        for x in self.NHOM:
            self.assertIn(x, muc, f"danh sach khong dam thieu: {x}")

    def test_tu_choi_khong_thanh_buc_tuong(self):
        muc = _read(VUI)
        self.assertIn("bức tường", muc)
        self.assertIn("không giảng đạo", muc.lower())

    def test_tu_hai_xu_khac(self):
        muc = _read(VUI)
        self.assertIn("bỏ hài hẳn", muc)
        self.assertIn("ban-giao", muc)

    def test_agents_va_router_deu_liet(self):
        for f in ("AGENTS.md", "knowledge/moi-loai-cau-hoi.md", "knowledge/cach-tu-van.md"):
            body = _read(f).lower()
            self.assertIn("không dám", body, f)
            self.assertIn("tự hại", body, f)


class NgoaiLeDaMo(unittest.TestCase):
    def test_luat_cu_khong_con_o_file_nao(self):
        """Luật cũ đã bỏ. Miễn trừ: quyet-dinh.md và vui-va-ngoai-le.md — hai file
        đó trích lại luật cũ để nói rõ là nó đã đổi."""
        for md in ROOT.rglob("*.md"):
            if ".git" in md.parts or md.name in ("quyet-dinh.md", "vui-va-ngoai-le.md"):
                continue
            body = md.read_text(encoding="utf-8")
            for cu in ("một nhịp, kéo về shop", "một nhịp rồi kéo về shop",
                       "một nhịp thành thật, không làm thầy, kéo về shop",
                       "một nhịp thành thật, kéo về shop"):
                self.assertNotIn(cu, body, f"{md.relative_to(ROOT)} con luat cu: {cu}")

    def test_quyet_dinh_ghi_lai_viec_mo(self):
        qd = _read("docs/quyet-dinh.md")
        self.assertIn("đã mở", qd)
        self.assertIn("vui-va-ngoai-le", qd)

    def test_khong_bia_chuyen_doi(self):
        self.assertIn("không chắc thì nói không chắc", _read(VUI))
        self.assertIn("Không bịa chuyện đời", _read("AGENTS.md") + _read(VUI))

    def test_viec_shop_thang_khi_chen_ngang(self):
        self.assertIn("việc thắng ngay", _read(VUI))


class LuatNhom(unittest.TestCase):
    def test_van_phai_goi_ten(self):
        """Nhóm vẫn requireMention — đây là thứ giữ cho lầy mạnh không thành spam."""
        self.assertIn("requireMention", _read("config/openclaw.zalouser.example.json5"))
        self.assertIn("chỉ nói khi được gọi tên", _read(VUI))
        self.assertIn("requireMention", _read("docs/quyet-dinh.md"))

    def test_khong_dua_nham_nguoi_thu_ba(self):
        body = _read(VUI)
        muc = body[body.index("## Trong nhóm"):body.index("## Reaction")]
        self.assertIn("người thứ ba", muc)
        self.assertIn("Không hùa", muc)
        self.assertIn("không bênh ai", muc)

    def test_bi_ca_nhom_choc(self):
        self.assertIn("không tự ái", _read(VUI))


class ThangLay(unittest.TestCase):
    def test_nguoi_la_chua_lay(self):
        body = _read(VUI)
        muc = body[body.index("## Thang lầy"):body.index("## Công tắc tắt")]
        self.assertIn("Chưa lầy", muc)

    def test_tu_gieu_la_an_toan_nhat(self):
        self.assertIn("Tự giễu", _read(VUI))

    def test_co_vi_du_dung_sai(self):
        mau = _read("knowledge/hoi-thoai-mau.md")
        self.assertIn("Lầy — đúng độ / quá độ", mau)
        for x in ("quán tính", "bot à", "panadol"):
            self.assertIn(x, mau, f"hoi-thoai-mau thieu vi du: {x}")


class ReactionSticker(unittest.TestCase):
    def test_reaction_thoai_mai_sticker_han_che(self):
        body = _read(VUI)
        muc = body[body.index("## Reaction và sticker"):body.index("## Kiểm lại")]
        self.assertIn("thoải mái", muc)
        self.assertIn("Thỉnh thoảng" if "Thỉnh thoảng" in muc else "thỉnh thoảng", muc)
        self.assertIn("tắt", muc)

    def test_giong_noi_nhac_lai(self):
        self.assertIn("Thả cảm xúc", _read("knowledge/giong-noi.md"))


class ChuShopHaDuocMuc(unittest.TestCase):
    def test_co_cau_phong_van_o_ca_hai_ban(self):
        for f in ("PHONG-VAN.md", "docs/bo-cau-hoi.md"):
            self.assertIn("vui và lầy", _read(f), f)

    def test_van_muoi_chu_de(self):
        for f in ("PHONG-VAN.md", "docs/bo-cau-hoi.md"):
            so = re.findall(r"^## (\d+)\.", _read(f), re.M)
            self.assertEqual(so, [str(i) for i in range(1, 11)], f)


if __name__ == "__main__":
    unittest.main()
