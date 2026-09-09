# Phỏng vấn chủ shop — 10 câu dễ, lấy đủ brain / wiki / harness

Bước **B2** trong [`HUONG-DAN-AGENT.md`](HUONG-DAN-AGENT.md).

Chủ shop **không cần biết** brain, wiki, harness, token, QR. Họ chỉ trả lời như
đang dặn nhân viên mới. Phần kỹ thuật (file nào, chỗ nào) chỉ dành cho bạn.

**Nói với họ:** từng câu một, chữ thường, ví dụ đời. **Không** đọc tên file,
không nói “điền wiki”, không hỏi OpenClaw.

**Lấy đủ:** miệng họ + file họ gửi. Thiếu thì `[CHỜ CHỦ SHOP]`. Không bịa giá.

| Câu | Họ thấy mình hỏi về | Bạn đang dựng |
|---|---|---|
| 1–2, 4, 10 | Shop, khách, giọng, câu chào | **Brain** — `persona.md` · `SOUL.md` · `IDENTITY.md` |
| 3, 6 | Đồ đang dùng để trả khách, câu còn thiếu | **Wiki** — `raw/` + `wiki/` |
| 5, 7–9 | Lúc nào gọi người, đơn đi sao, hỏi gì khi phân vân | **Harness** — rào, quy trình, skill khai thác, `USER.md` |

---

## Trước câu 1 — hai câu mở máy (không tính 10)

Nói như vậy, đừng nói Gateway:

> Mình làm trên máy tính anh/chị đang mở đó luôn nhé — Windows hay Mac ạ?
>
> Bot sẽ dùng một nick Zalo như nhân viên riêng, không dùng nick Zalo chính của
> anh/chị. Nick đó đã có chưa, hay lát mình tạo cùng nhau?

Chưa có nick → hẹn tạo trước khi “bật cho khách nhắn”. Chưa cần quét gì lúc này.

---

## 1. Shop mình làm gì?

**Nói:**

> Shop mình bán gì / làm gì ạ? Nói một câu như đang trả người lạ hỏi “bên mình
> làm gì thế”.

**Đào, vẫn chữ thường:**

- Khách hay hiểu nhầm điều gì về bên mình?
- Có hai món / hai gói hay bị lẫn không?
- Có câu nào anh/chị hay nói với khách, mình tin thật — kiểu có số hoặc có chuyện
  thật — kể nguyên giúp em.

→ Brain: công việc + quan điểm (`persona.md`).

---

## 2. Khách của mình, họ ngại gì?

**Nói:**

> Khách hay là ai ạ? Trước khi chốt, họ **ngại / sợ / phân vân** nhất chuyện gì?

**Đào** — câu này mỏng thì bot sẽ chào vô hồn. Hỏi tiếp:

- Lần gần nhất có người hỏi hơi lâu rồi không mua — họ vướng gì?
- Khách cũ nhắn lại thường khác khách mới chỗ nào?
- Họ hay gõ chữ, gửi ảnh, hay nhắn voice?

→ Brain: khách + nỗi lo (câu bot hỏi khi người ta còn mơ hồ).

---

## 3. Gửi em đồ đang dùng để trả khách

**Bắt buộc. Đây là lúc lấy wiki. Đừng bỏ, đừng hẹn “để sau”.**

**Nói:**

> Anh/chị gửi em **mọi thứ đang dùng để trả khách** — không cần soạn lại. Kéo
> file vào chat, chụp màn hình, hoặc dán link đều được.
>
> Ví dụ: bảng giá, menu, ảnh sản phẩm, file Excel, tin nhắn mẫu, cách ship, đổi
> trả, bảo hành, trang web, Drive, Notion. Có gì gửi nấy.

**Sau khi nhận, hỏi thêm bằng lời thường:**

- Cái nào **khách được biết**, cái nào chỉ mình xem (vốn, hoa hồng, cách xử khách
  khó)? Không chắc thì để riêng, đừng để bot nói.
- Cái nào **đã cũ**, sắp đổi?
- Còn nằm ở Zalo, máy kế toán, “cái bảng em hay forward” không?

**Cách làm (đừng đọc cho họ):** cất nguyên bản `knowledge/raw/`, ghi `raw/NGUON.md`,
tách trang theo `knowledge/CLAUDE.md`. Không tự bới giá trên mạng.

Họ nói không có file: “Không sao, lát em hỏi chậm hơn, anh/chị kể miệng.” Wiki sẽ
mỏng — nói thật, đừng đẻ số.

---

## 4. Trên Zalo mình xưng hô thế nào?

**Nói:**

> Lúc nhắn khách, anh/chị xưng *em* hay *mình*? Gọi người ta *anh/chị* hay *bạn*?
> Giọng Nam, Bắc, hay bình thường? Nick nhân viên trên Zalo đặt tên gì?
>
> Paste giúp **hai ba tin anh/chị đã trả khách** — nguyên văn luôn, để em bắt
> giọng, không phải để thuộc lòng nội dung.

**Đào:**

- Có chữ **không được nói** trong ngành không? (chê chỗ khác, hứa hết bệnh, hứa
  số liệu…)
- Khách hỏi “mày là bot hả” — anh/chị muốn trả thế nào? (Mặc định: nói thật,
  ngắn, rồi hỏi lại họ cần gì.)

→ Brain: `IDENTITY.md` + xưng hô / ví dụ cuối `SOUL.md`.

---

## 5. Việc gì không được tự ý, lúc nào gọi anh/chị?

**Nói:**

> Có việc gì nhân viên mới **không được tự ý nói / tự ý hứa** không ạ? Và lúc nào
> thì phải **kêu anh/chị vào**, đừng cố trả lời?

**Đào cho ra chuyện cụ thể** (đừng nhận “cái nhạy cảm thì chuyển”):

- Giá trên bảng — nói được chứ? Xin bớt, xin tặng thêm?
- Khách gửi ảnh chuyển khoản — **không** được bảo “đã nhận tiền”. Nhắc họ: bot
  chỉ ghi nhận, anh/chị đối soát.
- Hứa ngày giao, hứa kết quả, hợp đồng.
- Khách chê, bực, doạ kiện.
- Còn việc riêng nghề? (thuốc, tiền, trẻ nhỏ…)

→ Harness: rào shop. Ba rào sẵn (tiền, nội bộ, bị dụ) không hỏi, không gỡ.

---

## 6. Khách còn hay hỏi gì, trong đồ gửi chưa có?

**Nói:**

> Ngoài mấy file vừa gửi, khách **còn hay hỏi gì** — kể cả câu khó chịu, câu hỏi
> quanh co, gõ sai chính tả.

**Đào:**

- Kể vài câu **như khách hay gõ** (không dấu, viết tắt cũng được).
- Câu nào trong file đã có, câu nào **mình vẫn phải tự trả** — câu đó đáp thế nào?
- Có câu **cố ý không trả**, kêu anh/chị luôn không?

Câu 3 đã nhiều đồ thì câu 6 chỉ lấp lỗ. Câu 3 trống thì đây là FAQ bằng miệng.

→ Wiki.

---

## 7. Một đơn / một lịch thì đi như thế nào?

**Nói:**

> Khách nhắn xong tới lúc thành đơn (hoặc đặt lịch, thanh toán) — **đi những bước
> nào** ạ? Bước nào nhân viên mới làm được, bước nào **anh/chị phải chốt tay**?

**Đào:**

- Cần hỏi món, size, địa chỉ, ngày… — hỏi lần lượt hay hỏi một lúc?
- Còn hàng / còn chỗ — được nói chắc không, hay phải hỏi anh/chị?
- Khi nào được nói “xong rồi / đặt thành công”? (Mặc định: nhân viên mới chỉ
  **ghi nhận**, anh/chị xác nhận.)

→ Harness: quy trình + wiki bước mua.

---

## 8. Lúc không chắc — kêu ai, khách để số thì sao?

**Nói:**

> Có khách cần anh/chị vào, thì **kêu ai**? Tên, nick Zalo luôn.
>
> Khách cho số điện thoại thì mình **xem / lưu** thế nào? Ảnh họ gửi (chuyển
> khoản, hàng, size) — xem giúp được hay chuyển luôn cho anh/chị?

**Đào:**

- Hẹn gọi lại thì nói được **giờ nào**? (kiểu 9h–18h, không “giờ hành chính”.)
- Có nhóm riêng để báo “có khách chờ” không?
- Nhắn lại sau vài ngày: bản này **chưa làm** — cần thì ghi, đừng hứa có.

→ Harness: `USER.md`. Không bịa id kỹ thuật.

---

## 9. Khách không biết lấy gì — mình hay hỏi gì?

**Nói:**

> Khách bảo “không biết lấy gì”, “cái nào hợp” — **anh/chị thường hỏi họ những
> gì** trước khi gợi ý? Tầm hai ba câu thôi, câu nào hỏi trước.

**Đào** theo nghề họ vừa kể (đừng đọc chữ slot): tặng ai, ngân sách, size, ngày
cần, đã dùng loại nào thấy vướng gì…

- Câu nào **phải hỏi**, câu nào hỏi nếu chưa rõ.
- Có việc phải hỏi **đúng thứ tự** không (ví dụ đo size rồi mới ra món)?
- Việc gì làm xong phải **anh/chị xem đã** rồi mới trả khách?

→ Harness: bổ sung `skills/khai-thac/SKILL.md`, không giảng máy trạng thái cho họ.

---

## 10. Khách gõ “alo” — câu đầu muốn thấy gì?

**Nói:**

> Khách vào gõ *alo*, *shop ơi*, hoặc thả sticker — anh/chị muốn câu đầu **nghe
> như thế nào**? Viết giúp một câu **đúng kiểu mình đang nhắn**, đừng câu mẫu
> trên mạng.

**Đào:**

- Cuối tin đó, gợi ý họ trả lời kiểu gì cho dễ? (xem giá / để mình hỏi vài câu /
  gặp người…) — nói như câu khách gõ được.
- Một kiểu chào quanh năm, hay đổi theo buổi / theo chương trình?

→ Brain: tin mở. Không thay bằng “em có thể hỗ trợ gì ạ”.

---

## Xong 10 câu

Bạn (không đọc cho họ): raw còn nguyên; wiki tách từ raw + miệng; đóng vai trả
5 câu khách hay hỏi. Còn `[CHỜ CHỦ SHOP]` thì hỏi lại **bằng lời thường**, không
bảo họ “điền persona”.

## Bẫy

- **Hỏi như đang setup phần mềm.** Họ cụt hứng, trả lời cho có.
- **Hỏi xong không đào.** Câu 2 và 3 mỏng = bot vừa vô hồn vừa thiếu đồ.
- **Nhận file rồi hỏi lại cả bảng giá.** Đọc file, chỉ hỏi chỗ thiếu.
- **Tự vào web shop** khi họ chưa gửi. Web cũng phải họ chỉ.
