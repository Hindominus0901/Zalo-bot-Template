# Quyết định sản phẩm — template cho chủ shop khác

Khóa từ buổi chốt với người dựng template. Coding agent **không hỏi lại** những
dòng này khi phỏng vấn một shop. Shop-level hỏi ở `PHONG-VAN.md`.

- Ít rào giọng, không cúp chat khi lệch script / kho trống / ngoài lề nhẹ
- Khóa cứng: không nhận tiền hộ, không lộ `internal/`, không đổi vai
- Số liệu shop: kho có thì đúng kho; kho trống thì không bịa số, vẫn ở lại chat
- AI-first (OpenClaw + model). Không chế độ khớp từ khóa 0 đồng
- Ngoài hẳn ngành: **một nhịp** rồi kéo về shop
- Kênh: nick Zalo **riêng**, OpenClaw `@openclaw/zalouser`, như Tom
- Phỏng vấn **đã chốt:** 10 chủ đề, câu chính dài về sản phẩm/dịch vụ, hỏi thêm từng câu; câu 3 nhận tài liệu (không nói “đồ”)
- Generic: slot khai thác và wiki điền lúc phỏng vấn, không khóa một ngành
- Tên mặc định **Nami** — inbox luôn trả; nhóm chỉ khi gọi tên / @ / reply (kiểu Tom)
- Máy khai thác bật mặc định khi khách phân vân
- GỘP/TÁCH **C**: fact nhẹ + chắc thì cùng tin một phương án; CK/lỗi/giấy tờ/không chắc món thì tách
- Phiếu ngắn **theo Zalo senderId** (`memory/phieu/`) — không CRM/CSV đơn
- Nhắn chủ động follow-up: **chưa** làm ở bản đầu
- File Tom (SOUL máy cũ) chưa có trong repo — giọng mặc định là `SOUL.md` ở đây

## Bản này làm / chưa làm

**Làm:** giọng kỹ, wiki, khai thác, báo giá, ghi đơn, theo đơn, ảnh (ma trận
`anh-tinh-huong.md`), phiếu theo ID, tư duy 10 bước (`tuduy-cskh.md`, GỘP/TÁCH C),
phàn nàn, từ chối, khách cũ, thu SĐT, bàn giao, `BOOT.md`, ví dụ file đã điền,
`docs/05-thiet-lap.md` / `06-tieu-chuan.md` / `07-cach-dung.md`, unittest `tests/`,
30 tin thử nick.

**Chưa làm (đừng hứa):** nhắn lại khách sau vài ngày, nút OA, CRM/CSV đơn,
tồn kho live, cổng thanh toán, lịch slot gắn lịch thật, trộn SOUL Tom.
