# Bắt đầu — đọc cái này trước

Anh/chị **không cần biết máy tính**. Không phải gõ lệnh, không phải mở
PowerShell hay Terminal. Một trợ lý AI sẽ dẫn từng bước, việc máy móc nó tự làm.

## Ba bước để bắt đầu

1. **Giải nén** file zip vừa nhận.
   Windows: chuột phải vào file → *Extract All* (*Giải nén tất cả*) → *Extract*.
   Mac: bấm đúp vào file.
2. **Cài app Codex** của OpenAI (Windows hoặc Mac) — tải ở trang Codex của
   OpenAI (chatgpt.com/codex), đăng nhập bằng tài khoản ChatGPT có trả phí.
   Không cần cài gì khác, không cần mở PowerShell.
   *(Dùng Claude cũng được — app Claude, tab Code. Riêng Windows thì nó đòi cài
   thêm "Git for Windows"; trợ lý sẽ chỉ.)*
3. Mở app → chọn **mở thư mục** (Open folder) → chọn thư mục vừa giải nén → gõ
   vào ô chat:

   > bắt đầu dựng bot

Từ đó trợ lý dẫn anh/chị, **mỗi lần một việc**.

## Không hiểu chỗ nào → chụp màn hình gửi vào

- **Windows:** bấm **Windows + Shift + S**, kéo chọn vùng, rồi bấm **Ctrl + V**
  vào ô chat.
- **Mac:** bấm **Cmd + Shift + 4**, kéo chọn vùng; ảnh hiện ngoài màn hình nền,
  kéo ảnh vào ô chat.
- **Điện thoại:** chụp màn hình, gửi vào **Cloud của tôi** trên Zalo, mở Zalo
  trên máy tính, kéo ảnh vào ô chat.

**Đừng** chụp gửi: mã AI (dạng `sk-…`), mật khẩu VPS, mã QR đăng nhập Zalo.
Mấy thứ đó trợ lý sẽ mở **Notepad** cho anh/chị dán vào — không dán vào chat.

## Thứ tự sẽ làm

1. Thuê **máy chủ chạy 24/7** (VPS) ở **123host.vn** — gói Cloud VPS 2 GB,
   Ubuntu. 123host gửi email có địa chỉ IP và mật khẩu. Trợ lý chỉ từng nút.
2. Mở **tài khoản OpenAI API** (platform.openai.com), nạp tiền, tạo mã. Khác
   gói ChatGPT Plus — nạp riêng.
3. Tạo **nick Zalo riêng cho bot** (cần một SIM riêng).
4. Trợ lý tự nối hết lại. Anh/chị chỉ: dán mật khẩu VPS và mã OpenAI vào
   Notepad nó mở, quét một mã bằng điện thoại, nhắn một mã ngắn từ nick của
   mình, nhắn thử. **Không cần** VNC hay console của 123host.
5. **Kể về shop** — trợ lý hỏi, anh/chị trả lời, gửi bảng giá / ảnh nếu có.
   Bot học ngay, nhắn thử được ngay.

Cần chuẩn bị gì trước: [`CHUAN-BI.md`](CHUAN-BI.md).

---

*Trợ lý AI đọc: làm theo [`dung-bot/QUY-TRINH.md`](dung-bot/QUY-TRINH.md). `AGENTS.md` là não của bot Zalo, không phải hướng dẫn cho bạn.*
