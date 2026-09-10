---
name: follow-up
description: Hai nhánh chủ động — im sau giá (một tin rồi khóa) và sau đơn (câu mẫu chủ). Không broadcast, không nài lần hai.
---

# Follow-up — hai nhánh, có rào

Không phải CRM. Không ZNS. Không “Nami online”. Không hàng loạt.

Chỉ chạy lúc **heartbeat** (xem `HEARTBEAT.md`). Boot / restart **không** gửi.
Khách đang nhắn trong phiên → đừng xen tin follow-up; trả đúng 10 bước.

`USER.md` còn `[CHỜ CHỦ SHOP]` hoặc chữ **tắt** trên nhánh đó → **không gửi**.
Chưa có giờ được nhắn → không gửi (tránh đêm).

Một tin / khách / nhánh. Đúng `senderId` trên phiếu. Xong thì khóa nhánh trên phiếu.

## Điều kiện chung

1. Đọc `USER.md`: nhánh bật? delay là **số giờ**? giờ được nhắn (ví dụ 9h–21h)?
2. Quét `memory/phieu/*.md` — bỏ `MAU.md`, `README.md`.
3. Trong giờ `USER.md`. Ngoài giờ → để nhịp sau, đừng gửi, đừng ghi `da_gui`.
4. Họ vừa nhắn trong delay → chưa im, bỏ qua nhánh im.
5. Không chắc ID / kênh Zalo → không đoán, ghi `memory/` ngày, báo chủ.

## 1. Im sau giá

Phiếu phải có `da_bao_gia_luc` (đã nói **số wiki**, không phải “khoảng”).
`followup_im` = `chua`. Im quá delay chủ (thường 24–48h).

Tin: một cửa mở, giọng `giong-noi.md`. *Cứ nhắn khi cần.* Không nhắc giá lần
hai. Không “anh/chị còn đó không”. Không nài.

Gửi xong: `followup_im: da_gui` + giờ gửi. **Dừng vĩnh viễn** nhánh này — kể cả
họ im tiếp. Họ trả lời thì vào phiên thường (`tuduy-cskh.md`).

## 2. Sau đơn

Phải có việc đơn **thật** trên phiếu:

- `trang_thai_don` = `cho_chot` (đã `ghi-don`) hoặc `da_chot_chu` / `dang_giao` / `xong`
- có `don_ghi_luc` hoặc `don_chot_luc`

**Không** kích hoạt vì chỉ có ảnh CK / `anh_thay_gi` biên lai. CK ≠ đơn.

`followup_don` = `chua`. Delay + **câu mẫu đúng chữ chủ** trong `USER.md`.
Chưa có câu mẫu → không bịa, nhánh tắt.

Một nhịp. Không tự hỏi review / đánh giá nếu chủ chưa cho trong câu mẫu.

Gửi xong: `followup_don: da_gui`. Họ trả lời → `theo-don` hoặc `cham-khach-cu`
/ `xu-ly-phan-nan`. Không chào lại như khách mới.

## Đừng

- Broadcast, OA, ZNS, “nhắn hết inbox im”.
- Lần hai sau tin im. Đổi `da_gui` thành `chua`.
- Biến ảnh CK thành `cho_chot`.
- Hứa “em nhắc sau” khi `USER.md` đang tắt.
- Gửi lúc boot. Gửi ngoài giờ. Gửi khi thiếu wiki rồi đẻ số trong tin follow-up.
