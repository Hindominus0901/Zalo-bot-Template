"""Sinh knowledge/wiki/INDEX.md và khối nền cuối AGENTS.md.

OpenClaw chỉ nạp AGENTS.md, SOUL.md, IDENTITY.md, USER.md, MEMORY.md vào prompt
(đã kiểm trong code 2026.9.4). persona.md và INDEX.md KHÔNG được nạp — bot chỉ
thấy chúng nếu tự mở. Nên script chép cả hai vào một khối có đánh dấu ở cuối
AGENTS.md: bot biết shop bán gì và tra tờ nào mà không tốn lượt mở file.

Thứ tự luôn theo tên file — khối nằm ở tầng nền của prompt, đổi thứ tự là
làm vỡ cache (xem docs/12-prompt-va-cache.md).

Chạy với --kiem để chỉ kiểm tra, không ghi (dùng trong test / CI).
"""

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PUBLIC = ROOT / "knowledge" / "wiki" / "public"
INDEX = ROOT / "knowledge" / "wiki" / "INDEX.md"
PERSONA = ROOT / "knowledge" / "persona.md"
AGENTS = ROOT / "AGENTS.md"
MO = "<!-- NỀN SINH TỰ ĐỘNG — scripts/lam_chi_muc.py chép từ persona.md + INDEX.md. Đừng sửa tay. -->"
DONG = "<!-- HẾT NỀN SINH TỰ ĐỘNG -->"
CHO_CHU = "[CHỜ CHỦ SHOP]"

DAU = """<!-- FILE CỦA SHOP — giữ bản của bạn khi cập nhật template -->
# Chỉ mục sổ — tờ nào nói việc gì

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
    # Bỏ qua dòng đánh dấu FILE CỦA SHOP (và dòng trống) ở đầu file.
    while text.startswith("<!--") or text.startswith("\n"):
        if text.startswith("\n"):
            text = text[1:]
        else:
            text = text[text.index("-->") + 3:].lstrip("\n")
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


def _bo_dau(text: str) -> str:
    """Bỏ dấu FILE CỦA SHOP và H1 — trong AGENTS.md chúng thành nhiễu."""
    dong = [d for d in text.splitlines() if not d.startswith("<!-- FILE CỦA SHOP")]
    while dong and not dong[0].strip():
        dong.pop(0)
    return "\n".join(dong).strip()


def khoi_nen(index: str) -> str:
    persona = _bo_dau(PERSONA.read_text(encoding="utf-8")) if PERSONA.exists() else ""
    persona = persona.replace("\n# ", "\n### ").replace("\n## ", "\n### ")
    if persona.startswith("# "):
        persona = "### " + persona[2:]
    bang = index[index.index("| Tờ |"):].strip()
    return (f"{MO}\n## Shop này và sổ của shop (đã nạp — đừng mở lại hai file này)\n\n"
            f"{persona}\n\n### Sổ có những tờ nào\n\nMở đúng **một** tờ khi cần số. "
            f"`⏳` = chờ chủ điền, không nói số.\n\n{bang}\n{DONG}\n")


def agents_moi(nen: str) -> str:
    cu = AGENTS.read_text(encoding="utf-8")
    if MO in cu and DONG in cu:
        dau = cu[:cu.index(MO)]
        sau = cu[cu.index(DONG) + len(DONG):].lstrip("\n")
        return dau + nen + (("\n" + sau) if sau else "")
    return cu.rstrip("\n") + "\n\n" + nen


def main() -> int:
    if not PUBLIC.is_dir():
        print("khong thay knowledge/wiki/public/", file=sys.stderr)
        return 1
    moi = dung()
    ag = agents_moi(khoi_nen(moi))
    kiem = "--kiem" in sys.argv
    cu = INDEX.read_text(encoding="utf-8") if INDEX.exists() else ""
    ag_cu = AGENTS.read_text(encoding="utf-8")
    if moi == cu and ag == ag_cu:
        print("INDEX.md da khop")
        return 0
    if kiem:
        lech = [f for f, a, b in (("INDEX.md", moi, cu), ("AGENTS.md (khoi nen)", ag, ag_cu)) if a != b]
        print(f"{', '.join(lech)} lech voi wiki/public/ + persona.md — chay scripts/lam-chi-muc.sh",
              file=sys.stderr)
        return 1
    INDEX.write_text(moi, encoding="utf-8")
    AGENTS.write_text(ag, encoding="utf-8")
    print(f"da ghi INDEX.md + khoi nen AGENTS.md ({len(list(PUBLIC.glob('*.md')))} to)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
