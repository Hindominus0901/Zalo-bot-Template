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
        for needle in (
            "tuduy-cskh.md",
            "anh-tinh-huong.md",
            "phieu",
            "workflow-cskh.md",
            "follow-up",
            "TOOLS.md",
            "persona.md",
        ):
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

    def test_voice_plain_vietnamese(self):
        giong = _read("knowledge/giong-noi.md")
        self.assertIn("chữ đời", giong.lower())
        self.assertIn("chuyên ngành", giong.lower())
        for path in (
            "knowledge/hoi-thoai-mau.md",
            "knowledge/moi-loai-cau-hoi.md",
            "knowledge/khung-khai-thac.md",
        ):
            text = _read(path).lower()
            self.assertNotIn("lurk", text, msg=path)
            self.assertNotIn("bới giúp", text, msg=path)
            self.assertNotIn("funnel", text, msg=path)

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


class LogicFollowup(unittest.TestCase):
    def test_matrix_followup_gates(self):
        f = matrix()["followup"]
        self.assertEqual(f["mac_dinh"], "tat")
        self.assertEqual(f["nhanh"], ["im_sau_gia", "sau_don"])
        self.assertTrue(f["mot_tin_moi_nhanh"])
        self.assertFalse(f["lan_hai_khi_im"])
        self.assertTrue(f["ck_khong_kich_hoat_sau_don"])
        self.assertTrue(f["boot_khong_gui"])
        self.assertFalse(f["review_tu_hoi"])

    def test_user_defaults_off(self):
        text = _read("USER.md")
        self.assertIn("CHỜ CHỦ SHOP", text)
        self.assertIn("Im sau giá", text)
        self.assertIn("Sau đơn", text)
        self.assertIn("Câu mẫu sau đơn", text)
        self.assertIn("mặc định tắt", text.lower())

    def test_heartbeat_scans_phieu_boot_does_not(self):
        hb = _read("HEARTBEAT.md")
        boot = _read("BOOT.md")
        skill = _read("skills/follow-up/SKILL.md")
        self.assertIn("memory/phieu/", hb)
        self.assertIn("da_gui", hb)
        self.assertIn("Không broadcast", hb)
        self.assertIn("không", boot.lower())
        self.assertIn("follow-up", boot.lower())
        self.assertIn("không", boot.lower())
        self.assertIn("burst", boot.lower())
        self.assertIn("ảnh ck", skill.lower())
        self.assertIn("da_gui", skill)
        self.assertIn("USER.md", skill)

    def test_workflow_and_quyet_dinh_unlock(self):
        wf = _read("knowledge/workflow-cskh.md")
        qd = _read("docs/quyet-dinh.md")
        self.assertIn("Im sau giá", wf)
        self.assertIn("Sau đơn", wf)
        self.assertIn("follow-up", qd.lower())
        self.assertNotIn("Nhắn chủ động follow-up: **chưa** làm", qd)

    def test_interview_maps_to_user(self):
        pv = _read("PHONG-VAN.md")
        bo = _read("docs/bo-cau-hoi.md")
        for text in (pv, bo):
            self.assertIn("im sau khi em báo giá", text.lower())
            self.assertIn("đã ghi đơn", text.lower())
            self.assertIn("tắt", text.lower())
            self.assertNotIn("bản này **chưa làm**", text)
        self.assertIn("PHONG-VAN.md", bo)
        self.assertIn("độc lập", bo.lower())
        self.assertIn("bo-cau-hoi.md", pv)


class LogicToolsAndPrompt(unittest.TestCase):
    def test_tools_json_documented(self):
        data = json.loads((ROOT / "knowledge/logic/tools.json").read_text(encoding="utf-8"))
        catalog = _read("TOOLS.md") + _read("AGENTS.md")
        for row in data["co"]:
            self.assertIn(f"`{row['id']}`", catalog, msg=row["id"])
            if row.get("skill"):
                path = ROOT / "skills" / row["skill"] / "SKILL.md"
                self.assertTrue(path.is_file(), msg=row["skill"])
        for banned in data["khong"]:
            self.assertIn(banned, _read("TOOLS.md"))
        honest = _read("TOOLS.md")
        self.assertIn("read", honest)
        self.assertIn("message", honest)
        self.assertIn("`tools/`", honest)
        buoc_ids = [r["id"] for r in data.get("buoc", [])]
        self.assertIn("lay_id", buoc_ids)
        self.assertTrue(all(r.get("khong_phai_tool") for r in data["buoc"]))
        self.assertIn("Bước máy", honest)

    def test_wiki_cho_pages_are_stubs(self):
        expected = [
            "knowledge/wiki/public/ban-gi.md",
            "knowledge/wiki/public/gia.md",
            "knowledge/wiki/public/ship.md",
            "knowledge/wiki/public/thanh-toan.md",
            "knowledge/wiki/public/doi-tra.md",
            "knowledge/wiki/public/bao-hanh.md",
            "knowledge/wiki/public/con-hang.md",
            "knowledge/wiki/public/gio-truc.md",
            "knowledge/wiki/public/dia-chi.md",
            "knowledge/wiki/public/kiem-hang.md",
            "knowledge/wiki/public/dat-lich.md",
            "knowledge/wiki/public/si-ctv.md",
            "knowledge/wiki/public/hoa-don-vat.md",
            "knowledge/wiki/internal/gia-von-hoa-hong.md",
            "knowledge/wiki/internal/xu-khach-kho.md",
        ]
        for rel in expected:
            text = _read(rel)
            self.assertIn("CHỜ CHỦ SHOP", text, msg=rel)
            self.assertIn("Không nói số", text, msg=rel)
            low = text.lower()
            self.assertNotIn("150000", low, msg=rel)
            self.assertNotIn("giá tham khảo", low, msg=rel)

    def test_opener_locked_and_chin_nhom(self):
        locked = "tìm cho mình dùng hay để tặng"
        for path in (
            "knowledge/hoi-thoai-mau.md",
            "knowledge/moi-loai-cau-hoi.md",
            "knowledge/khung-khai-thac.md",
            "docs/00-tong-hop-cskh.md",
        ):
            self.assertIn(locked, _read(path), msg=path)
        zero = _read("docs/00-tong-hop-cskh.md")
        self.assertNotIn("tìm loại nào", zero)
        self.assertIn("chín nhóm", zero.lower())
        self.assertIn("Chín nhóm", _read("knowledge/moi-loai-cau-hoi.md"))

    def test_config_mau_merges_both_fragments(self):
        text = _read("docs/10-openclaw-config-mau.md")
        self.assertIn("dmPolicy", text)
        self.assertIn("mcp.example.json5", text)
        self.assertIn("openclaw.zalouser.example.json5", text)
        self.assertIn("enabled: false", text)
        self.assertIn("pairing", text.lower())

    def test_khoi_tao_has_b0_b7_and_write_map(self):
        text = _read(".claude/skills/khoi-tao/SKILL.md")
        for needle in ("B0", "B7", "persona.md", "USER.md", "dmPolicy", "Không bịa"):
            self.assertIn(needle, text)
        self.assertIn("PHONG-VAN.md", text)
        self.assertIn("04-kich-ban-thu.md", text)
        self.assertIn("giao-tiep-chu", text)
        self.assertIn("lam-viec-dung", text)
        self.assertIn("10-openclaw-config-mau.md", text)
        self.assertIn("tờ chờ", text)

    def test_system_prompt_routes_skills(self):
        text = _read("AGENTS.md")
        for needle in ("doc_wiki", "doc_anh", "gui_zalo", "Ba rào", "khai-thac", "follow-up", "giao-tiep"):
            self.assertIn(needle, text)
        stub = _read("knowledge/system-prompt.md")
        self.assertIn("AGENTS.md", stub)

    def test_mcp_bus_forbids_scrape(self):
        mcp = json.loads((ROOT / "knowledge/logic/mcp.json").read_text(encoding="utf-8"))
        self.assertEqual(mcp["tool"], "mcp_drive")
        self.assertIn("apify_scrape_gia", mcp["cam_mac_dinh"])
        doc = _read("docs/11-mcp-ung-dung.md")
        self.assertIn("mcp_drive", doc)
        self.assertIn("Google Drive", doc)
        self.assertIn("Không nối sẵn", doc)
