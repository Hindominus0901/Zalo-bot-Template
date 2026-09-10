# Từ shop của mình tới nhân viên chat

Bạn **không cần biết lập trình**. Có người ngồi cùng (người dựng). Việc của bạn:
nói như đang nhắn Zalo, gửi bảng giá / ảnh / file, rồi khi tới lúc thì **quét
mã trên điện thoại nick nhân viên**.

Người dựng bấm máy và viết sổ. File kỹ thuật họ đọc:
[`HUONG-DAN-AGENT.md`](../HUONG-DAN-AGENT.md) · bấm nút:
[`05-thiet-lap.md`](05-thiet-lap.md).

Sổ shop / dữ liệu khách giải thích thường: [`09-kho-va-du-lieu.md`](09-kho-va-du-lieu.md).

---

## Bot này là gì

Một **nick Zalo như nhân viên** (tên mặc định **Nami**). Khách nhắn inbox thì
được trả. Không phải Official Account, không nút bấm trên Zalo. Không cầm nick
Zalo chính của anh/chị — nick chính khỏi rối tin khách với tin setup.

Nami hỏi trước khi tư vấn. Chỗ **tiền / khiếu nại / không chắc** thì gọi anh/chị
vào, không tự nhận đã có tiền, không tự bớt giá.

```mermaid
flowchart LR
  A[Noi_chuyen_10_chu_de] --> B[Gui_bang_gia_anh_file]
  B --> C[Nguoi_dung_viet_so]
  C --> D[Anh_chi_soi_lai_so]
  D --> E[May_mo_va_nick_rieng]
  E --> F[Quet_ma_dien_thoai]
  F --> G[Nhan_thu_tu_nick_khac]
  G --> H[Mo_khach_that]
```

---

## Việc của anh/chị · việc của người ngồi cùng

| Anh/chị | Người dựng |
|---|---|
| Kể shop, khách hay lo gì, giờ trực | Hỏi từng câu, không nhồi một lúc |
| Gửi bảng giá, ảnh món, file chính sách | Cất nguyên, rồi viết thành tờ sổ nhỏ |
| Soi lại vài câu: giá, ship, đổi trả đúng miệng mình chưa | Sửa sổ cho khớp — **không đoán số** |
| Có nick nhân viên chưa, Windows hay Mac | Cài chỗ bot ngồi, nối nick |
| Quét mã bằng **app nick nhân viên** | Không xin ảnh mã / cookie về chat |
| Nhắn thử từ nick khác, xem chỗ lạ | Sửa sổ hoặc giọng; chỗ tiền anh/chị vào tay |

Không cần tạo “Bot …” trên Zalo. Không cần Official Account.

---

## Từng bước

Làm **theo thứ tự**. Chưa xong nói chuyện thì chưa quét mã. Còn chỗ “chưa hỏi
chủ” trên sổ giá thì **chưa mở khách thật**.

### 1. Ngồi máy đang dùng

Windows hay Mac — nói một câu. Làm trên máy đó. Máy tắt / ngủ = **mất tin lúc
đó**. Thử thì laptop để mở. Khách thật thì máy chạy suốt (người dựng nói rõ,
không tự thuê hộ).

### 2. Nick nhân viên riêng

Một nick Zalo **chỉ để chat khách**. Chưa có thì tạo cùng người dựng. Đừng gắn
ngân hàng, đừng dùng nick chính.

### 3. Trả lời từng câu

Người dựng hỏi khoảng **mười chủ đề**: bán / làm gì, khách ngại gì, tài liệu,
cách xưng hô, việc bot không được làm, câu khách hay hỏi, lúc đặt hàng, kêu ai
khi không chắc, lúc khách chưa chọn được, câu đầu khi họ gõ *alo*.

Nói dài về sản phẩm / dịch vụ. Câu thêm thì trả từng câu. Bộ chữ sẵn:
[`bo-cau-hoi.md`](bo-cau-hoi.md).

### 4. Gửi tài liệu

Bảng giá, ảnh món, file đổi trả, link nếu có. Gửi cái đang dùng với khách, không
cần làm đẹp. Không có file thì nói miệng — người dựng ghi “chưa có số”, bot
không bịa.

### 5. Người dựng viết sổ shop

Họ cắt tài liệu thành **tờ nhỏ** (một tờ một việc: ship, giá, đổi trả…). Phần
chỉ mình biết (vốn, hoa hồng) để ngăn riêng — bot không kể khách. Chi tiết:
[`09-kho-va-du-lieu.md`](09-kho-va-du-lieu.md).

### 6. Anh/chị soi lại

Nghe lại vài câu như khách hỏi: giá một món, ship, còn hàng, đổi trả. Sai thì
sửa **sổ**, đừng bảo “ừ coi như vậy”. Giọng nghe như tổng đài (*hỗ trợ gì ạ*,
menu 1/2/3) thì nói người dựng sửa cách nói, không sửa số.

### 7. Chỗ bot ngồi trên máy

Người dựng cài và nối thư mục shop. Anh/chị nhìn, không cần nhớ tên phần mềm.
Bắt buộc: khách lạ nhắn **vào được** (không kiểu “chỉ bạn bè đã kết nối”).

### 8. Quét mã

Mở **app nick nhân viên** trên điện thoại, quét mã trên máy. Đừng chụp mã gửi
người dựng. Xong, nick đó do chương trình cầm — anh/chị vẫn vào app được, đừng
đăng xuất đại.

### 9. Nhắn thử

Từ **một nick Zalo khác**, nhắn vào nick nhân viên. Người dựng có bảng việc thử
([`04-kich-ban-thu.md`](04-kich-ban-thu.md)): chào, hỏi giá, gửi ảnh chuyển
khoản, bảo đặt hàng, chê đắt… Đạt khi không bịa số, không nhận đã có tiền, không
nói đã đặt xong.

### 10. Mở khách

Chuẩn: [`06-tieu-chuan.md`](06-tieu-chuan.md). Sau đó xem tin Nami hàng ngày.
Sửa giá / ship = bảo người dựng **sửa tờ sổ**. Chỉ nhắn miệng “từ giờ giá X” rồi
quên sổ thì lần sau bot vẫn nói số cũ.

Nhắn lại khách khi họ im / sau đơn: **tắt** nếu anh/chị chưa nói muốn bật. Bật
thì nói rõ sau bao nhiêu giờ và đúng câu muốn gửi.

---

## Ngày thường, anh/chị làm gì

- Chỗ chuyển khoản, khiếu nại, khách khó: **vào tay**. Nami ghi nhận rồi gọi.
- Ngoài giờ: Nami vẫn trả giá / ship **nếu đã ghi trên sổ**. Không hứa “anh chị
  gọi ngay”.
- Đổi tên nhân viên: nói tên mới, người dựng sửa cho khớp.
- Tắt máy = khoảng đó khách nhắn không được.

Cách ngồi sau khi chạy: [`07-cach-dung.md`](07-cach-dung.md).
