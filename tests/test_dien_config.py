#!/usr/bin/env python3
"""scripts/dien_config.py — điền config cho người không rành kỹ thuật.

Chạy thật với OpenClaw 2026.9.4 đã làm bằng tay (docs/16-day-bot.md mục
"Đã kiểm thế nào"). Ở đây khoá các hàm thuần: điền đúng chỗ, chặn nhập sai.
"""

from __future__ import annotations

import importlib.util
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
_spec = importlib.util.spec_from_file_location("dien_config", ROOT / "scripts" / "dien_config.py")
dc = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(dc)

MAU = (ROOT / "config" / "openclaw.zalouser.example.json5").read_text(encoding="utf-8")
ID = "1111111111111111111"


def _khong_comment(s: str) -> str:
    return "\n".join(re.sub(r"//.*$", "", d) for d in s.splitlines())


class DienDungCho(unittest.TestCase):
    def setUp(self):
        self.ra = dc.dien(MAU, "Biết Tuốt", ID, "/srv/shop", dc.MODEL_MANH)
        self.code = _khong_comment(self.ra)

    def test_thay_het_senderid(self):
        self.assertNotIn(dc.CHO, self.ra)
        for cho in ('ownerAllowFrom: ["zalouser:' + ID, f'id: "{ID}"', f'"channel:zalouser:{ID}"'):
            self.assertIn(cho, self.code)

    def test_ten_vao_ca_hai_agent(self):
        self.assertEqual(self.code.count('identity: { name: "Biết Tuốt" }'), 2)
        self.assertNotIn('name: "Nami"', self.code)

    def test_workspace_tuyet_doi(self):
        """Máy thật: thiếu workspace ở từng agent thì agent chạy trong <gốc>/main —
        thư mục rỗng, không thấy AGENTS.md, sổ, skill nào."""
        self.assertEqual(self.code.count('workspace: "/srv/shop",'), 3)   # defaults + main + admin
        self.assertNotIn('workspace: ".",', self.code)

    def test_khong_lam_mat_rao(self):
        """Điền xong vẫn phải còn mọi rào — script không được "tối giản" config."""
        for rao in ('dmScope: "per-channel-peer"', 'allowFrom: ["*"]', 'mode: "off"',
                    'profile: "minimal"', '"group:runtime"', "enabled: false"):
            self.assertIn(rao, self.code, rao)

    def test_bo_trong_chu_thi_dong_an_toan(self):
        """Không có senderId → giữ chữ SENDERID_CHU: không khớp ai, không ai là chủ."""
        ra = _khong_comment(dc.dien(MAU, "Nami", "", "/srv/shop", dc.MODEL_MANH))
        self.assertIn('id: "SENDERID_CHU"', ra)
        self.assertNotRegex(ra, r'id:\s*""')   # chuỗi rỗng có thể khớp bậy — không bao giờ

    def test_tiet_kiem_doi_model(self):
        ra = _khong_comment(dc.dien(MAU, "Nami", ID, "/x", dc.MODEL_TIET_KIEM))
        self.assertIn(f'primary: "{dc.MODEL_TIET_KIEM}"', ra)
        self.assertIn("fallbacks: []", ra)

    def test_model_ghim_ten_day_du(self):
        """Bí danh "opus" tự trượt sang đời mới khi nâng OpenClaw — không dùng."""
        self.assertRegex(self.code, r'primary:\s*"anthropic/claude-[a-z]+-\d')


class ChanNhapSai(unittest.TestCase):
    def test_so_dien_thoai_bi_chan(self):
        for sdt in ("0912345678", "+84912345678", "0912 345 678"):
            with self.assertRaises(dc.Loi, msg=sdt):
                dc.kiem_sender(sdt)

    def test_chu_hay_dau_cach_bi_chan(self):
        for sai in ("chi Thanh", "abc123", "123 456 789"):
            with self.assertRaises(dc.Loi, msg=sai):
                dc.kiem_sender(sai)

    def test_sender_dung(self):
        self.assertEqual(dc.kiem_sender(f"  {ID} "), ID)
        self.assertEqual(dc.kiem_sender(""), "")

    def test_ten_co_ngoac_kep_bi_chan(self):
        """Ngoặc kép trong tên làm vỡ JSON5 — gateway không lên."""
        with self.assertRaises(dc.Loi):
            dc.kiem_ten('Nami "xịn"')


class DichCanhBao(unittest.TestCase):
    def test_canh_bao_rot_tin_duoc_dich(self):
        """Đúng chữ OpenClaw 2026.9.4 in ra khi thiếu allowFrom "*"."""
        that = ('! channels.zalouser.allowFrom: channels.zalouser.dmPolicy="open" but '
                'channels.zalouser.allowFrom does not include "*"; all DMs will be dropped.')
        self.assertTrue(any("RƠI HẾT" in l for l in dc.doc_canh_bao(that)))


if __name__ == "__main__":
    unittest.main()
