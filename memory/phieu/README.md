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

## Trần

**1800 ký tự một phiếu.** Tiêu đề mang sức chứa: `# Phiếu 123   [62% — 1.116/1.800]`.

Đầy thì bot **gộp dòng trùng ý** rồi ghi tiếp — không cắt cụt, không im lặng bỏ
dòng mới. Luật gộp và thứ tự hy sinh: `skills/phieu/SKILL.md`.

Phiếu phình quá 1800 mà gộp không xuống là dấu hiệu bot đang ghi chuyện vặt vào
phiếu. Fact bền mới ghi.

## Khi nào đọc

Mọi tin sau của cùng ID. Nhóm: file `{groupId}-{senderId}` chỉ khi có việc shop
(đặt, size) — không lập hồ sơ tán nhóm.
