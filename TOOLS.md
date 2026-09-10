# Tools — catalog máy, đừng bịa thêm

OpenClaw chỉ cho **file** (đọc/ghi workspace) + **kênh zalouser** (chữ, ảnh,
quote, typing/seen) + **message** tới kênh đã biết. Bản này **không** có API
shop. Máy đọc: `knowledge/logic/tools.json`.

Mỗi “tool” dưới = cách dùng file/kênh cho đúng việc. Gọi sai tên không được bịa
công cụ mới.

## Có

### `doc_file`

Đọc file workspace. Dùng cho persona, giọng, skill, `USER.md`, `SOUL.md`.
Không đọc `internal/` khi đang nói với khách lạ.

### `doc_wiki`

Số liệu shop. Đọc `knowledge/wiki/public/` (đúng tờ: giá, ship, đổi trả…).
Trang trống / `[CHỜ CHỦ SHOP]` = **THIEU**, không suy từ mạng. Skill `doc-wiki`.

### `doc_phieu` / `ghi_phieu`

`memory/phieu/{senderId}.md`. Đầu lượt đọc, cuối lượt ghi fact bền. Skill `phieu`.
Không CRM. Không đọc phiếu thành tiếng.

### `xem_anh`

Ảnh/voice/file inbound (vision / `media://inbound/`). Xem đã, đừng bắt gõ lại.
Skill `doc-anh` + `anh-tinh-huong.md`. Không ghi số CK/CCCD.

### `gui_zalo`

Trả đúng thread khách. Inbox luôn. Nhóm chỉ khi gọi tên / @ / reply. Một tin
gộp nếu họ dồn. Follow-up: **đúng senderId**, chỉ hai nhánh `follow-up`.

### `bao_chu`

Message tới nick/nhóm trong `USER.md`. Tóm tắt chữ thường. Chưa có kênh → chỉ
ghi `memory/` ngày, đừng đoán. Skill `ban-giao`. Heartbeat / BOOT cũng dùng cái này.

### `ghi_thieu`

Một dòng `memory/YYYY-MM-DD.md`: câu khách, giờ, thiếu tờ nào. Không tự viết
giá vào wiki.

## Không có — đừng giả

`tra_don` · `cong_ck` · `ton_kho_live` · `crm` · `luu_lead` (ngoài dòng memory) ·
`zns` · `broadcast` · `lich_slot` · `nut_oa`.

SĐT khách → dòng memory + `bao_chu`, không tool lead.

File gốc `knowledge/raw/` — không gửi raw cho khách.
