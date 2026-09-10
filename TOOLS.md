# Tools — catalog máy, đừng bịa thêm

OpenClaw: **file** + **zalouser** (chữ, ảnh, quote, typing/seen) + **message** +
**MCP** (Drive khi chủ bật). Máy đọc: `knowledge/logic/tools.json`,
`knowledge/logic/mcp.json`. Bus: `docs/11-mcp-ung-dung.md`.

Mỗi “tool” = cách dùng đúng việc. Gọi sai tên không được bịa công cụ mới.

## Có

### `doc_file`

Đọc file workspace (persona, giọng, skill, `USER.md`, `SOUL.md`).
Không đọc `internal/` khi đang nói với khách lạ.

### `doc_wiki`

Số shop trong `knowledge/wiki/public/`. Trống / `[CHỜ CHỦ SHOP]` = **THIEU**.
Skill `doc-wiki`.

### `doc_phieu` / `ghi_phieu`

`memory/phieu/{senderId}.md`. Skill `phieu`. Không CRM. Không đọc phiếu thành tiếng.

### `doc_anh` (cũ: `xem_anh`)

Đọc ảnh / voice / file inbound (vision / `media://inbound/`). **Xem đã**, đừng
bắt gõ lại. Xếp loại ma trận, GỘP/TÁCH, một dòng phiếu. Skill `doc-anh`.
Không ghi số CK/CCCD/OTP.

### `gui_zalo`

Trả đúng thread. Inbox luôn. Nhóm: gọi tên / @ / reply. Follow-up: đúng ID, hai
nhánh có rào.

### `bao_chu`

Message kênh `USER.md`. Chưa có kênh → chỉ `ghi_thieu`. Skill `ban-giao`.

### `ghi_thieu`

Một dòng `memory/YYYY-MM-DD.md`. Không tự viết giá vào wiki.

### `mcp_drive`

Google Drive **chỉ** file/thư mục chủ đã chỉ. Cất `raw/`. Skill `lam-viec`.
Chưa auth / `enabled: false` → xin file tay. **Không** gọi lúc chat khách.
Config mẫu: `config/mcp.example.json5`.

## Không có — đừng giả

`tra_don` · `cong_ck` · `ton_kho_live` · `crm` · `luu_lead` (ngoài dòng memory) ·
`zns` · `broadcast` · `lich_slot` · `nut_oa` · `apify_scrape_gia`.

SĐT khách → dòng memory + `bao_chu`. File `raw/` không gửi khách.
