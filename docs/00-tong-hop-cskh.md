# Bot CSKH trên Zalo làm được gì, và làm thế nào

Viết sau khi đọc bot cũ (`agent-cskh-zalo`), tài liệu Zalo, và các bài CSKH /
chatbot bán hàng 2025–2026. Đây là bản đồ năng lực, không phải hướng dẫn cài đặt.

---

## 1. Hai cửa vào Zalo — chọn sai là thiết kế sai

Zalo có **hai sản phẩm bot**, không phải hai gói của cùng một thứ.

| | **Zalo Bot Creator** | **Zalo OA** |
|---|---|---|
| Tạo từ | Tài khoản Zalo cá nhân, ~5 phút, không chờ duyệt | Doanh nghiệp, giấy tờ, chờ duyệt |
| API | `bot-api.zaloplatforms.com` | `openapi.zalo.me` |
| Chat 1-1 | Có | Có |
| Vào **nhóm chat** | Có (Basic: 3 nhóm, beta) | Không |
| Nút bấm, list, tin có thẻ | Tài liệu landing có nhắc; `sendMessage` hiện chỉ chắc chữ + ảnh + sticker + định dạng | Có: nút `oa.query.show` / `.hide`, list tối đa 5 mục, mở URL / gọi điện |
| Nhắn chủ động ra SĐT (ZNS) | Không | Có, nhưng chỉ tin giao dịch đã duyệt — không phải spam số lạ |
| Hạn mức Basic (đo từ bot thật, 2026) | 3.000 tin/tháng, 50 người | Theo gói OA, cao hơn |
| Tắt máy | Mất tin — Zalo không gửi bù | Webhook bền hơn nếu server sống |
| Tên bot | Bắt buộc bắt đầu bằng `Bot` | Tên OA |

Bot cũ chọn Bot Creator vì chủ shop tự dựng được, vào được nhóm, không cần OA.
Cái hình dung của template mới — **gợi ý tương tác / câu hỏi bấm được** — khớp
OA hơn. Landing page Bot Creator có viết "quick reply, nút, carousel" nhưng API
`sendMessage` công bố vẫn chỉ có chữ. **Chưa coi là có nút** cho tới khi thử thật.

Hệ quả thiết kế: viết lớp **gợi ý** độc lập với kênh. Trên Bot Creator là 2–3
câu hỏi viết ra cuối tin. Trên OA thì cùng nội dung đó thành nút `oa.query.show`.
Đừng gắn chết vào nút rồi mới nghĩ nội dung.

Cửa sổ 24–48 giờ trên OA: trong cửa sổ sau lần khách nhắn, OA trả lời tư vấn
thoải mái. Ngoài cửa sổ thì chỉ còn tin mẫu / ZNS đúng loại. Bot Creator không
nhắn trước cho người chưa từng nhắn tới.

---

## 2. Việc CSKH thật sự làm được — tám nhóm

Không phải "trả lời FAQ". Một nhân viên CSKH giỏi trên Zalo làm tám việc. Bot
làm được phần lớn nếu có kho tri thức và biết lúc nào phải dừng.

### A. Đón và định hướng

Khách vào, thường gõ rất ngắn: *hi*, *alo*, *shop ơi*, *còn hàng không*, *giá
bao nhiêu*. Bot không được đọc menu số (*nhắn 1 để xem bảng giá*) — khách thật
không đọc, rồi số lạc của lượt trước làm bot mở nhầm trang.

Làm đúng: trả lời ý vừa hỏi, rồi **đưa 2–3 hướng đi tiếp** bằng chữ đời thường.

> Dạ em đây ạ. Anh/chị đang tìm loại nào, hay muốn em hỏi giúp vài câu cho đúng ý?

### B. Khai thác bối cảnh — việc "dễ ăn" nhất

Đây là phần template cũ **đã có mầm** (`tu-van-chon-san-pham`, `lay-thong-tin-khach`)
nhưng chưa thành máy trạng thái. Ý hình dung lần này đúng hướng:

1. Người nhắn tới → bot chủ động hỏi, không đổ bảng giá lên đầu
2. Hỏi từng câu, tối đa 2–3 câu chẩn đoán
3. Đủ slot thì mới tư vấn
4. Tư vấn = **một** lựa chọn chính + **một** phương án thay thế, lý do trích từ lời khách

Khung slot và luật hỏi nằm ở [`knowledge/khung-khai-thac.md`](../knowledge/khung-khai-thac.md).

Câu hỏi hay hỏi về **tình huống**, không về danh tính:

| Nên hỏi | Đừng hỏi lúc đầu |
|---|---|
| Dùng cho việc gì / tặng ai / dịp nào | Tên, SĐT, địa chỉ |
| Đã dùng loại nào, vướng chỗ gì | "Anh/chị cần hỗ trợ gì ạ?" |
| Ngân sách / thời gian nếu giá phụ thuộc | Ba câu một lúc |

Cho một thứ hữu ích **trước** khi xin SĐT. Xin số mà chưa cho gì là bán kiểu chặn đường.

### C. Tư vấn và báo giá

Báo đúng số trong kho. Kèm **cái giá bao gồm gì**. Giá phụ thuộc tình huống thì
hỏi một câu rồi mới báo khoảng đúng — không đổ cả bảng.

Không ước lượng, không "khoảng", không suy giá gói B từ gói A. Không tự giảm giá.

### D. Xử lý từ chối

"Đắt quá" gần như không nói về giá — nói về **giá trị chưa rõ**. Hỏi họ đang so
với cái gì, rồi nói bằng số đo được (*bảo hành 24 tháng*), không bằng tính từ
(*chất lượng cao*). "Để em xem đã" là lời hoãn: nhận thoải mái, hỏi còn vướng gì,
không nài.

### E. Lấy lead và bàn giao người thật

Khi khách quan tâm thật: lưu liên hệ kèm lý do cụ thể, tóm tắt **họ hỏi gì và đã
được nói gì**, nói rõ ai gọi lại và khi nào (con số giờ làm việc, không phải
"trong giờ hành chính").

Chuyển sớm một lượt tốt hơn cố thêm một lượt. Phàn nàn, giảm giá, ảnh chuyển
khoản, hợp đồng — chuyển ngay.

### F. Đơn hàng

Tra đơn theo dữ liệu, không đoán ngày nhận. Ghi đơn tạm rồi **người thật chốt**.
Không nói "đã đặt thành công". Không xác nhận đã nhận tiền dù khách gửi ảnh
biên lai — nhận được *ảnh* thì nói; nhận được *tiền* thì không.

### G. Chăm khách cũ

Không bắt kể lại từ đầu. Nhớ size, món đã từ chối, tình huống dùng. Ghi nhớ trong
im lặng. Trục trặc sau mua thì sang xử lý phàn nàn, không chào bán.

### H. Vòng lặp học của shop

Mỗi câu bot không trả lời được thì ghi nguyên văn. Báo cáo cuối ngày: *"6 câu
không trả lời được, 3 người hỏi ship Đà Nẵng"*. Chủ viết thêm một trang, hôm sau
bot trả lời được. Đây là thứ làm bot khá lên theo tuần, không phải theo lần prompt.

---

## 3. Thao tác trên Zalo — khách thấy gì

### Khách gửi được

Chữ, ảnh, sticker, vị trí (OA), voice (Bot Creator có event `message.voice.received`).
**Bot Creator không nhận PDF/Word/Excel** — dặn chụp màn hình. Ảnh gửi dưới dạng
link tạm, phải tải ngay trong lượt.

Trong nhóm (Bot Creator): bot chỉ nghe khi được @mention hoặc reply tin của nó.
Gửi ảnh phải tag ngay trong chú thích tấm ảnh, không tag tin trước rồi gửi ảnh sau.

### Bot gửi được

Chữ ngắn (cắt ~1400–2000 ký tự), ảnh, sticker. OA thêm: list, nút, tin giao dịch
đã duyệt. Không bảng Markdown — Zalo hiện chữ thô. In đậm được nếu dùng
`parse_mode` / `text_styles` (Bot Creator).

### Nhịp một lượt tốt

1. Hiện "đang soạn" nếu API hỗ trợ (`sendChatAction`) — đừng để khách chờ im
2. 2–5 câu, vào việc ở câu đầu, không mở bài
3. Kết bằng **một** câu hỏi cụ thể, hoặc 2–3 gợi ý bấm/gõ được
4. Việc nặng (đọc ảnh, tra kho) thì tách tin: tin 1 ghi nhận, tin 2 trả lời

### Gợi ý tương tác — cách làm quanh việc không có nút

Template cũ cố tình **không** dùng menu đánh số. Đúng. Cách thay:

> Dạ có phải anh/chị đang hỏi về **bảng giá** không ạ — hay muốn em hỏi giúp cho đúng loại?

Khách sửa được trong một lượt. Khi lên OA, cùng hai nhánh đó thành hai nút
`oa.query.show` với payload là câu khách sẽ "gửi": `Xem bảng giá` / `Để em hỏi vài câu`.

Đừng gợi ý quá 3. Đừng gợi ý thứ bot không làm được.

---

## 4. Bot cũ đã có gì, template mới còn thiếu gì

Bốn trụ cột của `agent-cskh-zalo` giữ nguyên — chúng đúng:

| Trụ | File | Trả lời |
|---|---|---|
| Tính cách | `knowledge/persona.md` | Bot là ai, nói thế nào, không được nói gì |
| Kiến thức | `knowledge/wiki/` | Bot biết gì |
| Kỹ năng | `skills/` | Bot làm thế nào |
| Công cụ | `tools/` | Bot làm được gì |

Skill đã viết sẵn và viết rất chắc: tư vấn chọn món, lấy thông tin, báo giá,
từ chối, phàn nàn, chuyển người, tra/tạo đơn, chăm khách cũ, tra cứu, soát kho.

Ba lớp chặn không được gỡ: không trả lời khi chưa tra kho, không tự xác nhận
tiền, không lộ `internal/`.

**Chỗ hổng so với ý hình dung lần này:**

1. **Khai thác chưa phải máy trạng thái.** Skill bảo "hỏi 2–3 câu rồi đề xuất
   một món", nhưng không có chỗ lưu slot, không có điều kiện "đủ bối cảnh thì
   mới tư vấn", không có gợi ý cuối mỗi tin.
2. **Giọng persona mẫu còn đúng mà khô.** Luật chống sáo ngữ rất tốt. Chưa có
   lớp tính cách: hơi vui, hơi hài, luôn để ý khách — mà vẫn không thành MC.
3. **Chế độ 0 đồng không đọc persona / skill.** `tra_cuu` chỉ khớp wiki. Máy
   khai thác và giọng chỉ sống ở chế độ `ai`.
4. **Chưa nhắn chủ động** (nhắc lịch, follow-up) — chủ ý, vì hạn mức và vì chưa
   đo cửa sổ gửi trên Bot Creator.
5. **Chưa có nút / quick reply** vì kênh cũ không có (hoặc chưa chứng minh được).

OpenClaw đóng góp một ý tách file: `SOUL.md` = giọng và tính cách; luật vận hành
ở chỗ khác. Template mới nên tách `giong-noi.md` khỏi `persona.md` (bối cảnh
doanh nghiệp + ranh giới). Giọng dùng chung được giữa các shop; bối cảnh thì không.

File **Tom** không nằm trong repo này, không nằm trong `agent-cskh-zalo`,
`goclaw`, hay các repo GitHub khác của cùng tài khoản. Google Drive của phiên
này chưa kết nối. Cần đường dẫn / file đó trước khi trộn giọng Tom vào.

---

## 5. Luồng hội thoại mẫu — khách lạ, chưa biết mình cần gì

Đây là "việc dễ ăn" cần làm rất chắc.

```
Khách: alo shop
Bot:    Dạ em đây ạ. Anh/chị đang tìm cho mình dùng hay để tặng ai đó?
        Gợi ý: Mình dùng hằng ngày · Tặng người quen · Xem bảng giá

Khách: tặng sinh nhật bạn
Bot:    Sinh nhật vui ghê. Bạn ấy dùng kiểu nào em biết không —
        hay mình thích, hay đang thiếu món gì đó?
        Gợi ý: Bạn ấy hay dùng sẵn · Mình chọn giúp · Ngân sách khoảng...

Khách: ngân sách 500
Bot:    [ĐỦ SLOT: dịp + đối tượng + ngân sách]
        Vậy lấy A nhé — đúng tầm 500, hợp tặng, không vướng cái anh/chị vừa nói.
        Nếu hay mang đi xa thì lấy B thay.
        Anh/chị muốn em giữ giúp một suất, hay xem A khác B chỗ nào?
```

Ba lượt. Hỏi trước. Tư vấn sau. Một lựa chọn chính. Câu kết là bước tiếp, không
phải "cần hỗ trợ gì thêm không ạ".

---

## 6. Giới hạn đừng hứa

- Một con số sai về giá / ngày giao tốn hơn một câu "em kiểm tra lại"
- Bot không phải chủ shop — kể chuyện chủ thì ngôi thứ ba
- Không đoán anh/chị từ tên mơ hồ
- Không đọc kiến thức ngành ra như chính sách của shop này
- 3.000 tin/tháng Bot Creator ≈ 300 cuộc, ~10 cuộc/ngày
- ZNS không phải kênh nhắn lạnh

Nguồn đã đọc: README / persona / skill / `docs/01`–`04` của `agent-cskh-zalo`;
[Zalo Bot sendMessage](https://docs.zaloplatforms.com/docs/BOT/apis/sendMessage);
[nút OA](https://docs.zaloplatforms.com/docs/OA/phu-luc/cau-truc-cua-tham-so-buttons);
[OpenClaw SOUL](https://docs.openclaw.ai/concepts/soul);
các bài CSKH Zalo OA (Claude.vn, Mona, Loc Nguyen Data) — dùng để đối chiếu
năng lực, không copy kiến trúc 6 lớp vào template này.
