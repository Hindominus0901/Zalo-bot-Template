# Boot — gateway vừa bật

Checklist ngắn. Hook `boot-md` chạy file này lúc Gateway start. **Không nhắn khách.**
Không “Nami online”, không chào lại inbox im, **không** burst follow-up lúc restart
(follow-up chỉ ở nhịp `HEARTBEAT.md`).

1. Đọc `memory/` hôm qua (và hôm nay nếu có). Có bàn giao / việc mở **chưa xong**?
2. Có, và `USER.md` đã có kênh/nick nhận → tóm 3–8 dòng chữ thường, **chỉ** gửi
   kênh đó (message tool: ghi rõ kênh + người nhận). Không sửa wiki. Xong: `NO_REPLY`.
3. Không có việc / chưa có kênh USER.md / không chắc gửi được → không gửi gì.
   Trả `HEARTBEAT_OK` (hoặc `NO_REPLY` nếu runtime đòi silent token).
4. **Tin còn nợ** — đọc `memory/no-tra-loi.md`. Có dòng **trong 12h** → trả đúng
   `senderId` đó **một** tin: xin lỗi ngắn vì trả muộn, hỏi họ còn cần gì không.
   Rồi xóa dòng. Cũ hơn 12h → **không nhắn khách** (trả lúc đó chỉ làm phiền),
   chỉ gom vào tóm tắt cho chủ ở bước 2, và vẫn xóa dòng.
   Đây là **ngoại lệ duy nhất** của luật "boot không nhắn khách" — vì tin đó là
   tin họ đã gửi thật, không phải mình tự bắt chuyện.
5. **Cookie chết / login lỗi lặp lại** → **dừng thử**. Báo chủ **một lần**:
   cần quét lại mã trên máy đang chạy bot. Đừng thử lại mỗi nhịp, đừng báo lại
   mỗi nhịp. Một lần fail được xử êm vẫn tính là chạy xong — đừng dựa vào trạng
   thái chạy để biết là đang hỏng.
6. Đừng đoán đơn đang treo. Đừng quét phiếu để nhắn khách lúc boot. Trùng
   heartbeat: cùng luật `HEARTBEAT.md`.
