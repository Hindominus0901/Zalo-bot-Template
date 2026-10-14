#!/usr/bin/env python3
"""Thử giọng với chủ — bot THẬT trả từng tình huống, đặt cạnh câu chủ từng trả.

    python3 scripts/thu_giong.py                 # mọi tình huống trong hoi-thoai-shop.md
    python3 scripts/thu_giong.py --cau "giá bao nhiêu" --cau "shop ơi"
    python3 scripts/vps.py thu-giong             # từ máy người dựng, chạy trên VPS

Chạy trên máy có bot (VPS). Mỗi câu một phiên mới tên `thu-giong-…` qua
`openclaw agent --local`: không đụng phiên của khách thật, **không gửi lên
Zalo**. Tốn tiền GPT như một tin khách mỗi câu — báo chủ trước.

In ra từng cặp: Khách / Bot vừa trả / Chủ từng trả. Coding agent đọc cho chủ,
hỏi *"giống anh/chị nói chưa?"*, sửa `SOUL.md` mục giọng của chủ hoặc
`knowledge/hoi-thoai-shop.md`, đẩy sổ, chạy lại. Xong khi chủ nói "giống" ≥ 8/10.
"""

from __future__ import annotations

import argparse
import json
import re
import shutil
import subprocess
import sys
import time
from dataclasses import dataclass
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
HOI_THOAI = ROOT / "knowledge" / "hoi-thoai-shop.md"

# Khi sổ hội thoại còn ít — mấy câu chung, mỗi câu thử một nét (docs/04).
CAU_CHUNG = [
    "shop ơi",
    "bên mình bán gì vậy",
    "giá bao nhiêu",
    "mắc quá, bớt được không",
    "để em suy nghĩ thêm",
    "cho mình xin số tài khoản",
    "bạn là bot à",
    "hàng hôm qua nhận bị lỗi rồi",
    "ok cảm ơn shop",
    "ib",
]


@dataclass
class Tinh:
    ten: str
    khach: str
    dung: str = ""


def doc_tinh_huong(md: str) -> list[Tinh]:
    """Mỗi mục `## …` có dòng `**Khách:** …` là một câu thử. Bỏ phần chú thích
    `<!-- -->` (khuôn mẫu, không phải tình huống thật)."""
    md = re.sub(r"<!--.*?-->", "", md, flags=re.S)
    out: list[Tinh] = []
    for khoi in re.split(r"^## ", md, flags=re.M)[1:]:
        ten = khoi.splitlines()[0].strip()
        m = re.search(r"^\*\*Khách:\*\*\s*>?\s*(.+)$", khoi, re.M)
        if not m or "[CHỜ CHỦ SHOP" in m.group(1):
            continue
        dung = ""
        d = re.search(r"^\*\*Đúng\*\*[^\n]*\n((?:>.*\n?)+)", khoi, re.M)
        if d:
            dung = " ".join(x.lstrip("> ").strip() for x in d.group(1).splitlines()).strip()
        out.append(Tinh(ten, m.group(1).strip(), dung))
    return out


def lenh(oc: str, phien: str, cau: str, agent: str = "main") -> list[str]:
    # Không --deliver: câu trả lời KHÔNG đi lên Zalo.
    return [oc, "agent", "--local", "--agent", agent, "--session-id", phien,
            "--message", cau, "--json"]


def cau_tra(ra: str) -> str:
    try:
        d = json.loads(ra[ra.index("{"):])
    except (ValueError, json.JSONDecodeError):
        return ""
    chu = [p.get("text") or "" for p in d.get("payloads") or []]
    return "\n".join(x for x in chu if x).strip() or (d.get("meta") or {}).get("finalAssistantVisibleText", "")


def hoi_bot(oc: str, phien: str, cau: str, timeout: int = 180) -> str:
    try:
        r = subprocess.run(lenh(oc, phien, cau), capture_output=True, text=True, timeout=timeout)
    except subprocess.TimeoutExpired:
        return "(bot không trả lời kịp — quá 3 phút)"
    tra = cau_tra(r.stdout)
    if not tra:
        loi = (r.stderr or r.stdout).strip().splitlines()[-1:] or ["không rõ"]
        return f"(bot không trả lời — {loi[0][:200]})"
    return tra


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="Thử giọng bot thật với các tình huống của shop.")
    ap.add_argument("--cau", action="append", default=[], help="thử thêm một câu lẻ (lặp được)")
    ap.add_argument("--toi-da", type=int, default=20, help="tối đa bao nhiêu câu một lượt")
    ap.add_argument("--openclaw", default=shutil.which("openclaw") or "openclaw")
    a = ap.parse_args(argv)

    ds = doc_tinh_huong(HOI_THOAI.read_text(encoding="utf-8")) if HOI_THOAI.exists() else []
    ds += [Tinh("câu lẻ", c) for c in a.cau]
    if len(ds) < 10 and not a.cau:
        print(f"• hoi-thoai-shop.md mới có {len(ds)} tình huống — thêm câu chung cho đủ 10.\n")
        ds += [Tinh("câu chung", c) for c in CAU_CHUNG[:10 - len(ds)]]
    ds = ds[:a.toi_da]

    dau = time.strftime("%m%d%H%M")
    for i, t in enumerate(ds, 1):
        tra = hoi_bot(a.openclaw, f"thu-giong-{dau}-{i}", t.khach)
        print(f"── {i}/{len(ds)}. {t.ten}")
        print(f"Khách:          {t.khach}")
        print(f"Bot vừa trả:    {tra}")
        if t.dung:
            print(f"Chủ từng trả:   {t.dung}")
        print()
    print(f"Xong {len(ds)} câu. Đọc cho chủ từng cặp: \"giống anh/chị nói chưa? chưa thì "
          "anh/chị sẽ nói sao?\" — sửa SOUL.md (giọng của chủ) / hoi-thoai-shop.md rồi chạy lại.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
