# Phiếu khách — theo ID, không phải CRM

Mỗi người (inbox) một file. Bot **đọc đầu lượt, ghi cuối lượt** nếu có fact bền.
Khách không bao giờ được nghe nội dung file này.

ID: Zalo `senderId` (số). Tên file = đúng ID, không dấu, không `/`.

Git ignore hết `memory/phieu/*` trừ README + mẫu — tránh đẩy SĐT/ảnh khách lên GitHub.

## Khi nào tạo

Lần đầu biết một fact bền (size, món đang hỏi, ảnh thấy món X, đang tặng ai).
Đừng tạo phiếu lúc *alo*.

Trạng thái đơn / giờ báo giá / cờ follow-up: xem `MAU.md` + skill `follow-up`.
Ảnh CK không biến phiếu thành đã có đơn.

## Khi nào đọc

Mọi tin sau của cùng ID. Nhóm: file `{groupId}-{senderId}` chỉ khi có việc shop
(đặt, size) — không lập hồ sơ tán nhóm.
