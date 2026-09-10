# Sau phỏng vấn — bật nick cho khách nhắn

Nói với chủ shop bằng bước bấm, ít tên phần mềm. **Người chưa từng cài:** làm đúng
[`05-thiet-lap.md`](05-thiet-lap.md) (Windows/Mac, QR, lỗi hay gặp). Kỹ thuật kênh:
[`02-kenh-zalouser.md`](02-kenh-zalouser.md).

**Chưa xong phỏng vấn thì chưa bước này.** Còn `[CHỜ CHỦ SHOP]` là chưa bật.

---

## 1. Máy không tắt

Nick cá nhân: máy/VPS tắt là **mất tin lúc đó**. Thử thì máy để mở. Khách thật thì máy chạy suốt.

## 2. Cài chỗ bot ngồi (nếu chưa có)

OpenClaw Gateway trên máy đó. Workspace = thư mục bot của shop (repo này sau khi đã điền).

Merge `config/openclaw.zalouser.example.json5` vào config máy: `dmPolicy` phải là
**open** (khách lạ nhắn vào được).

## 3. Nick nhân viên

Nick Zalo **riêng**, số riêng. Không cầm nick chính của chủ.

## 4. Quét QR

Trên máy Gateway:

```bash
openclaw plugins install @openclaw/zalouser
openclaw channels login --channel zalouser
```

Chủ **tự quét** bằng app nick nhân viên. Đừng nhận ảnh QR/cookie về chat.

## 5. Nhắn thử

Từ một nick Zalo khác, chạy hết [`04-kich-ban-thu.md`](04-kich-ban-thu.md).
Sai số liệu thì sửa wiki, không sửa bằng đoán.

## 6. Nói với chủ những gì bot không làm

Không tự nhận đã có tiền. Không tự bớt giá. Không hứa ngày giao nếu wiki không có.
Tắt máy = mất tin.
