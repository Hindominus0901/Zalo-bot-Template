---
name: doc-wiki
description: Lấy số shop từ tờ sổ — giá, ship, đổi trả, còn hàng. Không đẻ số, không đọc internal cho khách.
---

# Đọc wiki (tool `doc_wiki`)

Trước khi nói giá / ship / còn hàng / đổi trả / bảo hành / thanh toán: **đọc tờ
đúng việc** trong `knowledge/wiki/public/`. Danh tờ: `wiki/TRANG-MAU.md`.

1. Đoán tờ từ câu họ (`gia.md`, `ship.md`…). Không chắc → đọc `persona.md` rồi
   mở 1–2 tờ liên quan, đừng đổ cả kho.
2. Có số, không `[CHỜ CHỦ SHOP]` → nói **đúng số**, giọng `SOUL.md`.
3. Trống / chờ chủ / không có tờ → **không** “khoảng”, không suy gói B từ A.
   Ở lại chat, hỏi rõ món, hẹn người chốt. `ghi_thieu` + `bao_chu` nếu cần quyền.
4. Giá phụ thuộc tình huống: hỏi **một** câu rồi mới báo đúng khoảng trong wiki,
   đừng đổ cả bảng.
5. Xin giảm, xin tặng, hỏi khuyến mãi: **không tự quyết**. Nói thật là anh/chị
   phụ trách, rồi `ban-giao`.
6. Vừa nói **số wiki** (không phải “khoảng / để anh chị báo”): phiếu ghi
   `da_bao_gia_luc`. Im sau đó → heartbeat / `follow-up` nhánh im, nếu chủ đã bật.
7. `internal/` chỉ khi nick người nói = `USER.md`. Với khách: làm như ngăn đó
   không tồn tại.
8. Tờ có `updated` quá **90 ngày**: vẫn nói đúng số trên tờ — **không** tự dán
   `[CHỜ CHỦ SHOP]` đè lên, **không** nói với khách là số có thể cũ. Chỉ ghi thêm
   một dòng `viec_mo` vào `memory/YYYY-MM-DD.md` để chủ xác nhận lại.
9. File gốc `raw/` không gửi. Hội thoại mẫu không phải giá shop.

Kiến thức đời (phối, dùng hàng) không đi tool này — nói rồi **tách miệng** với
chính sách bên em.

Skill `bao-gia` = alias khi việc là **giá** — luật số vẫn ở đây.
