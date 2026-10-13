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

**Thứ tự: nối máy trước, phỏng vấn sau.**

1. **B0** — ba câu chuẩn bị.
2. **NỐI** — nick Zalo của bot + VPS + bot chạy được (B4, B6, B7 làm ở đây, bằng
   `scripts/vps.py`).
3. **B1–B3** — phỏng vấn, viết sổ. **B5** — thử.
4. **ĐẨY SỔ** — đưa sổ lên VPS, nhắn thử, mở khách.

Lý do: người không rành máy kẹt ở phần máy, không kẹt ở phần kể chuyện shop. Làm
phần khó khi họ còn sức, và lúc phỏng vấn thì bot đã sống — viết xong tờ nào là
thử được tờ đó ngay trên Zalo.

Không tóm tắt rồi hỏi “anh/chị sẵn sàng chưa” — hỏi câu B0 ngay.

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

## Luật — người dựng không rành máy

Coi như người ngồi trước máy **chưa từng mở PowerShell / Terminal**. Đừng bắt
họ học.

1. **Bạn chạy mọi lệnh.** Không bao giờ bảo người gõ lệnh, mở PowerShell, mở
   Terminal, sửa file. Lệnh nào cũng là việc của bạn.
2. **Mỗi lần một việc**, tối đa ba dòng ngắn, gọi nút theo **đúng chữ trên màn
   hình** họ thấy (*bấm nút "Tạo VPS" màu xanh*), không theo tên kỹ thuật.
3. **Sau mỗi việc người làm trên màn hình:** *"Xong chưa ạ? Chỗ nào không thấy
   hay lạ thì chụp màn hình gửi vào đây, em xem giúp."* Dạy cách chụp ngay lần
   đầu:
   - Windows: bấm **Windows + Shift + S**, kéo chọn vùng, rồi bấm **Ctrl + V**
     vào ô chat này.
   - Mac: bấm **Cmd + Shift + 4**, kéo chọn vùng; ảnh ra ngoài màn hình nền, kéo
     ảnh đó vào ô chat.
   - Điện thoại: chụp màn hình, gửi vào **Cloud của tôi** trên Zalo, mở Zalo
     trên máy tính, lưu ảnh, kéo vào ô chat.
4. **Đọc ảnh rồi chỉ đúng một nút tiếp.** Ảnh mờ, thiếu thì xin chụp lại cả màn
   hình. Đừng đoán.
5. **Ảnh có mã AI (sk-ant-…), mật khẩu, mã QR đăng nhập** → bảo họ xoá ảnh đó.
   Với mã AI: vào console.anthropic.com **xoá mã đó, tạo mã mới**, vì ảnh chat
   đã lưu lại. Không bao giờ xin họ chụp mấy thứ này.
6. Kẹt hai lần cùng một chỗ → nói thật đang kẹt ở đâu, đề nghị nhờ người khác
   rành hơn làm riêng bước đó. Đừng vòng vòng.

Máy của người dựng chưa có Python thì bạn cài, không bảo họ cài:
Windows `winget install -e --id Python.Python.3.12` rồi gọi `py`; Mac thường đã
có `python3` (lần đầu máy hỏi cài công cụ dòng lệnh thì bảo họ bấm **Cài đặt**).

---

## B0 — Máy, nick, và mã kết nối AI

**Trước khi hỏi câu nào:** đọc `CHUAN-BI.md`. Đó là danh sách chủ shop phải tự
có. Thiếu mục nào thì lo mục đó xong rồi mới chạy tiếp — đừng dựng nửa chừng
rồi tắc.

**Đang chạy trong app chat** (Claude Cowork, ChatGPT Work, dots — không có
shell trên VPS): làm B0–B3, B5 nếu chạy được python, rồi **dừng ở B4**. Chạy
`python3 scripts/dong_goi.py`, đưa người dựng `docs/17-dung-bang-app-chat.md` để
chuyển sổ sang VPS. Đừng cài OpenClaw trong app, đừng nói đã làm B4–B7.

Máy chủ thuê ngoài mà người dựng chỉ có trình duyệt (không app SSH) →
`docs/18-cloudflare.md` phần 1. Đừng đề nghị cho bot sống trên Cloudflare
(phần 2 — chưa hỗ trợ).

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
| Windows / Mac / Linux | Máy này là chỗ **bạn** ngồi điều khiển. Bot sống trên VPS (phần NỐI). Không có VPS mà muốn chạy trên chính máy này → làm tay `docs/05-thiet-lap.md` |
| Chưa có nick nhân viên | Tạo nick Zalo mới **cùng họ** ở phần NỐI (số riêng). Đừng lấy nick chính, đừng gắn ngân hàng |
| Đã có nick | Ghi. Quét mã ở phần NỐI, **họ** quét bằng app nick đó |
| Đã có OpenClaw trên máy | B4 merge, đừng cài đè. Workspace = thư mục repo shop |

Nick: `docs/02-kenh-zalouser.md` (bạn đọc, họ không). Xong ba câu → **NỐI** ngay.

---

## NỐI — nick Zalo + VPS + bot chạy, trước khi phỏng vấn

Bạn chạy `scripts/vps.py` **trên máy này** (Windows dùng `py scripts\vps.py`). Nó
SSH vào VPS thay người, người không gõ lệnh nào. Đọc docstring đầu file một lần.

### N1. Nick Zalo của bot (người làm, bạn dẫn)

- SIM / số điện thoại **riêng** cho bot, không phải số chủ.
- Trên điện thoại: Zalo → đăng ký nick mới bằng số đó (Zalo cho một điện thoại
  giữ nhiều nick — *Cá nhân → Chuyển tài khoản → Thêm tài khoản*). Đặt tên và ảnh
  như nhân viên shop. **Không** gắn ngân hàng / ví.
- Xong: chụp màn hình trang cá nhân nick đó gửi vào để bạn chắc là nick mới,
  không phải nick chính.

### N2. Mã AI (người làm, bạn dẫn)

console.anthropic.com → đăng ký → **Billing**: nạp tiền → **API Keys → Create
Key**. Mã **chỉ hiện một lần**: bảo họ bấm Copy, **đừng** dán vào chat. Lát nữa
nó đi thẳng vào Notepad bạn mở (bước N4). Chụp màn hình các trang khác thì được.
Trang mã thì không.

### N3. VPS (người làm, bạn dẫn)

1. Chạy `vps.py khoa`. Giữ dòng `ssh-ed25519 …` nó in (an toàn để lộ).
2. Người thuê VPS ở nhà nào cũng được. Cần: **Ubuntu 22.04 hoặc 24.04**, **2 GB
   RAM** (1 GB vẫn chạy, máy sẽ tự thêm swap), đặt ở **Việt Nam hoặc
   Singapore**, đăng nhập **root**. Đọc ảnh họ chụp trang đăng ký để chỉ nút.
3. Trang tạo VPS có ô **SSH key / Khoá SSH** → dán dòng `ssh-ed25519 …` vào đó
   (gửi cho họ qua chat để họ copy). Không có ô đó → tạo xong mở **Console /
   VNC / Terminal** trên trang quản lý VPS, dán dòng `mkdir -p ~/.ssh && echo …`
   mà `vps.py khoa` in (đây là lần duy nhất người dán một dòng vào máy, và là
   dán, không phải gõ).
4. Xin họ chụp trang thông tin VPS → bạn đọc **địa chỉ IP**.

### N4. Bot chạy (bạn làm; người chỉ làm khi bạn gọi)

```
vps.py noi <IP>          # lưu địa chỉ, thử nối
vps.py day-len           # đẩy thư mục bot lên VPS
vps.py bat-dau           # chạy được bao nhiêu chạy bấy nhiêu
```

Bước cài máy chạy vài phút. Cho lệnh timeout dài hoặc chạy nền. `bat-dau` thoát
mã **3** = tới việc của người; dòng cuối `TRANG-THAI: {...}`:

| `can_nguoi` | Bạn làm | Người làm |
|---|---|---|
| `ma_ai` | `vps.py gui-ma-ai --mo` (mở Notepad) → chờ → `gui-ma-ai --gui` | Dán mã đã Copy ở N2 vào Notepad, bấm Lưu, đóng |
| `quet` | `vps.py lay-qr` — mã hiện lên màn hình máy này | Mở Zalo **nick bot** trên điện thoại → quét mã → quét hình trên màn hình → bấm đăng nhập |
| `chu` | Đọc mã `NAMI-xxxx` trong TRANG-THAI cho họ | Từ **nick chủ** nhắn đúng mã đó cho nick bot |
| `thu` | Đọc 5 câu trong TRANG-THAI | Từ một nick **khác** nhắn thử. Sổ chưa điền nên bot nói *chưa có số* — đúng |

Người làm xong → `vps.py bat-dau` lại. Ổn bước thử → `vps.py bat-dau --da-thu`.
Mã QR hết hạn → `lay-qr` lại. Bước `chu` không đọc được tin mà có đúng một
người vừa nhắn → hỏi chủ có phải họ không, rồi `bat-dau --chu-id <số>`.

`bat-dau` thoát **0** = máy xong: bot sống 24/7, chủ dạy được qua Zalo. Báo họ
một câu: *"Bot đã chạy, giờ mình kể về shop để bot biết nói gì."* → **B1**.

Lỗi lạ: `vps.py chay -- python3 scripts/kiem_tra_may.py`, đọc dòng đỏ, sửa.
Đừng đọc lỗi kỹ thuật cho người.

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
| 1b Kiểu shop | **Xóa tờ wiki không dùng** rồi chạy lại `scripts/lam_chi_muc.py` — bảng trong `knowledge/wiki/TRANG-MAU.md` | Bán hàng thì xóa `lo-trinh`/`ai-phu-hop`/`sau-khi-xong`; dịch vụ thì xóa `ship`/`kiem-hang` |
| 2 Khách ngại gì | `persona.md` → Khách và điều họ lo | `[CHỜ CHỦ SHOP]` |
| 3 Tài liệu | Cất `knowledge/raw/` nguyên. Một dòng `raw/NGUON.md`. Tách wiki (thuật toán dưới). Link Drive → skill `lam-viec-dung` + `mcp_drive` **chỉ nếu** MCP `enabled` | Chủ nói không có file → FAQ miệng câu 6; vẫn được |
| 4 Giọng, tên gọi, **mức lầy** | `IDENTITY.md` + `SOUL.md` đoạn cuối (xưng hô + 2–3 tin thật). Chủ muốn nghiêm hơn mặc định → ghi một dòng vào `persona.md` → Ranh giới. Config `identity.name` khớp lúc B4 | Tên mặc định **Nami**, giọng mặc định **vui và lầy** (`vui-va-ngoai-le.md`). Biệt hiệu nhóm: ghi `Gọi thêm` |
| 5 Không được tự ý + cam kết | `persona.md` → Ranh giới. Cam kết/không cam kết → `wiki/public/ai-phu-hop.md` + `lo-trinh.md` | Chủ muốn bot **đưa số tài khoản** → ghi rõ; mặc định **không đưa**. Bot **không bao giờ** hứa kết quả, kể cả chủ hay hứa ngoài đời |
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

Sổ điền ở máy này, bot chạy ở máy khác (app chat → VPS)? Chuyển bằng
`python3 scripts/dong_goi.py` → `python3 scripts/mo_goi.py`, hoặc GitHub — mọi
cách ở `docs/17-dung-bang-app-chat.md`.

---

## B4 — Config + máy (đã làm ở phần NỐI — đây là chi tiết và cách làm tay)

**Đường ngắn — một lệnh lo hết B4, B6, B7 (Linux / Mac):**

```bash
python3 scripts/bat_dau.py
```

Nó cài máy (Node, OpenClaw, plugin đúng bản ghim), điền config, vẽ mã QR ngay
trên terminal, cài gateway chạy 24/7, lấy senderId chủ, soi cả máy. Mỗi bước tự
kiểm "xong chưa" — **đứt giữa chừng thì gõ lại đúng lệnh đó**, nó chạy tiếp.

Nó chỉ dừng ở **bốn việc của người** — coding agent đọc output, chuyển đúng câu
đó cho chủ shop, chờ họ làm xong:

| | Người làm | Ai |
|---|---|---|
| ① | Dán mã AI (đã nạp tiền) | chủ / người giữ tài khoản AI |
| ② | Giơ điện thoại nick **bot** quét hình trên terminal | chủ |
| ③ | Từ nick **chủ**, nhắn mã `NAMI-xxxx` hiện trên màn hình | chủ |
| ④ | Từ một nick **khác**, nhắn thử năm câu | chủ hoặc người dựng |

`python3 scripts/bat_dau.py --xem` — chỉ xem bước nào xong. `--bo-qua chu` — để
bước nick chủ làm sau. Từng bước cũng chạy riêng được: `scripts/cai_dat.sh`,
`dien_config.py`, `quet_ma.py`, `lay_sender_id.py`, `kiem_tra_may.py`.

**Làm tay** — chỉ khi lệnh trên tắc, hoặc máy Windows:

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

**Điền config bằng script — đừng sửa JSON tay:**

```bash
python3 scripts/dien_config.py
```

Ba câu hỏi: tên bot, senderId chủ (bỏ trống được — chưa bật dạy bot), có tiết
kiệm không. Script gộp vào `~/.openclaw/openclaw.json` bằng `openclaw config
patch` (**không** xoá model/token có sẵn), sửa tên ở `IDENTITY.md` + config cho
khớp, rồi chạy `openclaw config validate` và báo warning bằng chữ thường.

senderId chủ chỉ có **sau khi** nick bot đăng nhập (B5). Lần đầu bỏ trống, quét
mã xong lấy ID (`docs/14-vps-headless.md` *Lấy senderId và groupId*) rồi chạy
lại: `python3 scripts/dien_config.py --chu <id>`.

Script không chạy được (không có `openclaw` trên máy này) thì nó ghi file đã
điền ra `openclaw.da-dien.json5` trong thư mục `config` để mang sang máy Gateway. Cái phải đúng —
script làm hết, đây để biết khi đọc lỗi (`docs/10` có bảng đủ):

- `dmPolicy: "open"` **và** `allowFrom: ["*"]` — thiếu `"*"` là rơi hết tin khách
- `session.dmScope: "per-channel-peer"` — mỗi khách một phiên (plugin Zalo cũng tự làm vậy; ghi rõ cho chắc)
- `identity` ở `agents.entries.<id>`, không ở `defaults`; tên khớp `IDENTITY.md`
- `workspace` ở **từng agent** — thiếu là agent chạy trong thư mục con rỗng
- Bot khách `tools.profile: "minimal"` — không shell, không web
- `openclaw config validate` → **đọc cả warning**. *Valid* mà có warning = chưa xong
- Model mặc định `anthropic/claude-opus-5` (có xem ảnh). Tiết kiệm: `claude-sonnet-5`

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

### Đẩy sổ lên VPS

```
vps.py day-so
```

Sổ vừa viết lên bot thật, bot dùng ngay tin sau. Nó **từ chối** nếu sổ trên VPS
đã đổi sau lần đẩy trước (chủ dạy bot qua Zalo trong lúc phỏng vấn) → chạy
`vps.py keo-so` trước, xem lại, rồi `day-so`. Phỏng vấn dài thì đẩy giữa chừng
cũng được, cứ xong vài chủ đề là đẩy, để chủ nhắn thử từng phần.

---

## B6 — Nối nick (cùng họ)

`bat_dau.py` bước 4 làm việc này. Làm riêng:

```bash
python3 scripts/quet_ma.py
```

Plugin Zalo **không** in mã ra terminal — nó ghi một file ảnh trên máy (đã đọc
trong mã nguồn plugin 2026.9.4). `quet_ma.py` vẽ ảnh đó thành mã QR ngay trong
cửa sổ SSH; mã đổi thì vẽ lại. Hết phải `scp` ảnh về.

Họ quét mã bằng **app nick nhân viên**. Đừng nhận ảnh mã/cookie về chat.

`openclaw directory self --channel zalouser` — thấy nick thì ổn.

Từ **nick Zalo khác**, chạy hết `docs/04-kich-ban-thu.md`. `dmPolicy: open` →
không cần mã pairing.

---

## B7 — Sống 24/7

`bat_dau.py` bước 5 cài gateway làm dịch vụ (tự lên khi máy khởi động lại), bước
7 soi cả máy. Soi lại bất cứ lúc nào: `python3 scripts/kiem_tra_may.py`.

**Máy chủ thuê ngoài không màn hình → `docs/14-vps-headless.md`.** Bước quét mã
làm khác, và phải bàn giao cho chủ shop quy trình **quét lại** khi phiên chết —
không làm thì lần đầu bot im là họ không biết gọi ai.

Nói thẳng: tắt máy / ngủ = **mất tin lúc đó**. Khách thật cần máy chạy suốt
(VPS). Không tự thuê hộ. `docs/02-kenh-zalouser.md`.

---

## Xong khi (tick hết mới được nói ổn)

- [ ] Mã kết nối AI đã có và đã vào config (không nằm trong repo, không nằm trong chat)
- [ ] `vps.py bat-dau` thoát 0; sổ đã `vps.py day-so`
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
| Khách lạ nhắn không vào | thiếu `allowFrom: ["*"]` hoặc `dmPolicy` còn `pairing`. `config validate`, restart |
| Gateway không lên | `config validate` — *Unrecognized key*, thường là `identity` để trong `defaults` |
| Nhóm gọi tên không trả | `identity.name` lệch; biệt hiệu thiếu tên gốc |
| Ảnh vào bảo gõ lại | Model không vision / plugin cũ |
| Mất tin lúc đi ngủ | Gateway tắt |
| Cookie chết | `openclaw channels logout --channel zalouser` rồi login lại |
| Giọng tổng đài | Workspace sai thư mục / chưa đọc `SOUL.md` |
