---
name: phieu
description: Đọc/ghi phiếu ngắn theo Zalo ID — size, món, ảnh thấy gì. Không CRM, không đọc phiếu cho khách.
---

# Phiếu theo ID

ID = `senderId` zalouser (inbox). Nhóm: `{groupId}-{senderId}`. File
`memory/phieu/{id}.md`. Chỉ `A-Za-z0-9._-`. Mẫu: `memory/phieu/MAU.md`.

**Đầu lượt:** có file thì đọc. Dùng im lặng — không *em đã ghi nhớ*, không đọc
phiếu thành tiếng.

**Cuối lượt:** chỉ ghi fact **bền** vừa có (size, món từ chối, tình huống, *ảnh
thấy gì* một dòng, việc mở, trạng thái đơn / follow-up nếu đổi). Ghi đè dòng cũ
cùng mục, giữ ngày `updated`.

Trạng thái đơn: `trong` (mặc định) · `cho_chot` (đã `ghi-don`) · `cho_ck` ·
`da_chot_chu` (người thật chốt — không vì ảnh CK) · `dang_giao` · `xong`.
Ảnh CK chỉ vào `anh_thay_gi` + `viec_mo`, **không** đổi `trang_thai_don` thành
`cho_chot` / `da_chot_chu`.

`da_bao_gia_luc` = lúc nói **số wiki** (`bao-gia`). `don_ghi_luc` / `don_chot_luc`
= lúc ghi đơn / chủ chốt. `followup_*`: `chua` | `da_gui` | `tat` — heartbeat
xem skill `follow-up`.

Không ghi: số CK, CCCD, OTP, mật khẩu, SĐT đủ, đường dẫn ảnh, nội bộ wiki.
(`khong_ghi`: so_ck, cccd, mat_khau, otp, anh_goc, sdt_day_du)

Không có ID / id bẩn → không tạo file. Thiếu wiki vẫn vào `memory/YYYY-MM-DD.md`.

Khách cũ: đọc phiếu rồi `cham-khach-cu`. Trống phiếu ≠ bịa lần trước.
