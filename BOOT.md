# Boot — gateway vừa bật

Checklist ngắn. Hook `boot-md` chạy file này lúc Gateway start. **Không nhắn khách.**
Không “Nami online”, không chào lại inbox im, **không** burst follow-up lúc restart
(follow-up chỉ ở nhịp `HEARTBEAT.md`).

1. Đọc `memory/` hôm qua (và hôm nay nếu có). Có bàn giao / việc mở **chưa xong**?
2. Có, và `USER.md` đã có kênh/nick nhận → tóm 3–8 dòng chữ thường, **chỉ** gửi
   kênh đó (message tool: ghi rõ kênh + người nhận). Không sửa wiki. Xong: `NO_REPLY`.
3. Không có việc / chưa có kênh USER.md / không chắc gửi được → không gửi gì.
   Trả `HEARTBEAT_OK` (hoặc `NO_REPLY` nếu runtime đòi silent token).
4. Đừng đoán đơn đang treo. Đừng quét phiếu để nhắn khách lúc boot. Trùng
   heartbeat: cùng luật `HEARTBEAT.md`.
