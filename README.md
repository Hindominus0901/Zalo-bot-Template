# Template trợ lý AI chăm sóc khách hàng trên Zalo

Coding agent **phỏng vấn chủ shop (10 chủ đề)**, nhận tài liệu sản phẩm/dịch vụ, rồi
điền workspace OpenClaw. Bot cầm **nick Zalo riêng**, nói như người: hỏi trước
khi tư vấn, không cụt cỡ khi khách lệch script.

Khác `agent-cskh-zalo`: ít rào giọng, được kiến thức chung, AI-first, kênh
`zalouser` (như Tom) — không Bot Creator.

## Chủ shop / coding agent làm gì

1. **Chủ shop (chữ thường):** [`docs/08-luong-chu-shop.md`](docs/08-luong-chu-shop.md) · sổ/dữ liệu: [`docs/09-kho-va-du-lieu.md`](docs/09-kho-va-du-lieu.md) · ngày thường: [`docs/07-cach-dung.md`](docs/07-cach-dung.md)
2. **Người dựng:** [`HUONG-DAN-AGENT.md`](HUONG-DAN-AGENT.md) · hỏi: [`docs/bo-cau-hoi.md`](docs/bo-cau-hoi.md) · kịch bản đủ: [`PHONG-VAN.md`](PHONG-VAN.md)
3. File gốc vào `knowledge/raw/`, wiki tách theo `knowledge/CLAUDE.md` (giải thích thường = file 09)
4. Bật nick (người chưa cài): [`docs/05-thiet-lap.md`](docs/05-thiet-lap.md) · thử: [`docs/04-kich-ban-thu.md`](docs/04-kich-ban-thu.md) · chuẩn: [`docs/06-tieu-chuan.md`](docs/06-tieu-chuan.md)
5. Test máy: `python3 -m unittest discover -s tests -v`

Đã khóa kênh và rào: [`docs/quyet-dinh.md`](docs/quyet-dinh.md).

## Brain / wiki / harness nằm ở đâu

| | File |
|---|---|
| Brain | `SOUL.md` · `giong-noi.md` · `cach-tu-van.md` · `tuduy-cskh.md` · `IDENTITY.md` (**Nami**) · `persona.md` |
| Wiki | `knowledge/wiki/` ← tách từ `knowledge/raw/` (câu 3) |
| Harness | `AGENTS.md` · `BOOT.md` · `HEARTBEAT.md` · `skills/` (kể cả `doc-anh`, `phieu`, `follow-up`) · `USER.md` · `memory/` + `memory/phieu/{id}.md` |

Chủ shop không cần biết ba chữ đó. Coding agent phỏng vấn theo `PHONG-VAN.md` rồi điền.

## Thiết kế

| File | Việc |
|---|---|
| [`docs/01-it-rao-da-dang.md`](docs/01-it-rao-da-dang.md) | Rào nào giữ, rào nào bỏ |
| [`docs/02-kenh-zalouser.md`](docs/02-kenh-zalouser.md) | Nick cá nhân + OpenClaw |
| [`knowledge/moi-loai-cau-hoi.md`](knowledge/moi-loai-cau-hoi.md) | Mọi kiểu tin đều được đáp |
| [`knowledge/giong-noi.md`](knowledge/giong-noi.md) | Ngôn từ, nhịp Zalo, xưng hô — không giọng tổng đài |
| [`knowledge/cach-tu-van.md`](knowledge/cach-tu-van.md) | Cách hỏi, cách trả, GỘP/TÁCH (rule C) |
| [`knowledge/tuduy-cskh.md`](knowledge/tuduy-cskh.md) | 10 bước một lượt + phiếu theo Zalo ID |
| [`knowledge/workflow-cskh.md`](knowledge/workflow-cskh.md) | Bản đồ vòng: vào → chọn → đơn → sau bán → follow-up |
| [`knowledge/anh-tinh-huong.md`](knowledge/anh-tinh-huong.md) | Mọi loại ảnh/voice — xem rồi đáp hoặc chọn giúp |
| [`knowledge/khung-khai-thac.md`](knowledge/khung-khai-thac.md) | Máy pha: phân vân thì hỏi trước |
| [`knowledge/tinh-huong.md`](knowledge/tinh-huong.md) | Ngoài giờ, sỉ, hết hàng, spam, VAT, teencode, im sau giá… |
| [`knowledge/hoi-thoai-mau.md`](knowledge/hoi-thoai-mau.md) | Few-shot đúng/sai: chào, hỏi, tư vấn, hài, phàn nàn |
| [`docs/05-thiet-lap.md`](docs/05-thiet-lap.md) | Cài OpenClaw + QR nick — từng bước Windows/Mac |
| [`docs/06-tieu-chuan.md`](docs/06-tieu-chuan.md) | Khi nào được nói bot ổn |
| [`docs/07-cach-dung.md`](docs/07-cach-dung.md) | Chủ shop / người dựng / người trực |
| [`docs/08-luong-chu-shop.md`](docs/08-luong-chu-shop.md) | Từng bước dựng bot — chữ thường, không cần biết lập trình |
| [`docs/09-kho-va-du-lieu.md`](docs/09-kho-va-du-lieu.md) | Ba ngăn kiến thức, wiki, phiếu khách, sửa giá sau này |
| [`docs/04-kich-ban-thu.md`](docs/04-kich-ban-thu.md) | Tin thử: tình huống + giọng + ảnh + follow-up |
| [`docs/vi-du-file-da-dien.md`](docs/vi-du-file-da-dien.md) | Shop **giả** — đừng copy số vào wiki thật |
| [`SOUL.md`](SOUL.md) | Tính cách Nami: để ý, thành thật, vui nhẹ, hài đúng lúc |
