# Tools — tên việc, không phải hàm trong repo

Repo **không** có thư mục `tools/` hay binary. OpenClaw thật: `read`, `write`,
`message` (zalouser), vision / `media://inbound/`, MCP nếu config `enabled`.

Cột dưới = cách dùng đúng việc. Gọi `doc_wiki` như tên tool native → sai; hãy
`read` tờ wiki. Máy đọc: `knowledge/logic/tools.json`. Bus: `docs/11-mcp-ung-dung.md`.

## Có

### `doc_file` → `read`

File workspace (persona, giọng, skill, `USER.md`). Không `read` `internal/` với khách lạ.

### `doc_wiki` → `read` `knowledge/wiki/public/`

Số shop. Trống / `[CHỜ CHỦ SHOP]` = **THIEU**. Skill `doc-wiki`.

### `doc_phieu` / `ghi_phieu` → `read` / `write` `memory/phieu/{senderId}.md`

Skill `phieu`. Không CRM. Không đọc phiếu thành tiếng.

### `doc_anh` (cũ: `xem_anh`) → vision / media inbound

**Xem đã**, đừng bắt gõ lại. Xếp loại ma trận, GỘP/TÁCH, một dòng phiếu. Skill
`doc-anh`. Không ghi số CK/CCCD/OTP. Không có script đọc ảnh trong repo.

### `gui_zalo` → `message` zalouser

Inbox luôn. Nhóm: gọi tên / @ / reply. Follow-up: đúng ID, hai nhánh có rào.

### `bao_chu` → `message` kênh `USER.md`

Chưa có kênh → chỉ `ghi_thieu`. Skill `ban-giao`.

### `ghi_thieu` → `write` `memory/YYYY-MM-DD.md`

Không tự viết giá vào wiki.

### `tra_don` → MCP sổ đơn của shop

**Chưa bật (`enabled: false`) = không gọi**, y như `mcp_drive`. Shop chưa có
phần mềm quản đơn thì tool này không tồn tại — xử như trước: hỏi mã đơn rồi
`ban-giao`.

Vào: mã đơn **hoặc** SĐT. Ra: `trang_thai`, `ngay_dat`, `mon`, `van_don`, `ghi_chu`.

Thang leo — rẻ trước, đắt sau, **không nhảy cóc**:

1. phiếu (`trang_thai_don`) đã đủ trả lời chưa
2. `tra_don`
3. chưa có mã / SĐT → hỏi khách **một** câu
4. vẫn không ra → `ban-giao`

Lỗi / timeout / không tìm thấy: nói thật *chưa tra được*, `ghi_thieu`, **không
đoán trạng thái**. Ảnh CK **không** kích hoạt tool này — CK chưa phải đơn.

Không đọc số CK, số thẻ, địa chỉ đầy đủ ra cho người khác trong nhóm. Mẫu:
`config/mcp.example.json5`. Skill `theo-don`.

### `mcp_drive` → MCP Google Drive

**Chưa bật (`enabled: false`) = không gọi.** Chỉ file/thư mục chủ đã chỉ; cất
`raw/`. Không lúc chat khách. Mẫu: `config/mcp.example.json5`. Skill `lam-viec`.

## Không có — đừng giả

`cong_ck` · `ton_kho_live` · `crm` · `luu_lead` (ngoài dòng memory) ·
`zns` · `broadcast` · `lich_slot` · `nut_oa` · `apify_scrape_gia`.

SĐT khách → dòng memory + `bao_chu`. File `raw/` không gửi khách.

## Bước máy, không phải tool

`lay_id` là bước 1 trong `tuduy-cskh.md` — lấy `senderId` từ metadata tin
OpenClaw / zalouser. Máy đọc: `knowledge/logic/tools.json` → `buoc`.
**Không** có hàm `lay_id` trong repo. Không ID → không bịa tên file phiếu; xử
lý trong phiên.

