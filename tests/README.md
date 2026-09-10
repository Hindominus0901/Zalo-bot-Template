# tests — khớp chữ trong repo, không phải bot sống

Chạy từ gốc repo:

    python3 -m unittest discover -s tests -v
Windows: thay `python3` bằng `py`.

Không cần pip. Xanh = file bắt buộc có mặt, ma trận khớp markdown, config mẫu
`dmPolicy: open`, không commit khóa. **Không** chứng minh Gateway, Zalo, vision,
hay câu trả lời model.

Nick thật: [`docs/04-kich-ban-thu.md`](../docs/04-kich-ban-thu.md). Tiêu chuẩn
mở khách: [`docs/06-tieu-chuan.md`](../docs/06-tieu-chuan.md).
