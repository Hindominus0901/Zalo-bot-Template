#!/usr/bin/env python3
"""scripts/lay_sender_id.py — lấy senderId chủ bằng một mã ngắn.

Đã chạy thật với kho phiên của OpenClaw 2026.9.4 (hai người nhắn, chọn đúng
người có mã). Ở đây khoá các phần lõi bằng SQLite tự dựng cùng cấu trúc.
"""

from __future__ import annotations

import importlib.util
import json
import sqlite3
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
_spec = importlib.util.spec_from_file_location("lay_sender_id", ROOT / "scripts" / "lay_sender_id.py")
ls = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(ls)


def _kho(d: Path, phien: dict[str, str]) -> str:
    """SQLite cùng hai bảng OpenClaw 2026.9.4 dùng: session_windows, transcript_events."""
    p = d / "openclaw-agent.sqlite"
    c = sqlite3.connect(p)
    c.execute("CREATE TABLE session_windows (session_id TEXT, session_key TEXT)")
    c.execute("CREATE TABLE transcript_events (session_id TEXT, seq INT, event_json TEXT, created_at INT)")
    for i, (khoa, tin) in enumerate(phien.items()):
        c.execute("INSERT INTO session_windows VALUES (?, ?)", (f"s{i}", khoa))
        c.execute("INSERT INTO transcript_events VALUES (?, 1, ?, 0)",
                  (f"s{i}", json.dumps({"role": "user", "content": tin}, ensure_ascii=False)))
    c.commit()
    c.close()
    return str(p)


class UngVien(unittest.TestCase):
    def test_chi_lay_tin_rieng_zalo(self):
        ds = [{"key": "agent:main:zalouser:direct:5555555555", "lastInteractionAt": 2000},
              {"key": "agent:main:zalouser:group:9999999999", "lastInteractionAt": 2000},   # nhóm
              {"key": "agent:main:main", "lastInteractionAt": 2000},                        # CLI
              {"key": "agent:main:telegram:direct:5555555555", "lastInteractionAt": 2000}]  # kênh khác
        self.assertEqual(ls.ung_vien(ds, 1000), [("5555555555", ds[0]["key"])])

    def test_bo_qua_phien_cu(self):
        ds = [{"key": "agent:main:zalouser:direct:5555555555", "lastInteractionAt": 500}]
        self.assertEqual(ls.ung_vien(ds, 1000), [])

    def test_co_tai_khoan(self):
        """dmScope per-account-channel-peer chèn account vào khoá."""
        ds = [{"key": "agent:main:zalouser:acc1:direct:5555555555", "updatedAt": "3000"}]
        self.assertEqual(ls.ung_vien(ds, 1000)[0][0], "5555555555")

    def test_khoa_khong_phai_so_bi_bo(self):
        ds = [{"key": "agent:main:zalouser:direct:SENDERID_CHU", "lastInteractionAt": 2000}]
        self.assertEqual(ls.ung_vien(ds, 1000), [])


class CoMa(unittest.TestCase):
    def test_tim_dung_nguoi_co_ma(self):
        with tempfile.TemporaryDirectory() as d:
            kho = _kho(Path(d), {"agent:main:zalouser:direct:5555555555": "NAMI-7777",
                                 "agent:main:zalouser:direct:6666666666": "xin chào"})
            self.assertTrue(ls.co_ma(kho, "agent:main:zalouser:direct:5555555555", "NAMI-7777"))
            self.assertFalse(ls.co_ma(kho, "agent:main:zalouser:direct:6666666666", "NAMI-7777"))

    def test_cau_truc_la_tra_none(self):
        """OpenClaw bản khác đổi bảng → không đoán, trả None để hỏi người."""
        with tempfile.TemporaryDirectory() as d:
            p = Path(d) / "x.sqlite"
            sqlite3.connect(p).execute("CREATE TABLE khac (a TEXT)").connection.commit()
            self.assertIsNone(ls.co_ma(str(p), "agent:main:zalouser:direct:1", "NAMI-1"))

    def test_khong_ghi_vao_kho(self):
        """Mở chế độ chỉ đọc — script không được đụng dữ liệu của OpenClaw."""
        with tempfile.TemporaryDirectory() as d:
            kho = _kho(Path(d), {"agent:main:zalouser:direct:5555555555": "NAMI-7777"})
            truoc = Path(kho).read_bytes()
            ls.co_ma(kho, "agent:main:zalouser:direct:5555555555", "NAMI-7777")
            self.assertEqual(Path(kho).read_bytes(), truoc)


class Ma(unittest.TestCase):
    def test_ma_ngau_nhien_bon_so(self):
        ma = {ls.sinh_ma() for _ in range(50)}
        self.assertTrue(all(m.startswith("NAMI-") and len(m) == 9 for m in ma))
        self.assertGreater(len(ma), 30)   # không lặp một mã


if __name__ == "__main__":
    unittest.main()
