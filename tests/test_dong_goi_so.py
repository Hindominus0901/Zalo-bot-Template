#!/usr/bin/env python3
"""scripts/dong_goi.py + mo_goi.py — chuyển sổ shop từ app chat sang VPS.

Đã chạy thật trong container: hai bản sao repo, sửa sổ ở bản A, gói ra khối
chữ, dán (kèm rác, CRLF, thụt lề) vào bản B — sổ khớp, chỉ mục B xanh. Ở đây
khoá: khớp từng byte, gói hỏng thì không ghi gì, không lọt thứ không được lọt.
"""

from __future__ import annotations

import importlib.util
import io
import os
import shutil
import sys
import tarfile
import tempfile
import unittest
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))


def _nap(ten):
    spec = importlib.util.spec_from_file_location(ten, ROOT / "scripts" / f"{ten}.py")
    m = importlib.util.module_from_spec(spec)
    sys.modules[ten] = m
    spec.loader.exec_module(m)
    return m


dg = _nap("dong_goi")
mg = _nap("mo_goi")

SO = ("IDENTITY.md", "USER.md", "MEMORY.md", "SOUL.md", "knowledge", "skills")


def _ban_sao(d: Path) -> Path:
    d.mkdir()
    for r in SO:
        src = ROOT / r
        (shutil.copytree if src.is_dir() else shutil.copy2)(src, d / r)
    return d


class GoiMo(unittest.TestCase):
    def setUp(self):
        self._t = tempfile.TemporaryDirectory()
        t = Path(self._t.name)
        self.a = _ban_sao(t / "A")
        self.b = _ban_sao(t / "B")
        (self.a / "knowledge/wiki/public/gia.md").write_text("# Giá\n\n- Gói A: 2.000.000đ\n", encoding="utf-8")
        (self.a / "knowledge/wiki/public/qua-tang.md").write_text("# Quà\n", encoding="utf-8")
        (self.a / ".env").write_text("ANTHROPIC_API_KEY=sk-ant-x\n")
        (self.a / "memory/phieu").mkdir(parents=True)
        (self.a / "memory/phieu/khach.md").write_text("Chị Lan 0909\n", encoding="utf-8")
        (self.a / "config").mkdir()
        (self.a / "config/openclaw.da-dien.json5").write_text("{ownerAllowFrom: ['1']}")

    def tearDown(self):
        self._t.cleanup()

    def test_khop_tung_byte(self):
        tep = mg.doc_khoi(dg.thanh_khoi(dg.gom(self.a)))
        mg.kiem(tep)
        mg.ghi(self.b, tep)
        for rel in tep:
            self.assertEqual((self.a / rel).read_bytes(), (self.b / rel).read_bytes(), rel)
        self.assertIn("qua-tang", "".join(tep))

    def test_khong_lot_bi_mat(self):
        tep = dg.gom(self.a)
        for cam in (".env", "memory/phieu/khach.md", "config/openclaw.da-dien.json5", "AGENTS.md"):
            self.assertNotIn(cam, tep)
        self.assertIn("knowledge/wiki/public/gia.md", tep)
        self.assertIn("SOUL.md", tep)

    def test_dan_kem_rac_crlf_thut_le(self):
        khoi = dg.thanh_khoi(dg.gom(self.a))
        ban = "ai đó gõ gì đây\r\n" + "".join("   " + d + "\r\n" for d in khoi.splitlines()) + "$ \n"
        self.assertEqual(mg.doc_khoi(ban), dg.gom(self.a))

    def test_sua_mot_ky_tu_khong_ghi_gi(self):
        dong = dg.thanh_khoi(dg.gom(self.a)).splitlines()
        dong[2] = ("B" if dong[2][0] != "B" else "C") + dong[2][1:]
        truoc = (self.b / "knowledge/wiki/public/gia.md").read_bytes()
        with self.assertRaises(mg.GoiHong):
            mg.doc_khoi("\n".join(dong))
        self.assertEqual((self.b / "knowledge/wiki/public/gia.md").read_bytes(), truoc)

    def test_thieu_duoi(self):
        khoi = dg.thanh_khoi(dg.gom(self.a)).splitlines()
        with self.assertRaises(mg.GoiHong):
            mg.doc_khoi("\n".join(khoi[:-1]))

    def test_giu_ban_cu(self):
        cu = (self.b / "knowledge/wiki/public/gia.md").read_bytes()
        kq = mg.ghi(self.b, dg.gom(self.a))
        self.assertIn("knowledge/wiki/public/gia.md", kq["đổi"])
        bk = list((self.b / ".ban-cu").rglob("gia.md"))
        self.assertEqual(len(bk), 1)
        self.assertEqual(bk[0].read_bytes(), cu)

    def test_zip(self):
        z = Path(self._t.name) / "so.zip"
        dg.thanh_zip(dg.gom(self.a), z)
        self.assertEqual(mg.doc_zip(z), dg.gom(self.a))


class ChanDuongDan(unittest.TestCase):
    def test_duong_xau(self):
        for rel in ("../x.md", "/etc/passwd", "scripts/bat_dau.py", "config/a.json5", "memory/phieu/a.md",
                    "knowledge/raw/a.md", ".env", "tests/x.md", "AGENTS.md", "knowledge/../SOUL.md",
                    "skills/day-bot/SKILL.md", "knowledge\\wiki\\x.md"):
            self.assertFalse(dg.hop_le(rel, b"<!-- FILE C\xe1\xbb\xa6A SHOP -->"), rel)

    def test_duong_tot(self):
        self.assertTrue(dg.hop_le("knowledge/wiki/public/moi.md", b"# x"))
        self.assertTrue(dg.hop_le("SOUL.md", b"# x"))
        self.assertTrue(dg.hop_le("IDENTITY.md", "<!-- FILE CỦA SHOP -->".encode()))
        self.assertFalse(dg.hop_le("IDENTITY.md", b"# khong co dau"))

    def test_goi_tu_che_bi_chan(self):
        """Gói không do dong_goi tạo (ai đó chế tay) có scripts/ → không ghi gì."""
        buf = io.BytesIO()
        with tarfile.open(fileobj=buf, mode="w:gz") as t:
            for rel, b in (("SOUL.md", b"# ok"), ("scripts/bat_dau.py", b"import os")):
                ti = tarfile.TarInfo(rel)
                ti.size = len(b)
                t.addfile(ti, io.BytesIO(b))
        import base64, hashlib
        du = buf.getvalue()
        khoi = f"{dg.MO} v1 {hashlib.sha256(du).hexdigest()} {len(du)}\n{base64.b64encode(du).decode()}\n{dg.DONG}\n"
        with self.assertRaises(mg.GoiHong):
            mg.kiem(mg.doc_khoi(khoi))

    def test_tar_co_symlink(self):
        buf = io.BytesIO()
        with tarfile.open(fileobj=buf, mode="w:gz") as t:
            ti = tarfile.TarInfo("SOUL.md")
            ti.type, ti.linkname = tarfile.SYMTYPE, "/etc/passwd"
            t.addfile(ti)
        import base64, hashlib
        du = buf.getvalue()
        khoi = f"{dg.MO} v1 {hashlib.sha256(du).hexdigest()} {len(du)}\n{base64.b64encode(du).decode()}\n{dg.DONG}\n"
        with self.assertRaises(mg.GoiHong):
            mg.doc_khoi(khoi)

    @unittest.skipIf(os.name == "nt", "symlink")
    def test_khong_ghi_qua_symlink(self):
        with tempfile.TemporaryDirectory() as t, tempfile.TemporaryDirectory() as ngoai:
            goc = Path(t)
            (goc / "SOUL.md").symlink_to(Path(ngoai) / "x.md")
            with self.assertRaises(mg.GoiHong):
                mg.ghi(goc, {"SOUL.md": b"# x"})
            self.assertFalse((Path(ngoai) / "x.md").exists())

    def test_zip_co_duong_xau(self):
        with tempfile.TemporaryDirectory() as t:
            z = Path(t) / "x.zip"
            with zipfile.ZipFile(z, "w") as f:
                f.writestr("../../ra-ngoai.md", "x")
            with self.assertRaises(mg.GoiHong):
                mg.kiem(mg.doc_zip(z))


if __name__ == "__main__":
    unittest.main()
