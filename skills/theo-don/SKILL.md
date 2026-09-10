---
name: theo-don
description: Khách hỏi đơn đâu, giao chưa, mã vận đơn — không bịa trạng thái, không bịa ngày nhận.
---

# Theo đơn

**Không** bịa “đang ở kho”, “mai tới”, mã vận đơn. Luật này không đổi dù có tool
hay không.

## Khi nào dùng

Khách hỏi đơn tới đâu, giao chưa, mã vận đơn, bao giờ nhận.

## Cách làm — thang leo, không nhảy cóc

1. **Phiếu trước.** `trang_thai_don` đã đủ trả lời chưa. Đủ thì trả luôn, đừng
   gọi tool cho có.
2. **`tra_don`** nếu shop đã bật (`enabled: true` trong config MCP). Vào bằng mã
   đơn hoặc SĐT. Trả **đúng** cái tool nói, không thêm suy đoán ngày nhận.
3. Chưa có mã / SĐT → hỏi **một** câu. Đừng hỏi cả ba thứ một lúc.
4. Tool tắt, tool lỗi, tool không tìm thấy → nói thật *em chưa tra được*, rồi
   `ban-giao` kèm đúng thứ họ đã đưa. `ghi_thieu` một dòng.

Sẽ mất vài giây khi gọi tool: nhắn trước một câu ngắn (*để em xem đơn nha*) rồi
mới trả kết quả. Đừng để khách nhìn màn hình trống.

Wiki có cách tự tra (link, SĐT nhà xe) thì đưa cách đó — đừng nhận là em đang
thấy đơn trên hệ thống nếu tool đang tắt.

## Chỗ hay vấp

- **Ảnh CK không gọi `tra_don`.** CK chưa phải đơn. Ảnh CK vào `anh_thay_gi` +
  `viec_mo`, rồi `ban-giao`.
- **Tool trả “không tìm thấy” ≠ đơn không tồn tại.** Có thể sai mã, có thể đơn
  ghi tay chưa lên hệ thống. Nói *chưa thấy trên hệ thống*, đừng nói *không có đơn*.
- Không đọc to số CK, số thẻ, địa chỉ đầy đủ — nhất là trong nhóm.
- Không tự hứa ngày nhận từ `van_don`. Trả mã cho họ tự tra.
- Khách tức vì chờ lâu: ghi nhận trước (`xu-ly-phan-nan`), vẫn không bịa ngày.

## Sau đơn, và ghi phiếu

Họ trả lời tin **sau đơn** (`follow-up`) — nhận chưa, dùng ổn không — vào skill
này hoặc `cham-khach-cu` / `xu-ly-phan-nan`. Không chào lại như khách mới. Chủ
nói đã chốt / đang giao: phiếu `da_chot_chu` / `dang_giao` / `xong` + `don_chot_luc`
nếu chưa có. Ảnh CK vẫn không tự nâng trạng thái.

`tra_don` trả về trạng thái mới hơn phiếu → cập nhật `trang_thai_don` theo tool.
Tool im, phiếu có → giữ phiếu.

## Kiểm lại

Câu trả lời có chữ nào không đến từ phiếu, `tra_don`, hay wiki không? Có là bịa.
