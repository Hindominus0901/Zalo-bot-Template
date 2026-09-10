"""Sinh knowledge/wiki/INDEX.md từ frontmatter các tờ trong wiki/public/.

Thứ tự luôn theo tên file — chỉ mục nằm ở tầng nền của prompt, đổi thứ tự là
làm vỡ cache (xem docs/12-prompt-va-cache.md).

Chạy với --kiem để chỉ kiểm tra, không ghi (dùng trong test / CI).
"""

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PUBLIC = ROOT / "knowledge" / "wiki" / "public"
INDEX = ROOT / "knowledge" / "wiki" / "INDEX.md"
CHO_CHU = "[CHỜ CHỦ SHOP]"

DAU = """# Chỉ mục sổ — tờ nào nói việc gì

Sinh tự động bởi `scripts/lam_chi_muc.py`. **Đừng sửa tay** — sửa `summary`
trong chính tờ đó rồi chạy lại.

Bot đọc bảng này để biết mở tờ nào, không phải đoán tên file. Tờ có dấu `⏳` là
đang chờ chủ shop điền: **không dùng để nói số**, nhưng không có nghĩa là shop
không làm việc đó.

| Tờ | Nói về | Trạng thái |
|---|---|---|
"""


def frontmatter(path: Path) -> dict:
    """Đọc frontmatter tối giản: key: value, một dòng một cặp."""
    text = path.read_text(encoding="utf-8")
    if not text.startswith("---\n"):
        return {}
    try:
        block = text.split("---\n", 2)[1]
    except IndexError:
        return {}
    out = {}
    for line in block.split("\n"):
        if ":" not in line or line.startswith(" "):
            continue
        key, _, val = line.partition(":")
        out[key.strip()] = val.strip().strip('"').strip("'")
    return out


def dung() -> str:
    dong = []
    for md in sorted(PUBLIC.glob("*.md"), key=lambda p: p.name):
        fm = frontmatter(md)
        title = fm.get("title") or md.stem
        summary = fm.get("summary") or ""
        cho = CHO_CHU in summary or not summary
        summary = summary.replace(CHO_CHU, "").strip() or "(chưa có mô tả)"
        summary = summary.replace("|", "/")
        dong.append(f"| `{md.name}` | {title} — {summary} | {'⏳' if cho else '✅'} |")
    return DAU + "\n".join(dong) + "\n"


def main() -> int:
    if not PUBLIC.is_dir():
        print("khong thay knowledge/wiki/public/", file=sys.stderr)
        return 1
    moi = dung()
    kiem = "--kiem" in sys.argv
    cu = INDEX.read_text(encoding="utf-8") if INDEX.exists() else ""
    if moi == cu:
        print("INDEX.md da khop")
        return 0
    if kiem:
        print("INDEX.md lech voi wiki/public/ — chay scripts/lam-chi-muc.sh", file=sys.stderr)
        return 1
    INDEX.write_text(moi, encoding="utf-8")
    print(f"da ghi INDEX.md ({len(list(PUBLIC.glob('*.md')))} to)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
