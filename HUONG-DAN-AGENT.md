# Hướng dẫn cho coding agent

> Nguồn sự thật khi **dựng bot cho một shop** từ template này. `CLAUDE.md` chỉ
> trỏ về đây. Sửa hướng dẫn thì sửa file này.

Bạn đang cầm một **template workspace OpenClaw**, không phải bot Python. Việc
của bạn là **phỏng vấn chủ shop** rồi điền giọng, kho, skill — để Gateway +
`zalouser` cầm một nick Zalo riêng, nói chuyện như người.

Chủ shop nhiều khả năng không biết lập trình. Đừng hỏi câu kỹ thuật nào ngoài
bước B0.

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

Câu đào sâu nhất buổi thường là **câu 2** (khách lo gì) và **câu 3** (tài liệu).
Bảng gộp một lúc thì hai câu đó bị lướt.

### 3. Không đổi kênh

Đây không phải Zalo Bot Creator, không phải OA. Nick riêng + QR `zalouser`.
Đừng bảo họ đi xin OA hay tạo "Bot …" trên Bot Manager.

---

## Thứ tự. Không nhảy bước.

### B0 — Máy và OpenClaw

Hỏi hoặc tự biết: Windows / macOS / Linux. Chỉ đưa lệnh hệ đó.

> Anh/chị đã cài OpenClaw và Gateway chạy được chưa ạ?

- Chưa → đi với họ theo docs OpenClaw (cài Gateway, chọn model). Đừng giả vờ
  template này tự cài OpenClaw hộ nếu môi trường của họ khác.
- Rồi → hỏi workspace đang ở đâu (`~/.openclaw/workspace` hay path khác). Template
  này **là** workspace: trỏ `agents.defaults.workspace` vào thư mục repo (bản
  private của họ, không phải bản mẫu công khai còn `[CHỜ CHỦ SHOP]`).

> Nick Zalo riêng cho bot đã có chưa? (Không dùng nick Zalo chính.)

Chưa có → bảo họ tạo nick + số riêng trước khi quét QR. Xem `docs/02-kenh-zalouser.md`.

Chưa cần quét QR lúc này. Dựng kho và file trước.

### B1 — Đọc khung, đừng đụng rào cứng

Đọc: `SOUL.md`, `AGENTS.md`, `docs/01-it-rao-da-dang.md`, `knowledge/moi-loai-cau-hoi.md`.

Không xóa ba rào trong `AGENTS.md` (tiền, nội bộ, jailbreak).

### B2 — Phỏng vấn

Làm đúng [`PHONG-VAN.md`](PHONG-VAN.md): **10 câu**, mỗi câu có đào. Từng câu một.

**Câu 3 là nhận tài liệu.** Đợi file/link. Cất vào `knowledge/raw/`, ghi
`raw/NGUON.md`. Đừng nhảy câu 4 khi họ chưa gửi gì và cũng chưa nói là không có file.

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
