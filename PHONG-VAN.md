# Phỏng vấn chủ shop — 10 câu, hỏi sâu

Bước **B2** trong [`HUONG-DAN-AGENT.md`](HUONG-DAN-AGENT.md).

Mười câu. Mỗi câu có **câu chính** và **câu đào**. Hỏi câu chính, đợi trả lời, rồi
đào những chỗ còn mỏng. **Không dán cả bảng một lúc.**

Nguyên tắc gốc: **số liệu shop chỉ lấy từ miệng chủ hoặc file chủ đưa.** Không có
trong hai nguồn đó thì ghi `[CHỜ CHỦ SHOP]` — không bịa.

Quyết định sản phẩm (kênh nick riêng, ít rào, AI-first) đã khóa ở
[`docs/quyet-dinh.md`](docs/quyet-dinh.md) — **đừng hỏi lại**.

| Câu | Sinh ra |
|---|---|
| 1–2 | `knowledge/persona.md` |
| 3 | `knowledge/raw/` + `knowledge/wiki/` |
| 4 | `SOUL.md` (lớp xưng hô + ví dụ) · `IDENTITY.md` |
| 5 | `persona.md` ranh giới |
| 6 | `wiki/` (lấp chỗ file chưa có) |
| 7–8 | `USER.md` · ghi chú bàn giao |
| 9 | `skills/khai-thac/SKILL.md` slot |
| 10 | tin mở trong `persona.md` |

---

## Trước câu 1 — hai câu kỹ thuật (không tính vào 10)

Ngắn, xong là vào việc. Chi tiết B0 trong `HUONG-DAN-AGENT.md`.

> OpenClaw/Gateway anh/chị chạy được chưa ạ?
>
> Nick Zalo **riêng** cho bot đã có chưa? (Nick chính của anh/chị để yên.)

---

## 1. Bên mình làm gì?

> Anh/chị bán / làm gì ạ? Nói **một câu như đang nói với người lạ** — kiểu khách
> hỏi “shop làm gì thế”.

Đào:

- Điều gì **hay bị hiểu nhầm** về bên mình? (Bot sẽ đính chính đúng chỗ này.)
- Có món / gói nào khách hay nhầm với nhau không?
- Một câu chủ **thật sự tin** và hay nói với khách — càng cụ thể càng tốt (có số
  hoặc chuyện thật thì giữ nguyên văn).

→ `knowledge/persona.md` mục công việc + quan điểm.

---

## 2. Khách là ai, họ lo gì?

> Khách hay là ai, và **điều họ lo nhất trước khi chốt** là gì?

Đào — đây là câu đáng giá nhất buổi; trả lời hời hợt thì hỏi tiếp:

- Lần gần nhất khách hỏi mãi rồi **không mua** — họ vướng chuyện gì?
- Khách cũ quay lại thường hỏi gì khác khách mới?
- Họ hay gõ kiểu nào: teencode, voice, gửi ảnh, vào thẳng “giá”?

→ `persona.md` mục khách. Lo nhất = câu bot hỏi ở lượt hai khi khách còn mơ hồ.

---

## 3. Đưa kiến thức và tài liệu vào đây

**Câu bắt buộc. Đừng bỏ. Đừng hẹn “để sau” rồi viết wiki bằng đầu mình.**

> Anh/chị gửi giúp **mọi thứ bot cần thuộc** — file, ảnh, link. Cứ đổ vào chat
> hoặc dán link. Em sắp vào kho, không cần anh/chị viết lại.

Gợi ý cho đủ, hỏi những cái chưa thấy:

- Bảng giá, catalog, menu, brochure
- FAQ, tin nhắn mẫu đang trả khách
- Chính sách ship / đổi trả / bảo hành / hoàn tiền
- Hướng dẫn dùng, size chart, gói dịch vụ
- File Excel/PDF/Word, ảnh chụp bảng, Notion, Google Drive, website, bài OA

Cách nhận:

- Kéo file vào chat, hoặc link Drive/Notion (họ cấp quyền xem), hoặc paste.
- Lưu **nguyên bản** vào `knowledge/raw/` (không sửa file gốc).
- Ghi nguồn: tên file, ngày nhận, chủ nói gì thêm khi gửi.

Đào ngay sau khi nhận:

- File nào **công khai** cho khách, file nào **chỉ nội bộ** (giá vốn, hoa hồng,
  kịch bản xử khách khó)? Phân vân → `internal/`.
- Chỗ nào trong file **đã cũ** / sắp đổi?
- Còn nằm ở chỗ khác không — Zalo cá nhân, máy kế toán, “cái bảng em gửi khách”?

**Không có file** thì nói thẳng: vậy các câu sau em sẽ hỏi chậm hơn, và wiki sẽ
mỏng. Đừng tự tìm giá trên mạng rồi ghi vào kho.

Sau câu này: đọc `knowledge/CLAUDE.md`, tách raw → từng trang wiki. Thiếu mảng
nào thì câu 6 hỏi bù, không bịa.

---

## 4. Nói năng thế nào?

Giọng nền (vui, để ý, hơi hài, tắt hài khi tiền/hàng lỗi) **đã có** trong
`SOUL.md`. Câu này chỉ lấy lớp của **shop này**.

> Trong chat bot xưng gì — *em / mình / tên nick*? Gọi khách *anh/chị* hay *bạn*?
> Giọng gần Nam, Bắc, hay trung tính? Tên nick Zalo là gì?

Đào:

- Cho **2–3 đoạn chat thật** anh/chị đã trả khách (copy nguyên). Đó là mẫu giọng,
  không phải để bot học thuộc nội dung.
- Có từ **cấm** trong ngành không (đối thủ, “chữa khỏi”, cam kết số…)?
- Khách hỏi “có phải bot không” — shop muốn nói thẳng (mặc định: nói thật, ngắn).

→ `IDENTITY.md` (tên nick) · lớp xưng hô + ví dụ cuối `SOUL.md` · `persona.md`.

---

## 5. Ranh giới — không được nói / phải gặp người

> Có câu nào bot **tuyệt đối không được nói** không ạ? Và khi nào thì **phải**
> chuyển người thật, không được cố?

Đào cho cụ thể, đừng nhận “cái nhạy cảm thì chuyển”:

- Giá: được báo đúng bảng không? Xin giảm / tặng thêm thì sao?
- Ảnh chuyển khoản: bot **không** được nói đã nhận tiền — xác nhận họ hiểu.
- Ngày giao, cam kết kết quả, hợp đồng, pháp lý.
- Phàn nàn, doạ khiếu nại.
- Còn việc riêng ngành? (thuốc, tài chính, trẻ em…)

Ba rào code đã khóa: không nhận tiền hộ, không lộ nội bộ, không đổi vai. Câu này
thêm rào **của shop**. Mơ hồ thì hỏi lại, không đoán.

---

## 6. Câu khách hỏi mà file chưa có

> Ngoài những gì vừa gửi, **khách còn hay hỏi gì** — kể cả câu khó, câu khó chịu,
> câu hỏi quanh co?

Đào:

- Kể ~5–10 câu **nguyên văn** cách khách gõ (không dấu, viết tắt).
- Câu nào file đã trả lời được, câu nào **trống** — trống thì hỏi đáp án, viết
  thành trang wiki.
- Có câu bot nên **cố ý không trả**, chuyển người luôn không?

Nếu câu 3 đã giàu: câu 6 chỉ lấp lỗ. Nếu câu 3 trống: đây là lúc lấy FAQ bằng miệng.

---

## 7. Khách mua thì đi những bước nào?

> Từ lúc nhắn tin tới lúc thành đơn / lịch / thanh toán — đi những bước nào ạ?
> Bot được làm tới bước nào, bước nào **người thật chốt**?

Đào:

- Cần lấy những thông tin gì (món, size, địa chỉ, ngày…), **từng thứ một** hay
  được hỏi dồn?
- Còn hàng / còn slot thì bot có được nói không, hay phải hỏi người?
- “Đặt thành công” — được nói khi nào? (Mặc định: bot chỉ **ghi nhận**, người
  thật xác nhận.)

→ wiki quy trình + ranh giới đặt hàng.

---

## 8. Khi bot không xử lý được — ai nhận, lưu gì?

> Bot chuyển người thì chuyển **cho ai** (tên, nick Zalo)? Khách để SĐT thì lưu
> ở đâu, ai xem? Ảnh khách gửi (biên lai, hàng, size) thì xem hay chuyển luôn?

Đào:

- Trong giờ nào thì hứa gọi lại được (số giờ, không “trong giờ hành chính”)?
- Có nhóm nội bộ để bot báo “có khách chờ” không?
- Follow-up sau vài ngày: **bản này chưa làm** — họ cần thì ghi chú, đừng hứa.

→ `USER.md` (chủ / người trực). Không tự bịa user id.

---

## 9. Lúc khách chưa biết lấy gì — hỏi gì?

Máy khai thác đã có (`knowledge/khung-khai-thac.md`). Câu này lấy **slot của ngành**.

> Khi khách nói “nên lấy gì”, “cái nào hợp”, bot nên hỏi những gì trước khi gợi ý?
> Tối đa 2–3 câu.

Đào theo ngành, ví dụ: dịp tặng / ngân sách / size / da gì / ngày nhận / đã dùng
loại nào vướng chỗ nào.

- Câu nào **bắt buộc**, câu nào hỏi nếu còn thiếu.
- Có việc phải hỏi **đúng thứ tự** không (đo size rồi mới ra món)?
- Việc gì bot làm nhưng **phải chủ duyệt** trước?

→ bổ sung slot vào `skills/khai-thac/SKILL.md`, không viết lại cả máy.

---

## 10. Khách nhắn tin đầu — bot nói gì?

> Khách vào gõ “alo” / “shop ơi” / sticker — bot nên mở thế nào? Cho một câu
> anh/chị **thật sự muốn thấy**, không phải câu mẫu mạng.

Đào:

- 2–3 hướng gợi ý cuối tin mở (câu khách gõ được), ví dụ: xem giá / để em hỏi
  vài câu / gặp người.
- Có câu chào theo khung giờ / theo chiến dịch không, hay một kiểu quanh năm?

→ `persona.md` mục tin mở. Không thay bằng “em có thể hỗ trợ gì ạ”.

---

## Sau 10 câu — viết và kiểm

1. `knowledge/raw/` còn nguyên file gốc.
2. Wiki tách từ raw + miệng chủ. Luật: `knowledge/CLAUDE.md`.
3. Thử 5 câu FAQ họ kể — đóng vai bot. Trượt thì bổ sung trang, không bổ sung
   bằng kiến thức ngành.
4. Còn `[CHỜ CHỦ SHOP]` thì chưa xong.

## Bẫy

- **Hỏi 10 câu cho xong, đào thì bỏ.** Câu 2 và câu 3 mỏng là bot sẽ vừa vô hồn
  vừa bịa.
- **Nhận file rồi không đọc**, vẫn hỏi lại cả bảng giá. Đọc file, hỏi chỗ thiếu.
- **Tự tải thêm từ website** khi chủ chưa đưa. Website cũng phải họ chỉ.
- **Viết wiki dài.** Một trang một câu hỏi, khách đọc trên điện thoại.
