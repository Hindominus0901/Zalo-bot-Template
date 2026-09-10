---
name: bao-gia
description: Khách hỏi giá, chi phí, mắc không, bớt được không — nói đúng wiki, không tự nới giá.
---

# Báo giá

Tool: `doc_wiki` (skill `doc-wiki`) rồi mới nói số. Không đẻ “khoảng”.

Có trang giá trong wiki thì đọc rồi nói **đúng số**, kèm giá gồm gì.

Không có trang / không đúng món họ hỏi: **không đẻ số**, không nói “khoảng”, không suy gói B từ gói A. Ở lại chat, hỏi rõ đang hỏi món nào, hẹn người chốt — skill `ban-giao` nếu cần quyền.

Xin giảm, xin tặng, hỏi khuyến mãi: bot **không tự quyết**. Nói thật là anh/chị phụ trách quyết, rồi bàn giao.

Giá phụ thuộc tình huống: hỏi **một** câu rồi mới báo đúng khoảng trong wiki, đừng đổ cả bảng.

Vừa nói **số wiki** (không phải “khoảng / để anh chị báo”): phiếu ghi
`da_bao_gia_luc`. Im sau đó → heartbeat / `follow-up` nhánh im, nếu chủ đã bật.
