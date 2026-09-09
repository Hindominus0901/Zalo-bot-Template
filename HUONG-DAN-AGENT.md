# Hướng dẫn cho coding agent

> Nguồn sự thật khi **dựng bot cho một shop** từ template này. `CLAUDE.md` chỉ
> trỏ về đây. Sửa hướng dẫn thì sửa file này.

Bạn đang cầm một **template workspace OpenClaw**, không phải bot Python. Việc
của bạn là **phỏng vấn chủ shop** rồi điền giọng, kho, skill — để Gateway +
`zalouser` cầm một nick Zalo riêng, nói chuyện như người.

Chủ shop **không biết lập trình**. Với họ: chữ thường, ví dụ đời. **Cấm** nói
wiki, harness, brain, token, QR, OpenClaw, Gateway, persona — trừ khi họ hỏi.
Kỹ thuật chỉ nằm ở file này và phần “Bạn đang dựng” trong `PHONG-VAN.md`.

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

Đọc: `SOUL.md`, `AGENTS.md`, `docs/01-it-rao-da-dang.md`, `knowledge/moi-loai-cau-hoi.md`.

Không xóa ba rào trong `AGENTS.md` (tiền, nội bộ, jailbreak).

### B2 — Phỏng vấn

Nói đúng **câu chính** (dài, về sản phẩm/dịch vụ). Rồi **hỏi thêm từng câu**
trong `PHONG-VAN.md`. Đừng đọc cả khối “Hỏi thêm” một lần.

Câu 3: xin **tài liệu sản phẩm, dịch vụ, giá, chính sách** — không nói “đồ”.

### B3 — Viết file, chỉ từ miệng chủ + raw

| Nguồn | File |
|---|---|
| Tên nick, vibe | `IDENTITY.md` |
| Bán gì, khách lo, ranh giới, tin mở | `knowledge/persona.md` |
| Bàn giao, giờ gọi lại | `USER.md` |
| File/ảnh/link câu 3 | `knowledge/raw/` rồi tách `knowledge/wiki/` |
| FAQ miệng câu 6 | `wiki/` (lấp chỗ raw thiếu) |
| Slot lúc phân vân | `skills/khai-thac/SKILL.md` |

Giọng nền đã có trong `SOUL.md`. Chỉ thêm xưng hô + đoạn chat thật của họ.

Wiki: `knowledge/CLAUDE.md`. Một trang một câu hỏi. Phân vân public/internal → `internal/`.

**Cấm:** tự mở website/Facebook shop khi họ chưa đưa, rồi ghi giá vào wiki.

### B4 — Config kênh

Copy `config/openclaw.zalouser.example.json5` vào `openclaw.json` của **máy
Gateway** (`~/.openclaw/openclaw.json`) — merge, đừng ghi đè model/token có sẵn.

Bắt buộc với CSKH:

- `channels.zalouser.enabled: true`
- `dmPolicy: "open"` — khách lạ vào được (không phải `pairing` như Tom cá nhân)
- `groupPolicy: "allowlist"` trừ khi họ nói rõ muốn nhóm nào

**Không commit** `openclaw.json` thật, cookie, QR.

### B5 — Thử trong đầu trước khi QR

Đọc lại 5 câu FAQ họ vừa kể, đóng vai bot theo `SOUL.md` + wiki vừa viết. Sai
trang thì sửa wiki. Còn `[CHỜ CHỦ SHOP]` thì chưa xong.

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

- `IDENTITY.md` và `knowledge/persona.md` không còn `[CHỜ CHỦ SHOP]`
- Câu 3: file gốc nằm trong `raw/` **hoặc** chủ nói rõ là không có tài liệu
- Wiki tách từ raw + miệng; ≥ 5 trang nếu họ có đủ FAQ
- `USER.md` có tên người nhận bàn giao
- Thử 5 câu FAQ — không bổ sung bằng kiến thức ngành
- Họ nhắn thử được từ nick khác vào nick bot

File trong `knowledge/raw/` bị `.gitignore` trên bản mẫu. Shop giữ bản private thì
có thể `git add -f` nếu họ muốn kho nằm trong git.
