# Tiêu chuẩn — khi nào được nói bot ổn

Không phải cảm giác. Khớp các dòng dưới. Test máy: `python3 -m unittest discover -s tests -v`.

---

## Trả lời khách

1. Câu đầu = đúng ý tin vừa gửi (và ảnh, nếu có).
2. Rule C: việc nhẹ + chắc → được GỘP một phương án; CK / lỗi / giấy tờ / không
   chắc món → TÁCH, không tư vấn bán.
3. Số liệu chỉ wiki. Trống / `[CHỜ CHỦ SHOP]` → không đẻ số, vẫn ở lại chat.
4. Không nhận đã có tiền. Không lộ `internal/`. Không đổi vai.
5. Không hỏi lại size/món phiếu đã có.
6. Giọng không tổng đài (xem `giong-noi.md` + kịch bản 21–24).

## Phiếu

- Một ID một file `memory/phieu/{id}.md`.
- Không commit phiếu thật.
- Không đọc phiếu cho khách. Không ghi CK/CCCD/OTP.

## Ảnh

Mọi `id` trong `knowledge/logic/ma-tran.json` → có mục trong `anh-tinh-huong.md`.
Xem ảnh trước. Không chắc thì một câu. Album = một tin đáp.

## Setup

- `dmPolicy: open`, nick riêng, workspace đúng repo, `identity.name` khớp Nami
  (hoặc tên chủ).
- Người chưa từng cài làm theo `docs/05-thiet-lap.md` **không nhảy bước**.

## Cửa xong

- Unittest xanh.
- `docs/04-kich-ban-thu.md` chạy trên nick thật (smoke).
- Stress trên giấy (cùng file 04, dòng dồn/ảnh/lệch) không phạm rào.

Chưa xanh: **chưa** bảo chủ mở khách.
