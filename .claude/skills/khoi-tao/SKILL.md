---
name: khoi-tao
description: Dựng bot CSKH Zalo cho một shop từ template. Dùng khi người dùng bảo dựng bot, setup, phỏng vấn chủ shop, làm Nami, khởi tạo workspace.
---

# Khởi tạo — dựng bot cho một shop

Làm theo **[`dung-bot/QUY-TRINH.md`](../../../dung-bot/QUY-TRINH.md)** — B0→B7.
Đó là nguồn duy nhất; file này chỉ để Claude Code tìm ra nó.

Bốn thứ đừng quên, kể cả khi đọc lướt quy trình:

1. **Không bịa số shop.** Chưa có thì `[CHỜ CHỦ SHOP: …]` rồi hỏi. Không "giá
   tham khảo", không copy số từ `docs/vi-du-file-da-dien.md` (shop giả).
2. **Không nói** wiki, harness, token, QR, OpenClaw, Gateway với chủ shop. Nói:
   sổ, nick nhân viên, quét mã, chỗ bot ngồi. Cách nói: skill `giao-tiep-chu`.
3. **Chưa có mã kết nối AI → dừng ở B0.** Dựng xong mà bot không nói được câu
   nào thì chủ shop nghĩ mình làm hỏng.
4. **Đừng sửa** `AGENTS.md`, `TOOLS.md`, `skills/*/SKILL.md` trừ khi chủ đổi
   việc thật (câu 7/9). Đừng viết lại giọng nền thành kịch bản tổng đài.

Chủ shop muốn tự xem: `docs/08-luong-chu-shop.md`. Đã khóa, đừng hỏi lại:
`docs/quyet-dinh.md`.
