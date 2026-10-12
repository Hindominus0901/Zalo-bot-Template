#!/usr/bin/env python3
"""scripts/bat_dau.py — dựng bot một lệnh, chạy tiếp được.

Đã chạy thật trong container (Node 22 sai bản đứng trước PATH, máy mới):
lần 1 nhận mã AI + điền config + soi máy; lần 2 bỏ qua ba bước đã xong, không
hỏi lại mã. Ở đây khoá thứ tự bước, bốn việc của người, và cách nhận "xong".
"""

from __future__ import annotations

import importlib.util
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SRC = (ROOT / "scripts" / "bat_dau.py").read_text(encoding="utf-8")
_spec = importlib.util.spec_from_file_location("bat_dau", ROOT / "scripts" / "bat_dau.py")
bd = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(bd)


def _openclaw_gia(d: Path, dang_nhap: bool, co_ma: bool) -> str:
    """openclaw giả, in đúng khuôn output 2026.9.4 đã thấy khi chạy thật."""
    dir_self = ('{"ok": true, "self": {"id": "123456789"}}' if dang_nhap else
                '{"ok": false, "error": {"message": "No saved Zalo session for profile \\"default\\""}}')
    prof = 1 if co_ma else 0
    p = d / "openclaw"
    p.write_text(f"""#!/bin/sh
case "$1 $2" in
  "--version "*) echo "OpenClaw 2026.9.4 (3a9d69d)";;
  "plugins list") echo '[{{"id": "zalouser", "version": "2026.9.4", "status": "loaded"}}]';;
  "directory self") echo '{dir_self}';;
  "models status") echo '{{"auth": {{"providers": [{{"provider": "anthropic", "profiles": {{"count": {prof}}}}}]}}}}';;
  *) exit 1;;
esac
""")
    os.chmod(p, 0o755)
    return str(p)


class ThuTuBuoc(unittest.TestCase):
    def test_dung_thu_tu(self):
        """Gateway phải chạy TRƯỚC bước nick chủ: tin của chủ chỉ được nhận khi
        gateway đang chạy — lay_sender_id.py tìm cuộc trò chuyện vừa có."""
        khoa = [k for k, *_ in bd.BUOC]
        self.assertEqual(khoa, ["may", "ma_ai", "config", "quet", "gateway", "chu", "soi", "thu"])

    def test_dung_bon_viec_cua_nguoi(self):
        """Cả quá trình người chỉ phải làm bốn việc — không lén thêm việc thứ năm."""
        for so in ("①", "②", "③", "④"):
            self.assertIn(f'viec_nguoi("{so}"', SRC)
        self.assertEqual(SRC.count("viec_nguoi(\""), 4)


class NhanXong(unittest.TestCase):
    def test_chua_dang_nhap(self):
        with tempfile.TemporaryDirectory() as d:
            self.assertFalse(bd.xong_quet(_openclaw_gia(Path(d), dang_nhap=False, co_ma=True)))

    def test_da_dang_nhap(self):
        with tempfile.TemporaryDirectory() as d:
            self.assertTrue(bd.xong_quet(_openclaw_gia(Path(d), dang_nhap=True, co_ma=True)))

    def test_ma_ai(self):
        with tempfile.TemporaryDirectory() as d:
            self.assertTrue(bd.xong_ma_ai(_openclaw_gia(Path(d), True, co_ma=True)))
        with tempfile.TemporaryDirectory() as d:
            self.assertFalse(bd.xong_ma_ai(_openclaw_gia(Path(d), True, co_ma=False)))


class NoiThat(unittest.TestCase):
    def test_con_buoc_de_sau_thi_khong_noi_xong(self):
        """Người không rành tin câu cuối. Còn bước để sau mà in "Xong" là nói dối."""
        with tempfile.TemporaryDirectory() as d:
            oc = _openclaw_gia(Path(d), dang_nhap=True, co_ma=True)
            env = dict(os.environ, PATH=d + os.pathsep + os.environ["PATH"], HOME=d)
            r = subprocess.run([sys.executable, str(ROOT / "scripts" / "bat_dau.py"),
                                "--bo-qua", "config,quet,gateway,chu,soi,thu"],
                               capture_output=True, text=True, env=env, timeout=120,
                               stdin=subprocess.DEVNULL)
            self.assertEqual(r.returncode, 1, r.stdout + r.stderr)
            self.assertIn("CHƯA XONG", r.stdout)
            self.assertNotIn("Xong hết", r.stdout)
            self.assertIn("đã xong", r.stdout)   # bước 1–2 nhận ra đã xong, không làm lại
            self.assertTrue(oc)

    def test_xem_khong_lam_gi(self):
        with tempfile.TemporaryDirectory() as d:
            _openclaw_gia(Path(d), dang_nhap=False, co_ma=False)
            env = dict(os.environ, PATH=d + os.pathsep + os.environ["PATH"], HOME=d)
            r = subprocess.run([sys.executable, str(ROOT / "scripts" / "bat_dau.py"), "--xem"],
                               capture_output=True, text=True, env=env, timeout=120,
                               stdin=subprocess.DEVNULL)
            self.assertEqual(r.returncode, 0)
            self.assertNotIn("VIỆC CỦA NGƯỜI", r.stdout)


if __name__ == "__main__":
    unittest.main()
