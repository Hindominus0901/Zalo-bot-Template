# Cách dùng — ba người, ba việc

Chủ shop **chưa từng dựng bot:** đọc [`08-luong-chu-shop.md`](08-luong-chu-shop.md)
(từng bước) và [`09-kho-va-du-lieu.md`](09-kho-va-du-lieu.md) (sổ / dữ liệu).
File này là việc ngày thường sau khi nick đã sống.

Template không tự chạy khi clone. Cần nick + chỗ bot ngồi. Thiết lập kỹ thuật:
[`05-thiet-lap.md`](05-thiet-lap.md).

---

## Chủ shop (không cần biết OpenClaw)

Nhắn với người dựng bot như đang nói chuyện. Trả lời từng câu phỏng vấn, gửi
bảng giá / ảnh / file. Không cần tạo OA.

Sau khi nick sống: xem tin Nami; chỗ tiền / khiếu nại thì **vào tay**. Ngoài giờ
Nami vẫn trả giá/ship nếu đã ghi; không hứa gọi ngay.

Muốn đổi giá, đổi câu trả lời, thêm luật, hẹn bot nhắc việc: **nhắn riêng cho
bot** như nhắn nhân viên (mục *Người trực* dưới). Đổi tên nhân viên thì nói
người dựng — tên phải đổi cùng lúc ở hai chỗ.

## Người dựng (coding agent / freelancer)

[`../dung-bot/QUY-TRINH.md`](../dung-bot/QUY-TRINH.md) + `HUONG-DAN-AGENT.md`. Phỏng vấn `PHONG-VAN.md`.
Đừng bịa wiki. Bot chat: `AGENTS.md` + `TOOLS.md` + `skills/`.

Xong bước kỹ thuật: `docs/05-thiet-lap.md`. `tests/` = kho chữ; nick:
`04-kich-ban-thu.md`.

Phiếu: bot tự ghi. Đừng mở CRM. Đừng commit `memory/phieu/` thật.

## Người trực / chủ lúc bot đã chạy

`USER.md` = nick được đọc `internal/` và nhận bàn giao. BOOT không nhắn khách.
Heartbeat báo thiếu wiki về nick này; nhắn khách **chỉ** khi anh/chị đã bật
follow-up trong `USER.md` (im sau giá / sau đơn — một tin mỗi nhánh). Chưa điền
= tắt.

**Sửa giá, dạy bot, giao việc: nhắn RIÊNG cho nick bot** — *“từ giờ gói A là
2 triệu nha em”*, *“9h mai nhắc chị gọi chị Lan”*. Bot nhắc lại, chờ chị gật,
rồi tự sửa sổ / tự hẹn giờ. Đủ cách nói và bot sẽ từ chối gì:
[`16-day-bot.md`](16-day-bot.md).

Trong **nhóm** thì nói vậy bot không sửa — nhóm có khách đọc chung. Và chỉ nick
chủ đã khai lúc dựng mới dạy được; người khác tự xưng là chủ cũng không.
