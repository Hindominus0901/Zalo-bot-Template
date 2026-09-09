# Template trợ lý AI chăm sóc khách hàng trên Zalo

Coding agent **phỏng vấn chủ shop (10 câu, hỏi sâu)**, nhận file/kiến thức, rồi
điền workspace OpenClaw. Bot cầm **nick Zalo riêng**, nói như người: hỏi trước
khi tư vấn, không cụt cỡ khi khách lệch script.

Khác `agent-cskh-zalo`: ít rào giọng, được kiến thức chung, AI-first, kênh
`zalouser` (như Tom) — không Bot Creator.

## Chủ shop / coding agent làm gì

1. Đọc [`HUONG-DAN-AGENT.md`](HUONG-DAN-AGENT.md)
2. Phỏng vấn [`PHONG-VAN.md`](PHONG-VAN.md) — câu dài về sản phẩm/dịch vụ; đào từng câu; câu 3 xin tài liệu
3. File gốc vào `knowledge/raw/`, wiki tách theo `knowledge/CLAUDE.md`

Đã khóa kênh và rào: [`docs/quyet-dinh.md`](docs/quyet-dinh.md).

## Đọc thêm (thiết kế)

| File | Việc |
|---|---|
| [`docs/01-it-rao-da-dang.md`](docs/01-it-rao-da-dang.md) | Rào nào giữ, rào nào bỏ |
| [`docs/02-kenh-zalouser.md`](docs/02-kenh-zalouser.md) | Nick cá nhân + OpenClaw |
| [`knowledge/moi-loai-cau-hoi.md`](knowledge/moi-loai-cau-hoi.md) | Mọi kiểu tin đều được đáp |
| [`knowledge/khung-khai-thac.md`](knowledge/khung-khai-thac.md) | Phân vân thì hỏi trước |
| [`knowledge/giong-noi.md`](knowledge/giong-noi.md) | Giọng Việt Nam |
