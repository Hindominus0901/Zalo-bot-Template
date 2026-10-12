#!/usr/bin/env python3
"""scripts/quet_ma.py — vẽ QR đăng nhập Zalo ra terminal.

Tự sinh PNG bằng stdlib (đủ kiểu màu, đủ năm bộ lọc dòng) rồi kiểm script đọc
lại đúng từng ô. Điện thoại có quét được màn hình terminal không thì phải thử
tay — xem docs/04-kich-ban-thu.md.
"""

from __future__ import annotations

import importlib.util
import random
import struct
import unittest
import zlib
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
_spec = importlib.util.spec_from_file_location("quet_ma", ROOT / "scripts" / "quet_ma.py")
qm = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(qm)


def _ma_tran(n: int = 29, hat: int = 7) -> list[list[bool]]:
    """Ma trận kiểu QR: ba mẫu định vị 7×7 ở ba góc, còn lại ngẫu nhiên."""
    rd = random.Random(hat)
    m = [[rd.random() < 0.5 for _ in range(n)] for _ in range(n)]

    def dinh_vi(r0, c0):
        for r in range(-1, 8):
            for c in range(-1, 8):
                rr, cc = r0 + r, c0 + c
                if 0 <= rr < n and 0 <= cc < n:
                    vien = r in (0, 6) or c in (0, 6)
                    loi = 2 <= r <= 4 and 2 <= c <= 4
                    m[rr][cc] = (0 <= r <= 6 and 0 <= c <= 6) and (vien or loi)
    dinh_vi(0, 0)
    dinh_vi(0, n - 7)
    dinh_vi(n - 7, 0)
    return m


def _chunk(kind: bytes, body: bytes) -> bytes:
    return struct.pack(">I", len(body)) + kind + body + struct.pack(">I", zlib.crc32(kind + body))


def _loc(dong: bytes, truoc: bytes, loai: int, bpp: int) -> bytes:
    out = bytearray()
    for x, v in enumerate(dong):
        a = dong[x - bpp] if x >= bpp else 0
        b = truoc[x]
        c = truoc[x - bpp] if x >= bpp else 0
        du = {0: 0, 1: a, 2: b, 3: (a + b) >> 1, 4: qm._paeth(a, b, c)}[loai]
        out.append((v - du) & 0xFF)
    return bytes([loai]) + bytes(out)


def _png(m, co=4, vien=4, kieu="gray", depth=8) -> bytes:
    """Mã hoá ma trận thành PNG. Bộ lọc dòng xoay vòng 0..4 để thử cả năm."""
    n = len(m)
    W = (n + 2 * vien) * co

    def den(x, y):
        r, c = y // co - vien, x // co - vien
        return 0 <= r < n and 0 <= c < n and m[r][c]

    ctype, kenh, plte, trns = {"gray": (0, 1, b"", b""), "rgb": (2, 3, b"", b""),
                               "rgba": (6, 4, b"", b""), "graya": (4, 2, b"", b""),
                               "pal": (3, 1, b"\xff\xff\xff\x00\x00\x00", b"")}[kieu]
    bpp = max(1, kenh * depth // 8)
    raw, truoc = b"", bytes(((W * kenh * depth) + 7) // 8)
    for y in range(W):
        if depth == 1:
            bits = [0 if den(x, y) else 1 for x in range(W)]
            dong = bytearray((W + 7) // 8)
            for x, bit in enumerate(bits):
                dong[x // 8] |= bit << (7 - x % 8)
            dong = bytes(dong)
        else:
            px = []
            for x in range(W):
                d = den(x, y)
                if kieu == "pal":
                    px += [1 if d else 0]
                elif kieu == "gray":
                    px += [0 if d else 255]
                elif kieu == "graya":
                    px += [0 if d else 255, 255]
                elif kieu == "rgb":
                    px += [0, 0, 0] if d else [255, 255, 255]
                else:   # rgba: nền trắng là điểm TRONG SUỐT
                    px += [0, 0, 0, 255] if d else [0, 0, 0, 0]
            dong = bytes(px)
        raw += _loc(dong, truoc, y % 5, bpp)
        truoc = dong
    hdr = struct.pack(">IIBBBBB", W, W, depth, ctype, 0, 0, 0)
    png = b"\x89PNG\r\n\x1a\n" + _chunk(b"IHDR", hdr)
    if plte:
        png += _chunk(b"PLTE", plte)
    return png + _chunk(b"IDAT", zlib.compress(raw)) + _chunk(b"IEND", b"")


class DocLaiDungTungO(unittest.TestCase):
    def _thu(self, **kw):
        m = _ma_tran()
        w, h, s = qm.doc_png(_png(m, **kw))
        self.assertEqual(qm.ra_o(w, h, s), m, kw)

    def test_xam(self):
        self._thu(kieu="gray")

    def test_rgb(self):
        self._thu(kieu="rgb")

    def test_rgba_nen_trong_suot(self):
        """Nền trong suốt phải thành trắng, không phải đen."""
        self._thu(kieu="rgba")

    def test_xam_alpha(self):
        self._thu(kieu="graya")

    def test_bang_mau(self):
        self._thu(kieu="pal")

    def test_mot_bit(self):
        self._thu(kieu="gray", depth=1)

    def test_co_o_khac_nhau(self):
        for co in (1, 3, 8):
            self._thu(kieu="gray", co=co)

    def test_ma_lon(self):
        m = _ma_tran(n=57, hat=3)
        w, h, s = qm.doc_png(_png(m, co=5))
        self.assertEqual(qm.ra_o(w, h, s), m)


def _them_khung_va_logo(m, khung=True, logo=True):
    """Ảnh từ máy chủ Zalo chưa từng thấy được (máy dựng không với tới id.zalo.me)
    — có thể có khung, có logo giữa. Đặt cả hai vào ảnh thử."""
    n = len(m)
    co, vien = 4, 4
    W = (n + 2 * vien) * co + 2 * 12
    img = [[1.0] * W for _ in range(W)]
    for r in range(n):
        for c in range(n):
            if m[r][c]:
                for yy in range(co):
                    for xx in range(co):
                        img[12 + (vien + r) * co + yy][12 + (vien + c) * co + xx] = 0.0
    if khung:   # khung đen dày 3 điểm sát mép ảnh
        for i in range(W):
            for d in range(3):
                img[d][i] = img[W - 1 - d][i] = img[i][d] = img[i][W - 1 - d] = 0.0
    if logo:    # ô vuông trắng giữa mã, cạnh 5 ô
        g = 12 + (vien + n // 2 - 2) * co
        for yy in range(g, g + 5 * co):
            for xx in range(g, g + 5 * co):
                img[yy][xx] = 1.0
    return W, W, img


class ChiuDuocAnhLa(unittest.TestCase):
    def test_khung_vien_den(self):
        """Lấy "điểm đen đầu tiên" làm góc mã thì khung đen làm hỏng hết."""
        m = _ma_tran()
        w, h, s = _them_khung_va_logo(m, khung=True, logo=False)
        self.assertEqual(qm.ra_o(w, h, s), m)

    def test_logo_giua(self):
        """Logo che giữa: đúng mọi ô ngoài vùng logo (QR tự chịu được phần che)."""
        m = _ma_tran()
        n = len(m)
        w, h, s = _them_khung_va_logo(m, khung=True, logo=True)
        o = qm.ra_o(w, h, s)
        self.assertEqual(len(o), n)
        g = n // 2 - 2
        for r in range(n):
            for c in range(n):
                if not (g <= r < g + 5 and g <= c < g + 5):
                    self.assertEqual(o[r][c], m[r][c], (r, c))


class Ve(unittest.TestCase):
    def test_moi_ky_tu_la_hai_o(self):
        m = _ma_tran()
        hinh = qm.ve(m, mau=False).splitlines()
        cao = len(m) + 2 * qm.VIEN
        self.assertEqual(len(hinh), (cao + 1) // 2)
        self.assertTrue(all(len(d) == cao for d in hinh))

    def test_co_vien_trang(self):
        """Không có vùng trắng quanh mã thì điện thoại không bắt được."""
        dau = qm.ve(_ma_tran(), mau=False).splitlines()[0]
        self.assertEqual(dau.strip(), "")

    def test_co_mau_thi_ep_nen_trang(self):
        self.assertIn("\x1b[", qm.ve(_ma_tran(), mau=True))


class BatDongQR(unittest.TestCase):
    def test_bat_dung_dong_plugin_in(self):
        """Đúng chữ plugin zalouser 2026.9.4 in: runtime.log(`Scan QR image: ${qrPath}`)."""
        m = qm.DONG_QR.search("Scan QR image: /tmp/openclaw/openclaw-zalouser-qr-default.png\n")
        self.assertEqual(m.group(1), "/tmp/openclaw/openclaw-zalouser-qr-default.png")

    def test_khong_bat_nham(self):
        self.assertIsNone(qm.DONG_QR.search("Waiting for login…"))

    def test_anh_khong_phai_png(self):
        with self.assertRaises(qm.LoiAnh):
            qm.doc_png(b"khong phai png")


if __name__ == "__main__":
    unittest.main()


class ChayVoiOpenclawGia(unittest.TestCase):
    """Luồng thật: chạy `openclaw channels login`, bắt dòng ảnh, vẽ ra terminal."""

    def test_bat_va_ve(self):
        import os
        import subprocess
        import sys
        import tempfile
        with tempfile.TemporaryDirectory() as d:
            anh = Path(d) / "openclaw-zalouser-qr-default.png"
            anh.write_bytes(_png(_ma_tran()))
            gia = Path(d) / "openclaw"
            gia.write_text("#!/bin/sh\necho 'Waiting for QR...'\n"
                           f"echo 'Scan QR image: {anh}'\necho 'Login successful'\n")
            os.chmod(gia, 0o755)
            r = subprocess.run([sys.executable, str(ROOT / "scripts" / "quet_ma.py"),
                                "--openclaw", str(gia), "--khong-mau"],
                               capture_output=True, text=True, timeout=60)
            self.assertEqual(r.returncode, 0, r.stderr)
            self.assertIn("NICK BOT", r.stdout)      # lời dặn chữ thường
            self.assertIn("█", r.stdout)             # có vẽ mã
            self.assertIn("Login successful", r.stdout)   # chữ của openclaw vẫn đi qua

    def test_khong_co_openclaw(self):
        import subprocess
        import sys
        r = subprocess.run([sys.executable, str(ROOT / "scripts" / "quet_ma.py"),
                            "--openclaw", "/khong/co/openclaw"], capture_output=True, text=True)
        self.assertEqual(r.returncode, 1)
        self.assertIn("cai_dat.sh", r.stderr)
