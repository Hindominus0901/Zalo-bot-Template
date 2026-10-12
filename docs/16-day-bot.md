# Dạy bot và giao việc qua Zalo

Bot chạy rồi thì chủ shop **không cần người dựng** cho việc hằng ngày. Nhắn
riêng cho bot như nhắn nhân viên.

---

## Phần cho chủ shop

### Dạy bot

Nhắn **riêng** cho nick bot, nói thường — không cần câu lệnh:

> *Từ giờ khách hỏi ship Hà Nội thì báo 25k nha em.*
>
> *Đừng gọi khách là “bạn”, gọi anh/chị.*
>
> *Gói VIP giờ là 4 triệu 990, không phải 4 triệu 500 nữa.*
>
> *Cái em đề xuất hôm qua ok đó, áp đi.*

Bot sẽ **nhắc lại một câu và hỏi** *“em sửa nhé chị?”*. Chị gật thì bot mới
sửa, rồi đọc lại dòng mới. Từ **tin khách tiếp theo** bot đã nói theo cái mới.

Lỡ dạy sai: *“bỏ cái vừa sửa đi em”* — bot trả lại như cũ.

Mỗi tối bot tự xem lại hôm nay khách hỏi gì mà sổ chưa có, rồi **đề xuất** cho
chị. Chị chỉ cần nói *“ok”* với cái nào muốn giữ.

### Giao việc có giờ

> *9h sáng mai nhắc chị gọi lại chị Lan.*
>
> *Chiều thứ 6 nhắn chị Lan hỏi nhận hàng chưa.*
>
> *Sáng thứ 2 hàng tuần nhắn nhóm lớp lịch học tuần này, tới hết tháng 12.*
>
> *Em đang hẹn những gì?* · *Huỷ cái nhắn chị Lan đi.*

Bot hỏi lại cho đủ: **mấy giờ, gửi ai, nói gì, một lần hay lặp** — rồi đọc lại
để chị gật. Lời gửi khách bot viết thì bot đọc cho chị duyệt trước.

### Bot sẽ từ chối, kể cả chị bảo

- **Nhắn hàng loạt khách.** Zalo khoá nick gửi hàng loạt — mất nick là mất
  hết khách đang chat. Đăng trong nhóm thì được.
- **Nhắn người chưa từng chat với nick bot.**
- **Nói đã nhận tiền, đưa số tài khoản / mã QR.** Chuyện tiền luôn qua người.
- Thêm trang sổ mới, đổi tên bot, đổi cài đặt máy — nhờ người dựng.

### Chỉ dạy được khi nhắn riêng

Trong **nhóm**, kể cả chị nói *“từ giờ…”*, bot không sửa gì — nhóm có khách đọc
chung. Người khác nhắn riêng tự xưng là chị cũng không dạy được: máy kiểm
**nick**, không kiểm lời.

---

## Phần cho người dựng

### Bật lên

Cần **senderId của chủ** (`14-vps-headless.md` mục *Lấy senderId và groupId*),
rồi:

```bash
python3 scripts/dien_config.py
```

Script hỏi tên bot, senderId chủ, có tiết kiệm không → gộp vào config thật
bằng `openclaw config patch` (không ghi đè token gateway hay mã AI) → chạy
`openclaw config validate` và dịch warning ra chữ thường. Chặn sẵn lỗi hay gặp:
gõ **số điện thoại** thay cho senderId.

Bỏ trống senderId vẫn chạy được — chỉ là chưa ai dạy được. **Đóng an toàn**:
không khớp ai thì không ai là chủ.

### Cách khoá — ở tầng máy, không phải tầng chữ

| Rào | Ở đâu | Chặn gì |
|---|---|---|
| Hai agent | `agents.entries.main` / `admin` | Khách và chủ chạy hai bộ quyền khác nhau |
| Định tuyến | `bindings` khớp `peer: { kind: "direct", id: <senderId chủ> }` | Chỉ tin **riêng** từ đúng nick chủ vào `admin`. Nhóm luôn vào `main` |
| Chủ là ai | `commands.ownerAllowFrom` | Người không khớp: **code** gỡ `automations`, `gateway`, `sessions` |
| Tool bot khách | `main.tools.profile: "minimal"` + đọc, ghi, gửi tin, xem ảnh | Không shell, không web, không hẹn giờ, không xem phiên người khác |
| Skill bot khách | `main.skills` (danh sách cho phép) | Bot khách không nạp `day-bot`, `giao-viec` |
| Lớp hai | `admin.tools.toolsBySender` | Lỡ ai khác lọt vào `admin`: vẫn không ghi, không hẹn giờ, không gửi tin |
| Toàn cục | `tools.deny`, `elevated: false`, `fs.workspaceOnly` | Không ai chạy lệnh shell trên VPS, không ai ghi ra ngoài repo |
| Tự học tắt | `skills.workshop.autonomous.mode: "off"` | *“Từ giờ luôn…”* của khách không tự thành skill |

Lời dặn trong `AGENTS.md` và skill (*“chỉ chủ mới dạy được”*) là lớp **thứ
hai**. Lớp thứ nhất là config — model có muốn cũng không gọi được tool không có.

### Giới hạn — nói thẳng

- **Ghi file không khoá theo thư mục được.** OpenClaw chỉ có
  `fs.workspaceOnly` (cấm ghi **ra ngoài** repo). Muốn khoá từng thư mục thì phải
  chạy Docker sandbox — template chưa làm. Nghĩa là:
  - Bot **khách** có `write` (để ghi phiếu khách, `ghi_thieu`) và về kỹ thuật ghi
    được mọi file trong repo. Rào còn lại là `AGENTS.md` + `<policy>`. Cái mất
    đi so với trước: shell, web, hẹn giờ, đọc phiên người khác.
  - Bot **admin** ghi được `AGENTS.md`. Chấp nhận được vì chỉ chủ tới được đó —
    và `day-bot` liệt kê đúng chỗ được sửa, phải nhắc lại + chờ gật.
- **Chủ chuyển tiếp tin của khách vào chat riêng** là đường lọt duy nhất của
  lời lạ vào agent có quyền ghi. `day-bot` coi tin chuyển tiếp là dữ liệu; vẫn
  nên dặn chủ đừng dán nguyên tin lạ rồi bảo *“làm theo cái này”*.
- **Lùi xa hơn hôm nay** cần `git` — bot admin không có shell. Cài một lịch
  `git commit` mỗi đêm trên VPS (ngoài bot) thì có điểm lùi hằng ngày:

  ```bash
  ( crontab -l 2>/dev/null; echo '50 23 * * * cd /duong/toi/repo-shop && git add -A knowledge MEMORY.md SOUL.md AGENTS.md && git commit -qm "tu dong: so cuoi ngay" || true' ) | crontab -
  ```

  `memory/` (phiếu khách) đã nằm trong `.gitignore` — không commit dữ liệu khách.

### Đã kiểm thế nào

Trên OpenClaw **2026.9.4** + plugin `@openclaw/zalouser` 2026.9.4, Node v24.21.0:

- `openclaw config validate` — config mẫu, cả bản chưa điền và đã điền: *valid*,
  không warning.
- Hàm định tuyến của chính OpenClaw (`resolveAgentRoute`): chủ nhắn riêng →
  `admin`; khách A, khách B → `main`, **mỗi người một phiên**; chủ nhắn trong
  nhóm → `main`. Config template cũ: chủ, A, B **chung một phiên** `agent:main:main`.
- `openclaw skills list --agent`: `main` thấy 16/18 skill, không có `day-bot`,
  `giao-viec`; `admin` thấy 18/18; cả hai chạy đúng thư mục repo.
- `openclaw security audit`: config cũ **4 critical** — bot khách có `exec`,
  `process`, `apply_patch`, hẹn giờ, đổi gateway. Config mới còn 2, đều có lý do:
  token gateway (máy thật đã có từ `openclaw onboard`) và `automations` ở
  `admin` (chủ cần hẹn giờ; code gỡ với người không phải chủ).
- `scripts/dien_config.py` chạy trên config giả lập máy đã `onboard`: token
  gateway còn nguyên sau khi gộp.

**Chạy lượt bot thật** — OpenClaw thật, model thay bằng một máy chủ giả API
Claude ghi lại nguyên văn mọi request (`openclaw agent --local`):

| Thử | Kết quả |
|---|---|
| Tool bot khách nhận thật | `read`, `write`, `edit`, `message`, `view_image`, `session_status` — hết |
| Tool bot chủ, người gửi là chủ | thêm `write`, `edit`, `automations`, `message`; **không** `exec`, `terminal`, web, `gateway` |
| Tool bot chủ, người gửi lạ (lớp hai) | không ghi, không hẹn giờ, không gửi tin |
| Ra lệnh bot khách gọi `exec` / `automations` / `terminal` | OpenClaw từ chối cả ba: *"isn't available"* |
| Bot chủ gọi `write` | Ghi đúng `memory/nhat-ky-sua/` của repo shop |
| Sửa `MEMORY.md` / tờ wiki giữa hai lượt | Lượt sau thấy chữ mới, không restart |
| Khách B nhắn sau khách A | Request của B **không** có tên, SĐT của A |
| Prompt bot khách | Có `<policy>`, khối *Shop này + sổ*, SOUL, IDENTITY, USER, MEMORY; không có `TOOLS.md`. ~32.800 ký tự (template ~19.500 + khung OpenClaw ~13.000) |

Lần chạy này bắt được hai chỗ mà kiểm config không thấy: OpenClaw **tự thêm**
`apply_patch` đi kèm `write`/`edit`, và bot chủ có sẵn `terminal` / `portal` /
`dashboard` dù profile không liệt kê. Cả hai nay bị cấm tường minh.

**Chưa kiểm** — cần nick thật / mã API: giọng và độ khôn thật của Claude; lượt
heartbeat thật (follow-up); chủ nhắn riêng thật sự vào `admin` qua plugin
(đã kiểm hàm định tuyến, chưa kiểm tin Zalo thật đi qua nó); một việc hẹn giờ
thật gửi tới `user:<id>` / `group:<id>`; bot admin sửa sổ rồi bot khách nói theo
ở tin kế. Kịch bản thử: `04-kich-ban-thu.md` mục *Dạy bot*.
