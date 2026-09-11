"""Sáu tình huống CSKH hay gặp trên Zalo mà lớp nội dung từng bỏ sót.

Vẫn là khớp chữ trong repo. Xem tests/README.md.
"""

import json
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
TH = "knowledge/tinh-huong.md"


def _read(rel: str) -> str:
    return (ROOT / rel).read_text(encoding="utf-8")


def matrix() -> dict:
    return json.loads(_read("knowledge/logic/ma-tran.json"))


class SauMucMoi(unittest.TestCase):
    MUC = [
        "## Khách xin số tài khoản / mã QR",
        "## Khách bấm gọi Zalo",
        "## Món shop không bán",
        "## Chửi bậy / quấy rối / gạ gẫm",
        "## Khách thu hồi tin",
    ]

    def test_du_muc(self):
        body = _read(TH)
        for muc in self.MUC:
            self.assertIn(muc, body, f"tinh-huong.md thieu {muc}")

    def test_ngay_nghi_nam_trong_muc_ngoai_gio(self):
        body = _read(TH)
        self.assertIn("Ngày nghỉ / Tết", body)


class KhongDuaSoTaiKhoan(unittest.TestCase):
    def test_tool_bi_khoa_o_ca_hai_noi(self):
        khong = json.loads(_read("knowledge/logic/tools.json"))["khong"]
        for x in ("gui_qr", "gui_stk"):
            self.assertIn(x, khong, x)
            self.assertIn(x, _read("TOOLS.md"), x)

    def test_luat_la_ban_giao(self):
        body = _read(TH)
        muc = body[body.index("## Khách xin số tài khoản"):body.index("## OTP")]
        self.assertIn("ban-giao", muc)
        self.assertIn("không", muc.lower())

    def test_wiki_thanh_toan_cam_dien_so(self):
        self.assertIn("Đừng điền số tài khoản", _read("knowledge/wiki/public/thanh-toan.md"))

    def test_khong_co_chuoi_nao_giong_so_tai_khoan(self):
        """Bot đọc được knowledge/ và skills/ — đừng để lọt số nào vào đó."""
        for goc in ("knowledge", "skills"):
            for md in (ROOT / goc).rglob("*.md"):
                for dong in md.read_text(encoding="utf-8").split("\n"):
                    if "CHỜ CHỦ SHOP" in dong or "```" in dong:
                        continue
                    self.assertIsNone(
                        re.search(r"(?<!\d)\d{8,16}(?!\d)", dong),
                        f"{md.relative_to(ROOT)}: chuoi giong so tai khoan -> {dong.strip()[:70]}",
                    )


class NgayNghi(unittest.TestCase):
    def test_user_md_co_truong(self):
        self.assertIn("Ngày nghỉ / Tết", _read("USER.md"))

    def test_ca_followup_va_heartbeat_deu_rao(self):
        for f in ("skills/follow-up/SKILL.md", "HEARTBEAT.md"):
            self.assertIn("ngày nghỉ", _read(f).lower(), f)

    def test_khong_don_gui_bu(self):
        self.assertIn("gửi bù", _read("skills/follow-up/SKILL.md"))

    def test_ma_tran_co_co(self):
        self.assertTrue(matrix()["followup"]["ngay_nghi_khong_gui"])

    def test_wiki_gio_truc_co_cho_dien(self):
        self.assertIn("Ngày nghỉ", _read("knowledge/wiki/public/gio-truc.md"))


class GoiZalo(unittest.TestCase):
    def test_noi_ro_khong_nghe_duoc_va_khong_hua_goi_lai(self):
        body = _read(TH)
        muc = body[body.index("## Khách bấm gọi Zalo"):body.index("## “Ai đây”")]
        self.assertIn("không nghe máy được", muc)
        self.assertIn("USER.md", muc)
        self.assertIn("Đừng hứa", muc)


class KhongBanMonDo(unittest.TestCase):
    def test_nam_truoc_muc_het_hang_va_muc_het_hang_con_nguyen(self):
        body = _read(TH)
        self.assertIn("## Hết hàng / còn không", body, "doi ten muc Het hang la vo test_stress")
        self.assertLess(body.index("## Món shop không bán"), body.index("## Hết hàng / còn không"))

    def test_phan_biet_voi_het_hang(self):
        body = _read(TH)
        muc = body[body.index("## Món shop không bán"):body.index("## Hết hàng / còn không")]
        self.assertIn("hết hàng", muc.lower())
        self.assertIn("CHỜ CHỦ SHOP", muc, "phai noi ro so con cho thi khong duoc noi khong ban")

    def test_router_cau_hoi_tro_sang(self):
        self.assertIn("Món shop không bán", _read("knowledge/moi-loai-cau-hoi.md"))

    def test_van_chin_nhom(self):
        """Đừng thêm nhóm thứ mười."""
        self.assertIn("Chín nhóm", _read("knowledge/moi-loai-cau-hoi.md"))


class QuayRoi(unittest.TestCase):
    def test_tach_khi_va_tuduy_khop_nhau(self):
        self.assertIn("quay_roi", matrix()["tach_khi"])
        self.assertIn("quay_roi", _read("knowledge/tuduy-cskh.md"))

    def test_khong_dung_giong_phan_nan(self):
        body = _read(TH)
        muc = body[body.index("## Chửi bậy"):body.index("## Ứng tuyển")]
        self.assertIn("Không xin lỗi", muc)
        self.assertIn("Không giảng đạo", muc)
        self.assertIn("không chặn được", muc)

    def test_skill_phan_nan_phan_luong(self):
        skill = _read("skills/xu-ly-phan-nan/SKILL.md")
        self.assertIn("quấy rối", skill.lower())
        self.assertIn("**Kiểm lại:**", skill)

    def test_bang_agents_co_hang(self):
        self.assertIn("Chửi bậy", _read("AGENTS.md"))


class ThuHoiTin(unittest.TestCase):
    def test_khong_nhac_lai(self):
        body = _read(TH)
        muc = body[body.index("## Khách thu hồi tin"):body.index("## Shop ở đâu")]
        self.assertIn("Đừng nhắc lại", muc)

    def test_skill_phieu_co_luat(self):
        skill = _read("skills/phieu/SKILL.md")
        self.assertIn("thu hồi", skill)
        self.assertIn("**Kiểm lại:**", skill)


class PhongVanVanMuoiChuDe(unittest.TestCase):
    def test_khong_them_chu_de_thu_muoi_mot(self):
        for f in ("PHONG-VAN.md", "docs/bo-cau-hoi.md"):
            so = re.findall(r"^## (\d+)\.", _read(f), re.M)
            self.assertEqual(so, [str(i) for i in range(1, 11)], f)


if __name__ == "__main__":
    unittest.main()
