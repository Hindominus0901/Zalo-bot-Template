# Hướng dẫn cho coding agent

> Luật khi **dựng bot cho một shop**. Bước B0→B7: skill
> [`dung-bot/QUY-TRINH.md`](dung-bot/QUY-TRINH.md) — đừng
> copy bước ở đây rồi lệch với skill.

Bạn cầm **template workspace OpenClaw**, không phải bot Python. Phỏng vấn chủ
rồi điền giọng + sổ. Nói với chủ:
[`.claude/skills/giao-tiep-chu/SKILL.md`](.claude/skills/giao-tiep-chu/SKILL.md).
File / Drive: [`.claude/skills/lam-viec-dung/SKILL.md`](.claude/skills/lam-viec-dung/SKILL.md)
+ [`docs/11-mcp-ung-dung.md`](docs/11-mcp-ung-dung.md).
Cấu hình gộp: [`docs/10-openclaw-config-mau.md`](docs/10-openclaw-config-mau.md).

Chủ xem trước (chữ thường): [`docs/08-luong-chu-shop.md`](docs/08-luong-chu-shop.md),
[`docs/09-kho-va-du-lieu.md`](docs/09-kho-va-du-lieu.md). **Cấm** nói wiki,
harness, brain, token, QR, OpenClaw, Gateway, persona — trừ khi họ hỏi.

Đã khóa (đừng hỏi lại): [`docs/quyet-dinh.md`](docs/quyet-dinh.md).

Bot lúc chat: `AGENTS.md` (OpenClaw nạp) + `SOUL.md` + `TOOLS.md`. Đừng sửa
não chat trừ khi chủ đổi việc (câu 7/9).

## Cửa vào — agent nào đọc file nào

Không biết trước khách dùng agent gì, nên mỗi cửa đều trỏ về một nguồn:

| Agent | File nó tự nạp |
|---|---|
| Claude Code | `CLAUDE.md` (+ `.claude/skills/`) |
| Cursor | `.cursor/rules/dung-bot.mdc` |
| Gemini · Antigravity | `GEMINI.md` |
| Copilot | `.github/copilot-instructions.md` |
| Codex · còn lại | `AGENTS.md` — xem cảnh báo dưới |

`AGENTS.md` là tên chuẩn mà Codex và nhiều agent khác tự nạp, **nhưng trong repo
này nó đã là não con bot** — OpenClaw nạp workspace theo đúng tên đó, nên không
đổi tên được. Vì vậy tám dòng đầu `AGENTS.md` là biển chỉ đường: đọc tới đó thì
quay sang `dung-bot/QUY-TRINH.md`, đừng nhận mình là Nami.

Thêm một cửa mới (agent mới ra) → thêm file **mỏng**, trỏ về
`dung-bot/QUY-TRINH.md`, và thêm tên nó vào `CuaVao.CUA` trong
`tests/test_dong_goi.py`. Đừng chép lại quy trình.

---

## Ba điều tuyệt đối

### 1. Không bịa số liệu shop

Wiki + đoạn giá trong `persona.md` chỉ từ miệng chủ hoặc file họ đưa. Chưa có →
`[CHỜ CHỦ SHOP]` rồi hỏi. Không “giá tham khảo”, không “shop kiểu này thường”.
Kiến thức chung bot được nói với khách — **bạn** không nhét vào wiki như chính sách.

### 2. Không bỏ phỏng vấn

Câu chính dài, về sản phẩm/dịch vụ. Hỏi thêm từng câu (`PHONG-VAN.md`). Câu 2
và câu 3 mỏng = buổi hỏng.

### 3. Không đổi kênh

Không OA, không Bot Creator. Nick riêng + quét mã `zalouser`. Chi tiết bấm:
[`docs/05-thiet-lap.md`](docs/05-thiet-lap.md).

---

## Thứ tự (chi tiết trong `dung-bot/QUY-TRINH.md`)

B0 máy + nick → B1 đọc khung, giữ ba rào `AGENTS.md` → B2 hỏi / B3 viết ngay →
B4 merge config → B5 đóng vai + chỉ mục + unittest **kho chữ** → B6 quét mã → B7 máy mở.

Viết file sau mỗi câu: bảng trong `dung-bot/QUY-TRINH.md`. Wiki: `knowledge/CLAUDE.md`. **Cấm**
tự mở web shop lấy giá; **cấm** copy `docs/vi-du-file-da-dien.md`.

Unittest xanh = file khớp nhau, **không** = bot sống. Mở khách: [`docs/04-kich-ban-thu.md`](docs/04-kich-ban-thu.md)
trên nick thật + [`docs/06-tieu-chuan.md`](docs/06-tieu-chuan.md).

## Xong khi

Tick list đầy đủ trong `dung-bot/QUY-TRINH.md`. Tóm: IDENTITY khớp config; persona hết chỗ
bắt buộc; raw hoặc chủ nói không có tài liệu; wiki chỉ tờ có chữ; USER.md có
người nhận bàn giao; 04 trên nick; họ nhắn thử được.
