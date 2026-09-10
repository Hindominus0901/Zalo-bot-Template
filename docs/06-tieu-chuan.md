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

## Cửa 3 — máy (dòng 35–50)

Sáu dòng trên là giọng và phán đoán. Máy thì hỏng kiểu khác: không sai câu nào
cả, chỉ mất tin, phình phiếu, hoặc đội tiền. Đạt khi:

7. **Nền prompt không vỡ.** Sau ~50 lượt một phiên, phần đầu prompt phải đọc lại
   từ cache. Tiền không giảm = có gì đó bay hơi lọt vào nền (`docs/12`).
8. **Không mất tin.** Tắt gateway rồi bật lại: tin trong 12h được trả một lần,
   cũ hơn thì chỉ báo chủ. Không burst.
9. **Phiếu không phình.** Chat dài mà `size` / `trang_thai_don` / `ban_giao` vẫn
   còn nguyên sau khi phiếu chạm trần.
10. **Bàn giao không tắt bot.** Đang chờ người thật một việc, hỏi việc khác vẫn
    trả bình thường.
11. **Chỉ mục khớp thư mục.** `scripts/lam-chi-muc.sh` chạy xong `git diff` phải
    sạch. Lệch = bot đang tra một tờ không tồn tại.
12. **Vòng học không đụng sổ.** Sau một đêm, `git status` trong `knowledge/`
    phải sạch. Có thay đổi = skill `hoc-lai` đang tự sửa số, hỏng.

Cửa 3 không cần xong trước khi mở khách — nhưng cần xong trước khi để bot chạy
**không có người ngó** qua đêm.

Chưa xong cửa 2: **chưa** bảo chủ mở khách. Unittest xanh một mình không đủ.
