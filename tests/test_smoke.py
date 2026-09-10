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


class SmokeConfig(unittest.TestCase):
    def test_example_config_is_cskh_not_tom_pairing(self):
        text = _read("config/openclaw.zalouser.example.json5")
        self.assertIn('dmPolicy: "open"', text)
        self.assertIn("zalouser", text)
        self.assertIn("Nami", text)
        self.assertNotRegex(text, r'dmPolicy:\s*"pairing"')

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
