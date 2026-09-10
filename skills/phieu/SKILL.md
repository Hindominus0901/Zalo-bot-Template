---
name: phieu
description: Đọc/ghi phiếu ngắn theo Zalo ID — size, món, ảnh thấy gì. Không CRM, không đọc phiếu cho khách.
---

# Phiếu theo ID

ID = `senderId` zalouser (inbox). Nhóm: `{groupId}-{senderId}`. File
`memory/phieu/{id}.md`. Chỉ `A-Za-z0-9._-`. Mẫu: `memory/phieu/MAU.md`.

**Đầu lượt:** có file thì đọc. Dùng im lặng — không *em đã ghi nhớ*, không đọc
phiếu thành tiếng.

**Cuối lượt:** chỉ ghi fact **bền** vừa có (pha, việc cần, size, món từ chối,
tình huống / chỗ trống đã biết, *ảnh thấy gì* một dòng, việc mở, trạng thái
đơn / follow-up nếu đổi). Ghi đè dòng cũ cùng mục, giữ ngày `updated`.

Pha + chỗ đã biết (`viec_can`, `tinh_huong`, `rang_buoc`, `da_thu`, `lo_ngai`,
`hoi_roi`) nằm **trên phiếu**, không giữ object YAML trôi. Đã có thì **đừng hỏi
lại**. `hoi_roi` = số câu chẩn đoán đã hỏi (tối đa 3 rồi tư vấn trên cái có).

Trạng thái đơn: `trong` (mặc định) · `cho_chot` (đã `ghi-don`) · `cho_ck` ·
`da_chot_chu` (người thật chốt — không vì ảnh CK) · `dang_giao` · `xong`.
Ảnh CK chỉ vào `anh_thay_gi` + `viec_mo`, **không** đổi `trang_thai_don` thành
`cho_chot` / `da_chot_chu`.

`ban_giao`: `khong` (mặc định) · `dang_cho` (đã gọi người, chưa xong) · `xong`.
Kèm `ban_giao_luc` và `ban_giao_ve` (chủ đề nào đang chờ). Luật: `skills/ban-giao`.

`da_bao_gia_luc` = lúc nói **số wiki** (`bao-gia`). `don_ghi_luc` / `don_chot_luc`
= lúc ghi đơn / chủ chốt. `followup_*`: `chua` | `da_gui` | `tat` — heartbeat
xem skill `follow-up`.

## Trần 1800 ký tự — đầy thì gộp, không cắt bừa

Tiêu đề phiếu mang sức chứa: `# Phiếu 123   [62% — 1.116/1.800]`. Cập nhật con số
đó mỗi lần ghi.

Sắp ghi mà biết sẽ vượt 1800: **đừng cắt cụt, đừng bỏ dòng mới.** Phiếu đang nằm
sẵn trước mắt — đọc lại nó, **gộp hai dòng cùng ý thành một**, hoặc bỏ dòng đã cũ,
rồi ghi. Làm hết trong **cùng một lượt**, đừng hẹn lần sau.

Thứ tự hy sinh khi phải gọn, từ trên xuống:

1. `da_thu` cũ
2. `lo_ngai` đã xử xong
3. `mon_da_noi` cũ — giữ 3 món gần nhất
4. `anh_thay_gi` cũ — giữ dòng gần nhất

**Không bao giờ bỏ:** `goi` · `size` · `trang_thai_don` · `da_bao_gia_luc` ·
`don_ghi_luc` · `don_chot_luc` · `followup_im` · `followup_don` · `viec_mo`.

Gộp xong vẫn vượt → giữ nguyên nhóm không-bao-giờ-bỏ, phần còn lại rút thành một
dòng `tom_tat:` bằng chữ mình. Vẫn vượt nữa thì đó là phiếu hỏng: ghi một dòng
vào `memory/YYYY-MM-DD.md` cho chủ xem, đừng làm phiếu phình tiếp.

Không ghi: số CK, CCCD, OTP, mật khẩu, SĐT đủ, đường dẫn ảnh, nội bộ wiki.
(`khong_ghi`: so_ck, cccd, mat_khau, otp, anh_goc, sdt_day_du)

Không có ID / id bẩn → không tạo file. Thiếu wiki vẫn vào `memory/YYYY-MM-DD.md`.

Khách cũ: đọc phiếu rồi `cham-khach-cu`. Trống phiếu ≠ bịa lần trước.

**Kiểm lại:** Phiếu còn dưới trần chưa? Có dòng nào là chuyện vặt của một lượt, không phải fact bền?
