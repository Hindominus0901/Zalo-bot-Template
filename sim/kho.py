"""Đọc workspace: USER.md, phiếu, ma trận. Chỉ stdlib.

Đây là chỗ duy nhất biết định dạng file. Mọi thứ khác nhận dict.
"""

from __future__ import annotations

import json
import re
from dataclasses import dataclass, field
from datetime import date, datetime, time
from pathlib import Path

GOC = Path(__file__).resolve().parent.parent
CHO = "CHỜ CHỦ SHOP"


def _gia_tri(dong: str) -> str:
    """`- **Tên:** giá trị` → `giá trị`."""
    return dong.split(":**", 1)[1].strip() if ":**" in dong else ""


def _chua_dien(v: str) -> bool:
    return not v or CHO in v or v.lower().strip() in ("tắt", "tat", "—", "-")


def _gio(v: str) -> tuple[time, time] | None:
    """`9h–21h`, `9h-21h`, `09:00-21:00` → (bắt đầu, kết thúc). Không đọc được → None."""
    if _chua_dien(v):
        return None
    so = re.findall(r"(\d{1,2})(?::(\d{2}))?\s*[h:]?", v)
    cap = [(int(h), int(p or 0)) for h, p in so if 0 <= int(h) <= 23][:2]
    if len(cap) != 2:
        return None
    return time(*cap[0]), time(*cap[1])


def _ngay_nghi(v: str) -> list[tuple[tuple[int, int], tuple[int, int]]]:
    """`28/1–5/2, 10/3` → [((1,28),(2,5)), ((3,10),(3,10))]. Không nghỉ → []."""
    if _chua_dien(v) or "không nghỉ" in v.lower():
        return []
    khoang = []
    for phan in re.split(r"[,;]", v):
        cap = re.findall(r"(\d{1,2})\s*/\s*(\d{1,2})", phan)
        if len(cap) >= 2:
            khoang.append(((int(cap[0][1]), int(cap[0][0])), (int(cap[1][1]), int(cap[1][0]))))
        elif len(cap) == 1:
            md = (int(cap[0][1]), int(cap[0][0]))
            khoang.append((md, md))
    return khoang


@dataclass
class Chu:
    """USER.md — người vận hành."""

    co_kenh_bao: bool = False
    gio_goi_lai: tuple[time, time] | None = None
    gio_followup: tuple[time, time] | None = None
    ngay_nghi: list = field(default_factory=list)
    im_sau_gia_gio: int | None = None
    sau_don_gio: int | None = None
    cau_mau_sau_don: str = ""

    @classmethod
    def doc(cls, duong: Path | None = None) -> "Chu":
        t = (duong or GOC / "USER.md").read_text(encoding="utf-8")
        c = cls()
        for dong in t.split("\n"):
            if not dong.startswith("- **"):
                continue
            ten, v = dong[4:].split(":**")[0].lower(), _gia_tri(dong)
            if "giờ được hẹn gọi lại" in ten:
                c.gio_goi_lai = _gio(v)
            elif "giờ được nhắn follow-up" in ten:
                c.gio_followup = _gio(v)
            elif "ngày nghỉ" in ten:
                c.ngay_nghi = _ngay_nghi(v)
            elif "nhóm" in ten or "nick zalo nhận bàn giao" in ten:
                c.co_kenh_bao = c.co_kenh_bao or not _chua_dien(v)
            elif "im sau giá" in ten:
                c.im_sau_gia_gio = None if _chua_dien(v) else int(re.search(r"\d+", v).group())
            elif ten.startswith("sau đơn"):
                c.sau_don_gio = None if _chua_dien(v) else int(re.search(r"\d+", v).group())
            elif "câu mẫu sau đơn" in ten:
                c.cau_mau_sau_don = "" if _chua_dien(v) else v
        return c

    def dang_nghi(self, ngay: date) -> bool:
        for dau, cuoi in self.ngay_nghi:
            md = (ngay.month, ngay.day)
            if dau <= cuoi:
                if dau <= md <= cuoi:
                    return True
            elif md >= dau or md <= cuoi:   # khoảng vắt qua năm mới, ví dụ 28/12–5/1
                return True
        return False

    def trong_gio_followup(self, luc: datetime) -> bool:
        if self.gio_followup is None:
            return False
        dau, cuoi = self.gio_followup
        return dau <= luc.time() <= cuoi


@dataclass
class Phieu:
    """memory/phieu/{id}.md — một khách."""

    id: str
    truong: dict = field(default_factory=dict)

    @classmethod
    def tu_chu(cls, id: str, noi_dung: str) -> "Phieu":
        tr = {}
        for dong in noi_dung.split("\n"):
            if dong.startswith("- **"):
                tr[dong[4:].split(":**")[0].strip()] = _gia_tri(dong)
        return cls(id=id, truong=tr)

    def lay(self, ten: str, mac_dinh: str = "") -> str:
        return self.truong.get(ten, mac_dinh).strip()

    def gio(self, ten: str) -> datetime | None:
        v = self.lay(ten)
        for dinh in ("%Y-%m-%d %H:%M", "%Y-%m-%dT%H:%M", "%Y-%m-%d"):
            try:
                return datetime.strptime(v, dinh)
            except ValueError:
                continue
        return None

    def do_dai(self) -> int:
        return sum(len(k) + len(v) + 8 for k, v in self.truong.items())


def ma_tran() -> dict:
    return json.loads((GOC / "knowledge/logic/ma-tran.json").read_text(encoding="utf-8"))
