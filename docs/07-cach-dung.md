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

Muốn đổi tên nhân viên: nói tên mới — người dựng sửa `IDENTITY.md` + config cho khớp.

## Người dựng (coding agent / freelancer)

Skill `.claude/skills/khoi-tao` + `HUONG-DAN-AGENT.md` B0→B7. Phỏng vấn
`PHONG-VAN.md`. Đừng bịa wiki. Đừng viết lại `giong-noi.md` thành kịch bản OA.
Bot chat: `knowledge/system-prompt.md` + `TOOLS.md` + `skills/`.

Xong bước kỹ thuật: `docs/05-thiet-lap.md`. Kiểm: `tests/` + `04-kich-ban-thu.md`.

Phiếu: bot tự ghi. Đừng mở CRM. Đừng commit `memory/phieu/` thật.

## Người trực / chủ lúc bot đã chạy

`USER.md` = nick được đọc `internal/` và nhận bàn giao. BOOT không nhắn khách.
Heartbeat báo thiếu wiki về nick này; nhắn khách **chỉ** khi anh/chị đã bật
follow-up trong `USER.md` (im sau giá / sau đơn — một tin mỗi nhánh). Chưa điền
= tắt.

Sửa giá: sửa **trang wiki**, không nhắn “Nami ơi từ giờ giá X” rồi quên file
(nói miệng thì bot có thể nhớ phiếu, wiki mới là số lần sau).
