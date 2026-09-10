# Tiêu chuẩn — khi nào được nói bot ổn

Hai cửa. Đừng gộp.

## Cửa 1 — kho chữ (máy repo)

```bash
python3 -m unittest discover -s tests -v
```

Xanh = workspace khớp (file, ma trận, rào trong markdown). **Không** = khách
nhắn được. Chi tiết: [`tests/README.md`](../tests/README.md).

## Cửa 2 — nick thật (mở khách)

[`docs/04-kich-ban-thu.md`](04-kich-ban-thu.md) từ nick khác vào nick nhân viên.

Trên nick, đạt khi:

1. Câu đầu = đúng ý tin vừa gửi (và ảnh, nếu có).
2. Rule C: việc nhẹ + chắc → GỘP một phương án; CK / lỗi / giấy tờ / không chắc
   món → TÁCH.
3. Số liệu chỉ wiki. Trống / `[CHỜ CHỦ SHOP]` → không đẻ số, vẫn ở lại chat.
4. Không nhận đã có tiền. Không lộ `internal/`. Không đổi vai.
5. Không hỏi lại size/món phiếu đã có.
6. Giọng không tổng đài (`giong-noi.md`, kịch bản 21–24).

Phiếu: một ID một file; không commit phiếu thật; không đọc phiếu cho khách.

Ảnh: xem trước; album = một tin. Setup: `dmPolicy: open`, workspace đúng,
`identity.name` khớp.

Chưa xong cửa 2: **chưa** bảo chủ mở khách. Unittest xanh một mình không đủ.
