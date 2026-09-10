# Hướng dẫn cho coding agent

> Nguồn sự thật khi **dựng bot cho một shop** từ template này. `CLAUDE.md` chỉ
> trỏ về đây. Sửa hướng dẫn thì sửa file này.

Bạn đang cầm một **template workspace OpenClaw**, không phải bot Python. Việc
của bạn là **phỏng vấn chủ shop** rồi điền giọng, kho — để Gateway + `zalouser`
cầm một nick Zalo riêng, nói chuyện như người.

**Làm từng bước, đủ chi tiết:** skill
[`.claude/skills/khoi-tao/SKILL.md`](.claude/skills/khoi-tao/SKILL.md) — đọc rồi
chạy B0→B7, viết file ngay sau mỗi câu. Nói với chủ:
[`.claude/skills/giao-tiep/SKILL.md`](.claude/skills/giao-tiep/SKILL.md). File /
Drive / MCP: [`.claude/skills/lam-viec/SKILL.md`](.claude/skills/lam-viec/SKILL.md)
+ [`docs/11-mcp-ung-dung.md`](docs/11-mcp-ung-dung.md). Đừng chỉ đưa chủ `docs/08`
rồi đoán phần kỹ thuật.

Bot lúc chat khách (đừng nhầm với lúc dựng): system
`knowledge/system-prompt.md` · tool `TOOLS.md` · skill `skills/README.md`.

Chủ shop **không biết lập trình**. Với họ: chữ thường, ví dụ đời. Đưa họ
[`docs/08-luong-chu-shop.md`](docs/08-luong-chu-shop.md) và
[`docs/09-kho-va-du-lieu.md`](docs/09-kho-va-du-lieu.md) nếu muốn xem trước.
**Cấm** nói wiki, harness, brain, token, QR, OpenClaw, Gateway, persona — trừ
khi họ hỏi. Kỹ thuật chỉ nằm ở file này và phần “Bạn đang dựng” trong `PHONG-VAN.md`.

Đã khóa sẵn (đừng hỏi lại): [`docs/quyet-dinh.md`](docs/quyet-dinh.md).

---

## Ba điều tuyệt đối không được làm

### 1. Không bịa số liệu shop

Trang trong `knowledge/wiki/` và đoạn giá / ship / đổi trả trong `knowledge/persona.md`
chỉ viết từ **câu chủ shop đã nói**. Chưa hỏi thì ghi `[CHỜ CHỦ SHOP: …]` rồi hỏi.

Không có "giá tham khảo". Không có "shop kiểu này thường…". Kiến thức chung được
**bot** dùng khi chat với khách (phối đồ, giải thích khái niệm) — không được **bạn**
nhét vào wiki như chính sách của shop này.

### 2. Không bỏ phỏng vấn

Câu chính **nói dài, rõ sản phẩm/dịch vụ**. Đào thì **hỏi thêm từng câu**, đừng
nhồi. Câu 2 (khách ngại gì) và câu 3 (tài liệu) mỏng là buổi hỏng.

### 3. Không đổi kênh

Đây không phải Zalo Bot Creator, không phải OA. Nick riêng + QR `zalouser`.
Đừng bảo họ đi xin OA hay tạo "Bot …" trên Bot Manager.

---

## Thứ tự. Không nhảy bước.

### B0 — Máy và nick nhân viên

Tự biết Windows / macOS / Linux. Với họ chỉ hỏi:

> Mình làm trên máy tính anh/chị đang mở đó luôn nhé — Windows hay Mac ạ?
>
> Bot dùng một nick Zalo như nhân viên riêng, không dùng nick chính. Nick đó có
> chưa, hay lát mình tạo cùng nhau?

Chưa có OpenClaw trên máy: dẫn cài **bằng bước bấm**, đừng đọc tên Gateway trừ
khi cần. Workspace = thư mục repo (bản của họ). Nick: `docs/02-kenh-zalouser.md`.
Chưa quét QR lúc này.

### B1 — Đọc khung, đừng đụng rào cứng

Đọc: `SOUL.md`, `knowledge/giong-noi.md`, `knowledge/cach-tu-van.md`, `AGENTS.md`,
`knowledge/workflow-cskh.md`, `docs/01-it-rao-da-dang.md`,
`knowledge/moi-loai-cau-hoi.md`, `knowledge/hoi-thoai-mau.md`.

Không xóa ba rào trong `AGENTS.md` (tiền, nội bộ, jailbreak).

Hình file đã điền (shop **giả**): `docs/vi-du-file-da-dien.md` — **cấm** chép số
ở đó vào wiki / persona shop đang dựng.

### B2 — Phỏng vấn

Nói đúng **câu chính** (dài, về sản phẩm/dịch vụ). Rồi **hỏi thêm từng câu**
trong `PHONG-VAN.md`. Đừng đọc cả khối “Hỏi thêm” một lần.

Câu 3: xin **tài liệu sản phẩm, dịch vụ, giá, chính sách** — không nói “đồ”.

**Viết ngay sau mỗi câu** (đủ bước ở skill `khoi-tao`):

| Câu | File |
|---|---|
| 1–2, 5, 10 | `knowledge/persona.md` |
| 3 | `knowledge/raw/` + `raw/NGUON.md` + tách `wiki/` |
| 4 | `IDENTITY.md` + đoạn cuối `SOUL.md` |
| 6 | tờ `wiki/public/` |
| 7 | `skills/ghi-don/SKILL.md` (bước shop, giữ không tự chốt) |
| 8 | `USER.md` kể cả Follow-up (chưa nói = tắt) |
| 9 | `skills/khai-thac/SKILL.md` (slot) |

### B3 — Viết file, chỉ từ miệng chủ + raw

| Nguồn | File |
|---|---|
| Tên nick, tên gọi, vibe | `IDENTITY.md` + `agents.defaults.identity.name` (khớp nhau) |
| Xưng hô + 2–3 tin thật của chủ | `SOUL.md` đoạn cuối — **không** viết lại `giong-noi.md` / `cach-tu-van.md` |
| Bán gì, khách lo, ranh giới, tin mở | `knowledge/persona.md` |
| Bàn giao, giờ gọi lại, nhóm nội bộ | `USER.md` |
| Follow-up: tắt / delay / câu mẫu sau đơn | `USER.md` (câu 8). Chưa điền = **tắt** |
| File/ảnh/link câu 3 | `knowledge/raw/` rồi tách `knowledge/wiki/` — danh sách trang: `wiki/TRANG-MAU.md` |
| FAQ miệng câu 6 | `wiki/` (lấp chỗ raw thiếu) |
| Slot lúc phân vân | `skills/khai-thac/SKILL.md` |
| Bước chốt đơn / đặt | `skills/ghi-don/SKILL.md` (câu 7) |

Giọng nền đã có trong `SOUL.md` + `giong-noi.md` + `cach-tu-van.md`. Chỉ thêm
xưng hô + đoạn chat thật của họ vào `SOUL.md`. Đừng thay bằng kịch bản OA
(*cảm ơn đã liên hệ*, *đừng ngần ngại*).

Wiki: `knowledge/CLAUDE.md` (chữ thường cho chủ: `docs/09-kho-va-du-lieu.md`).
Một trang một câu hỏi. Phân vân public/internal → `internal/`.
Trang địa chỉ / sỉ-CTV / VAT / kiểm hàng: chỉ tạo khi chủ có dữ liệu (`wiki/TRANG-MAU.md`).

Tách raw: (1) cất nguyên (2) dòng `NGUON.md` (3) cắt tờ nhỏ + frontmatter
(4) không dấu, gạch ngang (5) im + chưa nói = `[CHỜ CHỦ SHOP]` (6) **cấm** file trống.

**Cấm:** tự mở website/Facebook shop khi họ chưa đưa, rồi ghi giá vào wiki.
**Cấm:** copy giá từ `docs/vi-du-file-da-dien.md` (Tiệm Mây là shop bịa).

### B4 — Config kênh

B4–B7 chi tiết bấm nút (Windows/Mac, QR, lỗi hay gặp): [`docs/05-thiet-lap.md`](docs/05-thiet-lap.md).
Chuẩn xong: [`docs/06-tieu-chuan.md`](docs/06-tieu-chuan.md).

Copy `config/openclaw.zalouser.example.json5` vào `openclaw.json` của **máy
Gateway** (`~/.openclaw/openclaw.json`) — merge, đừng ghi đè model/token có sẵn.

Bắt buộc với CSKH:

- `channels.zalouser.enabled: true`
- `dmPolicy: "open"` — khách lạ vào được (không phải `pairing` như Tom cá nhân)
- `groupPolicy: "allowlist"` trừ khi họ nói rõ muốn nhóm nào
- `groups."*".requireMention: true` — nhóm phải gọi tên / @ / reply
- `agents.defaults.identity.name` **khớp** `IDENTITY.md` (mặc định Nami)

Có biệt hiệu (*shop ơi*): `agents.entries.main.groupChat.mentionPatterns` gồm
**tên gốc + biệt hiệu**. Chỉ ghi biệt hiệu thì hết nhận *Nami ơi*.

Muốn checklist lúc Gateway bật: `openclaw hooks enable boot-md`. `BOOT.md` **cấm**
nhắn khách và **cấm** burst follow-up lúc restart; bàn giao dở chỉ gửi kênh trong
`USER.md`. Follow-up (nếu chủ bật) nằm ở `HEARTBEAT.md` + skill `follow-up`.

**Không commit** `openclaw.json` thật, cookie, QR.

### B5 — Thử trong đầu, rồi thử nick

Đọc lại 5 câu FAQ họ vừa kể, đóng vai bot theo `SOUL.md` + `giong-noi.md` +
`cach-tu-van.md` + wiki vừa viết + `knowledge/hoi-thoai-mau.md` (giọng, không lấy
giá mẫu). Sai trang thì sửa wiki. Giọng tổng đài thì sửa giọng, không sửa wiki.
Còn `[CHỜ CHỦ SHOP]` trên persona / giá thì chưa xong phần số.

Sau QR: chạy [`docs/04-kich-ban-thu.md`](docs/04-kich-ban-thu.md) từ nick khác
và `python3 -m unittest discover -s tests -v` trên máy repo.

### B6 — Nối nick (cùng họ)

Trên máy Gateway:

```bash
openclaw plugins install @openclaw/zalouser
openclaw channels login --channel zalouser
```

Họ quét QR bằng **app nick bot**. Đừng nhận QR/screenshot cookie về chat.

Nhắn thử từ một nick khác. `dmPolicy: open` thì không cần mã pairing.

### B7 — Sống 24/7

Nói thẳng: tắt Gateway / máy ngủ = **mất tin lúc đó**. Khách thật thì cần VPS.
Xem `docs/02-kenh-zalouser.md`. Không tự thuê VPS hộ.

---

## Xong khi

- `IDENTITY.md` có tên (Nami hoặc tên chủ chọn); `identity.name` trên config khớp
- `knowledge/persona.md` không còn `[CHỜ CHỦ SHOP]` bắt buộc (câu 1–2, 4, 5, 10)
- Câu 3: file gốc nằm trong `raw/` **hoặc** chủ nói rõ là không có tài liệu
- Wiki tách từ raw + miệng; tạo trang trong `wiki/TRANG-MAU.md` **chỉ khi có dữ liệu**
- `USER.md` có tên + nick người nhận bàn giao + giờ gọi lại
- Thử theo `docs/04-kich-ban-thu.md` — không bổ sung bằng kiến thức ngành
- Họ nhắn thử được từ nick khác vào nick bot

File trong `knowledge/raw/` bị `.gitignore` trên bản mẫu. Shop giữ bản private thì
có thể `git add -f` nếu họ muốn kho nằm trong git.
