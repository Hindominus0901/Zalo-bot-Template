# Chuẩn bị trước khi dựng bot

Đọc file này **trước tiên**, kể cả khi anh/chị không biết lập trình. Không có
đủ những thứ dưới thì dựng tới giữa chừng sẽ tắc.

Người dựng (coding agent) đọc thêm: [`dung-bot/QUY-TRINH.md`](dung-bot/QUY-TRINH.md).

## Cả quá trình, anh/chị chỉ phải làm bốn việc

Phần máy — cài đặt, cấu hình, chạy 24/7 — trợ lý AI tự làm (nó chạy
`scripts/vps.py` và `scripts/bat_dau.py`, anh/chị không gõ lệnh nào). Làm
**trước** phỏng vấn. Nó chỉ dừng lại nhờ anh/chị:

1. **Dán mã AI** — mã kết nối của tài khoản AI đã nạp tiền (mục 1 dưới), dán
   vào ô Notepad trợ lý mở sẵn. Không dán vào chat.
2. **Quét mã** — cầm điện thoại đang đăng nhập **nick bot**, quét hình hiện
   trên màn hình máy tính.
3. **Nhắn một mã ngắn** — từ **nick Zalo của anh/chị**, nhắn cho nick bot đúng
   mã kiểu `NAMI-4821` hiện trên màn hình. Để máy biết anh/chị là chủ — sau đó
   anh/chị dạy bot, giao việc qua Zalo được.
4. **Nhắn thử** — từ một nick khác, nhắn bot năm câu, xem trả lời có ổn không.

Trước bốn việc đó là ba việc chuẩn bị có trợ lý dẫn: tạo nick Zalo cho bot,
mở tài khoản AI, thuê VPS. Kẹt chỗ nào thì **chụp màn hình gửi trợ lý**
([`BAT-DAU.md`](BAT-DAU.md) có cách chụp). Sau cùng là trả lời câu hỏi về shop
(phỏng vấn) và gửi tài liệu. Muốn bốn việc
trên trôi chảy thì chuẩn bị đủ những thứ dưới đây **trước**.

---

## Phải có

### 1. Tài khoản AI có nạp tiền, và mã kết nối (API key)

Bot suy nghĩ bằng **GPT của OpenAI** (mặc định GPT-5.6 Terra — trả lời khôn,
xem được ảnh). Anh/chị mở tài khoản **API** ở platform.openai.com, nạp tiền,
tạo mã. **Gói ChatGPT Plus không dùng được cho bot** — API nạp tiền riêng.

Giá GPT-5.6 Terra (theo danh mục của bản OpenClaw đang ghim): $2.5 cho 1 triệu
token đọc vào ($0.25 nếu phần đầu lặp lại được nhớ đệm), $15 cho 1 triệu token
viết ra. Mỗi lượt bot đọc khoảng 13–15 nghìn token (sổ + luật + lịch sử chat —
đã đo trên bản thật), một tin khách có thể tốn 1–3 lượt.

**Ước chừng 300–2.000 đồng mỗi tin khách** — tức khoảng **$15–120 một tháng**
nếu 50 tin khách mỗi ngày. Khoảng rộng vì còn tuỳ tin dài ngắn, có ảnh không,
bot phải đọc mấy tờ sổ. Đây là ước tính, chưa đo bằng tiền thật: xem *Usage*
trên platform.openai.com sau tuần đầu. Muốn rẻ hơn khoảng 2,5 lần thì dùng
bản tiết kiệm (GPT-5.6 Luna), kém tinh tế hơn chút.

**Đây là chi phí chạy hàng tháng, không phải trả một lần.** Tính theo lượng
tin: khách nhắn càng nhiều thì càng tốn. Bot rảnh thì gần như không tốn.

GPT-5.6 Terra **nhìn được ảnh** — khách CSKH gửi ảnh suốt (ảnh món, ảnh chuyển
khoản, ảnh hàng lỗi). Đã có mã Claude (Anthropic) thì dùng mã đó cũng được.

### 2. Một nick Zalo riêng cho bot, và một số điện thoại riêng

**Không dùng nick Zalo chính của anh/chị.** Bot cầm nick nào thì nick đó chạy
24/7 và không dùng tay song song được.

Nick mới cần một số điện thoại chưa đăng ký Zalo. Sim rẻ cũng được. Đừng gắn
ngân hàng hay giấy tờ quan trọng vào nick này.

### 3. Điện thoại đang đăng nhập nick bot

Để **quét mã** lúc bật, và **quét lại** mỗi khi phiên đăng nhập chết. Chuyện
đó sẽ xảy ra, không phải một lần rồi thôi — cứ giữ điện thoại đó đăng nhập sẵn.

### 3b. Biết trước: sẽ có lúc phải quét lại mã

Phiên đăng nhập của bot **sẽ chết** — vài tuần hay vài tháng một lần, không đoán
được. Lúc đó bot im, khách nhắn không ai trả.

Không phải hỏng, không phải mất dữ liệu. Chỉ cần quét lại mã như lần đầu. Nhưng
anh/chị cần **biết gọi ai** khi nó xảy ra, và người đó phải vào được máy chủ.
Hỏi người dựng dán sẵn bốn bước quét lại vào chỗ anh/chị tìm được.

### 4. Một nick Zalo thứ hai để nhắn thử

Nick của anh/chị hoặc của nhân viên. Không tự nhắn từ chính nick bot — không
thử được gì.

### 5. Một máy chạy suốt ngày đêm

VPS thuê, hoặc một máy để bàn không tắt. **Tắt máy là mất tin khách**: Zalo cá
nhân không gửi bù tin lúc bot ngủ.

Máy không màn hình (VPS) thì bước quét mã làm khác — người dựng xem
[`docs/14-vps-headless.md`](docs/14-vps-headless.md).

Người dựng không có app SSH? Vào VPS ngay trên trình duyệt (cần một tên miền):
[`docs/18-cloudflare.md`](docs/18-cloudflare.md). Bot thì vẫn sống trên VPS —
chưa cho sống trên Cloudflare được.

### 6. Trên máy đó: `git`, Python 3, và **Node đúng bản**

Node phải là **24.16 trở lên nhưng dưới 25**, hoặc **26.1 trở lên**. Node 22, 23
hay 25 thì cài hỏng ngay từ đầu. Người dựng kiểm bằng `node --version`.

Người dựng cài. Windows thì lúc cài Python nhớ tick **Add to PATH**.

### 7. Một coding agent

Chỗ người dựng ngồi làm. Bản trả tiền. Cái nào cũng được:

- **Claude Code** · **Cursor** · **Codex** · **Antigravity** · **Copilot**

Repo đã có sẵn cửa vào cho cả năm — mở lên là agent tự biết phải làm gì. Không
cần chọn theo template, chọn theo cái người dựng quen tay.

Không quen dòng lệnh? **Claude Cowork**, **ChatGPT Work**, **dots** làm được phần
hỏi và điền sổ. Bot vẫn cần máy chạy 24/7 (mục 3). Xem `docs/17-dung-bang-app-chat.md`.

---

## Tuỳ shop, không bắt buộc

- **Google Drive** — nếu bảng giá / tài liệu của anh/chị nằm trên Drive và muốn
  bot đọc được. Cần đăng nhập cho phép. Xem [`docs/11-mcp-ung-dung.md`](docs/11-mcp-ung-dung.md).
- **Phần mềm quản đơn có API** — nếu muốn khách hỏi *đơn tới đâu rồi* thì bot
  tra được thật. Không có thì bot hỏi mã đơn rồi chuyển cho anh/chị, vẫn chạy.

---

## Chuẩn bị sẵn cho buổi phỏng vấn

Người dựng sẽ hỏi anh/chị **10 chủ đề** về shop. Có sẵn mấy thứ này thì buổi
đó nhanh và bot trả lời đúng hơn:

- Bảng giá (file, ảnh chụp, hay chỉ cần nói miệng cũng được)
- Chính sách ship, đổi trả, bảo hành — cái nào đã chốt
- Vài tin nhắn thật anh/chị đã trả khách, để bot học giọng
- Nick Zalo / nhóm nội bộ để bot gọi khi gặp chuyện tiền hoặc khiếu nại

Chưa có thì vẫn dựng được — chỗ nào thiếu bot sẽ nói *chưa chắc phần đó* chứ
không bịa số. Bổ sung sau lúc nào cũng được.

---

## Một điều nên biết trước

Bot cầm **nick Zalo cá nhân**, và cách nó nối vào Zalo là không chính thức.
Zalo có thể khoá hoặc hạn chế nick đó. Vì vậy: nick riêng, số riêng, đừng gắn
gì quan trọng vào. Mất nick thì tạo nick mới quét lại, sổ và dữ liệu vẫn còn.

Chi tiết cho người dựng: [`docs/02-kenh-zalouser.md`](docs/02-kenh-zalouser.md).
