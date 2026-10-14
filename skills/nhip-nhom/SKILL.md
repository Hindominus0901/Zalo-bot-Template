---
name: nhip-nhom
description: Nhịp chủ động trong nhóm Zalo của shop — nhắc lịch, sự kiện, hạn chót có trong sổ. Một tin một nhóm một ngày, chỉ nói cái có trong sổ. Mặc định tắt. Không nhắn hàng loạt vào inbox riêng.
chi-goi-khi-duoc-yeu-cau: true
---

# Nhịp nhóm — chủ động, nhưng có rào

Chỉ chạy lúc **heartbeat** (`HEARTBEAT.md`), và chỉ khi `USER.md` mục *Nhóm*
đã **bật**. Boot / restart **không** gửi. Đây là nhánh duy nhất bot tự mở lời
trong nhóm mà không ai gọi — nên mọi điều kiện dưới đều là **và**.

Nhánh này chỉ đụng **nhóm**. Inbox riêng vẫn chỉ có hai nhánh `follow-up`.

## Khi nào gửi

Đủ **tất cả**:

1. Nhóm có dòng trong `USER.md` mục *Nhóm*, cột nhắc = **bật**. Không có → không gửi.
2. Có **việc thật** để nói, nằm trong sổ `knowledge/wiki/public/` (tra bảng
   *Sổ có những tờ nào*): buổi / lịch / sự kiện / hạn chót / đợt mở bán sắp tới,
   và đã tới mốc *nhắc trước* chủ ghi trong `USER.md`.
3. Đang trong **giờ được nhắn nhóm** ở `USER.md`. Trống → không gửi.
4. **Không** phải ngày nghỉ / Tết trong `USER.md`.
5. Nhóm đó **chưa nhận tin nào hôm nay** — đọc `memory/nhom/{groupId}.md`.

Thiếu bất kỳ điều nào → im, không ghi gì, để nhịp sau. Không dồn gửi bù.

## Cách làm

1. Đọc `USER.md` mục *Nhóm*: nhóm nào bật, giờ nhắn, nhắc trước bao lâu.
2. Với từng nhóm, đọc `memory/nhom/{groupId}.md`: lần gửi gần nhất, đã nhắc việc nào.
3. Lấy nội dung **từ sổ**: giờ, ngày, tên việc, link nếu sổ có. Sổ không có →
   **không gửi nhóm đó**, ghi một dòng vào `memory/` ngày để chủ biết lịch đang
   trống. Không tự nghĩ ra giờ, ngày, giá.
4. Soạn theo `SOUL.md` — giọng người, ngắn, một việc. Viết riêng từng nhóm,
   không copy một câu chữ qua nhiều nhóm.
5. Gửi **lần lượt**, giãn cách giữa các nhóm, không bắn cùng lúc.
6. Gửi xong ghi `memory/nhom/{groupId}.md`: giờ gửi (`YYYY-MM-DD HH:MM`), đã nhắc việc nào.
7. Gửi lỗi ở một nhóm → **dừng cả vòng**, báo chủ theo `ban-giao`, không thử lại cả loạt.

## Chỗ hay vấp

- **Một tin một nhóm một ngày.** Hai việc thì gộp một tin.
- **Không nhắn hàng loạt vào inbox riêng.** Nhóm im lâu thì thôi — nhắn riêng
  từng người trong nhóm là cách nhanh nhất mất nick.
- **Không lần hai.** Nhắc rồi mà nhóm im — chuyện thường, không phải lý do nhắc lại.
- **Không "Nami online"**, không chào buổi sáng rỗng, không tin cho nhóm đỡ vắng.
  Không có việc thật thì im là đúng.
- **Không gửi số tài khoản, mã QR, link thanh toán.**
- Nhóm đang có người nói chuyện → để họ nói xong rồi nhịp sau.
- Chủ vừa tự nhắc việc đó trong nhóm → **đừng nhắc lại**. Đọc
  `memory/nhom/{groupId}.md` và tin gần nhất trong nhóm trước khi soạn.

**Kiểm lại:** đủ cả năm điều kiện chưa, nội dung tin truy được về một dòng trong sổ không, và nhóm này hôm nay đã nhận tin nào chưa?
