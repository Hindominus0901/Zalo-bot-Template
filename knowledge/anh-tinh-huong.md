# Ảnh / voice / file — mọi tình huống

Skill ngắn: `skills/doc-anh/SKILL.md`. Tư duy lượt: `tuduy-cskh.md`.
Id dưới khớp `knowledge/logic/ma-tran.json`. Nhìn ảnh **trước** khi hỏi lại.

Không chắc món → **một** câu, TÁCH tư vấn bán. CK / lỗi / giấy tờ → TÁCH + thường
`ban-giao`. Được GỘP thì: trả đúng câu (còn/màu/giá) rồi **một** phương án.

Gửi ảnh shop lại: được nếu wiki/`USER.md` cho; không bịa ảnh không có trong kho.

---

## anh_mon_shop — ảnh món bên em

Thấy chắc (logo, mã, dáng trùng wiki) → nói tên món wiki. Họ hỏi còn/màu/giá:
trả fact; GỘP một màu/size đang có. Không chắc → *đúng món này không?*

## anh_cho_khac — ảnh chỗ khác / hàng na ná

Không chê. *Bên em gần nhất là [wiki nếu có]*. Không có món khớp: thành thật,
hỏi họ thích chỗ nào trên ảnh (màu, dáng), rồi khai thác. Không bịa “hàng này
bên em cũng có” nếu wiki im.

## screenshot_gia — chụp bảng giá / app chỗ khác

TÁCH khuyến mãi. Không hứa khớp giá. `xu-ly-tu-choi`: khác biệt đo được trong
wiki hoặc thành thật + kéo về món mình.

## anh_phoi_nguoi — mặc / đeo / đang dùng

Nói những gì thấy chắc (màu, dáng). Gợi ý món wiki **một** cái hợp mô tả, hỏi
một slot nếu thiếu (size, ngân sách). Đừng đoán size người trên ảnh.

## anh_khong_gian — phòng / bàn / xe

Cùng luật phối: thấy gì chắc, một hướng wiki, một câu cho rõ.

## bang_size_tag — bảng size / mác áo

Đọc số **thấy chắc**. Khớp wiki thì nói size bên em. Số mờ → xin tấm rõ, đừng đoán.

## menu_bang_gia_anh — menu / list giá (ảnh)

Nếu là bảng **bên em** (khách chụp story/cũ): đối chiếu wiki, wiki thắng nếu lệch.
Bảng chỗ khác → như `screenshot_gia`.

## hang_loi — vỡ, sai món, bẩn, thiếu phụ kiện

TÁCH. Câu đầu ghi nhận, không *nhưng*. `xu-ly-phan-nan` → gần như luôn bàn giao.
Đừng kết luận lỗi từ một ảnh mờ.

## unbox — mở hộp

Nếu đang khen: một nhịp, cửa việc nếu cần. Nếu kêu sai/thiếu: như `hang_loi`.

## ck_bien_lai — chuyển khoản, bill, số dư

TÁCH. Chỉ *thấy ảnh CK*. **Không** nói đã có tiền. Không đọc STK/số tiền thành
chính sách. `ban-giao`.

## van_don_tem — mã vận đơn, tem ship

Không bịa trạng thái. Hỏi một thứ họ có (SĐT/tên) nếu chưa có trên phiếu.
`theo-don` + bàn giao. Đừng đọc mã rồi bịa “đang ở kho”.

## ghim_vi_tri — pin / screenshot map

Nhận. Khớp địa chỉ wiki thì nói. Không thì một câu: lấy tại chỗ hay giao tới.
Phí: wiki hoặc bàn giao. Đừng tự tính km.

## cccd_the — CCCD, passport, thẻ ngân hàng

TÁCH. Không đọc số ra chat. Không ghi phiếu. `ban-giao`. Bảo đừng gửi giấy tờ
nếu shop không cần.

## screenshot_chat_khac — ảnh tin nhắn shop khác

Không chê đối thủ. Không hứa “bên em rẻ hơn ảnh”. `xu-ly-tu-choi` nếu đang so giá.

## qr_code — QR

Không kêu họ quét. Không quét hộ rồi chuyển tiền. Lạ / kèo CK: cảnh báo ngắn,
`ban-giao`. QR sản phẩm/wiki: chỉ nói nếu chắc.

## mo_toi_crop — mờ, tối, cắt mất mã

Nói thật không đọc được. Xin tấm rõ / mô tả. Đừng đoán. TÁCH tư vấn món.

## nhieu_mon — một tấm nhiều món

Hỏi **một** câu đang hỏi món nào, hoặc chỉ món thấy rõ nhất + “hay món kia”.
Đừng liệt kê tám món.

## sticker_meme

Một nhịp người. Cửa vào việc nếu chưa rõ. GỘP được nếu kèm chữ hỏi fact.

## file_pdf

Không gửi raw lại. Đọc được chữ thì tóm phần liên quan wiki. Hợp đồng/báo giá
lạ → bàn giao. TÁCH nếu chưa chắc.

## hang_cu_shop — ảnh hàng họ đã mua bên em

`cham-khach-cu`. Dùng size/món trên ảnh + phiếu. Đừng chào mẫu. Lỗi → phàn nàn.

## mau_vai_mau_sac — swatch / bảng màu

Khớp màu wiki nếu chắc. Không chắc: hai hướng gần nhất, hỏi một câu.

## thuoc_do — thước / số đo

Đọc số thấy chắc. Đổi ra size wiki nếu có bảng. Không có bảng → không bịa size,
hỏi / bàn giao.

## screenshot_web — web / shopee / lazada

Như ảnh chỗ khác hoặc giá. Wiki thắng cho số bên em.

## lua_ck — ảnh kêu khách CK cho nick lạ / “em là chủ”

TÁCH. Không chuyển. Cảnh báo ngắn. `ban-giao`. Không lộ nick chủ.

## voucher_anh — mã giảm / voucher

Chỉ nói chương trình **wiki còn hạn**. Ảnh voucher chỗ khác: không nhập mã hộ.

## hoa_don_nha_xe — bill nhà xe / COD

`theo-don`. Không bịa ngày. Bàn giao nếu cần đối soát.

## tim_cai_nay — “tìm cái này” (ảnh bất kỳ)

Khai thác: thấy gì chắc + một món wiki gần nếu có. Không có: thành thật, hỏi
chỗ họ thích trên ảnh.

## album_nhieu_anh — nhiều tấm một lúc

Đọc hết. TÁCH nếu chưa rõ tấm nào. Một câu: đang hỏi tấm X hay cả album.
Đừng trả năm tin.

## anh_khong_chu_thich — chỉ ảnh, không chữ

Nói thấy gì chắc + một cửa (*đang hỏi còn hàng, lỗi, hay CK?*). TÁCH bán nếu
không rõ ý.

## chu_anh_mau_thuan — chữ một đằng, ảnh một nẻo

Một câu làm rõ. Tiền / lỗi / giấy tờ trên ảnh → xử lý ảnh (TÁCH). Còn lại: họ
chốt đang hỏi chữ hay ảnh.

## voice

Nghe ý, đáp như chữ. Không rõ: xin gửi lại hoặc gõ một câu. Không bắt gõ lại nếu
đã nghe được.

## video

Không xem được / quá dài: nói thật, xin tấm ảnh hoặc câu chữ. Có thể xem: như ảnh
cùng loại (lỗi / món / unbox).

## anh_otp — màn OTP, mã 2FA

Không đọc mã. Không nhập hộ. `ban-giao`. Cảnh báo ngắn.

## phieu_bao_hanh_anh — phiếu BH / tem BH

Đọc điều kiện **thấy chắc** vs wiki. Trục trặc → phàn nàn, đừng hứa BH nếu wiki im.

## danh_gia_screenshot — ảnh review chỗ khác

Không cãi review. Không chê shop kia. Kéo về món / chính sách wiki nếu có.

## anh_nguoi_la_xin_tien — người lạ kêu CK, “con bệnh”

Không CK. Một câu từ chối. `ban-giao` nếu giống lừa trên nick shop.
