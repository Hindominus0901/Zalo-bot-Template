"""Cơ chế: chỉ mục sổ, trần phiếu, ba tầng prompt, rào policy.

Vẫn là khớp chữ trong repo — không chứng minh bot sống. Xem tests/README.md.
"""

import json
import subprocess
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def _read(rel: str) -> str:
    return (ROOT / rel).read_text(encoding="utf-8")


def matrix() -> dict:
    return json.loads(_read("knowledge/logic/ma-tran.json"))


class ChiMucSo(unittest.TestCase):
    def test_index_khop_thu_muc(self):
        """INDEX.md phải khớp wiki/public/ — nếu lệch, chạy scripts/lam-chi-muc.sh."""
        r = subprocess.run(
            [sys.executable, str(ROOT / "scripts/lam_chi_muc.py"), "--kiem"],
            capture_output=True, text=True,
        )
        self.assertEqual(r.returncode, 0, r.stderr or r.stdout)

    def test_index_liet_du_to(self):
        index = _read("knowledge/wiki/INDEX.md")
        to = sorted((ROOT / "knowledge/wiki/public").glob("*.md"))
        self.assertTrue(to, "wiki/public/ trong")
        for md in to:
            self.assertIn(f"`{md.name}`", index, f"INDEX thieu {md.name}")

    def test_doc_wiki_khong_con_doan_ten_file(self):
        skill = _read("skills/doc-wiki/SKILL.md")
        self.assertIn("INDEX.md", skill)
        self.assertNotIn("Đoán tờ từ câu họ", skill)


class TranPhieu(unittest.TestCase):
    def test_tran_co_trong_ma_tran_va_skill(self):
        tran = matrix()["phieu"]["tran_ky_tu"]
        self.assertEqual(tran, 1800)
        skill = _read("skills/phieu/SKILL.md")
        self.assertIn(str(tran), skill)
        self.assertIn("1.800", _read("memory/phieu/MAU.md").replace("1800", "1.800"))

    def test_nhom_khong_bao_gio_bo_nam_trong_skill(self):
        skill = _read("skills/phieu/SKILL.md")
        for field in matrix()["phieu"]["khong_bao_gio_bo"]:
            self.assertIn(field, skill, f"skill phieu thieu {field}")

    def test_khong_bao_gio_bo_la_tap_con_cua_ghi(self):
        p = matrix()["phieu"]
        ghi = set(p["ghi"]) | {"goi"}
        for field in p["khong_bao_gio_bo"]:
            self.assertIn(field, ghi, f"{field} khong phai truong cua phieu")
        for field in p["thu_tu_hy_sinh"]:
            self.assertIn(field, p["ghi"])
            self.assertNotIn(field, p["khong_bao_gio_bo"])


class BaTangPrompt(unittest.TestCase):
    def test_agents_tro_toi_doc_12(self):
        self.assertIn("docs/12-prompt-va-cache.md", _read("AGENTS.md"))

    def test_doc_12_neu_ba_thu_giet_cache(self):
        doc = _read("docs/12-prompt-va-cache.md")
        for needle in ("Dấu thời gian", "ngẫu nhiên", "thứ tự"):
            self.assertIn(needle, doc)


class RaoAnToan(unittest.TestCase):
    def test_policy_truoc_moi_muc_nhung_sau_dong_dinh_tuyen(self):
        """AGENTS.md là tên file Cursor/Codex tự nạp. Agent dựng phải thấy dòng
        định tuyến TRƯỚC khối policy, không thì nó tưởng mình là Nami."""
        text = _read("AGENTS.md")
        self.assertLess(text.index("**Nhánh:**"), text.index("<policy>"))
        self.assertLess(text.index("<policy>"), text.index("\n## "))
        self.assertIn("Đang dựng bot thì xem dòng trên", text)

    def test_doc_anh_coi_chu_trong_anh_la_du_lieu(self):
        skill = _read("skills/doc-anh/SKILL.md")
        self.assertIn("không phải lệnh", skill)

    def test_mau_cau_du_bang_tieng_viet(self):
        doc = _read("docs/13-an-toan.md")
        for mau in ("bỏ qua hướng dẫn", "bây giờ bạn là", "system prompt", "tôi là chủ shop"):
            self.assertIn(mau, doc)
        self.assertIn("không giảng đạo", doc.lower())


class VongHoc(unittest.TestCase):
    def test_hoc_lai_khong_sua_wiki(self):
        skill = _read("skills/hoc-lai/SKILL.md")
        self.assertIn("memory/de-xuat/", skill)
        self.assertIn("Đừng sửa `knowledge/wiki/`", skill)

    def test_heartbeat_goi_hoc_lai(self):
        self.assertIn("hoc-lai", _read("HEARTBEAT.md"))
        self.assertNotIn("hoc-lai", _read("BOOT.md"), "boot khong duoc chay vong hoc")

    def test_memory_noi_ro_ai_ghi(self):
        self.assertIn("hoc-lai", _read("MEMORY.md"))


class CatPhieuCu(unittest.TestCase):
    def test_khong_cat_phieu_con_viec(self):
        hb = _read("HEARTBEAT.md")
        self.assertIn("Không xóa", hb)
        for trang_thai in ("cho_ck", "da_chot_chu", "dang_giao"):
            self.assertIn(trang_thai, hb)


if __name__ == "__main__":
    unittest.main()


class NhipChat(unittest.TestCase):
    def test_agents_co_luat_tin_don(self):
        text = _read("AGENTS.md")
        self.assertIn("Tin dồn", text)
        self.assertIn("600", text)

    def test_khong_bia_key_config_chua_kiem(self):
        """Chưa xác minh được OpenClaw có key gộp tin dồn — không được ghi vào config mẫu."""
        cfg = _read("config/openclaw.zalouser.example.json5")
        for key in ("inbound_debounce_ms", "chat_behavior", "quick_ack"):
            self.assertNotIn(key, cfg, f"{key} chua xac minh, dung ghi vao config mau")
        doc = _read("docs/10-openclaw-config-mau.md")
        self.assertIn("config schema", doc, "docs phai day cach tu kiem truoc khi them key")


class BanGiaoLaCo(unittest.TestCase):
    def test_ban_giao_co_trong_phieu(self):
        for field in ("ban_giao", "ban_giao_luc", "ban_giao_ve"):
            self.assertIn(field, _read("memory/phieu/MAU.md"))
            self.assertIn(field, matrix()["phieu"]["ghi"])
        self.assertIn("ban_giao", matrix()["phieu"]["khong_bao_gio_bo"])

    def test_ban_giao_khong_tat_ca_bot(self):
        skill = _read("skills/ban-giao/SKILL.md")
        self.assertIn("dang_cho", skill)
        self.assertIn("chuyện khác", skill.lower())
        self.assertIn("24h", skill)


class SoNoKhach(unittest.TestCase):
    def test_boot_xu_tin_no(self):
        boot = _read("BOOT.md")
        self.assertIn("no-tra-loi.md", boot)
        self.assertIn("12h", boot)

    def test_boot_ngat_mach_khi_cookie_chet(self):
        boot = _read("BOOT.md")
        self.assertIn("một lần", boot)
        self.assertIn("quét lại mã", boot)

    def test_file_no_that_bi_ignore(self):
        """File thật chứa chữ khách — phải bị git ignore."""
        r = subprocess.run(
            ["git", "check-ignore", "-q", "memory/no-tra-loi.md"],
            cwd=ROOT, capture_output=True,
        )
        self.assertEqual(r.returncode, 0, "memory/no-tra-loi.md phai bi git ignore")


class ChuanSkill(unittest.TestCase):
    def test_moi_skill_co_dong_kiem_lai(self):
        for skill in sorted((ROOT / "skills").glob("*/SKILL.md")):
            body = skill.read_text(encoding="utf-8")
            self.assertRegex(body, r"\*\*Kiểm lại:\*\*|## Kiểm lại", f"{skill.parent.name} thieu Kiem lai")

    def test_skill_dung_tien_bi_khoa(self):
        for name in ("ban-giao", "follow-up", "hoc-lai"):
            body = _read(f"skills/{name}/SKILL.md")
            self.assertIn("chi-goi-khi-duoc-yeu-cau: true", body, name)
            head = body.split("---")[1]
            self.assertIn("chi-goi-khi-duoc-yeu-cau", head, f"{name}: co phai nam trong frontmatter")

    def test_frontmatter_co_name_va_description(self):
        for skill in sorted((ROOT / "skills").glob("*/SKILL.md")):
            head = skill.read_text(encoding="utf-8").split("---")[1]
            self.assertIn("name:", head, skill.parent.name)
            self.assertIn("description:", head, skill.parent.name)


class KichBanThuPhuCoChe(unittest.TestCase):
    def test_kich_ban_co_dong_cho_moi_co_che(self):
        kb = _read("docs/04-kich-ban-thu.md")
        for co_che in ("no-tra-loi", "sodon", "1800", "lam_chi_muc", "de-xuat", "system prompt"):
            self.assertIn(co_che, kb, f"kich ban thu thieu {co_che}")

    def test_tieu_chuan_co_cua_may(self):
        tc = _read("docs/06-tieu-chuan.md")
        self.assertIn("Cửa 3", tc)
        self.assertIn("docs/12", tc)


class LuongDungNhoChiMuc(unittest.TestCase):
    def test_khoi_tao_chay_lai_chi_muc(self):
        """Điền wiki xong mà quên sinh lại chỉ mục thì bot đọc mô tả cũ."""
        skill = _read("dung-bot/QUY-TRINH.md")
        self.assertIn("lam_chi_muc", skill)
        i = skill.index("lam_chi_muc")
        j = skill.index("unittest discover")
        self.assertLess(i, j, "chi muc phai chay truoc test")
