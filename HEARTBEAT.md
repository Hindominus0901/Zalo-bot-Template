# Nhịp nội bộ + follow-up có rào

Heartbeat **báo chủ** (thiếu wiki / bàn giao dở). Được nhắn khách **chỉ** hai
nhánh trong `skills/follow-up/SKILL.md` khi `USER.md` đã bật và phiếu đủ điều
kiện. Không broadcast. Không “Nami online”. Không nài lần hai.

Gateway restart: `BOOT.md` — không burst follow-up.

OpenClaw có thể chuyển nội dung file này vào DB (`openclaw doctor --fix`).
**Giữ file workspace làm nguồn.** Máy đã migrate thì sửa file rồi đồng bộ theo
doctor — đừng chỉ sửa trên UI rồi để file lệch.

1. Mở `memory/YYYY-MM-DD.md` hôm nay (và hôm qua nếu cần).
2. Có câu thiếu trang hoặc bàn giao chưa xong → gom **3–8 dòng** cho người trong
   `USER.md`, chữ thường, không nói wiki/token. Gửi đúng kênh họ đã cho
   (nhóm nội bộ / nick chủ). Chưa có kênh → chỉ ghi file, đừng đoán.
3. Follow-up: `USER.md` còn `[CHỜ CHỦ SHOP]` / **tắt** trên nhánh → **bỏ qua**
   quét khách. Đã bật → đọc `skills/follow-up/SKILL.md`, quét `memory/phieu/*.md`
   (bỏ `MAU.md`, `README.md`). Đủ điều kiện + trong giờ → **một** tin Zalo đúng
   `senderId` đó, ghi phiếu `da_gui`. Ảnh CK không kích hoạt sau-đơn.
4. **Nhịp cuối ngày** (sau giờ đóng trong `USER.md`, một lần một ngày): đọc
   `skills/hoc-lai/SKILL.md`. Nó ghi đề xuất vào `memory/de-xuat/` và tóm tắt
   cho chủ. Không có gì đáng đề xuất thì **không viết file, không gửi tin**.
   Đang có khách trong phiên → để nhịp sau.
5. Không có gì mới (cả chủ lẫn khách) → trả `HEARTBEAT_OK`, đừng viết báo cáo rỗng.
6. **Cất phiếu cũ** (nhịp cuối ngày, cùng lúc với `hoc-lai`): phiếu không đổi
   quá **180 ngày** → chuyển sang `memory/phieu/.cu/`. **Không xóa.** Khách cũ
   nhắn lại thì kéo ngược ra rồi đọc như thường.
   **Không cất** phiếu đang có `trang_thai_don` là `cho_ck`, `da_chot_chu` hay
   `dang_giao` — việc chưa xong thì tuổi phiếu không tính. Cũng không cất phiếu
   còn `viec_mo`.
7. Đừng bịa số liệu vào wiki từ báo cáo. Chủ bổ sung rồi coding agent / người
   viết wiki mới được sửa trang.
