#!/usr/bin/env python3
"""scripts/vps.py — agent trên máy người dựng điều khiển VPS.

Đã chạy thật trong container: sshd cổng 2222 làm "VPS", một user riêng. Chạy
đủ chuỗi khoa → (dán dòng vào console) → noi → day-len → bat-dau (dừng ở mã AI)
→ gui-ma-ai --mo/--gui → bat-dau (qua config, dừng ở quét vì container không
vào được Zalo) → lay-qr (ảnh khớp từng byte) → day-so → chủ sửa trên VPS →
day-so từ chối → keo-so. Ở đây khoá phần không cần ssh: gói gì, bỏ gì, báo lỗi
ssh bằng chữ thường, mã AI không lọt ra màn hình.
"""

from __future__ import annotations

import importlib.util
import io
import os
import sys
import tarfile
import unittest
from contextlib import redirect_stdout
from pathlib import Path
from unittest import mock

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))
_spec = importlib.util.spec_from_file_location("vps", ROOT / "scripts" / "vps.py")
vps = importlib.util.module_from_spec(_spec)
sys.modules["vps"] = vps
_spec.loader.exec_module(vps)


def _ten_trong(goi: bytes) -> set[str]:
    with tarfile.open(fileobj=io.BytesIO(goi), mode="r:gz") as t:
        return set(t.getnames())


class GoiTemplate(unittest.TestCase):
    def setUp(self):
        self.ten = _ten_trong(vps._goi_template(cap_nhat=False)[0])

    def test_co_du_thu_bot_can(self):
        for f in ("AGENTS.md", "SOUL.md", "scripts/bat_dau.py", "scripts/cai_dat.sh",
                  "config/openclaw.zalouser.example.json5", "knowledge/wiki/public/gia.md",
                  "memory/phieu/README.md"):
            self.assertIn(f, self.ten)

    def test_khong_mang_bi_mat_va_du_lieu_song(self):
        for x in self.ten:
            self.assertFalse(x.startswith(".git/"), x)
            self.assertNotIn("__pycache__", x)
            self.assertFalse(x.endswith((".env", ".vps.json", ".key", ".pem")), x)
            self.assertNotEqual(x, "config/openclaw.da-dien.json5")
            if x.startswith("memory/"):
                self.assertIn(Path(x).name, vps.GIU_TRONG_MEMORY, x)
            if x.startswith("knowledge/raw/"):
                self.assertIn(Path(x).name, ("NGUON.md", ".gitkeep"), x)

    def test_cap_nhat_khong_de_so_shop(self):
        """VPS đã chạy: chủ có thể đã dạy bot qua Zalo — đẩy code không được đè sổ."""
        ten = _ten_trong(vps._goi_template(cap_nhat=True)[0])
        for so in ("knowledge/wiki/public/gia.md", "IDENTITY.md", "USER.md", "SOUL.md"):
            self.assertNotIn(so, ten)
        self.assertIn("scripts/bat_dau.py", ten)
        self.assertIn("AGENTS.md", ten)


class LoiSsh(unittest.TestCase):
    def test_chu_thuong(self):
        cases = {
            "root@1.2.3.4: Permission denied (publickey).": "chìa khoá",
            "ssh: connect to host 1.2.3.4 port 22: Connection timed out": "sai địa chỉ IP",
            "ssh: connect to host 1.2.3.4 port 22: Connection refused": "từ chối",
            "WARNING: REMOTE HOST IDENTIFICATION HAS CHANGED!": "known_hosts",
        }
        for err, chu in cases.items():
            self.assertIn(chu, vps._giai_thich_ssh(err), err)

    def test_khong_co_ssh(self):
        with mock.patch.object(vps.subprocess, "run", side_effect=FileNotFoundError):
            with self.assertRaises(vps.Loi) as c:
                vps.tu_xa({"ip": "1.2.3.4"}, "true")
        self.assertIn("OpenSSH", str(c.exception))


class MaAi(unittest.TestCase):
    def setUp(self):
        self.cu = vps.FILE_MA, vps.CAU_HINH
        import tempfile
        self._t = tempfile.TemporaryDirectory()
        vps.FILE_MA = Path(self._t.name) / "ma.txt"
        vps.CAU_HINH = Path(self._t.name) / ".vps.json"
        vps.CAU_HINH.write_text('{"ip": "1.2.3.4"}')

    def tearDown(self):
        vps.FILE_MA, vps.CAU_HINH = self.cu
        self._t.cleanup()

    def test_gui_ma_khong_in_va_xoa_file(self):
        ma = "sk-ant-api03-ABCDEFGHIJKLMNOP_qrstu-123"
        vps.FILE_MA.write_text("Dán mã…\n\n   " + ma + "  \n")
        gui = {}

        def gia(ch, lenh, **kw):
            gui["vao"] = kw.get("vao")
            return 0, b"OK"

        out = io.StringIO()
        with mock.patch.object(vps, "tu_xa", gia), redirect_stdout(out):
            self.assertEqual(vps.cmd_gui_ma_ai(vps.argparse.Namespace(mo=False, gui=True)), 0)
        self.assertEqual(gui["vao"], (ma + "\n").encode())
        self.assertNotIn("sk-ant", out.getvalue())
        self.assertFalse(vps.FILE_MA.exists())

    def test_chua_dan_ma(self):
        vps.FILE_MA.write_text("Dán mã AI (bắt đầu bằng sk-ant-) vào dòng dưới…\n\n")
        with self.assertRaises(vps.Loi):
            vps.cmd_gui_ma_ai(vps.argparse.Namespace(mo=False, gui=True))


class Noi(unittest.TestCase):
    def test_dia_chi_la_bi_chan(self):
        """Địa chỉ đi thẳng vào lệnh ssh — chặn mọi thứ không phải IP / tên máy."""
        with self.assertRaises(vps.Loi):
            vps.cmd_noi(vps.argparse.Namespace(ip="1.2.3.4; rm -rf ~", user="root", cong=22))

    def test_vps_json_bi_ignore(self):
        self.assertIn(".vps.json", (ROOT / ".gitignore").read_text())


if __name__ == "__main__":
    unittest.main()
