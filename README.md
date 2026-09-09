# Template trợ lý AI chăm sóc khách hàng trên Zalo

Coding agent **phỏng vấn chủ shop (10 chủ đề)**, nhận tài liệu sản phẩm/dịch vụ, rồi
điền workspace OpenClaw. Bot cầm **nick Zalo riêng**, nói như người: hỏi trước
khi tư vấn, không cụt cỡ khi khách lệch script.

Khác `agent-cskh-zalo`: ít rào giọng, được kiến thức chung, AI-first, kênh
`zalouser` (như Tom) — không Bot Creator.

## Chủ shop / coding agent làm gì

1. Đọc [`HUONG-DAN-AGENT.md`](HUONG-DAN-AGENT.md)
2. Bộ câu hỏi xem nhanh: [`docs/bo-cau-hoi.md`](docs/bo-cau-hoi.md) · kịch bản đủ: [`PHONG-VAN.md`](PHONG-VAN.md)
3. File gốc vào `knowledge/raw/`, wiki tách theo `knowledge/CLAUDE.md`
4. Bật nick: [`docs/03-bat-nick.md`](docs/03-bat-nick.md)

Đã khóa kênh và rào: [`docs/quyet-dinh.md`](docs/quyet-dinh.md).

## Brain / wiki / harness nằm ở đâu

| | File |
|---|---|
| Brain | `SOUL.md` · `IDENTITY.md` · `knowledge/persona.md` |
| Wiki | `knowledge/wiki/` ← tách từ `knowledge/raw/` (câu 3) |
| Harness | `AGENTS.md` · `skills/khai-thac/` · `skills/bao-gia/` · `skills/xu-ly-phan-nan/` · `skills/ban-giao/` · `USER.md` |

Chủ shop không cần biết ba chữ đó. Coding agent phỏng vấn theo `PHONG-VAN.md` rồi điền.

## Thiết kế

| File | Việc |
|---|---|
| [`docs/01-it-rao-da-dang.md`](docs/01-it-rao-da-dang.md) | Rào nào giữ, rào nào bỏ |
| [`docs/02-kenh-zalouser.md`](docs/02-kenh-zalouser.md) | Nick cá nhân + OpenClaw |
| [`knowledge/moi-loai-cau-hoi.md`](knowledge/moi-loai-cau-hoi.md) | Mọi kiểu tin đều được đáp |
| [`knowledge/khung-khai-thac.md`](knowledge/khung-khai-thac.md) | Phân vân thì hỏi trước |
| [`SOUL.md`](SOUL.md) | Giọng Việt Nam |
