#!/usr/bin/env python3
"""Người bán: đóng bản zip giao khách — đúng những gì đã commit, không lẫn bí mật.

    python3 scripts/lam_ban_zip.py           # → dist/zalo-bot-<VERSION>.zip

Lấy từ `git archive HEAD`: file chưa commit, `.env`, `.vps.json`, phiếu khách
đều không vào được. Khách giải nén, mở thư mục bằng Claude Code / Codex, đọc
`BAT-DAU.md`.
"""

from __future__ import annotations

import re
import subprocess
import sys
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CAM = re.compile(r"(?:^|/)(?:\.env|\.vps\.json|openclaw\.json|secrets[^/]*|[^/]*\.(?:key|pem))$"
                 r"|/memory/(?!(?:phieu/|de-xuat/|nhat-ky-sua/)?(?:README\.md|MAU\.md|\.gitkeep)$)")


def main() -> int:
    if subprocess.run(["git", "status", "--porcelain"], cwd=ROOT, capture_output=True,
                      text=True).stdout.strip():
        print("• Còn thay đổi chưa commit — chúng KHÔNG vào zip.", file=sys.stderr)
    ban = (ROOT / "VERSION").read_text().strip()
    dich = ROOT / "dist" / f"zalo-bot-{ban}.zip"
    dich.parent.mkdir(exist_ok=True)
    r = subprocess.run(["git", "archive", "--format=zip", f"--prefix=zalo-bot-{ban}/",
                        "-o", str(dich), "HEAD"], cwd=ROOT)
    if r.returncode != 0:
        print("✗ git archive lỗi", file=sys.stderr)
        return 1
    with zipfile.ZipFile(dich) as z:
        ten = z.namelist()
    xau = [t for t in ten if not t.endswith("/") and CAM.search(t)]
    if xau:
        dich.unlink()
        print("✗ Zip có thứ không được giao: " + ", ".join(xau[:10]), file=sys.stderr)
        return 1
    print(f"✓ {dich.relative_to(ROOT)} — {len(ten)} file, {dich.stat().st_size // 1024} KB")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
