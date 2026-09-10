# Bot CSKH trên Zalo làm được gì, và làm thế nào

> **Nghiên cứu / bản đồ năng lực** — không phải hướng dẫn cài. Dựng shop:
> [`08-luong-chu-shop.md`](08-luong-chu-shop.md). Cài nick: [`05-thiet-lap.md`](05-thiet-lap.md).
> Thử: [`04-kich-ban-thu.md`](04-kich-ban-thu.md). Sổ: [`09-kho-va-du-lieu.md`](09-kho-va-du-lieu.md).

Viết sau khi đọc bot cũ (`agent-cskh-zalo`), tài liệu Zalo, và các bài CSKH /
chatbot bán hàng 2025–2026.

---

## 1. Kênh đã chốt — nick cá nhân như Tom

Bản này **không** dùng Bot Creator hay OA. Bot cầm một tài khoản Zalo người,
login QR qua OpenClaw `zalouser`. Chi tiết và rủi ro nick:
[`02-kenh-zalouser.md`](02-kenh-zalouser.md).

Bảng dưới chỉ để nhớ vì sao không chọn hai cửa kia.

| | **Nick cá nhân (đang dùng)** | Zalo Bot Creator | Zalo OA |
|---|---|---|---|
| Khách thấy | Người trong danh bạ | Tên bắt đầu `Bot` | Trang OA |
| API | `zca-js` (unofficial) | `bot-api.zaloplatforms.com` | `openapi.zalo.me` |
| Nút / list | Không — gợi ý bằng chữ | Chưa chắc | Có |
| Vào nhóm | Như thành viên | 3 nhóm, @mention | Không |
| Hạn Basic | Không áp 3.000 tin / 50 user | Có | Theo gói |
| Rủi ro | Khóa nick nếu bị coi là bot | Token | Token |

Gợi ý tương tác: 2–3 câu gõ được + quote reply + typing/seen. Không gắn nút OA.

---

## 2. Việc CSKH thật sự làm được — chín nhóm

Không phải "trả lời FAQ". Một nhân viên CSKH giỏi trên Zalo làm chín việc
(A–I trong [`moi-loai-cau-hoi.md`](../knowledge/moi-loai-cau-hoi.md)) — và
còn **ở lại chat** khi khách hỏi lệch, hỏi đời, hỏi kho chưa có. Biết lúc nào
dừng là lúc tiền / khiếu nại / quyền quyết, không phải lúc câu hơi lạ.

Chỗ cố ý khác bot cũ: [`01-it-rao-da-dang.md`](01-it-rao-da-dang.md).

### A. Đón và định hướng

Khách vào, thường gõ rất ngắn: *hi*, *alo*, *shop ơi*, *còn hàng không*, *giá
bao nhiêu*. Bot không được đọc menu số (*nhắn 1 để xem bảng giá*) — khách thật
không đọc, rồi số lạc của lượt trước làm bot mở nhầm trang.

Làm đúng: trả lời ý vừa hỏi, rồi **đưa 2–3 hướng đi tiếp** bằng chữ đời thường.

> Alo có em, Nami đây. Anh/chị đang tìm cho mình dùng hay để tặng ai đó?

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

Skill: [`skills/xu-ly-tu-choi/SKILL.md`](../skills/xu-ly-tu-choi/SKILL.md). Không
nới giá, không chê đối thủ. Im sau báo giá: một cửa mở rồi dừng.

### E. Lấy lead và bàn giao người thật

Khi khách quan tâm thật: lưu liên hệ kèm lý do cụ thể, tóm tắt **họ hỏi gì và đã
được nói gì**, nói rõ ai gọi lại và khi nào (con số giờ làm việc, không phải
"trong giờ hành chính").

Chuyển sớm một lượt tốt hơn cố thêm một lượt. Phàn nàn, giảm giá, ảnh chuyển
khoản, hợp đồng — chuyển ngay.

Skill: [`thu-lead`](../skills/thu-lead/SKILL.md) (SĐT → `memory/` + bàn giao, không
CRM) và [`ban-giao`](../skills/ban-giao/SKILL.md). Từ chối cho số thì không hỏi lần hai.

### F. Đơn hàng

Tra đơn theo dữ liệu, không đoán ngày nhận. Ghi đơn tạm rồi **người thật chốt**.
Không nói "đã đặt thành công". Không xác nhận đã nhận tiền dù khách gửi ảnh
biên lai — nhận được *ảnh* thì nói; nhận được *tiền* thì không.

### G. Chăm khách cũ

Không bắt kể lại từ đầu. Nhớ size, món đã từ chối, tình huống dùng. Ghi nhớ trong
im lặng. Trục trặc sau mua thì sang xử lý phàn nàn, không chào bán.

Skill: [`skills/cham-khach-cu/SKILL.md`](../skills/cham-khach-cu/SKILL.md) — **reactive**
(cùng thread / họ vừa nói). Không CRM, không bịa đơn cũ, không *em đã ghi nhớ*.

### H. Vòng lặp học của shop

Mỗi câu bot không trả lời được thì ghi nguyên văn. Báo cáo cuối ngày: *"6 câu
không trả lời được, 3 người hỏi ship Đà Nẵng"*. Chủ viết thêm một trang, hôm sau
bot trả lời được. Đây là thứ làm bot khá lên theo tuần, không phải theo lần prompt.

---

## 3. Thao tác trên Zalo — khách thấy gì

### Khách gửi được

Chữ, ảnh, sticker, voice, file — nick cá nhân nhận được gần như Zalo người thật.
Ảnh/file phải xử lý ngay trong lượt (OpenClaw có hàng đợi local; socket `zca-js`
không replay tin lúc gateway tắt).

Trong nhóm: mặc định chỉ nghe khi được gọi tên (**Nami** / biệt hiệu), khi @,
hoặc khi người ta reply tin của bot. Cấu hình `requireMention`.

### Bot gửi được

Chữ (cắt ~2000 ký tự), ảnh, sticker, quote reply, reaction, typing/seen.
Không nút, không list OA, không bảng Markdown. Giọng thô như nhắn tay.

### Nhịp một lượt tốt

1. Typing + seen (zalouser lo, best-effort) — đừng để khách chờ im
2. Bắt nhịp khách: 3 chữ thì 1–2 câu; phân vân thì ở lại. Vào việc ở câu đầu
3. Kết bằng **một** câu hỏi cụ thể, hoặc 2–3 gợi ý gõ được
4. Việc nặng thì tách tin: tin 1 ghi nhận, tin 2 trả lời

### Gợi ý tương tác — chữ, không nút

Nick cá nhân không có nút OA. Cách làm:

> Dạ có phải anh/chị đang hỏi về **bảng giá** không ạ — hay muốn em hỏi giúp cho đúng loại?

Khách sửa được trong một lượt. Thêm quote reply tin họ nếu đang phân vân. Đừng
đánh số 1/2/3. Đừng gợi ý thứ bot không làm được. Tối đa 3 hướng.

---

## 4. Bot cũ đã có gì, template mới còn thiếu gì

Bốn trụ cột của `agent-cskh-zalo` **giữ chỗ sửa** — không giữ nội quy đi kèm:

| Trụ | File | Trả lời |
|---|---|---|
| Tính cách · ngôn từ · cách tư vấn | `SOUL.md` + `giong-noi.md` + `cach-tu-van.md` + `persona.md` | Người thế nào, gõ thế nào, hỏi/trả thế nào |
| Kiến thức | `knowledge/wiki/` | Số liệu shop — không phải giấy phép được nói |
| Kỹ năng | `skills/` | Cách hay khi gặp tình huống đó, không phải cổng bắt buộc |
| Công cụ | `TOOLS.md` (tên việc → `read`/`write`/`message`) | Bot làm được gì — không có thư mục `tools/` |

Skill cũ viết chắc, nhưng nhiều cái biến thành rào: "ngoài kho thì dừng", "đọc
wiki rồi mới được trả lời", "ngoài phạm vi dù biết cũng im". Template này **không
mang ba câu đó sang**. Chi tiết: [`01-it-rao-da-dang.md`](01-it-rao-da-dang.md).

Rào là **prompt** — khối `<policy>` đầu `AGENTS.md`, không có middleware trong
repo. Thứ rào này làm được và không làm được: [`13-an-toan.md`](13-an-toan.md).

**Chỗ hổng so với ý hình dung lần đầu** (đã lấp phần giọng/tư vấn trên workspace;
còn runtime và Tom):

1. **Khai thác** đã có máy pha (`khung-khai-thac.md`) + cách hỏi (`cach-tu-van.md`) — vẫn tắt khi khách hỏi fact.
2. **Giọng** không còn danh sách cấm khô: `SOUL.md` tính cách, `giong-noi.md` ngôn từ, `hoi-thoai-mau.md` few-shot. Đối ngược kịch bản OA.
3. **Chế độ 0 đồng không đọc persona / skill** — template này AI-first; FAQ khớp
   từ khóa để bot cũ lo.
4. **Câu ngoài script / kho trống bị cúp** — xem `moi-loai-cau-hoi.md`.
5. **Runtime:** workspace OpenClaw + zalouser, chưa dựng trên nick thật. File Tom (SOUL máy cũ) chưa có trong repo.

Từ chối / lead / khách cũ: đã có skill (`xu-ly-tu-choi`, `thu-lead`, `cham-khach-cu`).
Few-shot: `knowledge/hoi-thoai-mau.md`. Restart: `BOOT.md` (không nhắn khách,
không burst follow-up). Bản đồ vòng: `knowledge/workflow-cskh.md`.

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
Bot:    Alo có em, Nami đây. Anh/chị đang tìm cho mình dùng hay để tặng ai đó?
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
- Kiến thức ngành được nói, miễn tách miệng với chính sách shop — đừng đọc số liệu shop từ kiến thức chung
- Gateway tắt = mất tin lúc đó (socket personal không replay)
- Nick bot unofficial — xem cảnh báo khóa nick ở `02-kenh-zalouser.md`

Nguồn đã đọc: README / persona / skill / `docs/01`–`04` của `agent-cskh-zalo`;
[Zalo Bot sendMessage](https://docs.zaloplatforms.com/docs/BOT/apis/sendMessage);
[nút OA](https://docs.zaloplatforms.com/docs/OA/phu-luc/cau-truc-cua-tham-so-buttons);
[OpenClaw SOUL](https://docs.openclaw.ai/concepts/soul);
các bài CSKH Zalo OA (Claude.vn, Mona, Loc Nguyen Data) — dùng để đối chiếu
năng lực, không copy kiến trúc 6 lớp vào template này.

Đã nới rào (xem [`01-it-rao-da-dang.md`](01-it-rao-da-dang.md)). Kênh: [`02-kenh-zalouser.md`](02-kenh-zalouser.md). Phỏng vấn: [`bo-cau-hoi.md`](bo-cau-hoi.md) / [`PHONG-VAN.md`](../PHONG-VAN.md). Bật nick: [`03-bat-nick.md`](03-bat-nick.md). Thử: [`04-kich-ban-thu.md`](04-kich-ban-thu.md). Tình huống Zalo: [`tinh-huong.md`](../knowledge/tinh-huong.md). Hội thoại mẫu: [`hoi-thoai-mau.md`](../knowledge/hoi-thoai-mau.md). Ví dụ điền (shop giả): [`vi-du-file-da-dien.md`](vi-du-file-da-dien.md).
