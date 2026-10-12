#!/usr/bin/env python3
"""scripts/cai_dat.sh — cài máy một lệnh.

Đã chạy thật trong container Linux có sẵn Node 22 SAI bản đứng trước trong PATH:
tải Node v24.21.0, kiểm SHA256, cài OpenClaw + plugin 2026.9.4, ~1 phút; chạy
lại thì bỏ qua hết. Ở đây khoá cú pháp và việc bản ghim khớp nhau mọi chỗ.
"""

from __future__ import annotations

import re
import shutil
import subprocess
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SH = (ROOT / "scripts" / "cai_dat.sh").read_text(encoding="utf-8")


class CaiDat(unittest.TestCase):
    def test_cu_phap_bash(self):
        if not shutil.which("bash"):
            self.skipTest("không có bash")
        r = subprocess.run(["bash", "-n", str(ROOT / "scripts" / "cai_dat.sh")], capture_output=True, text=True)
        self.assertEqual(r.returncode, 0, r.stderr)

    def test_ban_ghim_khop_moi_cho(self):
        """Lệnh cài một bản, lệnh soi đòi bản khác = người dựng thấy đỏ vô cớ."""
        node = re.search(r'NODE_BAN="([\d.]+)"', SH).group(1)
        oc = re.search(r'OC_BAN="([\d.]+)"', SH).group(1)
        km = (ROOT / "scripts" / "kiem_tra_may.py").read_text(encoding="utf-8")
        self.assertIn(f'BAN_OPENCLAW = "{oc}"', km)
        d05 = (ROOT / "docs" / "05-thiet-lap.md").read_text(encoding="utf-8")
        self.assertIn(oc, d05)
        self.assertIn(node, (ROOT / "docs" / "14-vps-headless.md").read_text(encoding="utf-8"))

    def test_kiem_sha_truoc_khi_giai_nen(self):
        """Không bao giờ giải nén Node tải về mà chưa so mã SHA256."""
        self.assertLess(SH.index("SHASUMS256.txt"), SH.index("tar -xzf"))
        self.assertIn('[ "$can" != "$co_sha" ]', SH)

    def test_khong_tu_lam_khi_khong_co_nguoi(self):
        """Không có người ngồi trước máy (không tty, không --yes) thì không tự
        thêm swap / đổi múi giờ / sửa .bashrc."""
        self.assertIn('[ -t 0 ] || return 1', SH)

    def test_chi_cho_openclaw_chay_script_cai_dat(self):
        self.assertIn("--allow-scripts=openclaw", SH)
