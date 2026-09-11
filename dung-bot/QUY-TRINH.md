# Quy trình dựng bot — B0 tới B7

**Đây là nguồn duy nhất.** Mọi cửa vào (Claude Code, Cursor, Copilot, README)
đều trỏ về file này. Đừng chép các bước ra chỗ khác — chép là lệch.

Coding agent nào cũng làm được. Bạn đang **dựng**, không đang trả lời khách.

Trước khi bắt đầu: [`../CHUAN-BI.md`](../CHUAN-BI.md) — thứ chủ shop phải tự có.
Thiếu là dựng nửa chừng tắc.

Câu hỏi đọc cho chủ: `PHONG-VAN.md` (nguồn) / `docs/bo-cau-hoi.md` (bản đọc —
đừng sửa hai nơi độc lập). Chủ muốn xem trước (chữ thường):
`docs/08-luong-chu-shop.md`, `docs/09-kho-va-du-lieu.md`. Đã khóa, đừng hỏi lại:
`docs/quyet-dinh.md`. Bản đồ repo: [`../HUONG-DAN-AGENT.md`](../HUONG-DAN-AGENT.md).

Làm **đúng thứ tự B0→B7**. Không nhảy QR trước phỏng vấn. Không tóm tắt rồi hỏi
“anh/chị sẵn sàng chưa” — hỏi câu B0 ngay.

Nói với chủ: skill `giao-tiep-chu`. File/Drive/MCP: skill `lam-viec-dung` +
`docs/11-mcp-ung-dung.md`.

Bot lúc chạy: `AGENTS.md` (OpenClaw nạp). Đừng sửa `AGENTS.md` / `TOOLS.md` /
`skills/*/SKILL.md` trừ khi chủ đổi việc thật (câu 7/9). Giọng nền
(`giong-noi.md`, `cach-tu-van.md`) **không viết lại** thành kịch bản OA.

---

---

## Luật — nhắc mỗi phiên

1. **Không bịa số shop.** Wiki + đoạn giá trong `persona.md` chỉ từ miệng chủ
   hoặc file họ đưa. Chưa có → `[CHỜ CHỦ SHOP: …]` rồi hỏi. Không “giá tham khảo”,
   không “shop kiểu này thường”.
2. **Không nói** wiki, harness, brain, token, QR, OpenClaw, Gateway, persona với
   chủ — trừ khi họ hỏi. Nói: sổ, nick nhân viên, quét mã, chỗ bot ngồi.
3. **Không đổi kênh.** Không OA, không Bot Creator, không “Bot …” trên Bot Manager.
4. **Không** tự mở web/Facebook shop rồi chép giá. **Không** copy số
   `docs/vi-du-file-da-dien.md` (Tiệm Mây = giả).
5. Câu 2 (khách ngại) và câu 3 (tài liệu) mỏng = buổi hỏng. Đào từng câu.

---

## B0 — Máy, nick, và mã kết nối AI

**Trước khi hỏi câu nào:** đọc `CHUAN-BI.md`. Đó là danh sách chủ shop phải tự
có. Thiếu mục nào thì lo mục đó xong rồi mới chạy tiếp — đừng dựng nửa chừng
rồi tắc.

Tự biết OS. Với họ hỏi **ba câu** (M1/M2/M3 trong `PHONG-VAN.md`):

> Mình làm trên máy tính anh/chị đang mở đó luôn nhé — Windows, Mac hay máy chủ
> thuê ngoài ạ?

> Bot dùng một nick Zalo như nhân viên riêng, không dùng nick chính. Nick đó có
> chưa, hay lát mình tạo cùng nhau?

> Bot suy nghĩ bằng AI thuê ngoài nên cần một mã kết nối anh/chị đăng ký — tài
> khoản Claude, ChatGPT hay Gemini loại có nạp tiền. Anh/chị có chưa ạ?

**Chưa có mã kết nối → dừng ở đây.** Mở tài khoản cùng họ trước. Dựng xong mà
không có key thì bot không nói được câu nào, và họ sẽ nghĩ mình làm hỏng.
Key **không** commit vào repo — nó đi thẳng vào config máy Gateway ở B4.

Máy chủ thuê ngoài không màn hình → bước quét mã làm khác, xem
`docs/14-vps-headless.md` **trước** khi tới B6.

| Họ nói | Bạn làm |
|---|---|
| Windows / Mac / Linux | Ghi nhớ. Cài chỗ bot ngồi **sau B3**, lệnh trong `docs/05-thiet-lap.md` |
| Chưa có nick nhân viên | Tạo nick Zalo mới **cùng họ** (số riêng). Đừng lấy nick chính, đừng gắn ngân hàng |
| Đã có nick | Ghi. QR sau B3, **họ** quét bằng app nick đó |
| Đã có OpenClaw trên máy | B4 merge, đừng cài đè. Workspace = thư mục repo shop |

Chưa quét mã lúc này. Nick: `docs/02-kenh-zalouser.md` (bạn đọc, họ không).

---

## B1 — Đọc khung, đừng đụng rào

Đọc hết (im): `SOUL.md`, `knowledge/giong-noi.md`, `knowledge/cach-tu-van.md`,
`AGENTS.md`, `TOOLS.md`, `docs/01-it-rao-da-dang.md`, `knowledge/hoi-thoai-mau.md`.

Không xóa ba rào `AGENTS.md` (tiền, nội bộ, jailbreak). Hình file đã điền:
`docs/vi-du-file-da-dien.md` — **cấm** chép số vào shop đang dựng.

---

## B2 + B3 — Hỏi rồi viết ngay

Mỗi chủ đề: nói **câu chính** trong `PHONG-VAN.md` (dài). Đợi họ kể. Rồi **một**
câu “Hỏi thêm” nếu họ chưa phủ. Đừng đọc cả khối Hỏi thêm.

**Viết file ngay sau mỗi chủ đề**, đừng chờ hết 10.

| Câu | Viết | Chưa có thì |
|---|---|---|
| 1 Bán/làm gì | `knowledge/persona.md` → Công việc. Món shop **không** bán → `wiki/public/ban-gi.md` | `[CHỜ CHỦ SHOP]`. Không có danh sách không-bán thì bot không dám nói *bên em không có* |
| 2 Khách ngại gì | `persona.md` → Khách và điều họ lo | `[CHỜ CHỦ SHOP]` |
| 3 Tài liệu | Cất `knowledge/raw/` nguyên. Một dòng `raw/NGUON.md`. Tách wiki (thuật toán dưới). Link Drive → skill `lam-viec-dung` + `mcp_drive` **chỉ nếu** MCP `enabled` | Chủ nói không có file → FAQ miệng câu 6; vẫn được |
| 4 Giọng, tên gọi, **mức lầy** | `IDENTITY.md` + `SOUL.md` đoạn cuối (xưng hô + 2–3 tin thật). Chủ muốn nghiêm hơn mặc định → ghi một dòng vào `persona.md` → Ranh giới. Config `identity.name` khớp lúc B4 | Tên mặc định **Nami**, giọng mặc định **vui và lầy** (`vui-va-ngoai-le.md`). Biệt hiệu nhóm: ghi `Gọi thêm` |
| 5 Không được tự ý | `persona.md` → Ranh giới (thêm của shop). Không xóa rào sẵn | Chủ muốn bot **đưa số tài khoản** → ghi rõ vào Ranh giới; mặc định template là **không đưa** |
| 6 FAQ miệng | Mỗi câu một tờ `wiki/public/` hoặc gom cùng chủ đề | Không đẻ số |
| 7 Bước đặt | `skills/ghi-don/SKILL.md` — chỉ bước shop này, giữ “không tự chốt” | — |
| 7b Sổ đơn | Có phần mềm + API → bật `sodon` trong `config/mcp.example.json5`; không có → để `enabled: false` | để tắt |
| 8 Kêu ai + follow-up | `USER.md`: tên, nick bàn giao, giờ gọi lại, **ngày nghỉ / Tết**, SĐT, ảnh, nhóm, **Follow-up** (tắt / giờ / câu mẫu). Ngày nghỉ chép luôn sang `wiki/public/gio-truc.md` | Follow-up chưa nói = **để CHỜ / tắt**. Ngày nghỉ chưa nói = để CHỜ, heartbeat không rào được |
| 9 Phân vân | `skills/khai-thac/SKILL.md` — đúng câu họ hay hỏi, 2–3 slot | — |
| 10 Câu đầu | `persona.md` → Tin mở | Không viết *hỗ trợ gì ạ* |

Wiki: `knowledge/CLAUDE.md`. Một tờ một câu hỏi. Phân vân công khai/nội bộ →
`internal/`. Template **đã có tờ chờ** (`wiki/TRANG-MAU.md`). Điền số; xóa
banner khi có số. Đừng tạo thêm tờ trống. Đừng copy shop giả.

Giọng nền đã có. Chỉ thêm xưng hô + tin thật vào `SOUL.md`. Đừng thay bằng
*cảm ơn đã liên hệ*, *đừng ngần ngại*.

### Tách wiki (câu 3) — làm đúng

1. Copy/ghi file gốc vào `knowledge/raw/`, giữ tên nguồn (`bang-gia-2026-04.pdf`).
2. Hàng `raw/NGUON.md`: ngày, ai gửi, công khai hay nội bộ.
3. Đọc hết. Cắt **nhiều tờ nhỏ**. Frontmatter như `CLAUDE.md` (`title`, `summary`,
   `updated`, `sources`).
4. Tên file: chữ thường, không dấu, gạch ngang. `public/` trừ vốn / hoa hồng /
   kịch bản khách khó → `internal/`.
5. File im + miệng chưa nói → giữ `[CHỜ CHỦ SHOP]` trên tờ chờ, bot chưa được dùng số.
6. Ảnh menu: đọc chữ, viết sổ; đừng bảo khách “xem file đính kèm”.
7. Đừng tạo thêm tờ trống. Đừng xóa tờ chờ chỉ vì chưa có số.

---

## B4 — Config (sau khi sổ đã có chữ)

Chi tiết bấm: `docs/05-thiet-lap.md`. Mẫu gộp một file:
`docs/10-openclaw-config-mau.md`. Nói với họ từng nút, ít tên phần mềm.

**Windows:** PowerShell → nếu chặn script:
`Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope Process` →
`iwr -useb https://openclaw.ai/install.ps1 | iex` → onboard. Workspace = **đường
dẫn tuyệt đối** thư mục repo shop.

**Mac/Linux:** `curl -fsSL https://openclaw.ai/install.sh | bash` →
`openclaw onboard --install-daemon`.

Kiểm: `openclaw --version` · `openclaw doctor` · `openclaw gateway status`.
Chưa chạy: `openclaw gateway install`.

Merge `config/openclaw.zalouser.example.json5` vào `~/.openclaw/openclaw.json`
(Windows: user OpenClaw). **Đừng xóa** model/token có sẵn.

Bắt buộc:

- `channels.zalouser.enabled: true`
- `dmPolicy: "open"` — không `pairing`
- `groupPolicy: "allowlist"` + `groups."*".requireMention: true`
- `agents.defaults.identity.name` **khớp** `IDENTITY.md`
- `agents.defaults.workspace` = path tuyệt đối repo
- Model **vision** (Claude / GPT-4o / Gemini…)

Biệt hiệu (*shop ơi*): `mentionPatterns` gồm **tên gốc + biệt hiệu**.

Hook boot: `openclaw hooks enable boot-md` (tuỳ). `BOOT.md` không nhắn khách.

**Không commit** `openclaw.json`, cookie, QR, phiếu thật.

---

## B5 — Thử trong đầu, rồi máy

Đóng vai Nami: 5 câu FAQ họ vừa kể + wiki vừa viết + `SOUL` / `giong-noi` /
`hoi-thoai-mau` (giọng, không lấy giá Tiệm Mây). Sai số → sửa **wiki**. Giọng
tổng đài → sửa `SOUL` đoạn shop / nhắc `giong-noi`, không sửa số.

Còn `[CHỜ CHỦ SHOP]` trên persona / giá → nói thật: chưa xong phần số, chưa mở
khách thật.

Trên máy repo — **chỉ mục trước, test sau**, rồi chạy giả lập:

```bash
python3 scripts/lam_chi_muc.py       # Mac / Linux
python3 -m unittest discover -s tests -v

# Windows:
# py scripts\lam_chi_muc.py
# py -m unittest discover -s tests -v
```

Rồi:

```bash
python3 -m sim.chay nhip     # rào follow-up có chạy đúng không
python3 -m sim.chay nen      # nền prompt có gì bay hơi lọt vào không
```

Hai lệnh này chạy **luật thật**, không cần nick. `sim/README.md`.

Vừa điền `summary` cho các tờ wiki xong → chỉ mục đang cũ. Không chạy lại thì
test đỏ ở `test_index_khop_thu_muc`, và bot sẽ đọc mô tả cũ để chọn tờ.

Xanh = **kho chữ khớp** (file, ma trận, rào trong markdown). **Không** = bot
sống trên nick. Fail → đọc tên test, sửa file, chạy lại. Đừng đoán giá cho khớp.

Mở khách: `docs/04-kich-ban-thu.md` trên nick thật + `docs/06-tieu-chuan.md`.

---

## B6 — Nối nick (cùng họ)

```bash
openclaw plugins install @openclaw/zalouser
openclaw channels login --channel zalouser
```

Họ quét mã bằng **app nick nhân viên**. Đừng nhận ảnh mã/cookie về chat.

`openclaw directory self --channel zalouser` — thấy nick thì ổn.

Từ **nick Zalo khác**, chạy hết `docs/04-kich-ban-thu.md`. `dmPolicy: open` →
không cần mã pairing.

---

## B7 — Sống 24/7

**Máy chủ thuê ngoài không màn hình → `docs/14-vps-headless.md`.** Bước quét mã
làm khác, và phải bàn giao cho chủ shop quy trình **quét lại** khi phiên chết —
không làm thì lần đầu bot im là họ không biết gọi ai.

Nói thẳng: tắt máy / ngủ = **mất tin lúc đó**. Khách thật cần máy chạy suốt
(VPS). Không tự thuê hộ. `docs/02-kenh-zalouser.md`.

---

## Xong khi (tick hết mới được nói ổn)

- [ ] Mã kết nối AI đã có và đã vào config (không nằm trong repo)
- [ ] `IDENTITY.md` có tên; `identity.name` khớp
- [ ] `persona.md` hết `[CHỜ CHỦ SHOP]` bắt buộc (câu 1–2, 4, 5, 10)
- [ ] Câu 3: có `raw/` **hoặc** chủ nói không có tài liệu
- [ ] Wiki chỉ tờ có dữ liệu; `internal/` không lộ
- [ ] `USER.md` có tên + nick nhận bàn giao + giờ gọi lại + **ngày nghỉ**
- [ ] Follow-up: đã hỏi; chưa nói = tắt
- [ ] Sinh lại chỉ mục rồi chạy test — xanh (kho chữ, không phải nick)
- [ ] `docs/04-kich-ban-thu.md` trên nick thật (sau QR) — **cửa mở khách**
- [ ] Họ nhắn thử được từ nick khác
- [ ] Khớp `docs/06-tieu-chuan.md`
- [ ] **Máy chủ không màn hình:** xong checklist cuối `docs/14-vps-headless.md`
      — gateway tự lên sau reboot, múi giờ Việt Nam, và chủ shop đã biết bốn
      bước quét lại mã

Unittest xanh mà chưa chạy 04 trên nick: **chưa** bảo mở khách.

---

## Lỗi hay gặp (nói chữ thường với chủ, sửa kỹ thuật im)

| Hiện | Làm |
|---|---|
| Khách lạ nhắn không vào | `dmPolicy` còn `pairing` → `open`, restart |
| Nhóm gọi tên không trả | `identity.name` lệch; biệt hiệu thiếu tên gốc |
| Ảnh vào bảo gõ lại | Model không vision / plugin cũ |
| Mất tin lúc đi ngủ | Gateway tắt |
| Cookie chết | `openclaw channels logout --channel zalouser` rồi login lại |
| Giọng tổng đài | Workspace sai thư mục / chưa đọc `SOUL.md` |
