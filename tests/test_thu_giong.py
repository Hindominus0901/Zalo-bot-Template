#!/usr/bin/env python3
"""Giọng của chủ — khuôn đúc giọng, danh mục tình huống, và bước thử giọng.

Đã chạy thật `scripts/thu_giong.py` với OpenClaw 2026.9.4 + máy giả GPT: ba
tình huống → ba phiên `thu-giong-…` riêng, model nhận đúng câu khách, phiên cũ
không đổi, bảng in đủ ba dòng. Ở đây khoá phần không cần OpenClaw.
"""

from __future__ import annotations

import importlib.util
import json
import os
import re
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
_spec = importlib.util.spec_from_file_location("thu_giong", ROOT / "scripts" / "thu_giong.py")
tg = importlib.util.module_from_spec(_spec)
sys.modules["thu_giong"] = tg
_spec.loader.exec_module(tg)

MAU = """# Bản đồ hội thoại
<!-- khuôn:
## 9. Ví dụ trong chú thích
**Khách:** không được tính
-->

## 1. Hỏi giá

**Khách:** nến này bao nhiêu vậy shop

**Sai** (đọc cả bảng)
> Dạ bên em có 100k, 150k

**Đúng** (giọng chủ)
> Hũ nhỏ 120k nha.
> Anh/chị để phòng nào ạ?

## 2. Chưa có câu đúng

**Khách:** > bạn là bot hả

## 3. Còn chờ

**Khách:** [CHỜ CHỦ SHOP]
"""


class DocTinhHuong(unittest.TestCase):
    def test_tach_dung_khach_va_dung(self):
        ds = tg.doc_tinh_huong(MAU)
        self.assertEqual([t.khach for t in ds], ["nến này bao nhiêu vậy shop", "bạn là bot hả"])
        self.assertEqual(ds[0].dung, "Hũ nhỏ 120k nha. Anh/chị để phòng nào ạ?")
        self.assertEqual(ds[1].dung, "")

    def test_file_that_cua_template_doc_duoc(self):
        """Bản giao chưa có tình huống — script vẫn chạy, không lấy khuôn làm câu thử."""
        ds = tg.doc_tinh_huong((ROOT / "knowledge" / "hoi-thoai-shop.md").read_text(encoding="utf-8"))
        self.assertEqual(ds, [])


class KhongLenZalo(unittest.TestCase):
    def test_moi_cau_mot_phien_khong_deliver(self):
        l = tg.lenh("openclaw", "thu-giong-1", "giá bao nhiêu")
        self.assertIn("--local", l)
        self.assertNotIn("--deliver", l)
        self.assertEqual(l[l.index("--session-id") + 1], "thu-giong-1")
        self.assertEqual(l[l.index("--agent") + 1], "main")

    def test_doc_cau_tra(self):
        ra = 'log rác\n' + json.dumps({"payloads": [{"text": "Dạ có em ạ", "mediaUrl": None}], "meta": {}})
        self.assertEqual(tg.cau_tra(ra), "Dạ có em ạ")
        self.assertEqual(tg.cau_tra("không phải json"), "")

    @unittest.skipIf(os.name == "nt", "shell giả")
    def test_chay_voi_openclaw_gia(self):
        with tempfile.TemporaryDirectory() as d:
            gia = Path(d) / "openclaw"
            log = Path(d) / "goi.txt"
            gia.write_text(f"#!/bin/sh\necho \"$@\" >> {log}\n"
                           "echo '{\"payloads\": [{\"text\": \"Dạ em đây\"}]}'\n")
            os.chmod(gia, 0o755)
            from contextlib import redirect_stdout
            import io
            out = io.StringIO()
            with redirect_stdout(out):
                tg.main(["--openclaw", str(gia), "--cau", "shop ơi", "--cau", "giá bao nhiêu"])
            goi = log.read_text().splitlines()
            self.assertEqual(len(goi), 2)
            phien = [re.search(r"--session-id (\S+)", g).group(1) for g in goi]
            self.assertEqual(len(set(phien)), 2, "mỗi câu một phiên riêng")
            self.assertIn("Bot vừa trả:    Dạ em đây", out.getvalue())


class KhuonGiong(unittest.TestCase):
    def test_soul_du_tam_o(self):
        soul = (ROOT / "SOUL.md").read_text(encoding="utf-8")
        muc = soul.split("## Shop này — giọng của chủ")[1]
        for i in range(1, 9):
            self.assertRegex(muc, rf"(?m)^{i}\. \*\*", f"thiếu ô {i}")
        self.assertIn("Mượn giọng, không mượn đời tư", muc)

    def test_vi_du_da_dien_khop_khuon(self):
        vd = (ROOT / "docs" / "vi-du-file-da-dien.md").read_text(encoding="utf-8")
        for i in range(1, 9):
            self.assertRegex(vd, rf"(?m)^{i}\. \*\*", f"ví dụ thiếu ô {i}")

    def test_danh_muc_tinh_huong(self):
        ht = (ROOT / "knowledge" / "hoi-thoai-shop.md").read_text(encoding="utf-8")
        for nhom in "ABCDEFGHI":
            self.assertRegex(ht, rf"\| {nhom}\. ", f"thiếu nhóm {nhom}")
        self.assertIn("20 tình huống", ht)

    def test_cong_thu_giong_trong_quy_trinh(self):
        qt = (ROOT / "dung-bot" / "QUY-TRINH.md").read_text(encoding="utf-8")
        self.assertIn("vps.py thu-giong", qt)
        self.assertIn("8 trên 10", qt)

    def test_phong_van_xin_nguon_giong(self):
        for f in ("PHONG-VAN.md", "docs/bo-cau-hoi.md"):
            body = (ROOT / f).read_text(encoding="utf-8")
            self.assertIn("livestream", body, f)
            self.assertIn("kết câu", body, f)


if __name__ == "__main__":
    unittest.main()
