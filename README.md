# Template trợ lý AI chăm sóc khách hàng trên Zalo

Repo này đang được dựng thành **template** để một coding agent phỏng vấn chủ
doanh nghiệp, rồi sinh ra một bot CSKH nói tiếng Việt như người thật: hỏi trước
khi tư vấn, quan tâm trước khi bán.

Hiện tại đây là bản **nghiên cứu + khung thiết kế**. Chưa phải code chạy được.

## Đọc gì trước

| File | Việc |
|---|---|
| [`docs/00-tong-hop-cskh.md`](docs/00-tong-hop-cskh.md) | Bot CSKH trên Zalo làm được gì, thao tác thế nào, cái gì đã có ở bot cũ, cái gì còn thiếu |
| [`knowledge/khung-khai-thac.md`](knowledge/khung-khai-thac.md) | Máy trạng thái: khai thác → đủ bối cảnh → tư vấn → chốt / bàn giao |
| [`knowledge/giong-noi.md`](knowledge/giong-noi.md) | Giọng Việt Nam, tính cách vui – hài – luôn quan tâm |
| [`PHONG-VAN.md`](PHONG-VAN.md) | Câu hỏi còn thiếu trước khi viết code |

## Nguồn đang tổng hợp

- Bot cũ: [`Hindominus0901/agent-cskh-zalo`](https://github.com/Hindominus0901/agent-cskh-zalo) — bốn trụ cột, skill CSKH, kho wiki, lớp chặn an toàn, Zalo Bot Creator
- OpenClaw: tách **giọng** (`SOUL.md`) khỏi **luật vận hành** (`AGENTS.md`)
- Zalo Bot Creator API và Zalo OA OpenAPI — hai sản phẩm khác nhau, năng lực khác nhau

## Việc tiếp theo

Trả lời các câu trong `PHONG-VAN.md`. Khi đủ ý, agent sẽ bắt đầu dựng template
(persona, skill khai thác, gợi ý tương tác, rồi mới tới code).
