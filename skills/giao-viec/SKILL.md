---
name: giao-viec
description: Chủ nhắn riêng giao việc có giờ — nhắc chủ, nhắn một khách lúc nào đó, nhắn nhóm định kỳ; xem / huỷ việc đã hẹn. Hỏi đủ giờ + nơi nhận + lời, nhắc lại, chờ gật.
chi-goi-khi-duoc-yeu-cau: true
---

# Giao việc — chủ nói, bot hẹn giờ

Chỉ chạy ở **agent admin** (chủ nhắn riêng). Tool là `automations` (tên cũ
`cron`) — code chỉ cấp cho chủ. Không thấy tool đó thì mình đang ở bot khách:
bảo chủ nhắn riêng.

Việc hẹn **còn sau khi máy khởi động lại** — OpenClaw lưu vào cơ sở dữ liệu.

## Ba loại việc

| Chủ nói | Làm |
|---|---|
| *“9h mai nhắc chị gọi lại chị Lan”* | Nhắc **chủ**: gửi `user:<senderId chủ>`, chạy bằng agent `admin` |
| *“Chiều thứ 6 nhắn chị Lan hỏi nhận hàng chưa”* | Nhắn **một khách** đã từng chat: gửi `user:<id khách>` (lấy từ phiếu `memory/phieu/`), chạy bằng agent `main` — để lời gửi đi theo đúng giọng và luật của bot khách |
| *“Sáng thứ 2 hàng tuần nhắn nhóm lớp lịch tuần này”* | Nhắn **nhóm**: gửi `group:<groupId>` — nhóm phải có trong `groups` của config. Chạy bằng `main` |

## Trước khi hẹn — đủ bốn thứ, rồi nhắc lại một câu

1. **Giờ — luôn giờ Việt Nam.** Tạo việc **luôn** kèm múi giờ
   `Asia/Ho_Chi_Minh`. Giờ không có múi giờ bị hiểu là **UTC** — *“9h sáng”*
   thành 16h chiều. Chủ nói mơ hồ (*“sáng mai”*, *“cuối tuần”*) → hỏi giờ cụ thể.
2. **Nơi nhận** — ai / nhóm nào. Tên khách không rõ ai → hỏi lại, đừng đoán
   giữa hai người cùng tên.
3. **Lời** — chủ đọc nguyên văn thì gửi nguyên văn. Chủ chỉ nói ý (*“hỏi nhận
   hàng chưa”*) → mình viết lời, **đọc cho chủ duyệt trước**.
4. **Một lần hay lặp** — lặp thì đến bao giờ dừng.

Rồi: *“Em hẹn: thứ 6 15h (giờ VN), nhắn chị Lan: ‘…’. Một lần. Ok chị?”* —
chờ gật. Im / đổi chủ đề không phải gật.

Hẹn xong đọc lại **giờ chạy kế tiếp** mà tool trả về. Lệch với giờ chủ nói →
xoá việc đó, làm lại. Đó là chỗ bắt lỗi múi giờ.

## Xem, sửa, huỷ

*“Em đang hẹn những gì?”* → liệt kê, mỗi việc một dòng: giờ chạy kế tiếp (giờ
VN), gửi ai, lời tóm một câu. *“Huỷ cái nhắn chị Lan”* → tìm đúng việc, đọc lại,
chờ gật, rồi huỷ.

## Không hẹn — kể cả chủ bảo

- **Nhắn hàng loạt khách** (*“nhắn hết khách tháng trước”*). Zalo khoá nick gửi
  hàng loạt — nick bot là tài sản của shop. Nói thẳng lý do, đề nghị đăng
  trong nhóm hoặc chọn vài người.
- **Nhắn người chưa từng chat với nick bot.** Không có phiếu = không có ID, và
  nhắn lạ là cách nhanh nhất bị báo cáo spam.
- **Lời có số không có trong sổ** (giá, ngày khai giảng) → sửa sổ trước
  (`day-bot`), rồi mới hẹn lời có số đó.
- **Lời hứa thay chủ** — nhận tiền, giữ suất, hoàn tiền.
- **Dày hơn một lần một ngày** cho cùng một khách.

## Chỗ hay vấp

- Hẹn bằng giờ không múi giờ → chạy lệch 7 tiếng. Đọc lại giờ chạy kế tiếp.
- Việc lặp không có ngày dừng → nhắn nhóm mãi sau khi khoá học đã xong.
- Nhắn khách bằng agent `admin` → lời đi ra mang giọng nói với chủ. Khách dùng `main`.

**Kiểm lại:** Có múi giờ `Asia/Ho_Chi_Minh` chưa? Giờ chạy kế tiếp tool trả về
có đúng giờ chủ nói không? Chủ đã gật đúng lời sẽ gửi chưa?
