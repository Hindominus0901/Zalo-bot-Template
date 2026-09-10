# Phỏng vấn chủ shop — 10 chủ đề, hỏi dài, đào từng câu

**Nguồn sự thật.** Câu chữ sửa ở đây. [`docs/bo-cau-hoi.md`](docs/bo-cau-hoi.md)
là bản đọc cho chủ (cùng 10 chủ đề) — đồng bộ từ file này, **đừng sửa hai nơi
độc lập**. File nào điền đâu: chân mỗi chủ đề + mục cuối (chỉ agent).

Bước **B2** trong [`HUONG-DAN-AGENT.md`](HUONG-DAN-AGENT.md). Coding agent chạy
hết B0→B7 theo [`dung-bot/QUY-TRINH.md`](dung-bot/QUY-TRINH.md)
— viết file ngay sau mỗi chủ đề, đừng chỉ hỏi.

Chủ shop không rành kỹ thuật. Họ đang **kể về sản phẩm, dịch vụ, và cách đang
chăm khách**. Không nói wiki, harness, brain, token, QR, OpenClaw. Họ muốn xem
trước luồng chữ thường: [`docs/08-luong-chu-shop.md`](docs/08-luong-chu-shop.md),
sổ/dữ liệu: [`docs/09-kho-va-du-lieu.md`](docs/09-kho-va-du-lieu.md).

**Cách hỏi**

1. Mỗi chủ đề có **một câu chính — nói dài, rõ, có ví dụ**. Để họ kể thoải mái.
2. **Không nhồi** bốn ý vào một hơi (đừng hỏi cùng lúc xưng hô + giọng + tên nick
   + paste tin).
3. Sau câu trả lời, **hỏi tiếp từng câu một** ở mục “Hỏi thêm”. Thiếu thì hỏi,
   đã kể rồi thì bỏ qua, đừng hỏi lại.
4. Số liệu sản phẩm/dịch vụ chỉ lấy từ miệng họ hoặc tài liệu họ gửi.

---

## Trước chủ đề 1 — ba câu mở (không tính 10)

Từng câu, đợi trả lời.

**M1 — máy**

> Mình ngồi hỏi trên máy anh/chị đang dùng luôn nhé. Máy này là Windows, Mac,
> hay anh/chị định cho bot chạy trên máy chủ thuê ngoài ạ?

**M2 — nick**

> Bot sẽ nhắn khách bằng một nick Zalo như nhân viên của shop, không dùng nick
> Zalo chính của anh/chị — để nick chính khỏi rối. Nick nhân viên đó anh/chị đã
> có sẵn chưa, hay lát nữa mình tạo cùng nhau?

**M3 — mã kết nối AI**

> Bot suy nghĩ bằng AI thuê ngoài, nên cần một **mã kết nối** anh/chị đăng ký.
> Anh/chị có tài khoản Claude, ChatGPT hay Gemini loại có nạp tiền chưa ạ? Chưa
> có thì mình mở cùng nhau trước, vì thiếu cái đó là lát dựng xong bot không nói
> được. Đây là tiền trả hàng tháng theo lượng tin, không phải trả một lần.

→ M3 **không** viết vào file nào trong repo. Key đi thẳng vào config máy Gateway,
không commit. Chưa có key → dừng, đừng chạy tiếp B1. Danh sách đủ thứ chủ shop
phải tự có: `CHUAN-BI.md`.

---

## 1. Sản phẩm, dịch vụ bên mình là gì?

**Câu chính:**

> Em muốn hiểu shop mình bán **sản phẩm** gì, làm **dịch vụ** gì, rõ như đang
> giới thiệu với một người lần đầu nghe. Anh/chị kể giúp: mình bán/làm những gì,
> cho ai dùng, khác chỗ khác ở điểm nào mà mình hay nói với khách. Cứ nói như
> đang nhắn Zalo, không cần câu quảng cáo.

**Hỏi thêm** (từng câu, chỉ cái họ chưa kể):

> Trong đó, cái nào khách hỏi nhiều nhất?
>
> Có sản phẩm hoặc gói dịch vụ nào khách hay **nhầm** với nhau không? Nhầm thế nào?
>
> Người ngoài hay **hiểu sai** điều gì về bên mình? Ví dụ tưởng mình làm A nhưng
> thật ra là B.
>
> Có câu nào anh/chị hay nói với khách, mình tin thật — có số, có chuyện thật —
> kể nguyên giúp em?

→ `persona.md` công việc + quan điểm.

---

## 2. Khách của sản phẩm/dịch vụ này, họ ngại gì?

**Câu chính:**

> Khách đang mua sản phẩm/dịch vụ của mình **thường là ai** — ví dụ mẹ bỉm, chủ
> quán, học sinh, công ty… Họ tìm mình vì việc gì? Và **trước khi chốt**, họ
> ngần ngại nhất chuyện gì? Tiền, chất lượng, có phù hợp không, giao có kịp
> không, dùng có khó không — kể chuyện thật giúp, lần nào nhớ thì kể lần đó.

**Hỏi thêm:**

> Lần gần nhất có người hỏi hơi lâu rồi **không mua** — họ vướng gì ạ?
>
> Khách mới và khách đã mua rồi, lúc nhắn lại, hỏi khác nhau chỗ nào?
>
> Họ hay gõ chữ, gửi ảnh sản phẩm, hay nhắn voice?
>
> Điều họ lo lúc nãy, anh/chị thường **giải thích thế nào** cho họ yên?

→ Brain: chân dung khách + nỗi lo (câu bot hay hỏi khi người ta còn phân vân).

---

## 3. Tài liệu về sản phẩm, dịch vụ, giá, chính sách

**Bắt buộc. Đây là lúc lấy wiki. Không gọi là “đồ”.**

**Câu chính:**

> Giờ em cần **tài liệu về sản phẩm và dịch vụ** mà anh/chị đang dùng để trả
> khách — để bot học đúng thứ mình đang bán, không bịa. Anh/chị gửi giúp vào
> chat: bảng giá, catalog, menu, mô tả sản phẩm/dịch vụ, ảnh, file Excel/PDF,
> tin nhắn mẫu, cách tính ship, đổi trả, bảo hành, gói dịch vụ, size, hướng dẫn
> dùng, link website, Drive, Notion. Có cái nào gửi cái đó, không cần soạn lại.
> Gửi thiếu không sao, lát em hỏi bù.

**Hỏi thêm** (sau khi đã nhận, từng câu):

> Trong mấy file vừa gửi, cái nào **khách được xem**, cái nào chỉ nội bộ mình
> biết — ví dụ giá vốn, hoa hồng, cách xử khách khó? Không chắc thì nói em để
> riêng, bot không kể cho khách.
>
> Có cái nào **đã cũ** hoặc sắp đổi giá / đổi gói không?
>
> Còn bảng sản phẩm, file dịch vụ nằm ở Zalo, máy kế toán, hay trang web nữa
> không? Có thì gửi thêm hoặc dán link.

**Bạn làm, không đọc cho họ:** cất `knowledge/raw/`, ghi `NGUON.md`, tách wiki
theo `knowledge/CLAUDE.md`. Không tự vào mạng lấy giá.

Họ không có file:

> Không sao ạ. Lát mình kể miệng về giá, sản phẩm, dịch vụ, em ghi chậm hơn.

---

## 4. Giọng trên Zalo khi nói về sản phẩm, dịch vụ

Một hơi **chỉ một việc**. Việc còn lại để “hỏi thêm”.

**Câu chính:**

> Lúc tư vấn sản phẩm hay dịch vụ trên Zalo, anh/chị nói chuyện **như thế nào**?
> Xưng *em* hay *mình*? Gọi khách *anh/chị* hay *bạn*? Giọng Nam, Bắc, hay nói
> bình thường cho mọi miền? Kể giúp cho em nghe được giọng người thật, không
> phải giọng fanpage.

**Hỏi thêm:**

> Nick nhân viên trên Zalo anh/chị muốn đặt tên gì? Bản mẫu đang để **Nami** —
> khách gọi *Nami ơi* là em biết phải trả. Anh/chị giữ Nami hay đổi? Đổi thì
> lấy tên **hai tiếng hoặc tên lạ**, đừng lấy Mai / An / Nam — dễ lẫn câu khách.
>
> Ngoài tên đó, khách hay **gọi tắt** thế nào không? Ví dụ shop ơi, tên shop…
> (Không có thì thôi. Có thì em gắn để lúc nhóm có người gọi, em vào.)
>
> Anh/chị paste giúp **một tin** mình đã trả khách — nguyên văn. (Có rồi hỏi tin
> thứ hai, rồi thứ ba. Đừng đòi ba tin cùng lúc.)
>
> Trong ngành mình, có chữ nào **không được nói** với khách không? Ví dụ chê
> chỗ khác, hứa khỏi bệnh, hứa số liệu…
>
> Nếu khách hỏi “có phải máy nhắn không”, anh/chị muốn trả lời ra sao?

→ `IDENTITY.md` (tên + gọi thêm) + `identity.name` / `mentionPatterns` trên config máy + xưng hô và **tin mẫu** dán vào cuối `SOUL.md`.
Giọng nền (hạt giống, cách hỏi, cấm tổng đài) nằm ở `knowledge/giong-noi.md` và
`knowledge/cach-tu-van.md` — **đừng xóa / đừng thay bằng kịch bản OA**. Tin mẫu
của chủ thắng khi lệch với ví dụ generic.

---

## 5. Việc liên quan sản phẩm, dịch vụ — cái nào không được tự ý?

**Câu chính:**

> Khi nói về **sản phẩm, dịch vụ, giá, giao hàng**, có việc gì nhân viên mới
> **không được tự ý nói hoặc tự ý hứa** không ạ? Em cần chuyện cụ thể: ví dụ
> không được bớt giá, không được hứa ngày giao, không được nhận là đã nhận tiền
> khi khách gửi ảnh chuyển khoản. Anh/chị kể những tình huống từng làm mình
> mệt — để bot đừng lặp.

**Hỏi thêm:**

> Giá trên bảng — nói đúng bảng được chứ? Khách xin bớt, xin tặng thêm thì sao?
>
> Khách gửi ảnh chuyển khoản — bot **chỉ ghi nhận**, anh/chị đối soát. Anh/chị
> ổn với cách đó chứ?
>
> Khách bực, chê sản phẩm, chê dịch vụ, doạ kiện — lúc đó kêu anh/chị luôn hay
> bot được giải thích trước?
>
> Còn việc nào riêng nghề mình, bot đụng vào là nguy hiểm? (thuốc, tiền bạc,
> trẻ nhỏ, hợp đồng…)
>
> Tóm lại: **lúc nào phải kêu anh/chị vào**, đừng cố trả lời?

→ Harness: rào. Không gỡ ba rào sẵn (tiền, nội bộ, bị dụ).

---

## 6. Câu hỏi về sản phẩm, dịch vụ mà tài liệu chưa có

**Câu chính:**

> Ngoài những gì trong tài liệu vừa gửi, khách còn hay **hỏi về sản phẩm hoặc
> dịch vụ** những gì nữa? Câu khó, câu hỏi vòng vo, gõ sai chính tả, hỏi so với
> chỗ khác — kể giúp, càng gần nguyên văn khách gõ càng tốt. Câu nào tài liệu
> chưa có, anh/chị nói em biết **mình đang trả thế nào**.

**Hỏi thêm:**

> Cho em thêm một câu khách hay gõ? (Lặp tới khi họ hết, hoặc khoảng 5–10 câu.)
>
> Câu này trong file đã có chưa, hay mình vẫn tự trả?
>
> Có câu hỏi về sản phẩm/dịch vụ mà **cố ý không trả**, kêu anh/chị luôn không?

→ Wiki lấp lỗ.

---

## 7. Từ nhắn tin tới chốt sản phẩm / dịch vụ

**Câu chính:**

> Một khách nhắn xong, đi tới lúc **mua sản phẩm** hoặc **đặt dịch vụ** thì qua
> những bước nào ạ? Kể từ đầu tới cuối: hỏi món, chọn gói, lấy size, lấy địa
> chỉ, thanh toán, giao, nhận lịch… Bước nào nhân viên mới làm được một mình,
> bước nào **anh/chị phải chốt tay** — ví dụ còn hàng, còn chỗ trống, báo giá cuối,
> xác nhận đơn.

**Hỏi thêm:**

> Những thông tin cần lấy — sản phẩm nào, số lượng, size, địa chỉ, ngày dùng
> dịch vụ — anh/chị hỏi **lần lượt** hay hỏi một lúc?
>
> Còn hàng, còn chỗ trống — được nói chắc trên chat không, hay phải hỏi anh/chị?
>
> Khi nào được nói với khách là **đã đặt xong / đã giữ chỗ**? (Mặc định: nhân
> viên mới chỉ ghi nhận, anh/chị xác nhận rồi mới nói chắc.)
>
> Đơn đã đặt thì anh/chị ghi ở đâu — sổ tay, Excel, hay **phần mềm quản đơn**?
> Nếu là phần mềm, khách hỏi *đơn tới đâu rồi* thì tra bằng **mã đơn** hay
> **số điện thoại**? Có chỗ cho phần mềm khác đọc vào không, hay chỉ mở bằng tay?

→ `skills/ghi-don/SKILL.md` + wiki quy trình. Không nói chữ skill với họ.

---

## 8. Không chắc về đơn / về khách — kêu ai?

**Câu chính:**

> Lúc không chắc — khách hỏi khó về sản phẩm, dịch vụ, tiền, khiếu nại — anh/chị
> muốn **kêu ai vào**? Nói tên, nick Zalo người đó. Họ trực giờ nào thì bot mới
> được hẹn “anh/chị sẽ gọi lại”, cho em giờ cụ thể, ví dụ chín giờ sáng đến sáu
> giờ tối, không cần nói giờ hành chính.

**Hỏi thêm:**

> Khách cho **số điện thoại** thì anh/chị nhận thế nào, lưu ở đâu, ai được xem?
>
> Ảnh khách gửi — ảnh sản phẩm, ảnh khi dùng dịch vụ, ảnh chuyển khoản — bot
> xem giúp được hay chuyển luôn cho anh/chị?
>
> Có nhóm Zalo riêng để báo “có khách đang chờ” không?
>
> Khách **im sau khi em báo giá** — anh/chị muốn bot nhắn lại **một lần**
> không? Nói **tắt**, hoặc sau bao nhiêu giờ (24 hay 48 thường đủ). Chưa nói =
> tắt, em không nhắn.
>
> Sau khi **đã ghi đơn** hoặc anh/chị đã chốt — muốn bot hỏi một câu *nhận hàng
> chưa* / *dùng ổn không* không? Tắt, hoặc sau bao nhiêu giờ, **và viết đúng
> câu** muốn gửi. Không viết câu = tắt. Không tự hỏi đánh giá nếu anh/chị chưa
> cho câu đó. Ảnh chuyển khoản **không** tính là đã có đơn.

→ `USER.md` (kể cả mục Follow-up) + `knowledge/tinh-huong.md`. Ảnh CK/hàng → skill `doc-anh`. Follow-up → `skills/follow-up/SKILL.md`. Chưa điền = tắt.

---

## 9. Khách chưa chọn được sản phẩm / dịch vụ

**Câu chính:**

> Khách bảo không biết lấy **sản phẩm** nào, **gói dịch vụ** nào cho hợp —
> anh/chị, lúc đang nhắn tay, **thường hỏi họ những gì** trước khi gợi ý? Kể
> đúng câu mình hay hỏi, theo thứ tự mình hay hỏi. Ví dụ: dùng cho ai, dùng
> việc gì, ngân sách, size, ngày cần, đã dùng loại nào, chỗ nào chưa ưng. Tầm
> hai ba câu là vừa, để khách không thấy bị hỏi dồn.

**Hỏi thêm:**

> Câu nào **phải hỏi**, câu nào hỏi khi họ chưa nói rõ?
>
> Có việc phải hỏi **đúng thứ tự** không? Ví dụ biết size rồi mới ra sản phẩm,
> biết nhu cầu rồi mới ra gói dịch vụ.
>
> Gợi ý xong, việc gì phải **anh/chị xem đã** rồi mới trả khách?
>
> Anh/chị hay gợi ý **một** món/gói chính, hay đưa cả danh sách cho họ tự chọn?

→ `skills/khai-thac/SKILL.md` (đừng nói chữ skill với họ).

---

## 10. Khách mới gõ vào — câu đầu

**Câu chính:**

> Khách mới vào, gõ *alo*, *shop ơi*, hỏi *còn hàng không*, hoặc thả sticker —
> anh/chị muốn **câu đầu tiên** nghe như thế nào? Viết giúp đúng kiểu mình đang
> nhắn khi tư vấn sản phẩm dịch vụ, một câu có người, không phải câu “em có thể
> hỗ trợ gì ạ” trên mạng. Nếu muốn câu đó xong gợi ý họ trả lời cho dễ — ví dụ
> đang tìm sản phẩm, đang hỏi dịch vụ, hay muốn xem giá — kể luôn, bằng chữ
> khách gõ được.

**Hỏi thêm:**

> Cho em nghe thêm một cách mở khác, nếu khách hỏi thẳng giá hoặc hỏi thẳng một
> sản phẩm / một dịch vụ?
>
> Chào một kiểu quanh năm, hay đổi theo buổi sáng/tối, theo chương trình?

→ Brain: tin mở.

---

## Xong

Raw còn nguyên; wiki tách từ tài liệu + miệng; thử 5 câu khách hay hỏi về sản
phẩm/dịch vụ. Còn thiếu thì hỏi lại **bằng lời thường**.

## Bẫy

- **Hỏi cục** — bốn ý một hơi, họ trả một ý rồi bỏ.
- **Câu chính quá ngắn** — họ không biết kể sâu tới đâu.
- **Nói “đồ / kho / wiki”** — họ không hiểu mình cần tài liệu sản phẩm dịch vụ.
- **Nhận file rồi hỏi lại cả bảng giá.** Đọc file, hỏi chỗ thiếu.
- **Tự vào web** khi họ chưa gửi link.

---

## Chỉ agent — câu nào đi file nào

Không đọc bảng này cho chủ.

| Chủ đề | Họ đang kể | Bạn dựng |
|---|---|---|
| 1–2, 4, 10 | Sản phẩm/dịch vụ, khách, giọng, câu chào | Brain |
| 3, 6 | Tài liệu + câu khách hỏi thêm | Wiki |
| 5, 7–9 | Việc không được tự ý, đơn hàng, lúc phân vân | Harness (`ghi-don`, `khai-thac`, `ban-giao`) |
