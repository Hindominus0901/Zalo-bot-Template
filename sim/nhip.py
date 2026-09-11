"""Quyết định nhịp: follow-up, heartbeat, boot. Thuần, tất định, không gọi model.

Đây là chỗ hỏng thì mất tin khách hoặc nhắn lúc 4h sáng mùng 1 Tết. Luật gốc:
skills/follow-up/SKILL.md · HEARTBEAT.md · BOOT.md
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timedelta

from .kho import Chu, Phieu

DON_THAT = {"cho_chot", "da_chot_chu", "dang_giao", "xong"}


@dataclass(frozen=True)
class Quyet:
    gui: bool
    nhanh: str = ""
    ly_do: str = ""

    def __bool__(self) -> bool:
        return self.gui


def _chung(chu: Chu, luc: datetime) -> Quyet | None:
    """Rào chung cho cả hai nhánh. Trả Quyet(False) nếu chặn, None nếu qua."""
    if chu.dang_nghi(luc.date()):
        return Quyet(False, ly_do="ngày nghỉ / Tết — để nhịp sau, không gửi bù")
    if not chu.trong_gio_followup(luc):
        return Quyet(False, ly_do="ngoài giờ chủ cho nhắn (hoặc chưa điền giờ)")
    return None


def im_sau_gia(phieu: Phieu, chu: Chu, luc: datetime) -> Quyet:
    if chu.im_sau_gia_gio is None:
        return Quyet(False, ly_do="USER.md chưa bật nhánh im-sau-giá")
    if (chan := _chung(chu, luc)) is not None:
        return chan
    if phieu.lay("followup_im", "chua") != "chua":
        return Quyet(False, ly_do=f"nhánh đã khóa: followup_im={phieu.lay('followup_im')}")
    bao_gia = phieu.gio("da_bao_gia_luc")
    if bao_gia is None:
        return Quyet(False, ly_do="chưa nói số wiki lần nào (da_bao_gia_luc trống)")
    if luc - bao_gia < timedelta(hours=chu.im_sau_gia_gio):
        return Quyet(False, ly_do=f"chưa đủ {chu.im_sau_gia_gio}h kể từ lúc báo giá")
    return Quyet(True, "im", "đủ điều kiện — một tin rồi khóa nhánh")


def sau_don(phieu: Phieu, chu: Chu, luc: datetime) -> Quyet:
    if chu.sau_don_gio is None:
        return Quyet(False, ly_do="USER.md chưa bật nhánh sau-đơn")
    if not chu.cau_mau_sau_don:
        return Quyet(False, ly_do="chưa có câu mẫu của chủ — không bịa")
    if (chan := _chung(chu, luc)) is not None:
        return chan
    if phieu.lay("followup_don", "chua") != "chua":
        return Quyet(False, ly_do=f"nhánh đã khóa: followup_don={phieu.lay('followup_don')}")
    if (tt := phieu.lay("trang_thai_don", "trong")) not in DON_THAT:
        return Quyet(False, ly_do=f"chưa có đơn thật (trang_thai_don={tt}). Ảnh CK không tính")
    moc = phieu.gio("don_chot_luc") or phieu.gio("don_ghi_luc")
    if moc is None:
        return Quyet(False, ly_do="không có mốc giờ đơn")
    if luc - moc < timedelta(hours=chu.sau_don_gio):
        return Quyet(False, ly_do=f"chưa đủ {chu.sau_don_gio}h kể từ lúc ghi/chốt đơn")
    return Quyet(True, "don", "đủ điều kiện — đúng câu mẫu chủ, một nhịp")


def ban_giao_con_treo(phieu: Phieu, luc: datetime) -> Quyet:
    """Cờ bàn giao tự hết hạn 24h — nhưng không tự mở lại quyền nói về tiền."""
    if phieu.lay("ban_giao", "khong") != "dang_cho":
        return Quyet(False, ly_do="không có bàn giao treo")
    moc = phieu.gio("ban_giao_luc")
    if moc is None or luc - moc < timedelta(hours=24):
        return Quyet(False, ly_do="còn trong 24h, vẫn chờ người thật")
    return Quyet(True, "ban_giao_qua_han",
                 "quá 24h — ghi viec_mo, báo chủ MỘT lần, vẫn giữ dang_cho")


def boot_tin_no(dong_no: list[tuple[str, datetime]], luc: datetime) -> dict:
    """BOOT.md: nợ trong 12h → trả một tin; cũ hơn → chỉ báo chủ. Cả hai đều xoá dòng."""
    tra, chi_bao_chu = [], []
    for sender, nhan_luc in dong_no:
        (tra if luc - nhan_luc < timedelta(hours=12) else chi_bao_chu).append(sender)
    return {"tra_khach": tra, "chi_bao_chu": chi_bao_chu}
