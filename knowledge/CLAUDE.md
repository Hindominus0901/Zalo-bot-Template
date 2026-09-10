# Luật kho tri thức

Giải thích chữ thường cho chủ shop: [`docs/09-kho-va-du-lieu.md`](../docs/09-kho-va-du-lieu.md).
Luồng dựng bot (họ đọc): [`docs/08-luong-chu-shop.md`](../docs/08-luong-chu-shop.md).

Bot trả lời số liệu shop từ đây, không từ kiến thức chung trên mạng.

```
knowledge/
├─ CLAUDE.md          ← file này
├─ persona.md         ← shop này là ai, ranh giới (điền lúc phỏng vấn)
├─ raw/               ← file gốc chủ gửi. Không sửa. Không đưa raw cho khách.
└─ wiki/
   ├─ public/         ← khách được nghe
   └─ internal/       ← chỉ chủ / nhân viên; bot không nhắc sự tồn tại
```

Không có vector DB. Trang Markdown, liên kết `[[ten-trang]]`. Tên file: chữ thường,
không dấu, gạch ngang.

---

## Nhận tài liệu (câu 3 phỏng vấn)

1. Cất nguyên bản vào `raw/`, tên file giữ được nguồn (`bang-gia-2026-04.pdf`).
2. Thêm một dòng `raw/NGUON.md`: ngày nhận, ai gửi, file nào công khai / nội bộ.
3. Đọc hết. Tách thành **nhiều trang nhỏ** — mỗi trang một câu khách hay hỏi.
4. Số liệu chỉ lấy từ file hoặc miệng chủ. File im, miệng chưa nói → `[CHỜ CHỦ SHOP]`.
5. Giá / hoa hồng / giá vốn / kịch bản khách khó: `internal/` nếu phân vân.
6. Template đã có tờ chờ trong `wiki/public/` và `wiki/internal/` (xem
   `wiki/TRANG-MAU.md`). Điền số vào tờ đúng việc. Có số thì xóa banner
   `[CHỜ CHỦ SHOP]`. Đừng tạo thêm tờ trống. Đừng copy số shop giả.

Ảnh menu, screenshot Zalo: để `raw/`, đọc chữ trong ảnh rồi viết wiki; đừng bảo
khách “xem file đính kèm” nếu nick không gửi file ổn định.

---

## Một trang wiki

```markdown
---
title: Phí ship nội thành
summary: Nội thành 30k, 2 giờ; ngoại tỉnh bot không tự chốt phí.
updated: 2026-09-09
sources: [raw/bang-gia-2026-04.pdf]
---

# Phí ship nội thành

Nội dung ngắn, đúng chữ chính sách.

Liên quan: [[doi-tra]]
```

`summary` viết như đang mô tả cho người chưa mở trang. Trang > ~1400 ký tự thì tách.

`updated` là ngày số trên trang được chốt, không phải ngày sửa chữ. Quá **90 ngày**
thì trang vẫn dùng được — bot vẫn trả đúng số đó — nhưng bot ghi một dòng cho chủ
xác nhận lại. Không có cơ chế nào tự vô hiệu một trang: số cũ còn hơn không có số.

---

## Bot dùng kho thế nào

- Có trong wiki → nói đúng wiki, giọng `SOUL.md`.
- Không có → không đẻ số. Ở lại chat, hỏi rõ, hẹn chốt / bàn giao phần số.
  Ghi câu khách vào báo cáo thiếu trang (nếu workspace có `memory/`).
- Kiến thức chung (phối đồ, giải thích loại hàng) được nói, **tách miệng** với
  chính sách bên em.
