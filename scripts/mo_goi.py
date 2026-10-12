#!/usr/bin/env python3
"""Mở gói sổ shop (từ scripts/dong_goi.py) trên máy chạy bot.

    python3 scripts/mo_goi.py          # rồi dán khối chữ vào, xong tự dừng
    python3 scripts/mo_goi.py so.zip   # hoặc file zip / file .txt chứa khối chữ

Kiểm mã trước khi ghi: dán thiếu một dòng là không ghi gì. Chỉ ghi đúng sổ của
shop — không bao giờ ghi vào scripts/, config/, memory/. Bản cũ của tờ bị ghi đè
được giữ ở `.ban-cu/<giờ>/`. Xong thì làm lại chỉ mục (scripts/lam_chi_muc.py).
"""

from __future__ import annotations

import argparse
import base64
import binascii
import hashlib
import io
import subprocess
import sys
import tarfile
import time
import zipfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from dong_goi import DONG, MO, ROOT, hop_le  # noqa: E402


class GoiHong(Exception):
    pass


def doc_khoi(chu: str) -> dict[str, bytes]:
    """Khối chữ dán vào → {đường dẫn: nội dung}. Chịu được rác trước/sau, CRLF, thụt lề."""
    dong = [d.strip() for d in chu.replace("\r", "\n").split("\n")]
    try:
        dau = next(i for i, d in enumerate(dong) if d.startswith(MO))
    except StopIteration:
        raise GoiHong(f"Không thấy dòng {MO} — chép thiếu đầu gói.")
    try:
        cuoi = next(i for i in range(dau + 1, len(dong)) if dong[i] == DONG)
    except StopIteration:
        raise GoiHong(f"Không thấy dòng {DONG} — chép thiếu đuôi gói.")
    phan = dong[dau].split()
    if len(phan) < 3 or phan[1] != "v1":
        raise GoiHong("Gói bản lạ — kéo template mới về rồi thử lại.")
    try:
        du = base64.b64decode("".join(d for d in dong[dau + 1:cuoi] if d), validate=True)
    except (binascii.Error, ValueError):
        raise GoiHong("Gói bị sửa hoặc dán lẫn chữ khác — dán lại nguyên khối.")
    if hashlib.sha256(du).hexdigest() != phan[2]:
        raise GoiHong("Mã kiểm không khớp — dán thiếu hoặc rơi chữ. Không ghi gì. Dán lại nguyên khối.")
    out: dict[str, bytes] = {}
    try:
        with tarfile.open(fileobj=io.BytesIO(du), mode="r:gz") as t:
            for m in t.getmembers():
                if not m.isfile():
                    raise GoiHong(f"Gói có thứ không phải tờ sổ: {m.name}")
                out[m.name] = t.extractfile(m).read()
    except tarfile.TarError:
        raise GoiHong("Gói hỏng — dán lại nguyên khối.")
    return out


def doc_zip(p: Path) -> dict[str, bytes]:
    try:
        with zipfile.ZipFile(p) as z:
            if z.testzip() is not None:
                raise GoiHong("File zip hỏng — tải lại.")
            out = {}
            for i in z.infolist():
                if i.is_dir():
                    continue
                if (i.external_attr >> 16) & 0o170000 == 0o120000:
                    raise GoiHong(f"Zip có liên kết (symlink): {i.filename}")
                out[i.filename] = z.read(i)
            return out
    except zipfile.BadZipFile:
        raise GoiHong("Không phải file zip, hoặc tải về chưa xong.")


def kiem(tep: dict[str, bytes]) -> None:
    sai = [r for r, b in tep.items() if not hop_le(r, b)]
    if sai:
        raise GoiHong("Gói có tờ không được phép — không ghi gì: " + ", ".join(sorted(sai)))
    if not tep:
        raise GoiHong("Gói rỗng.")


def ghi(goc: Path, tep: dict[str, bytes]) -> dict[str, list[str]]:
    kq = {"mới": [], "đổi": [], "giữ nguyên": []}
    cu = goc / ".ban-cu" / time.strftime("%Y%m%d-%H%M%S")
    for rel in sorted(tep):
        dich = goc / rel
        if dich.is_symlink() or not dich.resolve().is_relative_to(goc.resolve()):
            raise GoiHong(f"Chỗ ghi lạ (liên kết ra ngoài): {rel}")
        if dich.exists():
            if dich.read_bytes() == tep[rel]:
                kq["giữ nguyên"].append(rel)
                continue
            (cu / rel).parent.mkdir(parents=True, exist_ok=True)
            (cu / rel).write_bytes(dich.read_bytes())
            kq["đổi"].append(rel)
        else:
            kq["mới"].append(rel)
        dich.parent.mkdir(parents=True, exist_ok=True)
        dich.write_bytes(tep[rel])
    return kq


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="Mở gói sổ shop.")
    ap.add_argument("tep", nargs="?", help="file .zip hoặc .txt; bỏ trống thì dán vào")
    ap.add_argument("--goc", default=str(ROOT), help=argparse.SUPPRESS)
    ap.add_argument("--khong-chi-muc", action="store_true", help=argparse.SUPPRESS)
    a = ap.parse_args(argv)
    goc = Path(a.goc)
    try:
        if a.tep:
            p = Path(a.tep)
            if not p.is_file():
                raise GoiHong(f"Không thấy file {p}")
            tep = doc_zip(p) if zipfile.is_zipfile(p) else doc_khoi(p.read_text(encoding="utf-8", errors="replace"))
        else:
            if sys.stdin.isatty():
                print(f"Dán cả khối vào đây (từ {MO} tới {DONG}). Dán xong tự dừng.", file=sys.stderr)
            dong = []
            for d in sys.stdin:
                dong.append(d)
                if d.strip() == DONG:
                    break
            tep = doc_khoi("".join(dong))
        kiem(tep)
        kq = ghi(goc, tep)
    except GoiHong as e:
        print(f"✗ {e}", file=sys.stderr)
        return 1
    for nhom, ds in kq.items():
        if ds:
            print(f"{nhom} ({len(ds)}): " + ", ".join(ds))
    if kq["đổi"]:
        print("Bản cũ của tờ bị đổi: thư mục .ban-cu/")
    cm = goc / "scripts" / "lam_chi_muc.py"
    if not a.khong_chi_muc and cm.exists():
        subprocess.run([sys.executable, str(cm)], cwd=goc, check=False)
    print("\n✓ Đã nhận sổ. Bước tiếp: python3 scripts/bat_dau.py")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
