# Trang wiki nên có — template đã có tờ chờ, điền lúc câu 3

Bot đọc trang **có chữ** như chính sách. Template đã để tờ chờ sẵn trong
`public/` và `internal/` — banner `[CHỜ CHỦ SHOP]` = **chưa dùng để nói số**,
không = “shop không ship / không đổi trả”.

Điền số vào tờ đúng việc. Có số thì xóa banner. **Đừng** tạo thêm tờ trống.
**Đừng** copy số từ [`docs/vi-du-file-da-dien.md`](../../docs/vi-du-file-da-dien.md).

Mỗi trang: frontmatter như `knowledge/CLAUDE.md`. Tên file chữ thường, không dấu.

## Nên có nếu chủ có dữ liệu

| File gợi ý | Khách hay hỏi |
|---|---|
| `public/ban-gi.md` | Shop bán / làm gì, một trang ngắn |
| `public/gia.md` | Giá, gói, gồm gì — hoặc tách từng món nếu bảng dài |
| `public/ship.md` | Phí, nội thành / tỉnh, thời gian **đã nói chắc** |
| `public/thanh-toan.md` | CK, COD, không nhận tiền mặt… |
| `public/doi-tra.md` | Đổi trả, hoàn, điều kiện |
| `public/bao-hanh.md` | Bảo hành, không bảo hành cái gì |
| `public/con-hang.md` | Khi nào được nói còn / hết; mặc định: không đoán |
| `public/gio-truc.md` | Giờ xem tin / gọi lại (trùng `USER.md`) |
| `public/dat-lich.md` | Chỉ khi làm dịch vụ có slot |
| `public/dia-chi.md` | Shop ở đâu, lấy trực tiếp, giờ mở cửa |
| `public/si-ctv.md` | Giá sỉ, CTV, đại lý — chỉ khi chủ có mức/điều kiện |
| `public/hoa-don-vat.md` | Xuất hoá đơn / VAT / cần MST |
| `public/kiem-hang.md` | Đồng kiểm, xem hàng khi nhận, khi nào không mở hộp |
| `public/lo-trinh.md` | **Dịch vụ / khóa học:** gồm gì, bao lâu, mấy buổi, ở đâu |
| `public/ai-phu-hop.md` | **Dịch vụ / khóa học:** hợp với ai, **chưa** hợp với ai |
| `public/sau-khi-xong.md` | **Dịch vụ / khóa học:** xong rồi còn hỗ trợ gì, bao lâu |
| `internal/gia-von-hoa-hong.md` | Vốn, hoa hồng, kịch bản khách khó |
| `internal/xu-khach-kho.md` | Việc bot không được kể |

FAQ miệng câu 6: một câu một trang, hoặc gom `public/faq-….md` nếu cùng chủ đề.

Còn `[CHỜ CHỦ SHOP]` trên trang = trang đó **chưa được dùng để nói số**.

---

## Tờ shop không dùng thì **xóa**, đừng để trống

Template ship đủ tờ cho cả bán hàng lẫn dịch vụ. Một shop chỉ dùng một phần:

| Shop kiểu | Xóa tờ |
|---|---|
| Bán hàng vật lý | `lo-trinh` · `ai-phu-hop` · `sau-khi-xong` |
| Coaching, đào tạo, tư vấn | `ship` · `kiem-hang` · `con-hang` (đổi thành *còn chỗ* trong `dat-lich`) |
| Dịch vụ tại chỗ (spa, sửa chữa) | `ship` · `kiem-hang` |

Xóa xong **chạy lại `scripts/lam_chi_muc.py`**. Để tờ trống lại thì nó nằm trong
chỉ mục, bot thấy tên tờ rồi mở ra đọc một trang không có gì — tốn lượt và làm
bot tưởng shop có việc đó.

Hình trang + persona đã điền (shop **giả**, đừng chép số):
[`docs/vi-du-file-da-dien.md`](../../docs/vi-du-file-da-dien.md).
