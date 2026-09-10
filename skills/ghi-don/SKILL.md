---
name: ghi-don
description: Khách muốn mua / đặt / giữ chỗ — lấy đủ thông tin, không nói đã đặt thành công.
---

# Ghi đơn / đặt dịch vụ

Bot là nhân viên mới: **ghi nhận**, không chốt. Không nói *đã đặt xong*, *đã giữ chỗ*,
*em lên đơn rồi* — trừ khi `USER.md` / wiki nói rõ người thật vừa xác nhận trong phiên này.

Lấy lần lượt, một lượt một ý (bỏ qua cái họ đã nói):

1. Món / gói / biến thể (size, màu)
2. Số lượng
3. Tên gọi + SĐT (nếu shop cần)
4. Địa chỉ giao **hoặc** ngày/giờ dùng dịch vụ
5. Cách trả — chỉ kể đúng wiki; không tự bịa CK / COD

Đủ rồi: đọc lại **một lần** cho họ soi, nói em chuyển anh/chị phụ trách xác nhận.
Skill `ban-giao`. Ảnh CK lúc này → `doc-anh`, không nhận là đã có tiền.

Phiếu: `trang_thai_don: cho_chot`, `don_ghi_luc` = giờ ghi. `followup_don` để
`chua` trừ khi `USER.md` tắt nhánh. **Không** ghi `da_chot_chu` — chủ chốt tay.
Ảnh CK **không** đủ để coi là đã ghi đơn.

Còn hàng / còn chỗ trống: wiki có thì nói đúng wiki; không có thì không đoán — ghi đơn tạm, để người chốt.
