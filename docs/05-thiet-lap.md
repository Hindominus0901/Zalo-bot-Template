# Thiết lập — cho người chưa từng cài

Chủ shop **không cần đọc file này** — họ đọc [`08-luong-chu-shop.md`](08-luong-chu-shop.md).
Coding agent đọc file này, rồi **bấm cùng họ**, nói chữ thường. Kịch bản phỏng
vấn xong mới tới đây (`HUONG-DAN-AGENT.md` B4–B7).

Còn `[CHỜ CHỦ SHOP]` trên persona / giá thì **chưa bật khách thật**.

Chuẩn xong: [`06-tieu-chuan.md`](06-tieu-chuan.md). Cách dùng sau khi chạy:
[`07-cach-dung.md`](07-cach-dung.md). File Drive: [`11-mcp-ung-dung.md`](11-mcp-ung-dung.md).

---

## Cần gì

Danh sách đầy đủ cho chủ shop: [`../CHUAN-BI.md`](../CHUAN-BI.md).
Dưới đây là bản cho người dựng.

1. Một **máy để mở suốt** (thử thì laptop; khách thật thì VPS). Tắt máy = mất tin.
2. Nick Zalo **riêng** cho nhân viên (Nami). Không cầm nick chính, không gắn ngân hàng.
3. Thư mục bot = repo này (đã phỏng vấn / đã điền).
4. Model **nhìn được ảnh** (Claude / GPT-4o / Gemini…). Chỉ chữ thì xem ảnh kém.
5. **API key của model** — chủ shop tự mở tài khoản và nạp tiền. Chưa có key là
   chưa dựng được; đừng hứa dựng xong rồi tính sau.
6. Trên máy đó: `git`, Python 3. Windows: cài Python nhớ tick **Add to PATH**;
   `python3` hay mở Microsoft Store nên dùng `py`.

Không xin OA. Không tạo “Bot …” trên Bot Manager.

---

## Đã test với

Template này viết theo hành vi của các bản dưới. **Người bán điền sau khi chạy
thật**, đừng để trống khi giao cho khách.

| Thứ | Bản | Lấy bằng lệnh |
|---|---|---|
| OpenClaw | `[CHỜ NGƯỜI BÁN]` | `openclaw --version` |
| Plugin `@openclaw/zalouser` | `[CHỜ NGƯỜI BÁN]` | `openclaw plugins list` |
| Node | `[CHỜ NGƯỜI BÁN]` | `node --version` |
| Python | 3.9 trở lên | `python3 --version` (Windows: `py --version`) |
| Ngày test | `[CHỜ NGƯỜI BÁN]` | |

Cài đúng bản đã test, đừng lấy `latest`:

```bash
openclaw plugins install @openclaw/zalouser@<bản-ở-bảng-trên>
```

## Lệnh không chạy như tài liệu thì làm gì

Sẽ xảy ra: OpenClaw ra bản mới, đổi tên lệnh hoặc đổi tên key config. Template
trong tay bạn là bản chụp, **không có ai đẩy bản vá xuống**.

1. `openclaw --version` — so với bảng trên. Bằng nhau mà vẫn lỗi thì là lỗi khác,
   đọc kỹ thông báo.
2. Lệnh không có: `openclaw --help` tìm tên mới. **Đừng đoán tên.**
3. Key config không nhận: `openclaw config schema` xem key thật tên gì.
   **Đừng thêm key mà `config schema` không có** — OpenClaw có thể nuốt im lặng,
   và mình tưởng đã bật.
4. Vẫn tắc: hạ về đúng bản trong bảng trên.

Cùng kỷ luật đó áp cho mọi key trong `10-openclaw-config-mau.md`: `dmPolicy`,
`groupPolicy`, `requireMention`, `agents.defaults.workspace`, `identity.name`,
`mentionPatterns`. Kiểm bằng `config schema` trước, đừng chép mù từ tài liệu.

---

## Windows (hay gặp)

1. Mở **PowerShell**. Nếu báo không chạy script:

```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope Process
```

2. Cài OpenClaw:

```powershell
iwr -useb https://openclaw.ai/install.ps1 | iex
```

Làm theo onboard. Workspace trỏ **đúng thư mục repo shop** (không để mặc định
trống nếu shop đã clone repo này).

3. Kiểm:

```powershell
openclaw --version
openclaw doctor
openclaw gateway status
```

Gateway chưa chạy: `openclaw gateway install` rồi `openclaw gateway status`.

## Mac / Linux

```bash
curl -fsSL https://openclaw.ai/install.sh | bash
openclaw onboard --install-daemon
openclaw doctor
openclaw gateway status
```

**VPS không màn hình → dừng ở đây, sang [`14-vps-headless.md`](14-vps-headless.md).**
Từ bước quét mã trở đi làm khác hẳn, và phần *quét lại khi phiên chết* là thứ
bắt buộc phải bàn giao cho chủ shop.

---

## Nối workspace CSKH

Config máy: `~/.openclaw/openclaw.json` (Windows: trong user OpenClaw).

**Merge** — đừng xóa model/token có sẵn. Một file nhìn gộp:
[`10-openclaw-config-mau.md`](10-openclaw-config-mau.md). Lấy khối trong
`config/openclaw.zalouser.example.json5`:

- `channels.zalouser.enabled: true`
- `dmPolicy: "open"` ← bắt buộc CSKH (không `pairing` như Tom)
- `groupPolicy: "allowlist"` + `groups."*".requireMention: true`
- `agents.defaults.identity.name`: **Nami** (hoặc tên đã điền IDENTITY)
- `agents.defaults.workspace`: đường dẫn **tuyệt đối** tới thư mục repo

```bash
openclaw plugins install @openclaw/zalouser
openclaw channels login --channel zalouser
```

Họ tự quét QR bằng **app nick nhân viên** trên điện thoại. Đừng nhận ảnh QR/cookie.

Máy không màn hình: [`14-vps-headless.md`](14-vps-headless.md) nhánh B.

`openclaw directory self --channel zalouser` — thấy nick bot thì login ổn.

---

## Model nhìn ảnh

Trong onboard / config agent: chọn model có vision. Không có vision: OpenClaw
vẫn để `media://inbound/…` — bảo coding agent kiểm model, đừng bảo khách “gõ lại
giúp em”.

---

## Thử

Từ **nick Zalo khác**, chạy hết [`04-kich-ban-thu.md`](04-kich-ban-thu.md)
(gồm ảnh CK, ảnh không chữ, tin dồn, nhóm).

Trên máy repo:

```bash
python3 -m unittest discover -s tests -v
Windows: thay `python3` bằng `py`.
```

Fail thì đọc tên test, sửa file workspace, chạy lại. Đừng đoán giá cho khớp.

---

## Lỗi hay gặp

| Hiện tượng | Làm |
|---|---|
| Khách lạ nhắn không vào | `dmPolicy` còn `pairing` → đổi `open`, restart gateway |
| Nhóm im khi gọi Nami | `identity.name` không khớp IDENTITY; biệt hiệu thiếu tên gốc |
| Ảnh gửi vào bot bảo gõ lại | Model không vision / plugin zalouser cũ — cập nhật plugin |
| Mất tin lúc đi ngủ | Gateway tắt — bật lại, VPS nếu mở khách |
| Cookie chết, không gửi được | `openclaw channels logout --channel zalouser` rồi login QR lại |
| `npm.ps1` bị chặn | ExecutionPolicy như trên, cài lại |
| Bot trả lời bằng tiếng công ty | Thiếu đọc `SOUL.md` / workspace sai thư mục |

Chi tiết rủi ro nick: [`02-kenh-zalouser.md`](02-kenh-zalouser.md).
