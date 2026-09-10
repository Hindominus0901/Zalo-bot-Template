# Nhịp nội bộ + follow-up có rào

Heartbeat **báo chủ** (thiếu wiki / bàn giao dở). Được nhắn khách **chỉ** hai
nhánh trong `skills/follow-up/SKILL.md` khi `USER.md` đã bật và phiếu đủ điều
kiện. Không broadcast. Không “Nami online”. Không nài lần hai.

Gateway restart: `BOOT.md` — không burst follow-up.

1. Mở `memory/YYYY-MM-DD.md` hôm nay (và hôm qua nếu cần).
2. Có câu thiếu trang hoặc bàn giao chưa xong → gom **3–8 dòng** cho người trong
   `USER.md`, chữ thường, không nói wiki/token. Gửi đúng kênh họ đã cho
   (nhóm nội bộ / nick chủ). Chưa có kênh → chỉ ghi file, đừng đoán.
3. Follow-up: `USER.md` còn `[CHỜ CHỦ SHOP]` / **tắt** trên nhánh → **bỏ qua**
   quét khách. Đã bật → đọc `skills/follow-up/SKILL.md`, quét `memory/phieu/*.md`
   (bỏ `MAU.md`, `README.md`). Đủ điều kiện + trong giờ → **một** tin Zalo đúng
   `senderId` đó, ghi phiếu `da_gui`. Ảnh CK không kích hoạt sau-đơn.
4. Không có gì mới (cả chủ lẫn khách) → trả `HEARTBEAT_OK`, đừng viết báo cáo rỗng.
5. Đừng bịa số liệu vào wiki từ báo cáo. Chủ bổ sung rồi coding agent / người
   viết wiki mới được sửa trang.
