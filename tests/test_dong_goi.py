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
        "AGENTS.md",                        # Codex + agent lạ tự nạp
        "GEMINI.md",                        # Gemini / Antigravity
        ".cursor/rules/dung-bot.mdc",       # Cursor
        ".github/copilot-instructions.md",  # Copilot
        "README.md",                        # người
        ".claude/skills/khoi-tao/SKILL.md",
    ]

    # Năm agent template hứa chạy được. Đổi danh sách thì đổi cả CUA ở trên.
    AGENT = ("Claude Code", "Cursor", "Codex", "Antigravity", "Copilot")

    def test_moi_cua_tro_ve_mot_nguon(self):
        for cua in self.CUA:
            self.assertIn(NGUON, _read(cua), f"{cua} khong tro toi {NGUON}")

    def test_cua_khong_phai_claude_code_noi_ro_agents_md_khong_danh_cho_ho(self):
        """AGENTS.md là não bot. Agent dựng đọc nhầm là tưởng mình là Nami."""
        for cua in ("CLAUDE.md", "GEMINI.md", ".cursor/rules/dung-bot.mdc",
                    ".github/copilot-instructions.md"):
            body = _read(cua)
            self.assertIn("AGENTS.md", body, cua)
            self.assertRegex(body, r"không phải hướng dẫn cho (bạn|bạn\.)", cua)

    def test_tieu_de_agents_md_tu_noi_no_khong_danh_cho_coding_agent(self):
        """Codex/Antigravity nạp AGENTS.md trước cả khi đọc hết. Agent nào chỉ
        liếc H1 cũng phải hiểu ngay là đừng làm theo file này."""
        h1 = _read("AGENTS.md").splitlines()[0]
        self.assertIn("KHÔNG phải hướng dẫn", h1, f"H1 hien tai: {h1!r}")

    def test_dau_agents_md_chi_duong_cho_tung_agent(self):
        """Tám dòng đầu phải nêu đích danh cửa của từng agent, không chỉ nói chung."""
        dau = "\n".join(_read("AGENTS.md").splitlines()[:10])
        for cua in ("CLAUDE.md", "GEMINI.md", ".cursor/rules/",
                    "copilot-instructions.md", NGUON):
            self.assertIn(cua, dau, f"dau AGENTS.md thieu {cua}")

    def test_hai_file_khach_doc_neu_du_ten_agent(self):
        """Khách dùng Codex mà README chỉ nói Cursor thì tưởng template khong hop."""
        for tai_lieu in ("README.md", "CHUAN-BI.md", "HUONG-DAN-AGENT.md"):
            body = _read(tai_lieu)
            for ten in self.AGENT:
                self.assertIn(ten, body, f"{tai_lieu} thieu {ten}")

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


class FileCuaShop(unittest.TestCase):
    """Khách điền đè lên file template — phải biết file nào của ai khi git pull."""

    MARK = "<!-- FILE CỦA SHOP — giữ bản của bạn khi cập nhật template -->"

    def _danh_sach(self) -> list[str]:
        doc = _read("docs/15-cap-nhat.md")
        sec = doc.split("### Của shop")[1].split("### Một phần")[0]
        return re.findall(r"^- `([^`]+)`$", sec, re.M)

    def test_danh_sach_khong_rong(self):
        self.assertGreater(len(self._danh_sach()), 10)

    def test_moi_file_trong_danh_sach_ton_tai_va_co_dau(self):
        for f in self._danh_sach():
            p = ROOT / f
            self.assertTrue(p.is_file(), f"docs/15 liet {f} nhung khong co file")
            self.assertTrue(p.read_text(encoding="utf-8").startswith(self.MARK),
                            f"{f} thieu dau FILE CUA SHOP")

    def test_khong_file_nao_mang_dau_ma_thieu_trong_danh_sach(self):
        """Chiều ngược lại — danh sách không được lệch với thực tế."""
        ds = set(self._danh_sach())
        for md in ROOT.rglob("*.md"):
            if ".git" in md.parts:
                continue
            if md.read_text(encoding="utf-8").startswith(self.MARK):
                rel = str(md.relative_to(ROOT))
                self.assertIn(rel, ds, f"{rel} co dau nhung khong nam trong docs/15")

    def test_moi_to_wiki_deu_la_cua_shop(self):
        for md in (ROOT / "knowledge/wiki/public").glob("*.md"):
            self.assertTrue(md.read_text(encoding="utf-8").startswith(self.MARK),
                            f"{md.name} thieu dau")


class ChiMucVanDocDuocFrontmatter(unittest.TestCase):
    """Dấu FILE CỦA SHOP nằm trước `---` từng làm hỏng bộ đọc frontmatter."""

    def test_index_co_title_that_khong_phai_ten_file(self):
        index = _read("knowledge/wiki/INDEX.md")
        self.assertNotIn("(chưa có mô tả)", index,
                         "INDEX mat summary — bo doc frontmatter dang hong")
        self.assertIn("Phí ship", index + _read("knowledge/wiki/public/ship.md"))


class GhimVersion(unittest.TestCase):
    def test_co_version_va_changelog(self):
        self.assertTrue((ROOT / "VERSION").is_file())
        self.assertTrue((ROOT / "CHANGELOG.md").is_file())

    def test_docs_05_co_khoi_da_test_voi(self):
        """Không đẩy fix được cho bản khách đã cầm — ít nhất phải có mốc đối chiếu."""
        doc = _read("docs/05-thiet-lap.md")
        self.assertIn("Đã test với", doc)
        self.assertIn("openclaw --version", doc)

    def test_co_chi_dan_khi_lenh_khong_nhu_tai_lieu(self):
        doc = _read("docs/05-thiet-lap.md")
        self.assertIn("config schema", doc)
        self.assertIn("đừng đoán", doc.lower())


class LienKetNoiBo(unittest.TestCase):
    """Ba đợt sửa đã đổi chỗ nhiều file. Link gãy là agent dựng đi vào ngõ cụt."""

    BO_QUA = ("http://", "https://", "mailto:", "#")

    def test_moi_link_markdown_deu_ton_tai(self):
        hong = []
        for md in ROOT.rglob("*.md"):
            if ".git" in md.parts:
                continue
            for dich in re.findall(r"\]\(([^)]+)\)", md.read_text(encoding="utf-8")):
                if dich.startswith(self.BO_QUA):
                    continue
                duong = (md.parent / dich.split("#")[0]).resolve()
                if not duong.exists():
                    hong.append(f"{md.relative_to(ROOT)} -> {dich}")
        self.assertEqual(hong, [], f"link gay: {hong}")

    def test_moi_duong_dan_trong_backtick_deu_ton_tai(self):
        """`knowledge/abc.md` trong backtick cũng là chỉ dẫn — sai là bot đọc hụt."""
        hong = []
        mau = re.compile(r"`((?:knowledge|skills|docs|config|scripts|tests|dung-bot)/[A-Za-z0-9._/-]+\.(?:md|json|json5|py|sh))`")
        # memory/ bị bỏ qua: file trong đó sinh lúc chạy (memory/2026-09-11.md,
        # memory/no-tra-loi.md), đúng là không có trong repo.
        for md in ROOT.rglob("*.md"):
            if ".git" in md.parts:
                continue
            for dich in set(mau.findall(md.read_text(encoding="utf-8"))):
                if not (ROOT / dich).exists():
                    hong.append(f"{md.relative_to(ROOT)} -> {dich}")
        self.assertEqual(hong, [], f"duong dan sai: {hong}")


class RepoTemplateGithub(unittest.TestCase):
    """Khách bấm Use this template rồi mở bằng agent của họ — mặt tiền phải đủ."""

    def test_co_license(self):
        lic = _read("LICENSE")
        self.assertIn("KHÔNG ĐƯỢC LÀM", lic, "phai noi ro cai khong duoc lam")
        self.assertIn("Bán lại", lic)
        self.assertIn("ZALO", lic.upper(), "phai canh bao rui ro khoa nick")

    def test_co_ci_chay_du_bon_cong(self):
        ci = _read(".github/workflows/kiem-tra.yml")
        for buoc in ("lam_chi_muc.py --kiem", "unittest discover",
                     "sim.chay nhip", "sim.chay nen"):
            self.assertIn(buoc, ci, f"CI thieu buoc: {buoc}")

    def test_ci_khong_can_cai_gi(self):
        """Cả test lẫn giả lập chạy bằng stdlib — CI không được pip install."""
        self.assertNotIn("pip install", _read(".github/workflows/kiem-tra.yml"))

    def test_readme_day_use_this_template(self):
        rm = _read("README.md")
        self.assertIn("Use this template", rm)
        self.assertIn("CHUAN-BI.md", rm)
        self.assertIn("dung-bot/QUY-TRINH.md", rm)

    def test_readme_noi_ro_dung_duoc_cho_nganh_nao(self):
        rm = _read("README.md")
        for nganh in ("coaching", "tư vấn", "dịch vụ"):
            self.assertIn(nganh, rm.lower(), nganh)
