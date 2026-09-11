"""Não tháo rời: chạy bằng luật (không cần key) hoặc cắm Claude thật.

Nửa tất định (rào giờ, phiếu, sổ nợ) chạy được với não `luat`. Nửa giọng
(lầy, tắt hài, không bịa số) chỉ kiểm được với não `claude`.
"""

from __future__ import annotations

import os
from dataclasses import dataclass, field

MODEL = "claude-opus-5"


@dataclass
class TraLoi:
    chu: str
    tu_cache: int = 0
    token_vao: int = 0
    token_ra: int = 0
    that: bool = False          # có phải model thật trả không


class NaoLuat:
    """Không gọi model. Trả câu đánh dấu, để kiểm đường đi chứ không kiểm giọng."""

    ten = "luat"

    def __call__(self, goi: dict) -> TraLoi:
        tin = goi["messages"][-1]["content"]
        return TraLoi(chu=f"[luat] đã nhận {len(tin)} ký tự", that=False)


class NaoClaude:
    """Gọi Claude thật. Cần `pip install anthropic` và một API key."""

    ten = "claude"

    def __init__(self, model: str = MODEL):
        try:
            import anthropic
        except ImportError as e:
            raise SystemExit(
                "Cần SDK: pip install anthropic\n"
                "Não `luat` chạy được không cần gì — dùng --nao luat để thử phần máy."
            ) from e
        self.client = anthropic.Anthropic()
        self.model = model

    def __call__(self, goi: dict) -> TraLoi:
        r = self.client.messages.create(
            model=self.model,
            max_tokens=2000,
            output_config={"effort": "low"},   # CSKH là việc nhẹ, không cần nghĩ sâu
            system=goi["system"],              # nền đã gắn cache_control ở sim/nen.py
            messages=goi["messages"],
        )
        chu = "".join(b.text for b in r.content if b.type == "text")
        return TraLoi(
            chu=chu,
            tu_cache=r.usage.cache_read_input_tokens or 0,
            token_vao=r.usage.input_tokens,
            token_ra=r.usage.output_tokens,
            that=True,
        )


def chon(ten: str, model: str = MODEL):
    if ten == "claude":
        return NaoClaude(model)
    if ten == "luat":
        return NaoLuat()
    raise SystemExit(f"não lạ: {ten} (chọn: luat | claude)")


def co_key() -> bool:
    return bool(os.environ.get("ANTHROPIC_API_KEY") or os.environ.get("ANTHROPIC_AUTH_TOKEN"))
