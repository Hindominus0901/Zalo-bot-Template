# Skill bot — gặp việc thì đọc

Skill = cách hay, không phải cổng. Khách đi tắt thì đi tắt. Não chat: `AGENTS.md`
(OpenClaw nạp). Tool: `TOOLS.md` (tên việc → `read`/`write`/`message`).

| Skill | Việc |
|---|---|
| `giao-tiep` | Nhịp nói: khách, chủ, nhóm |
| `lam-viec` | Ca trực, thiếu số, MCP Drive |
| `doc-wiki` | Số shop từ tờ sổ |
| `phieu` | Đọc/ghi phiếu theo Zalo ID |
| `doc-anh` | Tool `doc_anh` — ảnh, voice, file |
| `khai-thac` | Phân vân, chưa chọn |
| `bao-gia` | Giá, mắc, bớt — luật số ở `doc-wiki` |
| `ghi-don` | Muốn mua / đặt — không tự chốt |
| `theo-don` | Đơn đâu — không bịa trạng thái |
| `xu-ly-phan-nan` | Chê hàng, bực |
| `xu-ly-tu-choi` | Đắt, để xem, bên kia rẻ |
| `cham-khach-cu` | Đã mua, nhắn lại |
| `thu-lead` | Xin SĐT sau khi đã cho gì |
| `ban-giao` | Gọi người thật |
| `follow-up` | Heartbeat: im sau giá / sau đơn |
| `hoc-lai` | Heartbeat cuối ngày: đề xuất bài học + vá sổ cho chủ |

Coding agent **dựng shop**: `dung-bot/QUY-TRINH.md` · skill `giao-tiep-chu` ·
`lam-viec-dung`. MCP: `docs/11-mcp-ung-dung.md`.

---

## Viết skill mới

Bốn phần, theo thứ tự — nhưng chỉ tách thành mục `##` khi skill đủ dài để cần:

`Khi nào dùng` · `Cách làm` · `Chỗ hay vấp` · `Kiểm lại`

Skill ngắn thì viết liền, chỉ giữ dòng **Kiểm lại:** ở cuối. Mọi skill trong
repo đều có dòng đó — nó là câu tự soi trước khi gửi, không phải trang trí.

**Bài học, không phải nhật ký.** Một luật khái quát + một vế *vì sao*, gắn vào
bước nó ảnh hưởng, nói một lần. Không kể chuyện, không ngày tháng, không dán
nguyên đoạn chat.

`chi-goi-khi-duoc-yeu-cau: true` cho skill **đụng tiền hoặc hứa hẹn** — bot
không được tự kích, chỉ chạy khi đúng điều kiện máy. Hiện có: `ban-giao`,
`follow-up`, `hoc-lai`.

