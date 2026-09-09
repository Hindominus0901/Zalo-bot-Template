# Template trợ lý AI chăm sóc khách hàng trên Zalo

Repo này đang được dựng thành **template** để một coding agent phỏng vấn chủ
doanh nghiệp, rồi sinh ra một bot CSKH nói tiếng Việt như người thật: hỏi trước
khi tư vấn, quan tâm trước khi bán — và **không cụt cỡ khi khách hỏi lệch script**.

Khác bot cũ `agent-cskh-zalo`: ít rào giọng, được nói chuyện đời, được dùng kiến
thức chung. Chỉ khóa tiền, nội bộ, và việc bịa số liệu shop.

Hiện tại đây là bản **nghiên cứu + khung thiết kế**. Chưa phải code chạy được.

## Đọc gì trước

| File | Việc |
|---|---|
| [`docs/01-it-rao-da-dang.md`](docs/01-it-rao-da-dang.md) | Vì sao bot cũ cứng, rào nào giữ, rào nào bỏ |
| [`knowledge/moi-loai-cau-hoi.md`](knowledge/moi-loai-cau-hoi.md) | Mọi kiểu tin đều được đáp — FAQ, teencode, ngoài lề, kho trống |
| [`docs/00-tong-hop-cskh.md`](docs/00-tong-hop-cskh.md) | Bot CSKH trên Zalo làm được gì, thao tác thế nào |
| [`knowledge/khung-khai-thac.md`](knowledge/khung-khai-thac.md) | Khi khách phân vân: khai thác → tư vấn |
| [`knowledge/giong-noi.md`](knowledge/giong-noi.md) | Giọng Việt Nam, vui – hài – để ý; hướng chứ không phải nội quy |
| [`PHONG-VAN.md`](PHONG-VAN.md) | Câu hỏi còn thiếu trước khi viết code |

## Nguồn đang tổng hợp

- Bot cũ: [`Hindominus0901/agent-cskh-zalo`](https://github.com/Hindominus0901/agent-cskh-zalo) — bốn trụ cột, skill CSKH, kho wiki, lớp chặn an toàn, Zalo Bot Creator
- OpenClaw: tách **giọng** (`SOUL.md`) khỏi **luật vận hành** (`AGENTS.md`)
- Zalo Bot Creator API và Zalo OA OpenAPI — hai sản phẩm khác nhau, năng lực khác nhau

## Việc tiếp theo

Trả lời `PHONG-VAN.md` nhóm 0 (Tom, kênh Zalo, template cho ai) và câu 8b (ngoài
hẳn ngành thì xử lý tới đâu). Khung ít-rào / mọi-câu-hỏi đã viết; khi đủ ý thì
dựng runtime.
