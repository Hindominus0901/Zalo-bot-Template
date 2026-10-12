#!/usr/bin/env python3
"""scripts/kiem_tra_may.py — soi cả máy bot.

Đã chạy thật với OpenClaw 2026.9.4: config đúng → xanh; gỡ allowFrom, đổi
profile coding, bỏ nick chủ → đỏ / nhắc đúng dòng. Ở đây khoá các phép kiểm
thuần bằng đúng khuôn output thật đã thấy.
"""

from __future__ import annotations

import importlib.util
import json
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
_spec = importlib.util.spec_from_file_location("kiem_tra_may", ROOT / "scripts" / "kiem_tra_may.py")
km = importlib.util.module_from_spec(_spec)
sys.modules["kiem_tra_may"] = km   # dataclass cần module có trong sys.modules
_spec.loader.exec_module(km)


class Node(unittest.TestCase):
    def test_ban_dung(self):
        for v in ("v24.16.0", "v24.21.0", "v26.1.0", "v27.0.0"):
            self.assertEqual(km.kiem_node(v).muc, "ok", v)

    def test_ban_sai(self):
        """Node 22/23/25 cài OpenClaw hỏng ngay (EBADENGINE) — đã thử thật."""
        for v in ("v22.22.0", "v24.15.9", "v25.0.0", "v26.0.5"):
            self.assertEqual(km.kiem_node(v).muc, "loi", v)

    def test_chua_co(self):
        self.assertIn("cai_dat.sh", km.kiem_node(None).sua)


class Validate(unittest.TestCase):
    def test_rot_tin_la_do(self):
        """Đúng chữ OpenClaw in, kèm "Config valid" và exit 0 — vẫn phải ĐỎ."""
        ra = ('Config valid: ~/openclaw.json\n1 warning(s):\n  ! channels.zalouser.allowFrom: '
              'channels.zalouser.dmPolicy="open" but channels.zalouser.allowFrom does not '
              'include "*"; all DMs will be dropped.')
        self.assertEqual(km.kiem_validate(0, ra).muc, "loi")

    def test_key_la(self):
        ra = 'OpenClaw config is invalid\n  × openclaw.json:33 — agents.defaults: Unrecognized key: "identity"'
        d = km.kiem_validate(1, ra)
        self.assertEqual(d.muc, "loi")
        self.assertIn("Unrecognized", d.ten)

    def test_sach(self):
        self.assertEqual(km.kiem_validate(0, "Config valid: ~/openclaw.json").muc, "ok")


class Cfg(unittest.TestCase):
    TOT = {"session.dmScope": "per-channel-peer",
           "agents.entries.main.tools": {"profile": "minimal", "alsoAllow": ["read", "write", "message"]},
           "commands.ownerAllowFrom": ["zalouser:1111111111111111111"]}

    def test_tot(self):
        self.assertTrue(all(d.muc == "ok" for d in km.kiem_cfg(self.TOT)))

    def test_bot_khach_co_shell(self):
        g = dict(self.TOT, **{"agents.entries.main.tools": {"profile": "coding"}})
        self.assertIn("loi", [d.muc for d in km.kiem_cfg(g)])

    def test_cap_them_exec(self):
        g = dict(self.TOT, **{"agents.entries.main.tools": {"profile": "minimal", "alsoAllow": ["exec"]}})
        self.assertIn("loi", [d.muc for d in km.kiem_cfg(g)])

    def test_chua_khai_chu_chi_nhac(self):
        """Chưa khai chủ thì bot vẫn chạy được — nhắc, không đỏ."""
        g = dict(self.TOT, **{"commands.ownerAllowFrom": ["zalouser:SENDERID_CHU"]})
        muc = [d.muc for d in km.kiem_cfg(g)]
        self.assertNotIn("loi", muc)
        self.assertIn("nhac", muc)


class Skill(unittest.TestCase):
    def _js(self, ws, ten):
        return json.dumps({"workspaceDir": str(ws), "skills": [
            {"name": n, "source": "openclaw-workspace", "blockedByAgentFilter": False} for n in ten]})

    def test_sai_thu_muc(self):
        """Lỗi thật đã gặp: nhiều agent → agent chạy trong <gốc>/main rỗng."""
        with tempfile.TemporaryDirectory() as d:
            self.assertEqual(km.kiem_skill("main", self._js(Path(d) / "main", ["doc-wiki"]), Path(d)).muc, "loi")

    def test_bot_khach_thay_day_bot(self):
        with tempfile.TemporaryDirectory() as d:
            self.assertEqual(km.kiem_skill("main", self._js(d, ["doc-wiki", "day-bot"]), Path(d)).muc, "loi")

    def test_bot_chu_du(self):
        with tempfile.TemporaryDirectory() as d:
            self.assertEqual(km.kiem_skill("admin", self._js(d, ["doc-wiki", "day-bot", "giao-viec"]), Path(d)).muc, "ok")


class Gateway(unittest.TestCase):
    def test_chua_cai_va_khong_chay(self):
        """Đúng khuôn `openclaw gateway status --json` 2026.9.4."""
        js = json.dumps({"service": {"loaded": False}, "rpc": {"ok": False}})
        self.assertEqual([d.muc for d in km.kiem_gateway(js)], ["loi", "loi"])

    def test_chay_tot(self):
        js = json.dumps({"service": {"loaded": True}, "rpc": {"ok": True}})
        self.assertEqual([d.muc for d in km.kiem_gateway(js)], ["ok", "ok"])


class MayKhac(unittest.TestCase):
    def test_mui_gio(self):
        self.assertEqual(km.kiem_mui_gio("Asia/Ho_Chi_Minh").muc, "ok")
        self.assertEqual(km.kiem_mui_gio("Etc/UTC").muc, "loi")
        self.assertEqual(km.kiem_mui_gio(None).muc, "loi")

    def test_ram_nho_khong_swap(self):
        self.assertEqual(km.kiem_ram("MemTotal: 1000000 kB\nSwapTotal: 0 kB\n").muc, "loi")
        self.assertEqual(km.kiem_ram("MemTotal: 1000000 kB\nSwapTotal: 2097148 kB\n").muc, "ok")


if __name__ == "__main__":
    unittest.main()
