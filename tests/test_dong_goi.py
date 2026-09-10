"""Đóng gói: cửa vào cho agent lạ, chuẩn bị cho khách lạ, một nguồn quy trình.

Vẫn là khớp chữ trong repo. Xem tests/README.md.
"""

import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
NGUON = "dung-bot/QUY-TRINH.md"


def _read(rel: str) -> str:
    return (ROOT / rel).read_text(encoding="utf-8")


class CuaVao(unittest.TestCase):
    """Không biết trước khách dùng agent nào — cửa nào cũng phải tới nguồn."""

    CUA = [
        "CLAUDE.md",                        # Claude Code
        "AGENTS.md",                        # Cursor / Codex tự nạp
        ".cursor/rules/dung-bot.mdc",       # Cursor
        ".github/copilot-instructions.md",  # Copilot
        "README.md",                        # người
        ".claude/skills/khoi-tao/SKILL.md",
    ]

    def test_moi_cua_tro_ve_mot_nguon(self):
        for cua in self.CUA:
            self.assertIn(NGUON, _read(cua), f"{cua} khong tro toi {NGUON}")

    def test_cua_khong_phai_claude_code_noi_ro_agents_md_khong_danh_cho_ho(self):
        """AGENTS.md là não bot. Agent dựng đọc nhầm là tưởng mình là Nami."""
        for cua in ("CLAUDE.md", ".cursor/rules/dung-bot.mdc", ".github/copilot-instructions.md"):
            body = _read(cua)
            self.assertIn("AGENTS.md", body, cua)
            self.assertRegex(body, r"không phải hướng dẫn cho (bạn|bạn\.)", cua)

    def test_skill_khoi_tao_khong_chep_lai_quy_trinh(self):
        """Một nguồn. Skill là con trỏ mỏng, không phải bản sao."""
        skill = _read(".claude/skills/khoi-tao/SKILL.md")
        self.assertLess(len(skill), 2500, "skill khoi-tao phinh ra = dang nhan ban quy trinh")
        for buoc in ("## B2", "## B4", "## B5", "## B6"):
            self.assertNotIn(buoc, skill, f"skill khoi-tao chep lai {buoc}")

    def test_nguon_co_du_b0_toi_b7(self):
        nguon = _read(NGUON)
        for b in range(8):
            self.assertRegex(nguon, rf"B{b}\b", f"{NGUON} thieu B{b}")


class ChuanBi(unittest.TestCase):
    def test_chuan_bi_co_du_thu_bat_buoc(self):
        cb = _read("CHUAN-BI.md")
        for muc in ("API key", "nạp tiền", "số điện thoại", "nick Zalo thứ hai",
                    "24/7", "git", "Python"):
            self.assertIn(muc, cb, f"CHUAN-BI.md thieu {muc}")

    def test_noi_ro_la_chi_phi_hang_thang(self):
        """Thứ khách bực nhất nếu phát hiện muộn."""
        cb = _read("CHUAN-BI.md")
        self.assertIn("hàng tháng", cb)

    def test_duoc_tro_toi_tu_cho_khach_doc(self):
        for f in ("README.md", "docs/08-luong-chu-shop.md"):
            self.assertIn("CHUAN-BI.md", _read(f), f)

    def test_b0_dung_khi_chua_co_key(self):
        self.assertIn("mã kết nối", _read(NGUON))
        self.assertIn("M3", _read("PHONG-VAN.md"))
        self.assertIn("M3", _read("docs/bo-cau-hoi.md"))


class ChayDuocTrenWindows(unittest.TestCase):
    """Windows sạch không có bash, và `python3` hay mở Microsoft Store."""

    def test_khong_bat_buoc_bash_trong_tai_lieu(self):
        for md in ROOT.rglob("*.md"):
            if ".git" in md.parts:
                continue
            body = md.read_text(encoding="utf-8")
            self.assertNotIn("bash scripts/", body,
                             f"{md.relative_to(ROOT)}: lenh bash-only, Windows chay khong duoc")

    def test_co_chi_dan_windows(self):
        for f in ("tests/README.md", "docs/05-thiet-lap.md", NGUON):
            self.assertIn("py", _read(f), f)

    def test_script_chay_bang_python_thuan(self):
        self.assertTrue((ROOT / "scripts/lam_chi_muc.py").is_file())


class VpsHeadless(unittest.TestCase):
    def test_co_huong_dan_quet_ma_khong_man_hinh(self):
        doc = _read("docs/14-vps-headless.md")
        for muc in ("tmux", "scp", "127.0.0.1", "quét lại"):
            self.assertIn(muc, doc, f"docs/14 thieu {muc}")

    def test_quet_lai_la_viec_lap(self):
        """Cookie sẽ chết. Không có quy trình quét lại thì bot im mà chủ không biết làm gì."""
        doc = _read("docs/14-vps-headless.md")
        self.assertIn("việc lặp", doc)
        self.assertIn("BOOT.md", doc)

    def test_noi_ro_chua_xac_minh(self):
        self.assertIn("chưa xác minh", _read("docs/14-vps-headless.md").lower())

    def test_duoc_noi_vao_luong_dung(self):
        for f in ("docs/05-thiet-lap.md", NGUON, "CHUAN-BI.md"):
            body = _read(f)
            self.assertTrue("14-vps-headless" in body or "không màn hình" in body, f)


class DongBoHaiBanPhongVan(unittest.TestCase):
    """PHONG-VAN.md và docs/bo-cau-hoi.md cố ý là hai bản của cùng nội dung."""

    def test_cung_so_chu_de(self):
        def chu_de(body: str) -> list[str]:
            return re.findall(r"^## (\d+)\.", body, re.M)

        self.assertEqual(chu_de(_read("PHONG-VAN.md")), chu_de(_read("docs/bo-cau-hoi.md")))


if __name__ == "__main__":
    unittest.main()
