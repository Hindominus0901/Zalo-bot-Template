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
thấy gì* một dòng, việc mở). Ghi đè dòng cũ cùng mục, giữ ngày `updated`.

Không ghi: số CK, CCCD, OTP, mật khẩu, SĐT đủ, đường dẫn ảnh, nội bộ wiki.
(`khong_ghi`: so_ck, cccd, mat_khau, otp, anh_goc, sdt_day_du)

Không có ID / id bẩn → không tạo file. Thiếu wiki vẫn vào `memory/YYYY-MM-DD.md`.

Khách cũ: đọc phiếu rồi `cham-khach-cu`. Trống phiếu ≠ bịa lần trước.
