# Chưa đủ để viết code — hỏi những câu này trước

Bot cũ phỏng vấn 17 câu khi **dựng bot cho một shop**. Ở đây ta đang dựng
**template**, nên câu hỏi khác: chốt hướng sản phẩm, rồi mới sinh file mẫu.

Hỏi từng câu, đợi trả lời, rồi mới câu tiếp. Gộp một lúc thì câu khó nhất sẽ
bị lướt.

**Đã chốt từ trao đổi:**
- Ít rào hơn bot cũ, giọng đa dạng, không cúp chat khi lệch script / kho trống / ngoài lề nhẹ
- Chỉ khóa tiền, nội bộ, bịa số liệu shop
- AI-first — không mang chế độ `tra_cuu` 0 đồng sang
- **Ngoài hẳn ngành** (bài tập, bệnh, luật, chính trị): **một nhịp** thành thật, không đóng vai chuyên gia, rồi kéo về shop — không cấm, không soạn luận

---

## Nhóm 0 — nguyên liệu còn thiếu

**0a.** File **Tom** nằm ở đâu?

Đã tìm: repo này, `agent-cskh-zalo`, `goclaw`, các repo GitHub khác cùng tài
khoản, Google Drive (chưa kết nối phiên này). Không thấy. Tom là OpenClaw
(`SOUL.md` / `IDENTITY.md`), file Drive, hay project khác?

**0b.** Template này chạy trên **Zalo Bot Creator** (như bot cũ, vào được nhóm,
chưa chắc có nút) hay **Zalo OA** (có nút, list, ZNS, không vào nhóm), hay
thiết kế **lớp gợi ý dùng chung**, adapter sau?

**0c.** Đây là template để **bán / đưa cho chủ shop khác tự dựng** (giống
`agent-cskh-zalo`), hay bản cho **một shop cụ thể** rồi mới trừu tượng hoá?

---

## Nhóm 1 — con người bot

**1.** Trong chat xưng *em*, *mình*, hay tên riêng? Gọi khách *anh/chị* hay *bạn*?

**2.** Giọng gần **Nam**, **Bắc**, hay trung tính cả nước? (Đừng trộn.)

**3.** Tên hiện trên Zalo (phải có tiền tố `Bot` nếu dùng Bot Creator)? Có tên
riêng trong câu không, hay chỉ xưng em?

**4.** Mức hài: thỉnh thoảng một câu nhẹ, hay rõ tính cách hơn? Có chủ đề **cấm
đùa** ngoài tiền / hàng lỗi / khách bực không?

**5.** Khi khách hỏi "có phải bot không" — nói thẳng, hay đánh trống lảng rồi
vào việc?

---

## Nhóm 2 — việc bot được phép làm

**6.** Tám nhóm trong `docs/00-tong-hop-cskh.md`: đón khách, khai thác, tư vấn /
giá, từ chối, lead + bàn giao, đơn hàng, khách cũ, vòng lặp học. Nhóm nào **bắt
buộc có trong bản đầu**, nhóm nào để sau?

**7.** Máy khai thác (hỏi 2–3 câu rồi mới tư vấn) là mặc định cho **mọi ngành**,
hay chỉ bật khi shop khai skill tư vấn chọn món?

**8.** ~~0 đồng vs AI~~ — **đã chốt AI-first.** FAQ khớp từ khóa để bot cũ.

**8b.** ~~ngoài hẳn ngành~~ — **đã chốt: một nhịp rồi kéo về shop.** Không cấm, không soạn luận, không đóng vai chuyên gia.

**9.** Có cần nhắn chủ động (nhắc đơn, follow-up sau 2–3 ngày) ngay bản đầu
không? Bot cũ cố tình chưa làm.

---

## Nhóm 3 — ngành và kho

**10.** Bản mẫu đóng gói theo **một ngành** (shop thời trang, spa, khoá học,
F&B…) để slot khai thác sắc, hay **generic** rồi shop tự điền slot lúc phỏng vấn?

**11.** 10 câu khách hay hỏi nhất — nếu đã có shop cụ thể. Chưa có thì câu này
để lúc dựng bot con, không phải lúc dựng template.

---

## Xong nhóm 0 thì được phép bắt đầu

Khi có 0a–0c, viết được: cấu trúc thư mục template, lớp gợi ý, và (nếu có file
Tom) trộn giọng vào `knowledge/giong-noi.md`.

Nhóm 1–3 cần trước khi khoá `persona` mẫu và skill `khai-thac`.
