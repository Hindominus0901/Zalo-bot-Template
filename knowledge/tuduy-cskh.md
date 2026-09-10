# Tư duy CSKH — một lượt chat

Đã chốt với người dựng template: **C** (gộp/tách tùy nặng) + **phiếu ngắn theo ID**.
Không CRM. Ma trận máy đọc: `knowledge/logic/ma-tran.json`. Ảnh: `anh-tinh-huong.md`.
Phiếu: `skills/phieu/SKILL.md`.

Id bước (khớp ma-tran.json): `lay_id` · `doc_phieu` · `phan_loai_y_va_media` ·
`xem_anh_neu_co` · `doc_wiki_can` · `quyet_gop_tach` · `tra_cai_ho_hoi_truoc` ·
`tu_van_neu_gop_va_du` · `ghi_phieu_neu_ben` · `ghi_memory_ngay_neu_thieu_wiki`.

Mỗi tin khách, **im lặng** chạy hết 10 bước rồi mới gõ. Đừng nhảy cóc.

`lay_id` là **bước**, không phải tool trong `TOOLS.md`. ID lấy từ metadata tin.

```
1. Lấy ID
2. Đọc phiếu
3. Phân loại ý + media
4. Xem ảnh nếu có (vision / media ref)
5. Đọc wiki cần cho đúng câu họ hỏi
6. Quyết GỘP hay TÁCH
7. Trả đúng cái họ hỏi trước
8. Tư vấn chỉ khi được GỘP và đủ chỗ đứng
9. Ghi phiếu nếu có fact bền
10. Thiếu số wiki → memory/YYYY-MM-DD.md
```

---

## 1. ID

Inbox: ID = **Zalo user id** người gửi (`senderId` zalouser). Không lấy tên hiển thị
(đổi tên được). Không lấy số điện thoại làm tên file.

Nhóm: ID = `{groupId}-{senderId}`. Phiếu nhóm chỉ ghi việc shop, không lập hồ sơ
cả nhóm.

File: `memory/phieu/{id}.md`. `id` chỉ `A-Za-z0-9._-`. Lạ / có `/` → **không ghi
file**, chỉ nhớ trong phiên.

Lấy ID: metadata tin OpenClaw / zalouser. Không có ID → không bịa; xử lý trong
phiên, ghi `memory/` ngày nếu thiếu wiki.

## 2–5. Đọc rồi mới nói

Thứ tự đọc: phiếu (nếu có) → tin này (chữ + ảnh) → wiki **đúng câu đang hỏi**.

Đã có size / món từ chối trên phiếu thì **cấm hỏi lại**. Ảnh vừa thấy: ghi
*thấy gì* vào phiếu (chữ), không lưu ảnh, không đọc số CK/CCCD ra phiếu.

Model phải nhìn được ảnh (vision). Text-only: OpenClaw để `media://inbound/…`
— vẫn phải mở/xem, đừng bảo khách gõ lại.

## 6. GỘP hay TÁCH — rule C

**GỘP** (một tin: trả lời + một phương án) khi việc **nhẹ** và mình **chắc**:

- Fact ngắn wiki có (giá một món, ship nội thành nếu trang có, còn size nếu trang có)
- Ảnh **chắc** là món shop + họ hỏi màu / còn / lấy cái nào
- Phiếu đã đủ slot, họ chỉ hỏi thêm một fact

Gộp vẫn: **câu đầu = trả đúng cái họ hỏi**. Câu sau mới là một món / một thay thế.
Không nhét “tặng ai” vào tin hỏi phí ship.

**GỘP** khi (`gop_khi`): `fact_ngan_wiki_co` · `anh_chac_mon_va_hoi_mau_size_con` ·
`phieu_da_co_slot_va_ho_hoi_them_mot_fact`.

**TÁCH** khi (`tach_khi`): `ck_bien_lai` · `hang_loi` · `otp_man_hinh` · `cccd_the` ·
`khong_chac_mon` · `quyen_quyet_giam_gia_hop_dong` · `khach_buc` · `anh_mo_toi_crop` ·
`lua_ck` · `si_chua_co_wiki`.

- Ảnh CK / biên lai
- Hàng lỗi / unbox sai
- OTP, CCCD, QR lạ, kèo chuyển tiền
- Không chắc món trên ảnh
- Giảm giá / hợp đồng / quyền chủ
- Khách bực
- Ảnh mờ / album chưa biết họ hỏi tấm nào
- Sỉ mà wiki chưa có mức

Tách xong, họ hỏi tiếp chuyện nhẹ → lúc đó mới gộp.

## 7–8. Trả đúng cái đang trả lời

Tư vấn phải **bám câu vừa hỏi + ảnh vừa xem + phiếu**.

Sai: họ hỏi *còn size M không* mà mình kể combo. Đúng: *size M [wiki]*; nếu gộp
được mới thêm *lấy màu đang có / hết thì một thay thế wiki*.

Một món chính + một thay thế. Lý do = chữ họ hoặc *thấy trên ảnh*. Không catalog.

## 9–10. Ghi

Phiếu: size, món đã nói, món từ chối, tình huống, *ảnh thấy gì*, việc mở,
trạng thái đơn / `da_bao_gia_luc` nếu vừa đổi.
Không: số CK, CCCD, OTP, mật khẩu, SĐT đủ số, file ảnh.

Wiki thiếu: `memory/YYYY-MM-DD.md`. Heartbeat báo chủ; nhắn khách chỉ theo
`follow-up` khi `USER.md` đã bật. Bản đồ vòng: `workflow-cskh.md`.

---

## Ưu tiên khi lệch

| Lệch | Ưu tiên |
|---|---|
| Chữ hỏi A, ảnh là B | Một câu: đang hỏi A hay tấm ảnh. Tiền/lỗi trên ảnh → ảnh thắng, TÁCH |
| 10 tin dồn | Một tin gộp; ý việc > sticker |
| Phiếu vs tin mới | Tin mới thắng; phiếu chỉ để không hỏi lại cái chưa đổi |
| Wiki vs kiến thức chung | Số liệu = wiki. Phối/dùng = chung, tách miệng |
