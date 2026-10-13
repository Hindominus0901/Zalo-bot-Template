#!/usr/bin/env python3
"""scripts/bat_dau.py — dựng bot một lệnh, chạy tiếp được.

Đã chạy thật trong container (Node 22 sai bản đứng trước PATH, máy mới):
lần 1 nhận mã AI + điền config + soi máy; lần 2 bỏ qua ba bước đã xong, không
hỏi lại mã. Ở đây khoá thứ tự bước, bốn việc của người, và cách nhận "xong".
"""

from __future__ import annotations

import importlib.util
import json
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


def _oc_dang_nhap(d: Path) -> str:
    """openclaw giả: chưa đăng nhập; `channels login` in đúng dòng QR plugin in rồi chờ."""
    anh = d / "qr.png"
    anh.write_bytes(b"\x89PNG\r\n\x1a\n")
    p = d / "openclaw"
    p.write_text(f"""#!/bin/sh
case "$1 $2" in
  "directory self") echo '{{"ok": false, "error": {{"message": "No saved Zalo session"}}}}';;
  "channels login") echo "Generating QR login..."; echo "Scan QR image: {anh}"; sleep 30;;
  "sessions --agent") echo '{{"sessions": [], "path": null}}';;
  *) exit 1;;
esac
""")
    os.chmod(p, 0o755)
    return str(p)


class TuDong(unittest.TestCase):
    """--tu-dong: agent chạy qua SSH, không có người gõ. Việc người → CanNguoi (thoát 3)."""

    def setUp(self):
        self._t = tempfile.TemporaryDirectory()
        self.d = Path(self._t.name)
        self.cu = (bd.TIEN_DO, bd.MA_AI_TAM, bd.LOG_DANG_NHAP, bd.PID_DANG_NHAP, bd.TU_DONG,
                   bd.CO, bd.SO_LAN_CHO, bd.NGHI)
        bd.TIEN_DO = self.d / "tien-do.json"
        bd.MA_AI_TAM = self.d / ".ma-ai-tam"
        bd.LOG_DANG_NHAP = self.d / "dang-nhap.log"
        bd.PID_DANG_NHAP = self.d / "dang-nhap.pid"
        bd.TU_DONG, bd.SO_LAN_CHO, bd.NGHI = True, 1, 0.2
        bd.CO = bd.argparse.Namespace(ten=None, chu_id=None, da_thu=False)

    def tearDown(self):
        try:
            os.killpg(int(bd.PID_DANG_NHAP.read_text()), 9)
        except (OSError, ValueError):
            pass
        (bd.TIEN_DO, bd.MA_AI_TAM, bd.LOG_DANG_NHAP, bd.PID_DANG_NHAP, bd.TU_DONG,
         bd.CO, bd.SO_LAN_CHO, bd.NGHI) = self.cu
        self._t.cleanup()

    def test_thieu_ma_ai_thi_can_nguoi(self):
        os.environ.pop("ANTHROPIC_API_KEY", None)
        with self.assertRaises(bd.CanNguoi) as c:
            bd.lam_ma_ai("openclaw")
        self.assertEqual(c.exception.viec, "ma_ai")

    def test_ma_ai_sai_dau_xoa_file_va_bao_lai(self):
        """Đọc file mã một lần rồi xoá — kể cả khi mã sai."""
        os.environ.pop("ANTHROPIC_API_KEY", None)
        bd.MA_AI_TAM.write_text("khong-phai-ma\n")
        with self.assertRaises(bd.CanNguoi):
            bd.lam_ma_ai("openclaw")
        self.assertFalse(bd.MA_AI_TAM.exists())

    def test_quet_bat_dang_nhap_nen_va_tra_anh(self):
        oc = _oc_dang_nhap(self.d)
        with self.assertRaises(bd.CanNguoi) as c:
            bd.lam_quet(oc)
        self.assertEqual(c.exception.viec, "quet")
        self.assertTrue(c.exception.du_lieu["anh"].endswith("qr.png"))
        self.assertTrue(bd._dang_dang_nhap(), "đăng nhập phải còn chạy nền chờ người quét")
        # gọi lại: không bật đăng nhập thứ hai, vẫn trả đúng ảnh
        pid = bd.PID_DANG_NHAP.read_text()
        with self.assertRaises(bd.CanNguoi):
            bd.lam_quet(oc)
        self.assertEqual(bd.PID_DANG_NHAP.read_text(), pid)

    def test_chu_giu_nguyen_ma_giua_cac_lan_goi(self):
        """Người đang cầm mã NAMI-xxxx đi nhắn — gọi lại không được đổi mã."""
        oc = _oc_dang_nhap(self.d)
        with self.assertRaises(bd.CanNguoi) as c1:
            bd.lam_chu(oc)
        with self.assertRaises(bd.CanNguoi) as c2:
            bd.lam_chu(oc)
        self.assertRegex(c1.exception.du_lieu["ma"], r"^NAMI-\d{4}$")
        self.assertEqual(c1.exception.du_lieu["ma"], c2.exception.du_lieu["ma"])

    def test_chu_id_sai_dang(self):
        bd.CO.chu_id = "0909123456; rm -rf /"
        self.assertFalse(bd.lam_chu("openclaw"))

    def test_thu_can_xac_nhan(self):
        with self.assertRaises(bd.CanNguoi) as c:
            bd.lam_thu(None)
        self.assertEqual(len(c.exception.du_lieu["cau"]), 5)
        bd.CO.da_thu = True
        self.assertTrue(bd.lam_thu(None))
        self.assertTrue(bd.xong_thu(None))

    def test_dong_trang_thai_cho_agent(self):
        """Chạy cả lệnh: việc người → thoát 3, dòng cuối là JSON agent đọc được."""
        oc = _oc_dang_nhap(self.d)
        env = dict(os.environ, PATH=str(self.d) + os.pathsep + os.environ["PATH"], HOME=str(self.d))
        env.pop("ANTHROPIC_API_KEY", None)
        r = subprocess.run([sys.executable, str(ROOT / "scripts" / "bat_dau.py"), "--tu-dong",
                            "--bo-qua", "may"], capture_output=True, text=True, env=env,
                           timeout=120, stdin=subprocess.DEVNULL)
        self.assertTrue(oc)
        dong = [x for x in r.stdout.splitlines() if x.startswith("TRANG-THAI: ")]
        self.assertTrue(dong, r.stdout)
        tt = json.loads(dong[-1][len("TRANG-THAI: "):])
        self.assertEqual(r.returncode, 3, r.stdout)
        self.assertEqual(tt["can_nguoi"], "ma_ai")
        self.assertNotIn("Gõ / dán", r.stdout, "chế độ tự động không có người gõ")


if __name__ == "__main__":
    unittest.main()
