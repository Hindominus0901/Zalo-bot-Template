"""Dựng prompt ba tầng và soi xem có gì bay hơi lọt vào nền.

Luật gốc: docs/12-prompt-va-cache.md. Nền vỡ thì không có lỗi nào cả — chỉ là
tiền tăng đều, không ai nhìn. Đây là chỗ bắt việc đó trước khi mất tiền thật.
"""

from __future__ import annotations

import hashlib
import re
from dataclasses import dataclass, field
from pathlib import Path

from .kho import GOC

# Tầng 1–2: nền cố định. OpenClaw nạp sẵn mỗi phiên.
NEN = ["AGENTS.md", "SOUL.md", "TOOLS.md", "IDENTITY.md", "USER.md",
       "knowledge/persona.md", "knowledge/wiki/INDEX.md"]

# Thứ chỉ được nằm ở tầng 3 (đi cùng tin khách), không bao giờ ở nền.
BAY_HOI = [
    (re.compile(r"\b\d{1,2}[:/]\d{2}(:\d{2})?\b"), "dấu thời gian"),
    (re.compile(r"\b20\d{2}-\d{2}-\d{2}\b"), "ngày cụ thể"),
    (re.compile(r"\b[0-9a-f]{8}-[0-9a-f]{4}-", re.I), "id ngẫu nhiên"),
    (re.compile(r"session[_ ]?id|request[_ ]?id", re.I), "id phiên / id request"),
]
# Ví dụ trong tài liệu không tính. Miễn trừ phải HẸP — miễn trừ mọi dòng có
# backtick là bỏ soi 1/3 nền, tức là kiểm cho có.
MIEN_TRU = re.compile(r"ví dụ|CHỜ CHỦ SHOP", re.I)


@dataclass
class Nen:
    manh: list[tuple[str, str]] = field(default_factory=list)   # (tên file, nội dung)

    @classmethod
    def dung(cls, goc: Path | None = None) -> "Nen":
        g = goc or GOC
        return cls([(f, (g / f).read_text(encoding="utf-8")) for f in NEN if (g / f).exists()])

    def chuoi(self) -> str:
        """Thứ tự cố định theo NEN — đổi thứ tự là vỡ cache."""
        return "\n\n".join(n for _, n in self.manh)

    def van_tay(self) -> str:
        return hashlib.sha256(self.chuoi().encode("utf-8")).hexdigest()[:12]

    def ky_tu(self) -> int:
        return len(self.chuoi())

    def token_uoc(self) -> int:
        """Ước thô cho tiếng Việt có dấu: ~2.5 ký tự một token."""
        return round(self.ky_tu() / 2.5)

    def soi_bay_hoi(self) -> list[str]:
        """Tìm thứ đổi mỗi lượt mà lại nằm ở nền."""
        loi = []
        for ten, noi_dung in self.manh:
            trong_khoi_code = False
            for dong in noi_dung.split("\n"):
                if dong.lstrip().startswith("```"):
                    trong_khoi_code = not trong_khoi_code
                    continue
                if trong_khoi_code or MIEN_TRU.search(dong):
                    continue
                for mau, nhan in BAY_HOI:
                    if mau.search(dong):
                        loi.append(f"{ten}: {nhan} — {dong.strip()[:60]}")
        return loi


def luot(nen: Nen, tin_khach: str, phieu: str = "", wiki: str = "") -> dict:
    """Một lượt: nền giữ nguyên, thứ của lượt đi cùng tin khách.

    Trả về dạng messages của Messages API. `system` là nền → đặt cache_control
    ở đó; phiếu và wiki đi trong user message nên không đụng tới prefix.
    """
    phan = [p for p in (
        f"<phieu-khach>\n{phieu}\n</phieu-khach>" if phieu else "",
        f"<du-lieu-ngoai nguon=\"so-shop\">\n{wiki}\n</du-lieu-ngoai>" if wiki else "",
        tin_khach,
    ) if p]
    return {
        "system": [{"type": "text", "text": nen.chuoi(),
                    "cache_control": {"type": "ephemeral"}}],
        "messages": [{"role": "user", "content": "\n\n".join(phan)}],
    }
