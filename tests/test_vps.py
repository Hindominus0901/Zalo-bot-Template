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
        ma = "sk-proj-ABCDEFGHIJKLMNOP_qrstu-123"
        vps.FILE_MA.write_text("Dán mã…\n\n   " + ma + "  \n")
        gui = {}

        def gia(ch, lenh, **kw):
            gui["vao"] = kw.get("vao")
            return 0, b"OK"

        out = io.StringIO()
        with mock.patch.object(vps, "tu_xa", gia), redirect_stdout(out):
            self.assertEqual(vps.cmd_gui_ma_ai(vps.argparse.Namespace(mo=False, gui=True)), 0)
        self.assertEqual(gui["vao"], (ma + "\n").encode())
        self.assertNotIn("sk-proj", out.getvalue())
        self.assertFalse(vps.FILE_MA.exists())

    def test_chua_dan_ma(self):
        vps.FILE_MA.write_text("Dán mã OpenAI (bắt đầu bằng sk-) vào dòng dưới…\n\n")
        with self.assertRaises(vps.Loi):
            vps.cmd_gui_ma_ai(vps.argparse.Namespace(mo=False, gui=True))


class _PmGia:
    """paramiko giả: ghi lại lệnh chạy, nhận đúng một mật khẩu."""
    class AuthenticationException(Exception):
        pass

    class AutoAddPolicy:
        pass

    def __init__(self, dung):
        self.dung, self.lenh, self.mk = dung, [], []
        pm = self

        class Client:
            def set_missing_host_key_policy(self, _p):
                pass

            def connect(self, ip, port, username, password, **kw):
                pm.mk.append(password)
                if password != pm.dung:
                    raise _PmGia.AuthenticationException()

            def exec_command(self, lenh, timeout=None):
                pm.lenh.append(lenh)
                return None, io.BytesIO(b"OK\n"), None

            def close(self):
                pass

        self.SSHClient = Client


class MatKhau(unittest.TestCase):
    """123host gửi mật khẩu root — người dán vào Notepad, agent nối một lần, cài chìa khoá."""

    def setUp(self):
        import tempfile
        self._t = tempfile.TemporaryDirectory()
        self.cu = vps.FILE_MK, vps.KHOA
        vps.FILE_MK = Path(self._t.name) / "mk.txt"
        vps.KHOA = Path(self._t.name) / "khoa"
        vps.KHOA.write_text("bi-mat")
        Path(str(vps.KHOA) + ".pub").write_text("ssh-ed25519 AAAAthu zalo-bot\n")

    def tearDown(self):
        vps.FILE_MK, vps.KHOA = self.cu
        self._t.cleanup()

    def test_dung_mat_khau_cai_khoa_xoa_file(self):
        vps.FILE_MK.write_text(vps.DAU_MK + "\n\n  MatKhau!123  \n")
        pm = _PmGia("MatKhau!123")
        out = io.StringIO()
        with mock.patch.object(vps, "_paramiko", return_value=pm), redirect_stdout(out):
            vps.cai_khoa_bang_mat_khau("1.2.3.4", "root", 22)
        self.assertEqual(pm.mk, ["MatKhau!123"])
        self.assertIn("ssh-ed25519 AAAAthu zalo-bot", pm.lenh[0])
        self.assertIn("authorized_keys", pm.lenh[0])
        self.assertNotIn("MatKhau", out.getvalue())
        self.assertFalse(vps.FILE_MK.exists())

    def test_sai_mat_khau_noi_chu_thuong_giu_file(self):
        vps.FILE_MK.write_text(vps.DAU_MK + "\n\nsai\n")
        with mock.patch.object(vps, "_paramiko", return_value=_PmGia("dung")):
            with self.assertRaises(vps.Loi) as c:
                vps.cai_khoa_bang_mat_khau("1.2.3.4", "root", 22)
        self.assertIn("Mật khẩu chưa đúng", str(c.exception))
        self.assertTrue(vps.FILE_MK.exists(), "giữ file để người sửa lại")

    def test_file_trong(self):
        vps.FILE_MK.write_text(vps.DAU_MK + "\n\n")
        with self.assertRaises(vps.Loi):
            vps.cai_khoa_bang_mat_khau("1.2.3.4", "root", 22)


class MaApi(unittest.TestCase):
    def test_nhan_ca_openai_va_anthropic(self):
        for ma in ("sk-proj-AbCdEfGhIjKlMnOpQrStUv_123-xyz", "sk-ant-api03-ABCDEFGHIJKLMNOPQRSTUV"):
            self.assertEqual(vps.MA_API.search(f"  {ma}  ").group(0), ma)

    def test_tu_choi_chu_rac(self):
        for rac in ("sk-ngan", "Dán mã OpenAI (bắt đầu bằng sk-) vào dòng dưới", "ask-proj-AbCdEfGhIjKlMnOpQrStUv"):
            self.assertIsNone(vps.MA_API.search(rac), rac)


class Noi(unittest.TestCase):
    def test_dia_chi_la_bi_chan(self):
        """Địa chỉ đi thẳng vào lệnh ssh — chặn mọi thứ không phải IP / tên máy."""
        with self.assertRaises(vps.Loi):
            vps.cmd_noi(vps.argparse.Namespace(ip="1.2.3.4; rm -rf ~", user="root", cong=22))

    def test_vps_json_bi_ignore(self):
        self.assertIn(".vps.json", (ROOT / ".gitignore").read_text())


if __name__ == "__main__":
    unittest.main()
