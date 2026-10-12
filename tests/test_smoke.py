#!/usr/bin/env python3
"""Smoke: file bắt buộc, skill, gitignore, config CSKH, không lộ secret."""
from __future__ import annotations

import json
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def _read(rel: str) -> str:
    return (ROOT / rel).read_text(encoding="utf-8")


class SmokeRequiredFiles(unittest.TestCase):
    REQUIRED = [
        "SOUL.md",
        "AGENTS.md",
        "IDENTITY.md",
        "USER.md",
        "BOOT.md",
        "HUONG-DAN-AGENT.md",
        "PHONG-VAN.md",
        "knowledge/tuduy-cskh.md",
        "knowledge/workflow-cskh.md",
        "knowledge/system-prompt.md",
        "knowledge/logic/tools.json",
        "TOOLS.md",
        "skills/README.md",
        "skills/doc-wiki/SKILL.md",
        ".claude/skills/khoi-tao/SKILL.md",
        "dung-bot/QUY-TRINH.md",
        "CHUAN-BI.md",
        "docs/14-vps-headless.md",
        "knowledge/anh-tinh-huong.md",
        "knowledge/cach-tu-van.md",
        "knowledge/giong-noi.md",
        "knowledge/logic/ma-tran.json",
        "memory/phieu/README.md",
        "memory/phieu/MAU.md",
        "skills/phieu/SKILL.md",
        "skills/follow-up/SKILL.md",
        "HEARTBEAT.md",
        "docs/05-thiet-lap.md",
        "docs/06-tieu-chuan.md",
        "docs/07-cach-dung.md",
        "docs/08-luong-chu-shop.md",
        "docs/09-kho-va-du-lieu.md",
        "docs/10-openclaw-config-mau.md",
        "docs/11-mcp-ung-dung.md",
        "docs/12-prompt-va-cache.md",
        "docs/13-an-toan.md",
        "skills/hoc-lai/SKILL.md",
        "config/mcp.example.json5",
        "skills/giao-tiep/SKILL.md",
        "skills/lam-viec/SKILL.md",
        ".claude/skills/giao-tiep-chu/SKILL.md",
        ".claude/skills/lam-viec-dung/SKILL.md",
        "docs/04-kich-ban-thu.md",
        "config/openclaw.zalouser.example.json5",
    ]

    def test_required_files_exist(self):
        missing = [p for p in self.REQUIRED if not (ROOT / p).is_file()]
        self.assertEqual(missing, [], msg=f"thieu file: {missing}")


class SmokeSkills(unittest.TestCase):
    def test_every_matrix_skill_has_skill_md(self):
        matrix = json.loads(_read("knowledge/logic/ma-tran.json"))
        missing = []
        for name in matrix["skills"]:
            path = ROOT / "skills" / name / "SKILL.md"
            if not path.is_file():
                missing.append(str(path.relative_to(ROOT)))
                continue
            text = path.read_text(encoding="utf-8")
            self.assertIn(f"name: {name}", text)
        self.assertEqual(missing, [], msg=f"thieu skill: {missing}")

    def test_no_empty_public_wiki_pages(self):
        public = ROOT / "knowledge/wiki/public"
        if not public.is_dir():
            return
        for md in public.glob("*.md"):
            if md.name.upper() == "TRANG-MAU.md" or md.name == ".gitkeep":
                continue
            body = md.read_text(encoding="utf-8").strip()
            self.assertTrue(len(body) > 40, msg=f"trang wiki qua mong: {md.name}")


def _bo_comment(json5: str) -> str:
    """Bỏ // comment để kiểm cấu trúc, không bị câu cảnh báo trong comment lừa."""
    return "\n".join(re.sub(r"//.*$", "", dong) for dong in json5.splitlines())


def _khoi(text: str, khoa: str) -> str:
    """Nội dung trong `khoa: { ... }` đầu tiên, đếm ngoặc."""
    m = re.search(rf"\b{re.escape(khoa)}\s*:\s*\{{", text)
    if not m:
        return ""
    sau, sau_cung = 1, m.end()
    for i in range(m.end(), len(text)):
        if text[i] == "{":
            sau += 1
        elif text[i] == "}":
            sau -= 1
            if sau == 0:
                return text[m.end():i]
    return text[m.end():]


def _ten_bot() -> str:
    m = re.search(r"\*\*Name:\*\*\s*(.+)", _read("IDENTITY.md"))
    return m.group(1).strip() if m else ""


# Mọi chỗ in ra một khối config cho người chép. Thêm file có khối config thì thêm vào đây.
NOI_CO_CONFIG = [
    "config/openclaw.zalouser.example.json5",
    "docs/10-openclaw-config-mau.md",
    "docs/02-kenh-zalouser.md",
]


class SmokeConfig(unittest.TestCase):
    def test_example_config_is_cskh_not_tom_pairing(self):
        text = _read("config/openclaw.zalouser.example.json5")
        self.assertIn('dmPolicy: "open"', text)
        self.assertIn("zalouser", text)
        self.assertNotRegex(text, r'dmPolicy:\s*"pairing"')

    def test_ten_trong_config_khop_identity(self):
        """Plugin nhận "gọi mình" theo tên TRONG CONFIG, không đọc IDENTITY.md.
        Lệch là bot im trong nhóm. Không cắm cứng "Nami" — shop đổi tên vẫn xanh."""
        ten = _ten_bot()
        self.assertTrue(ten, "IDENTITY.md thieu dong **Name:**")
        cfg = _bo_comment(_read("config/openclaw.zalouser.example.json5"))
        self.assertRegex(cfg, rf'identity:\s*\{{\s*name:\s*"{re.escape(ten)}"')

    def test_open_luon_kem_allowfrom_sao(self):
        """Máy thật: open thiếu "*" vẫn báo valid, exit 0 — và rơi HẾT tin khách lạ."""
        for noi in NOI_CO_CONFIG:
            cfg = _bo_comment(_read(noi))
            if 'dmPolicy: "open"' not in cfg:
                continue
            so_open = cfg.count('dmPolicy: "open"')
            so_allow = len(re.findall(r'allowFrom:\s*\[[^\]]*"\*"', cfg))
            self.assertEqual(so_open, so_allow, f"{noi}: dmPolicy open thieu allowFrom [\"*\"]")

    def test_identity_khong_nam_trong_defaults(self):
        """agents.defaults.identity = Unrecognized key, gateway không lên."""
        for noi in NOI_CO_CONFIG:
            cfg = _bo_comment(_read(noi))
            for khoi in re.findall(r"```json5\n(.*?)```", cfg, re.S) or [cfg]:
                defaults = _khoi(_khoi(khoi, "agents"), "defaults")
                self.assertNotIn("identity", defaults, f"{noi}: identity nam trong agents.defaults")
                self.assertNotRegex(khoi, r"\bdefault:\s*true", f"{noi}: key default da bi go")

    def test_khong_tai_lieu_nao_day_key_cu(self):
        for path in ROOT.rglob("*.md"):
            if ".git" in path.parts or path.name == "CHANGELOG.md":
                continue
            self.assertNotIn("agents.defaults.identity", path.read_text(encoding="utf-8"),
                             str(path.relative_to(ROOT)))

    def test_moi_khach_mot_phien(self):
        """Máy thật (hàm định tuyến OpenClaw): thiếu dòng này thì chủ, khách A,
        khách B đều vào CHUNG phiên agent:main:main — lộ thông tin khách cho nhau."""
        cfg = _bo_comment(_read("config/openclaw.zalouser.example.json5"))
        self.assertRegex(cfg, r'session:\s*\{\s*dmScope:\s*"per-channel-peer"')

    def test_tu_hoc_va_tu_ghi_bo_nho_tat(self):
        """Mặc định OpenClaw: tự học "auto" (ai gõ "từ giờ luôn…" cũng thành skill),
        dreaming + memoryFlush bật (chép chữ khách vào MEMORY.md — file nạp nền)."""
        cfg = _bo_comment(_read("config/openclaw.zalouser.example.json5"))
        self.assertRegex(cfg, r'autonomous:\s*\{\s*mode:\s*"off"')
        self.assertRegex(cfg, r'dreaming:\s*\{\s*enabled:\s*false')
        self.assertRegex(cfg, r'memoryFlush:\s*\{\s*enabled:\s*false')

    def test_bot_khach_khong_co_shell_khong_hen_gio(self):
        """Không đặt tools thì OpenClaw dùng profile "coding": exec trên VPS cho
        khách. security audit xếp CRITICAL."""
        cfg = _bo_comment(_read("config/openclaw.zalouser.example.json5"))
        main = _khoi(_khoi(_khoi(cfg, "agents"), "entries"), "main")
        self.assertRegex(main, r'profile:\s*"minimal"')
        for cam in ("exec", "process", "apply_patch", "automations", "cron", "gateway", "web_fetch"):
            self.assertNotIn(f'"{cam}"', main, f"bot khach duoc cap {cam}")
        toan_cuc = _khoi(cfg, "tools")
        self.assertIn('"group:runtime"', toan_cuc)
        self.assertRegex(toan_cuc, r"elevated:\s*\{\s*enabled:\s*false")
        self.assertRegex(toan_cuc, r"workspaceOnly:\s*true")

    def test_chi_chu_nhan_rieng_moi_vao_admin(self):
        cfg = _bo_comment(_read("config/openclaw.zalouser.example.json5"))
        b = _khoi(cfg, "bindings") or cfg[cfg.index("bindings"):]
        self.assertRegex(b, r'(?s)agentId:\s*"admin".*?peer:\s*\{\s*kind:\s*"direct",\s*id:\s*"SENDERID_CHU"', )
        # admin phải đứng TRƯỚC binding chung, và khớp riêng peer — không khớp cả kênh.
        self.assertLess(b.index('"admin"'), b.index('"main"'))
        self.assertIn('ownerAllowFrom: ["zalouser:SENDERID_CHU"]', cfg)

    def test_moi_skill_khach_deu_duoc_khai_cho_bot_khach(self):
        """agents.entries.main.skills là danh sách cho phép: skill không có tên ở
        đó thì bot khách KHÔNG thấy (đã kiểm bằng `openclaw skills list`). Thêm
        skill mà quên khai = skill chết lặng. Hai skill chỉ-chủ thì ngược lại:
        tuyệt đối không được có trong danh sách của bot khách."""
        cfg = _bo_comment(_read("config/openclaw.zalouser.example.json5"))
        main = _khoi(_khoi(_khoi(cfg, "agents"), "entries"), "main")
        m = re.search(r"skills:\s*\[(.*?)\]", main, re.S)
        self.assertTrue(m, "main thieu danh sach skills")
        khai = set(re.findall(r'"([a-z0-9-]+)"', m.group(1)))
        co = {p.parent.name for p in (ROOT / "skills").glob("*/SKILL.md")}
        CHI_CHU = {"day-bot", "giao-viec"}
        self.assertEqual(khai & CHI_CHU, set(), "bot khach nap duoc skill chi-chu")
        self.assertEqual(co - CHI_CHU - khai, set(), "skill khach chua khai cho main")
        self.assertEqual(khai - co, set(), "khai skill khong ton tai")

    def test_moi_agent_co_workspace_rieng(self):
        """Nhiều agent: workspace ở defaults bị hiểu là thư mục gốc → agent chạy
        trong <gốc>/main, không thấy sổ. Phải đặt ở từng agent."""
        cfg = _bo_comment(_read("config/openclaw.zalouser.example.json5"))
        ent = _khoi(_khoi(cfg, "agents"), "entries")
        for ag in ("main", "admin"):
            self.assertRegex(_khoi(ent, ag), r"\bworkspace:", f"{ag} thieu workspace")

    def test_buoc_validate_co_trong_quy_trinh(self):
        for noi in ("dung-bot/QUY-TRINH.md", "docs/05-thiet-lap.md", "docs/10-openclaw-config-mau.md"):
            self.assertIn("config validate", _read(noi), noi)

    def test_gitignore_keeps_phieu_private(self):
        gi = _read(".gitignore")
        self.assertIn("memory/phieu", gi)
        self.assertIn("!memory/phieu/README.md", gi)
        self.assertIn("!memory/phieu/MAU.md", gi)

    def test_no_committed_secrets(self):
        for path in ROOT.rglob("*"):
            if path.is_dir() or ".git" in path.parts:
                continue
            if path.suffix.lower() in {".png", ".jpg", ".jpeg", ".webp", ".gif"}:
                continue
            try:
                text = path.read_text(encoding="utf-8")
            except (UnicodeDecodeError, OSError):
                continue
            self.assertNotRegex(text, r"-----BEGIN (RSA |OPENSSH )?PRIVATE KEY-----")
            if path.name == ".env":
                self.fail(".env khong duoc commit")


class SmokeDocs(unittest.TestCase):
    def test_setup_guide_has_windows_and_qr(self):
        text = _read("docs/05-thiet-lap.md")
        for needle in ("PowerShell", "dmPolicy", "zalouser", "QR", "vision", "unittest"):
            self.assertIn(needle, text, msg=f"thiet-lap thieu: {needle}")

    def test_kich_ban_thu_has_ck_and_image_rows(self):
        text = _read("docs/04-kich-ban-thu.md")
        low = text.lower()
        self.assertIn("chuyển khoản", low)
        self.assertIn("không chữ", low)
        self.assertIn("ảnh mờ", low)

    def test_chu_shop_flow_is_plain_language(self):
        luong = _read("docs/08-luong-chu-shop.md")
        kho = _read("docs/09-kho-va-du-lieu.md")
        self.assertIn("không cần biết lập trình", luong.lower())
        self.assertIn("nick nhân viên", luong.lower())
        self.assertIn("từng bước", luong.lower())
        self.assertIn("ba ngăn", kho.lower())
        self.assertIn("file gốc", kho.lower())
        self.assertIn("không đẻ số", kho)
        self.assertIn("phiếu", kho.lower())
        self.assertNotIn("vector DB", luong)

    def test_tieu_chuan_splits_repo_vs_nick(self):
        text = _read("docs/06-tieu-chuan.md")
        self.assertIn("kho chữ", text)
        self.assertIn("nick thật", text)
        self.assertIn("không", text.lower())
        readme = _read("tests/README.md")
        self.assertIn("không phải bot sống", readme.lower())
