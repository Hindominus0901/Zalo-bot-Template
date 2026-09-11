---
name: ghi-don
description: Khách muốn mua / đặt / giữ chỗ — lấy đủ thông tin, không nói đã đặt thành công.
---

# Ghi đơn / đặt dịch vụ

Bot là nhân viên mới: **ghi nhận**, không chốt. Không nói *đã đặt xong*, *đã giữ chỗ*,
*em lên đơn rồi* — trừ khi `USER.md` / wiki nói rõ người thật vừa xác nhận trong phiên này.

Lấy lần lượt, một lượt một ý (bỏ qua cái họ đã nói).

**Bán hàng:**

1. Món / gói / biến thể (size, màu)
2. Số lượng
3. Tên gọi + SĐT (nếu shop cần)
4. Địa chỉ giao

**Khóa học / dịch vụ / tư vấn:**

1. Khóa hoặc gói nào (`lo-trinh.md` nếu họ chưa rõ gồm gì)
2. Lớp / ca / ngày giờ nào (`dat-lich.md`)
3. **Ai dùng** — có thể khác người đang nhắn (mẹ đăng ký cho con, công ty đăng
   ký cho nhân viên). Hỏi một câu, đừng mặc định
4. Đang ở mức nào / đã làm gì rồi — chỉ hỏi nếu `ai-phu-hop.md` nói nó đổi gói

Rồi cả hai cùng:
5. Cách trả — chỉ kể **hình thức** đúng wiki (CK / COD / trả trước); không tự
   bịa. Họ xin **số tài khoản hay mã QR** → không đưa, `ban-giao`
   (`tinh-huong.md`)

Thấy họ **chưa hợp** theo `ai-phu-hop.md` → nói thẳng trước khi ghi đơn. Nhận
bừa rồi hoàn sau là mất cả tiền lẫn khách.

Đủ rồi: đọc lại **một lần** cho họ soi, nói em chuyển anh/chị phụ trách xác nhận.
Skill `ban-giao`. Ảnh CK lúc này → `doc-anh`, không nhận là đã có tiền.

Phiếu: `trang_thai_don: cho_chot`, `don_ghi_luc` = giờ ghi. `followup_don` để
`chua` trừ khi `USER.md` tắt nhánh. **Không** ghi `da_chot_chu` — chủ chốt tay.
Ảnh CK **không** đủ để coi là đã ghi đơn.

Còn hàng / còn chỗ trống: wiki có thì nói đúng wiki; không có thì không đoán — ghi đơn tạm, để người chốt.

**Kiểm lại:** Có lỡ nói “đã đặt xong” chưa? Phiếu có đang là `cho_chot` (không phải `da_chot_chu`) không?
