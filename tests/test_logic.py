#!/usr/bin/env python3
"""Logic: ma trận ↔ docs, GỘP/TÁCH, phiếu, tư duy 10 bước."""
from __future__ import annotations

import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def matrix() -> dict:
    return json.loads((ROOT / "knowledge/logic/ma-tran.json").read_text(encoding="utf-8"))


def _read(rel: str) -> str:
    return (ROOT / rel).read_text(encoding="utf-8")


class LogicMatrix(unittest.TestCase):
    def test_quyet_dinh_c_and_phieu_id(self):
        q = matrix()["quyet_dinh"]
        self.assertEqual(q["gop_tach"], "C")
        self.assertEqual(q["phieu"], "theo_id")
        self.assertFalse(q["crm"])
        self.assertIn("senderId", q["id_nguon"])

    def test_every_image_id_documented(self):
        docs = _read("knowledge/anh-tinh-huong.md")
        missing = [row["id"] for row in matrix()["anh"] if f"## {row['id']}" not in docs]
        self.assertEqual(missing, [], msg=f"anh-tinh-huong thieu heading: {missing}")

    def test_image_skills_exist(self):
        missing = []
        for row in matrix()["anh"]:
            skill = row["skill"]
            if not (ROOT / "skills" / skill / "SKILL.md").is_file():
                missing.append(f"{row['id']} -> {skill}")
        self.assertEqual(missing, [], msg=f"{missing}")

    def test_tach_images_are_marked_gop_false(self):
        by_id = {r["id"]: r for r in matrix()["anh"]}
        for key in (
            "ck_bien_lai",
            "hang_loi",
            "cccd_the",
            "anh_otp",
            "lua_ck",
            "mo_toi_crop",
            "chu_anh_mau_thuan",
        ):
            self.assertIn(key, by_id)
            self.assertFalse(by_id[key]["gop"], msg=f"{key} phai TACH")

    def test_gop_product_photo_may_advise(self):
        by_id = {r["id"]: r for r in matrix()["anh"]}
        self.assertTrue(by_id["anh_mon_shop"]["gop"])
        self.assertTrue(by_id["anh_phoi_nguoi"]["gop"])

    def test_tuduy_has_ten_steps_and_rule_c(self):
        text = _read("knowledge/tuduy-cskh.md")
        for step in matrix()["luot"]:
            self.assertIn(step, text)
        self.assertIn("GỘP", text)
        self.assertIn("TÁCH", text)
        self.assertIn("senderId", text)
        self.assertIn("memory/phieu/", text)
        for i in range(1, 11):
            self.assertTrue(str(i) in text)

    def test_gop_tach_ids_or_vietnamese_gloss(self):
        text = _read("knowledge/tuduy-cskh.md")
        for needle in ("Fact ngắn", "CK", "Hàng lỗi", "OTP", "CCCD", "Ảnh mờ"):
            self.assertIn(needle, text)
        for k in matrix()["gop_khi"] + matrix()["tach_khi"]:
            self.assertTrue(
                k in text or k.replace("_", " ") in text.lower(),
                msg=f"tuduy thieu gop/tach id {k}",
            )

    def test_agents_loads_thinking_layer(self):
        text = _read("AGENTS.md")
        for needle in ("tuduy-cskh.md", "anh-tinh-huong.md", "phieu"):
            self.assertIn(needle, text)

    def test_phieu_mau_has_fields(self):
        mau = _read("memory/phieu/MAU.md")
        for field in matrix()["phieu"]["ghi"]:
            self.assertIn(field, mau)
        skill = _read("skills/phieu/SKILL.md")
        for banned in matrix()["phieu"]["khong_ghi"]:
            self.assertIn(banned, skill)

    def test_cach_tu_van_mentions_rule_c(self):
        text = _read("knowledge/cach-tu-van.md")
        self.assertTrue("GỘP" in text or "gộp" in text)
        self.assertTrue("TÁCH" in text or "tách" in text)

    def test_image_ids_unique_and_typed(self):
        ids = [r["id"] for r in matrix()["anh"]]
        self.assertEqual(len(ids), len(set(ids)))
        for row in matrix()["anh"]:
            self.assertIsInstance(row["gop"], bool)
            self.assertIsInstance(row["ban_giao"], bool)
            self.assertTrue(row["skill"])

    def test_stress_ids_all_have_needles(self):
        from test_stress import StressCoverage

        documented = {row["id"] for row in matrix()["stress"]}
        self.assertEqual(documented, set(StressCoverage.EXPECT_NEEDLES))
