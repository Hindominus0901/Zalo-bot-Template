# Chuẩn bị trước khi dựng bot

Đọc file này **trước tiên**, kể cả khi anh/chị không biết lập trình. Không có
đủ những thứ dưới thì dựng tới giữa chừng sẽ tắc.

Người dựng (coding agent) đọc thêm: [`dung-bot/QUY-TRINH.md`](dung-bot/QUY-TRINH.md).

---

## Phải có

### 1. Tài khoản AI có nạp tiền, và mã kết nối (API key)

Bot suy nghĩ bằng một mô hình AI thuê ngoài — Claude, GPT-4o, hoặc Gemini.
Anh/chị mở tài khoản, nạp tiền, lấy mã kết nối, đưa cho người dựng.

**Đây là chi phí chạy hàng tháng, không phải trả một lần.** Tính theo lượng
tin: khách nhắn càng nhiều thì càng tốn. Bot rảnh thì gần như không tốn.

Chọn loại **nhìn được ảnh** — khách CSKH gửi ảnh suốt (ảnh món, ảnh chuyển
khoản, ảnh hàng lỗi). Loại chỉ đọc chữ sẽ bắt khách gõ lại, rất mất khách.

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

### 6. Trên máy đó: `git`, Python 3, và **Node đúng bản**

Node phải là **24.16 trở lên nhưng dưới 25**, hoặc **26.1 trở lên**. Node 22, 23
hay 25 thì cài xong bot không chạy. Người dựng kiểm bằng `node --version`.

Người dựng cài. Windows thì lúc cài Python nhớ tick **Add to PATH**.

### 7. Một coding agent

Chỗ người dựng ngồi làm. Bản trả tiền. Cái nào cũng được:

- **Claude Code** · **Cursor** · **Codex** · **Antigravity** · **Copilot**

Repo đã có sẵn cửa vào cho cả năm — mở lên là agent tự biết phải làm gì. Không
cần chọn theo template, chọn theo cái người dựng quen tay.

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
