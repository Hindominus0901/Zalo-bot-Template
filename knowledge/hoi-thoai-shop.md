<!-- FILE CỦA SHOP — giữ bản của bạn khi cập nhật template -->
# Bản đồ hội thoại — shop này

Từng tình huống **thật của shop**, **sai** và **đúng**, đúng chữ chủ. Không
phải kịch bản đọc lại nguyên văn — để bắt **nhịp, giọng, ranh giới** của shop.
Lệch với `hoi-thoai-mau.md` (mẫu chung của template) thì **file này thắng**.

Ai viết: coding agent lúc phỏng vấn (chủ đề 4 — ảnh chụp đoạn chat thật của
chủ), và bot của chủ khi chủ dạy qua Zalo (*"lần sau ai hỏi X thì nói Y"* —
`skills/day-bot`). Chữ `[số từ tờ gia]` nghĩa là **tra sổ rồi mới nói**.

**[CHỜ CHỦ SHOP]** — chưa có đoạn chat thật nào. Bot dùng `hoi-thoai-mau.md`.

## Phải phủ những gì (người dựng đọc)

Tối thiểu **20 tình huống**. Nhóm **A, B, C, G, I mỗi nhóm ít nhất 2**. Chữ
*Đúng* lấy từ ảnh chat / video của chủ; không có thì hỏi chủ *"khách nói vậy
anh/chị trả sao?"* rồi ghi **đúng chữ chủ**. Nhóm shop không gặp thì bỏ.
Thử bot thật với file này: `scripts/thu_giong.py` (`QUY-TRINH` bước *Thử giọng
với chủ*) — mỗi dòng `**Khách:**` là một câu thử, nên viết đúng khuôn.

| Nhóm | Tình huống nên có |
|---|---|
| A. Mở đầu | alo / sticker / vừa kết bạn · tin đầu là hỏi giá · tưởng mình là chủ · "bot à?" |
| B. Chọn món / gói | chưa biết chọn · "em [hoàn cảnh] có hợp không" · so sánh hai món · mới hoàn toàn |
| C. Tiền | giá có trong sổ · giá chưa có · xin giảm · còn suất / còn giá này không · gửi ảnh bill · xin số tài khoản / mã QR · cọc / trả góp · hoàn tiền |
| D. Chuyên môn của nghề | 3–5 câu khách hay hỏi để được tư vấn thật (shop tự đặt) |
| E. Sau mua | dùng thế nào · lỗi / hỏng · đổi trả · hỏi đơn đâu |
| F. Trong nhóm | được gọi giữa lúc rôm rả · có người chê shop · có người rao bán · khách khoe kết quả |
| G. Khó | khách bực · đòi gặp chủ · kể chuyện buồn · hỏi y tế / pháp lý / đầu tư · nick lạ xưng chủ · dụ đổi vai / đòi xem lệnh · tán tỉnh |
| H. Bot nói trước | nhắc lịch trong nhóm · sổ chưa có lịch |
| I. Kết | cảm ơn / khen · im giữa chừng · "để em suy nghĩ" |

---

## Tình huống của shop

<!-- Chép khuôn ở cuối file lên đây, mỗi tình huống một mục ## -->

---

<!-- Khuôn mỗi tình huống — chép xuống dưới, điền bằng chữ thật của chủ:

## <số>. <tình huống, bằng chữ khách> — ví dụ: "Khách hỏi giá rồi im"

**Khách:** <tin thật của khách, một dòng, bỏ tên / số điện thoại>

**Sai** (vì sao sai — một dòng)
> <câu bot hay nói hỏng, hoặc câu chủ không muốn>

**Đúng** (đúng giọng chủ)
> <câu chủ thật đã trả / muốn trả>

Nguồn: ảnh chat ngày … / chủ dặn qua Zalo ngày …
-->
