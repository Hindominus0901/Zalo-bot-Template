# Khung khai thác — hỏi trước, tư vấn sau

Nguyên tắc gốc: **khách đang phân vân thì hỏi trước, chọn giúp sau. Khách hỏi fact thì trả fact — đừng nhét khai thác.**

Đây là máy **khi họ đang tìm / chưa biết lấy gì**. Không phải phễu bắt mọi cuộc
chat đi qua. Skill cũ `tu-van-chon-san-pham` là bản rút của máy này.

---

## Bốn pha, một cuộc chat

```
MO_DAU  →  KHAI_THAC  →  TU_VAN  →  BUOC_TIEP
                ↑             │
                └──── chưa đủ ┘
         mọi lúc có thể  →  BAN_GIAO
```

| Pha | Bot đang làm | Xong khi |
|---|---|---|
| `MO_DAU` | Nhận ý vừa gõ, không bắt kể lại | Đã biết khách muốn hỏi hay muốn được hỏi |
| `KHAI_THAC` | Lấp slot, từng câu một | Đủ slot bắt buộc của tình huống đó, hoặc khách đòi tư vấn ngay |
| `TU_VAN` | Một lựa chọn chính + một thay thế | Khách hiểu *vì sao món đó*, lý do trích từ lời họ |
| `BUOC_TIEP` | Giữ chỗ / xem khác biệt / để SĐT / xem đã | Có một hành động rõ, không câu chúc |
| `BAN_GIAO` | Dừng bot, người thật vào | Khách biết ai gọi lại; tóm tắt đủ để người đó không hỏi lại từ đầu |

Khách hỏi thẳng một fact (*ship mấy ngày*, *còn size M không*) thì **trả lời fact
trước**, rồi mới rẽ vào khai thác nếu còn thiếu. Đừng hỏi dịp tặng khi họ chỉ hỏi
phí ship.

Khách đã tự khai đủ slot trong một tin (*tặng sinh nhật, ngân sách 500, bạn gái
hay mang đi làm*) thì **bỏ qua khai thác**, vào `TU_VAN` ngay. Hỏi lại cái đã có
là lỗi nặng.

---

## Slot — thứ bot cần biết, không phải form

Mỗi ngành điền bộ slot riêng lúc phỏng vấn. Bộ mặc định cho bán hàng / dịch vụ:

| Slot | Hỏi kiểu gì | Bắt buộc? |
|---|---|---|
| `viec_can` | Đang tìm gì / việc gì cần xong | Có, nếu tin mở chưa nói |
| `tinh_huong` | Dùng cho ai, dịp nào, ngày nào | Có với tư vấn chọn món |
| `rang_buoc` | Ngân sách, thời gian, chỗ ở / size | Chỉ khi giá hoặc món phụ thuộc |
| `da_thu` | Đã dùng gì, vướng chỗ nào | Không — nhưng đây là câu đáng giá nhất |
| `lo_ngai` | Điều họ lo trước khi chốt | Lấy từ persona shop, không hỏi thẳng "anh/chị lo gì" |

**Một lượt chỉ hỏi một slot.** Sau câu thứ ba mà vẫn thiếu thì tư vấn trên cái
đã có, nói rõ chỗ còn đoán, hoặc bàn giao — đừng thành buổi khảo sát.

Câu hỏi phải **trả lời được ngay trên điện thoại**, tốt nhất là chọn được một
trong hai/ba hướng. Tránh câu mở kiểu "anh/chị cần hỗ trợ gì thêm không ạ".

Cách đặt câu, cách trả, khi nào dừng: `knowledge/cach-tu-van.md`. Chữ gõ:
`knowledge/giong-noi.md`. File này chỉ là **máy pha + slot** — đừng hỏi đúng slot
mà giọng form (*đối tượng sử dụng*, *ngân sách dự kiến*).

---

## Gợi ý cuối tin

Mỗi tin ở pha `MO_DAU` và `KHAI_THAC` kết bằng 2–3 gợi ý. Chúng là **câu khách
có thể gõ y nguyên**, không phải nhãn nút kiểu app.

Ví dụ tin mở:

```
Alo có em, Nami đây. Anh/chị đang tìm cho mình dùng hay để tặng ai đó?
Gợi ý: Mình dùng hằng ngày · Tặng người quen · Xem bảng giá
```

Luật:

- Gợi ý phải là nhánh bot **làm được thật**
- Một gợi ý là lối thoát nhẹ (*Xem bảng giá*, *Gặp người thật*) — đừng nhốt khách trong một lối hỏi
- Trên nick cá nhân: để nguyên dạng chữ. Không đánh số 1/2/3. Không chờ nút OA
- Có thể quote reply tin khách. Typing/seen do OpenClaw `zalouser` lo
- Khi đã vào `TU_VAN`, gợi ý đổi sang bước tiếp: *Lấy A*, *Khác nhau chỗ nào*, *Để SĐT em giữ giúp*

---

## Đủ bối cảnh rồi thì tư vấn thế nào

1. Đọc kho trước. Không có khác biệt giữa hai món trong kho thì đừng bịa — bàn giao.
2. Đề xuất **một** món. Lý do phải nhắc lại chữ khách vừa nói.
3. Nêu **một** món thay thế, và *khi nào* nên lấy nó.
4. Không đẩy món đắt nhất theo mặc định.
5. Kết bằng một bước: giữ chỗ, xem khác biệt, hoặc để người thật gọi.

Sai điển hình: đọc cả danh mục. Đúng điển hình: "lấy A vì đúng cái anh/chị vừa kể".

---

## Khi khách không chơi theo kịch bản

| Họ làm | Bot làm |
|---|---|
| Trả lời ngoài gợi ý | Nhận ý đó, lấp slot, không bắt chọn lại |
| Đòi giá ngay | Báo giá đúng kho nếu hỏi được; giá phụ thuộc thì hỏi **một** câu rồi báo |
| Im, hoặc "ok" | Không nài. Một câu mở cửa rồi dừng. |
| Bực / chê / đòi người | Sang phàn nàn / bàn giao. Tắt khai thác, tắt hài |
| Hỏi đời / lệch script | Đáp theo `moi-loai-cau-hoi.md`, rồi quay lại pha đang dở nếu họ còn phân vân |
| Kho không có đúng món | Không bịa. Tư vấn hướng + hẹn chốt số, không cúp chat |

---

## Chỗ lưu

Mỗi cuộc chat giữ một object nhỏ, ví dụ:

```yaml
pha: KHAI_THAC
slot:
  viec_can: tặng
  tinh_huong: sinh nhật bạn
  rang_buoc: 500k
  da_thu: null
  lo_ngai: null
hoi_roi: 2          # đã hỏi 2 câu chẩn đoán
goi_y_lan_nay:
  - Bạn ấy hay dùng sẵn
  - Mình chọn giúp
  - Ngân sách khoảng...
```

Object này là dữ liệu, không phải prompt. Prompt chỉ thấy: pha hiện tại, slot đã
có, câu nên hỏi tiếp (nếu còn), và lệnh "đừng hỏi lại slot đã đầy".
