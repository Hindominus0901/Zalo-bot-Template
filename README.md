# Template trợ lý AI chăm sóc khách hàng trên Zalo

Repo này đang được dựng thành **template** để một coding agent phỏng vấn chủ
doanh nghiệp, rồi sinh ra một bot CSKH nói tiếng Việt như người thật: hỏi trước
khi tư vấn, quan tâm trước khi bán — và **không cụt cỡ khi khách hỏi lệch script**.

Khác bot cũ `agent-cskh-zalo`: ít rào giọng, được nói chuyện đời, được dùng kiến
thức chung. Chỉ khóa tiền, nội bộ, và việc bịa số liệu shop. Kênh là **nick Zalo
cá nhân** (OpenClaw + `zalouser`), không phải Bot Creator.

Hiện tại đây là bản **nghiên cứu + khung thiết kế**. Chưa phải code chạy được.

## Đọc gì trước

| File | Việc |
|---|---|
| [`docs/01-it-rao-da-dang.md`](docs/01-it-rao-da-dang.md) | Vì sao bot cũ cứng, rào nào giữ, rào nào bỏ |
| [`knowledge/moi-loai-cau-hoi.md`](knowledge/moi-loai-cau-hoi.md) | Mọi kiểu tin đều được đáp — FAQ, teencode, ngoài lề, kho trống |
| [`docs/02-kenh-zalouser.md`](docs/02-kenh-zalouser.md) | Nick Zalo cá nhân cầm bởi OpenClaw `zalouser`, như Tom |
| [`knowledge/khung-khai-thac.md`](knowledge/khung-khai-thac.md) | Khi khách phân vân: khai thác → tư vấn |
| [`knowledge/giong-noi.md`](knowledge/giong-noi.md) | Giọng Việt Nam, vui – hài – để ý; hướng chứ không phải nội quy |
| [`PHONG-VAN.md`](PHONG-VAN.md) | Câu hỏi còn thiếu trước khi viết code |

## Nguồn đang tổng hợp

- Bot cũ: [`Hindominus0901/agent-cskh-zalo`](https://github.com/Hindominus0901/agent-cskh-zalo) — bốn trụ cột, skill CSKH, kho wiki, lớp chặn an toàn, Zalo Bot Creator
- OpenClaw: tách **giọng** (`SOUL.md`) khỏi **luật vận hành** (`AGENTS.md`); kênh **zalouser** (nick cá nhân, QR login)
- Zalo Bot Creator / OA — đã đối chiếu rồi **không dùng** cho bản này

## Việc tiếp theo

Trả lời `PHONG-VAN.md`: file Tom / workspace OpenClaw (0a), template cho ai (0c).
Nick riêng + kênh zalouser + khung ít-rào đã chốt.
