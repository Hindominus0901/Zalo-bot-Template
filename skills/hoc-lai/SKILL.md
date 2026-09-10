---
name: hoc-lai
description: Cuối ngày đọc lại nhật ký và phiếu, đề xuất bài học + vá sổ cho chủ duyệt. Không tự sửa wiki, không nhắn khách.
chi-goi-khi-duoc-yeu-cau: true
---

# Học lại — một nhịp cuối ngày

Không phải việc lúc chat khách. Chỉ chạy ở **nhịp heartbeat cuối ngày**, ngoài
giờ khách (giờ lấy từ `USER.md`). Đang có khách trong phiên → bỏ qua, để nhịp sau.

Việc của skill này là **đề xuất**, không phải sửa. Chủ duyệt xong thì người
(hoặc coding agent) mới sửa sổ.

## Khi nào dùng

Heartbeat gọi, một lần một ngày, sau giờ đóng. Không gọi lúc boot. Không gọi
giữa lượt khách. Không gọi hai lần một ngày.

## Cách làm

1. Đọc `memory/YYYY-MM-DD.md` hôm nay. Không có file → **dừng, không viết gì**.
2. Đọc những phiếu `memory/phieu/*.md` có `updated` là hôm nay (bỏ `MAU.md`,
   `README.md`).
3. Viết `memory/de-xuat/YYYY-MM-DD.md`, ba mục — mục nào không có thì bỏ hẳn,
   đừng để đầu mục rỗng:

```markdown
# Đề xuất 2026-09-10

## Bài học cho MEMORY.md
- khách hỏi phí tỉnh trước khi hỏi giá món — nên có sẵn câu phí tỉnh

## Vá trang đã có
- knowledge/wiki/public/ship.md
  cũ: "Nội thành 30k"
  mới: "Nội thành 30k. Ngoại thành cùng tỉnh 45k"
  vì: chủ nhắn trong nhóm nội bộ lúc ~16h

## Trang còn thiếu
- phí ship Đà Nẵng — 3 khách hỏi trong tuần, sổ chưa có
```

4. `USER.md` đã có kênh nội bộ → gửi tóm tắt **3–8 dòng** chữ thường vào đúng
   kênh đó. Chưa có kênh → chỉ để lại file, không đoán chỗ gửi.
5. Không có gì đáng đề xuất → **im**. Trả `HEARTBEAT_OK`. Đừng viết file rỗng,
   đừng gửi tin "hôm nay không có gì".

## Chỗ hay vấp

- **Đừng sửa `knowledge/wiki/`.** Skill này chỉ ghi vào `memory/de-xuat/`.
  Chủ chốt số rồi mới có người sửa trang. Luật này đã có ở `HEARTBEAT.md` mục 5.
- **Đừng đẻ số.** Mục *Vá trang* chỉ được chép số **đúng chữ chủ đã nhắn** hoặc
  số đã nằm trong file chủ gửi. Suy ra, làm tròn, "shop kiểu này thường" — không.
- **Đừng chép nguyên chat khách.** Ghi bài học, không ghi nhật ký. Một luật
  khái quát + một vế *vì sao*. Không tên khách, không SĐT, không số CK.
- **Đừng đề xuất trang mới cho câu hỏi một lần.** Ba lần trở lên mới đáng một
  trang sổ.
- Đề xuất hôm qua chủ chưa duyệt → **đừng lặp lại y nguyên** hôm nay. Gộp vào
  một dòng "còn chờ chủ chốt: …".
- Đây là việc nền, chạy model rẻ cũng được. Không cần đọc `hoi-thoai-mau.md`
  hay `giong-noi.md` — không ai đọc bản đề xuất ngoài chủ.

## Kiểm lại

- `memory/de-xuat/YYYY-MM-DD.md` có tồn tại **chỉ khi** thật sự có đề xuất.
- `git status` sau khi chạy: **không** có thay đổi nào trong `knowledge/`.
- Mỗi dòng *Vá trang* truy ngược được về một câu của chủ hoặc một file trong
  `knowledge/raw/`. Không truy được thì dòng đó sai, bỏ.
