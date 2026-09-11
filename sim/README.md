# Giả lập — chạy luật máy mà không cần nick Zalo

Repo này là kho chữ; bot thật chạy trên OpenClaw. Giả lập ở đây **chạy phần máy
tất định** để bắt lỗi trước khi đụng tới nick thật.

```bash
python3 -m sim.chay nen      # nền prompt to bao nhiêu, có gì bay hơi lọt vào
python3 -m sim.chay nhip     # bảng rào follow-up / bàn giao / sổ nợ
python3 -m sim.chay chat "alo shop"
```

Chỉ cần `python3`, không cần cài gì.

---

## Kiểm được gì, không kiểm được gì

| Giả lập kiểm được (não `luat`, không cần key) | Chỉ kiểm được khi cắm model (`--nao claude`) |
|---|---|
| Rào follow-up: giờ, ngày nghỉ, cờ phiếu, delay | Giọng, lầy, tắt hài đúng lúc |
| Ảnh CK không kích hoạt nhánh sau-đơn | 10 bước tư duy, GỘP/TÁCH |
| Sổ tin nợ: 12h thì trả, cũ hơn chỉ báo chủ | Có bịa số không |
| Cờ bàn giao hết hạn 24h mà không tự mở quyền | Từ chối có thành bức tường không |
| Gộp tin dồn, chia tin không cắt mã đơn | |
| Nhóm phải gọi tên mới trả | |
| Khóa phiên, id phiếu | |
| Nền prompt: kích cỡ, vân tay, thứ bay hơi lọt vào | |

Cột phải cần `pip install anthropic` và một API key:

```bash
export ANTHROPIC_API_KEY=...
python3 -m sim.chay chat "uống panadol với bia được không shop" --nao claude
```

Nó in luôn `token vào / đọc lại từ cache / ra`. Nhắn vài lượt liên tiếp mà
`cache` vẫn 0 là nền đang vỡ — xem `docs/12-prompt-va-cache.md`.

---

## File

| File | Việc |
|---|---|
| `kho.py` | Đọc `USER.md`, phiếu, ma trận. Chỗ duy nhất biết định dạng file |
| `nhip.py` | Quyết định follow-up / bàn giao quá hạn / sổ nợ. Thuần, không gọi model |
| `kenh.py` | Gộp tin dồn, khóa phiên, nhóm gọi tên, chia tin |
| `nen.py` | Dựng prompt ba tầng, soi thứ bay hơi lọt vào nền |
| `nao.py` | Não tháo rời: `luat` hoặc `claude` |
| `chay.py` | CLI |

Test: `tests/test_gia_lap.py` — khác mọi file test kia ở chỗ nó chạy **luật**,
không khớp chữ. Đã đục lỗ thử (bỏ rào ngày nghỉ, cho ảnh CK tính là đơn) để
chắc test không rỗng.

---

## Giả lập **không** thay được nick thật

Nó không biết gì về Zalo: không đăng nhập, không gửi tin, không biết cookie chết
hay chưa. Xong giả lập vẫn phải chạy `docs/04-kich-ban-thu.md` trên nick.
