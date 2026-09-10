#!/usr/bin/env python3
"""Stress: dồn tin, album, lệch chữ/ảnh, wiki trống, rào tiền."""
from __future__ import annotations

import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def matrix() -> dict:
    return json.loads((ROOT / "knowledge/logic/ma-tran.json").read_text(encoding="utf-8"))


def _blob() -> str:
    parts = [
        (ROOT / "knowledge/tuduy-cskh.md").read_text(encoding="utf-8"),
        (ROOT / "knowledge/anh-tinh-huong.md").read_text(encoding="utf-8"),
        (ROOT / "docs/04-kich-ban-thu.md").read_text(encoding="utf-8"),
        (ROOT / "AGENTS.md").read_text(encoding="utf-8"),
        (ROOT / "knowledge/tinh-huong.md").read_text(encoding="utf-8"),
    ]
    return "\n".join(parts)


class StressCoverage(unittest.TestCase):
    EXPECT_NEEDLES = {
        "tin_don_10": ("Tin dồn", "một tin gộp", "mot_tin_gop"),
        "album_5_anh": ("album_nhieu_anh", "Đọc hết"),
        "chu_A_anh_B": ("chu_anh_mau_thuan", "Chữ hỏi A"),
        "wiki_trong": ("không đẻ số", "Không đẻ số"),
        "phieu_size_M": ("hỏi lại", "size"),
        "ck_nhan_tien_chua": ("đã có tiền", "chuyển khoản"),
        "cccd": ("cccd_the", "CCCD"),
        "nhom_khong_ten": ("Nhóm", "im"),
        "teencode_plus_anh": ("gõ lại", "teencode"),
        "giam_gia_plus_anh_mon": ("giảm giá", "quyền chủ"),
        "het_hang_anh_mon": ("Hết hàng", "hết"),
        "session_dai_50_luot": ("phiếu", "hỏi lại"),
    }

    def test_every_stress_case_is_documented(self):
        blob = _blob().lower()
        missing = []
        for row in matrix()["stress"]:
            needles = self.EXPECT_NEEDLES[row["id"]]
            if not any(n.lower() in blob for n in needles):
                missing.append(row["id"])
        self.assertEqual(missing, [], msg=f"stress chua nam trong docs: {missing}")

    def test_kich_ban_thu_has_image_and_flood_rows(self):
        text = (ROOT / "docs/04-kich-ban-thu.md").read_text(encoding="utf-8").lower()
        self.assertIn("tin dồn", text)
        self.assertIn("ảnh", text)
        self.assertIn("không chữ", text)
        self.assertIn("5 ảnh", text)

    def test_ban_giao_flags_on_money_and_id_photos(self):
        by_id = {r["id"]: r for r in matrix()["anh"]}
        for key in ("ck_bien_lai", "cccd_the", "lua_ck", "anh_otp"):
            self.assertTrue(by_id[key]["ban_giao"], msg=key)
