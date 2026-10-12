#!/usr/bin/env python3
"""Gói sổ shop đã điền để chuyển sang máy chạy bot (VPS).

    python3 scripts/dong_goi.py              # in một khối chữ — chép, dán vào VPS
    python3 scripts/dong_goi.py --zip so.zip # ghi file zip — kéo lên VPS

Bên VPS mở bằng `python3 scripts/mo_goi.py`. Mọi cách chuyển: docs/17-dung-bang-app-chat.md.

Chỉ gói **sổ của shop**: tờ có dòng `FILE CỦA SHOP`, `SOUL.md`, hai skill có
phần của shop, và mọi tờ trong `knowledge/wiki/`. Không bao giờ gói phiếu khách
(`memory/`), config đã điền (có senderId chủ), `.env`, khoá.

Gói có giá vốn / hoa hồng (`knowledge/wiki/internal/`) — đừng dán lên trang
công khai, đừng gửi vào nhóm chat.
"""

from __future__ import annotations

import argparse
import base64
import hashlib
import io
import re
import sys
import tarfile
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

DAU_SHOP = "FILE CỦA SHOP"
LUON_GOI = ("SOUL.md", "skills/khai-thac/SKILL.md", "skills/ghi-don/SKILL.md")
MO = "NAMI-GOI-BAT-DAU"
DONG = "NAMI-GOI-HET"
BAN = "v1"
NGAT = 76
TRAN_DAN = 400_000   # quá cỡ này dán qua SSH dễ rơi chữ

# Đường dẫn có thể vào gói. Mọi thứ khác — scripts/, config/, tests/, memory/,
# AGENTS.md (não bot, chỉ mục tự sinh lại) — bị chặn ở cả hai đầu.
_HINH = re.compile(r"^(?:[A-Z][A-Z-]*\.md|knowledge/[a-z0-9/_-]+\.md|skills/(?:khai-thac|ghi-don)/SKILL\.md)$")
CAM = re.compile(r"(?:^|/)(?:\.env|secrets[^/]*|[^/]*\.(?:key|pem))$|^(?:memory|config|scripts|tests|\.git|knowledge/raw)/"
                 r"|^(?:AGENTS|CLAUDE|GEMINI|TOOLS|BOOT|HEARTBEAT)\.md$")


def hop_le(rel: str, noi_dung: bytes) -> bool:
    """Một đường dẫn + nội dung có được vào (hoặc ra khỏi) gói không."""
    if not rel or rel.startswith("/") or "\\" in rel or ".." in rel.split("/"):
        return False
    if CAM.search(rel) or not _HINH.match(rel):
        return False
    if rel in LUON_GOI or rel.startswith("knowledge/wiki/"):
        return True
    return DAU_SHOP.encode("utf-8") in noi_dung[:300]


def gom(goc: Path) -> dict[str, bytes]:
    out: dict[str, bytes] = {}
    ung = [goc / r for r in LUON_GOI]
    ung += sorted((goc / "knowledge" / "wiki").rglob("*.md"))
    ung += sorted(goc.glob("*.md")) + sorted((goc / "knowledge").glob("*.md"))
    for p in ung:
        if not p.is_file() or p.is_symlink():
            continue
        rel = p.relative_to(goc).as_posix()
        b = p.read_bytes()
        if hop_le(rel, b):
            out[rel] = b
    return out


def thanh_tar(tep: dict[str, bytes]) -> bytes:
    buf = io.BytesIO()
    # mtime cố định → cùng sổ thì cùng gói, cùng mã kiểm
    with tarfile.open(fileobj=buf, mode="w:gz", compresslevel=9) as t:
        for rel in sorted(tep):
            ti = tarfile.TarInfo(rel)
            ti.size, ti.mtime, ti.mode = len(tep[rel]), 0, 0o644
            t.addfile(ti, io.BytesIO(tep[rel]))
    return buf.getvalue()


def thanh_khoi(tep: dict[str, bytes]) -> str:
    du = thanh_tar(tep)
    b64 = base64.b64encode(du).decode("ascii")
    dong = [b64[i:i + NGAT] for i in range(0, len(b64), NGAT)]
    return "\n".join([f"{MO} {BAN} {hashlib.sha256(du).hexdigest()} {len(du)}", *dong, DONG]) + "\n"


def thanh_zip(tep: dict[str, bytes], dich: Path) -> None:
    with zipfile.ZipFile(dich, "w", zipfile.ZIP_DEFLATED) as z:
        for rel in sorted(tep):
            z.writestr(rel, tep[rel])


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="Gói sổ shop để chuyển sang VPS.")
    ap.add_argument("--zip", metavar="FILE", help="ghi file zip thay vì in khối chữ")
    ap.add_argument("--goc", default=str(ROOT), help=argparse.SUPPRESS)
    a = ap.parse_args(argv)
    tep = gom(Path(a.goc))
    if not tep:
        print("Không thấy sổ nào để gói — đang đứng đúng thư mục bot chưa?", file=sys.stderr)
        return 1
    for rel in sorted(tep):
        print(f"  {rel}  ({len(tep[rel]):,} byte)", file=sys.stderr)
    if a.zip:
        thanh_zip(tep, Path(a.zip))
        print(f"\nĐã ghi {a.zip} ({len(tep)} tờ). Kéo lên VPS rồi chạy: "
              f"python3 scripts/mo_goi.py {Path(a.zip).name}", file=sys.stderr)
        return 0
    khoi = thanh_khoi(tep)
    print(khoi, end="")
    print(f"\n{len(tep)} tờ, {len(khoi):,} ký tự. Chép TỪ dòng {MO} TỚI dòng {DONG}, "
          f"rồi trên VPS chạy python3 scripts/mo_goi.py và dán vào.", file=sys.stderr)
    if len(khoi) > TRAN_DAN:
        print("Gói to — dán qua SSH dễ rơi chữ. Nên dùng --zip hoặc GitHub (docs/17).", file=sys.stderr)
    print("Gói có giá vốn / hoa hồng: đừng dán lên trang công khai hay nhóm chat.", file=sys.stderr)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
