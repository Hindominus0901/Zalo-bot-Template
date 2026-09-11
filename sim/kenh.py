"""Giả lập kênh zalouser: gộp tin dồn, session key, nhóm gọi tên, chia tin.

Luật gốc: AGENTS.md mục *Tin dồn và nhịp gửi* · *Khi nào trả lời*
· docs/02-kenh-zalouser.md · knowledge/vui-va-ngoai-le.md (nhóm)
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from datetime import datetime, timedelta

DEBOUNCE_MS = 1500
DEBOUNCE_MEDIA_MS = 3000
CHIA_TIN_TU = 600
KHONG_TACH = re.compile(r"\d[\d\s.\-]{6,}|[A-Z]{2,}\d{3,}")   # mã đơn, SĐT, dãy số


@dataclass
class Tin:
    sender: str
    chu: str = ""
    luc: datetime = field(default_factory=datetime.now)
    nhom: str | None = None
    co_media: bool = False

    @property
    def la_nhom(self) -> bool:
        return self.nhom is not None


def session_key(tin: Tin, agent: str = "nami") -> str:
    """Khoá phiên. Nhóm và inbox là hai phiên khác nhau — luật docs/12 + skills/phieu."""
    if tin.la_nhom:
        return f"agent:{agent}:zalouser:group:{tin.nhom}"
    return f"agent:{agent}:zalouser:direct:{tin.sender}"


def phieu_id(tin: Tin) -> str:
    """skills/phieu: inbox = senderId; nhóm = groupId-senderId."""
    goc = f"{tin.nhom}-{tin.sender}" if tin.la_nhom else tin.sender
    return goc if re.fullmatch(r"[A-Za-z0-9._-]+", goc) else ""


def gop_tin_don(tins: list[Tin], cua_so_ms: int = DEBOUNCE_MS) -> list[list[Tin]]:
    """Timer reset mỗi tin. Tin có media chờ lâu hơn — nhiều ảnh gửi lệch nhau."""
    cum: list[list[Tin]] = []
    for tin in sorted(tins, key=lambda t: t.luc):
        ms = max(cua_so_ms, DEBOUNCE_MEDIA_MS) if tin.co_media else cua_so_ms
        if cum and cum[-1][-1].sender == tin.sender and cum[-1][-1].nhom == tin.nhom \
                and tin.luc - cum[-1][-1].luc <= timedelta(milliseconds=ms):
            cum[-1].append(tin)
        else:
            cum.append([tin])
    return cum


def duoc_tra_loi(tin: Tin, ten: str = "Nami", biet_hieu: tuple[str, ...] = (),
                 reply_tin_bot: bool = False) -> bool:
    """Inbox luôn trả. Nhóm chỉ khi gọi tên / @ / reply tin mình."""
    if not tin.la_nhom:
        return True
    if reply_tin_bot:
        return True
    chu = tin.chu.lower()
    return any(t.lower() in chu for t in (ten, *biet_hieu) if t)


def chia_tin(tra_loi: str, nguong: int = CHIA_TIN_TU) -> list[str]:
    """Dài quá thì tách 2–3 tin, ranh giới là đoạn.

    **Không bao giờ tách bên trong một đoạn** — mã đơn, SĐT, địa chỉ nằm gọn
    trong một đoạn nên không bị cắt đôi. Một đoạn dài quá ngưỡng vẫn đi nguyên
    tin: thà một tin dài còn hơn khách copy nhầm nửa mã đơn.
    """
    if len(tra_loi) <= nguong:
        return [tra_loi]
    doan = [d.strip() for d in tra_loi.split("\n\n") if d.strip()]
    ra: list[str] = []
    for d in doan:
        if ra and len(ra[-1]) + len(d) + 2 <= nguong:
            ra[-1] += "\n\n" + d
        else:
            ra.append(d)
    while len(ra) > 3:                      # gộp hai tin ngắn nhất liền nhau
        i = min(range(len(ra) - 1), key=lambda k: len(ra[k]) + len(ra[k + 1]))
        ra[i : i + 2] = [ra[i] + "\n\n" + ra[i + 1]]
    return ra
