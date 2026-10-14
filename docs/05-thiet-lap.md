# Thiết lập — cho người chưa từng cài

Chủ shop **không cần đọc file này** — họ đọc [`08-luong-chu-shop.md`](08-luong-chu-shop.md).
Coding agent đọc file này, rồi **bấm cùng họ**, nói chữ thường. Đường chính là
VPS + `scripts/vps.py` (`dung-bot/QUY-TRINH.md` phần NỐI, làm trước phỏng vấn).
File này cho ai chạy bot trên chính máy mình.

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
4. Model **nhìn được ảnh** — mặc định GPT-5.6 Terra (OpenAI). Chỉ chữ thì xem ảnh kém.
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
| OpenClaw | `2026.9.4` | `openclaw --version` |
| Plugin `@openclaw/zalouser` | `2026.9.4` | `openclaw plugins list` |
| Node | **`>=24.16.0 <25` hoặc `>=26.1.0`** | `node --version` |
| Python | 3.9 trở lên | `python3 --version` (Windows: `py --version`) |
| Ngày đối chiếu | 2026-09-11 | |

**Node là chỗ hay tắc nhất.** OpenClaw không chạy trên Node 25, và không chạy
dưới 24.16. Node 22 hay 23 thì **cài hỏng ngay** — `npm install` báo
`EBADENGINE` và không có lệnh `openclaw` nào được cài.

Đối chiếu tên key với tài liệu đi kèm chính bản đang cài — nó nằm ngay trong
package, không cần mạng:

```bash
ls "$(npm root -g)/openclaw/docs/channels/zalouser.md"
```

Cài đúng bản đã test, đừng lấy `latest`:

```bash
openclaw plugins install @openclaw/zalouser@2026.9.4
```

## Lệnh không chạy như tài liệu thì làm gì

Sẽ xảy ra: OpenClaw ra bản mới, đổi tên lệnh hoặc đổi tên key config. Template
trong tay bạn là bản chụp, **không có ai đẩy bản vá xuống**.

1. `openclaw --version` — so với bảng trên. Bằng nhau mà vẫn lỗi thì là lỗi khác,
   đọc kỹ thông báo.
2. Lệnh không có: `openclaw --help` tìm tên mới. **Đừng đoán tên.**
3. Key config không nhận: `openclaw config validate` chỉ đúng key sai, rồi
   `openclaw config schema` xem key thật tên gì. Key lạ bị **từ chối to**
   (*Unrecognized key*, gateway không lên). Cái nguy là key **đúng tên mà thiếu
   cặp** — validate chỉ ra *warning*, vẫn báo valid.
4. Vẫn tắc: hạ về đúng bản trong bảng trên.

Cùng kỷ luật đó áp cho mọi key trong `10-openclaw-config-mau.md`: `dmPolicy`,
`allowFrom`, `groupPolicy`, `requireMention`, `agents.defaults.workspace`,
`agents.entries.main.identity.name`, `mentionPatterns`. Kiểm bằng
`config validate` sau khi merge, đừng chép mù từ tài liệu.

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
- `allowFrom: ["*"]` ← **bắt buộc đi kèm** `open`. Thiếu = rơi hết tin khách lạ
- `groupPolicy: "allowlist"` + `groups."*": { enabled: true, requireMention: true }`
- `agents.entries.main.identity.name`: **Nami** (hoặc tên đã điền IDENTITY).
  **Không** đặt ở `agents.defaults` — key đó không tồn tại, gateway không lên
- `agents.defaults.workspace`: đường dẫn **tuyệt đối** tới thư mục repo

Merge xong **luôn chạy** — trước khi bật gateway:

```bash
openclaw config validate
```

Đọc **hết** kết quả, không chỉ dòng đầu. Hai kiểu lỗi:

- *Unrecognized key* → config hỏng, gateway không lên. Đặt key sai chỗ (hay gặp
  nhất: `identity` nằm trong `defaults`).
- Dòng **warning** dưới chữ `Config valid` → config chạy được nhưng **sai**. Hay
  gặp nhất: `dmPolicy="open" but allowFrom does not include "*"; all DMs will be
  dropped` — bot sống mà mọi khách nhắn riêng đều rơi. Lệnh vẫn ra exit 0, nên
  **đừng tin chữ "valid"**, đọc warning.

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
| Khách lạ nhắn không vào | Thiếu `allowFrom: ["*"]` (`config validate` có warning *all DMs will be dropped*); hoặc `dmPolicy` còn `pairing` → `open`. Restart gateway |
| Gateway không lên | `openclaw config validate` — thường là *Unrecognized key* (`identity` để trong `defaults`) |
| Nhóm im khi gọi Nami | `agents.entries.main.identity.name` không khớp IDENTITY (plugin đọc tên **trong config**); biệt hiệu thiếu tên gốc. **Đừng tắt `requireMention`** để chữa — tắt là bot trả mọi tin trong nhóm |
| Ảnh gửi vào bot bảo gõ lại | Model không vision / plugin zalouser cũ — cập nhật plugin |
| Mất tin lúc đi ngủ | Gateway tắt — bật lại, VPS nếu mở khách |
| Cookie chết, không gửi được | `openclaw channels logout --channel zalouser` rồi login QR lại |
| `npm.ps1` bị chặn | ExecutionPolicy như trên, cài lại |
| Bot trả lời bằng tiếng công ty | Thiếu đọc `SOUL.md` / workspace sai thư mục |

Chi tiết rủi ro nick: [`02-kenh-zalouser.md`](02-kenh-zalouser.md).
