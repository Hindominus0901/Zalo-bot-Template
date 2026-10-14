# Lịch sử template

Đọc trước khi kéo bản mới. Cách kéo: [`docs/15-cap-nhat.md`](docs/15-cap-nhat.md).

Bản nào đổi thứ shop đang phụ thuộc — tên trường phiếu, tên tool, tên tờ wiki,
tên file — **phải ghi ở đây**. Không ghi = coi như không đổi.

## 0.4.9 — chạy thử đầu cuối như người mua, sửa ba lỗi lòi ra

Chạy **trọn quy trình người mua** trong container:
- "máy người dựng" là bản zip giải nén, HOME mới tinh;
- "VPS" là `sshd` với một user mới có mật khẩu, chưa cài gì;
- GPT là máy giả API.

**Chạy được:** test trong bản zip · `mat-khau` → `noi --mat-khau` (tự cài
paramiko, cài chìa khoá, xoá file mật khẩu) · `day-len` · `bat-dau` cài máy từ
con số không (Node 24.21 có kiểm SHA256, OpenClaw 2026.9.4, plugin Zalo) →
dừng ở mã AI · `gui-ma-ai` mã `sk-proj-…` → onboard OpenAI + config
`gpt-5.6-terra` (file mã tạm xoá ở cả hai đầu) · `day-so` · `thu-giong` qua SSH
(10 câu tới GPT, bảng đúng) · chủ sửa trên VPS → `day-so` từ chối → `keo-so` ·
`lay-qr` khi chưa có mã báo chữ thường · `kiem_tra_may` · `bat-dau --xem`.

**Ba lỗi đã sửa:**
- **`day-so` lần hai bị chặn oan** — báo "sổ trên VPS đã đổi" với chính các tờ
  mình vừa đẩy. Mốc đồng bộ tính tới giây, file ghi trong cùng giây bị coi là
  mới hơn. Nay mốc +1 giây, có test.
- Cài paramiko in hai dòng cảnh báo pip tiếng Anh → nay im, chỉ in khi lỗi.
- Qua SSH, dòng `▶ bước` in sau phần cài (Python gom chữ) → nay in từng dòng.
  Sau `day-so`, VPS in "Bước tiếp: bat_dau.py" dễ làm agent hiểu nhầm → nay in
  "bot dùng ngay từ tin sau".

**Không chạy được ở đây** (giới hạn của container, không phải lỗi bot):
- quét mã Zalo — container không vào được máy chủ Zalo;
- gateway làm dịch vụ — không có systemd;
- đổi múi giờ — không có timedatectl;
- giọng thật — không có mã GPT thật.

## 0.4.8 — đúc giọng của chủ như bot chị Thanh, và chủ chấm giọng bot thật

So lại lớp giao tiếp với bot chị Thanh: **nền giọng giống hệt**. Bot chị nói
hay hơn nhờ **phần giọng riêng của chủ** — template có nhưng mỏng (mục shop
trong `SOUL.md` chỉ có 2 dòng chờ, bot chị có ~50 dòng). Mang về **cách đúc
giọng**, không mang chữ của chị.

- **`SOUL.md` mục *Shop này — giọng của chủ*: tám ô** —
  1. xưng hô;
  2. câu cửa miệng (một cái mỗi tin);
  3. nét giọng + cách làm;
  4. ví dụ đời thường chủ hay ví;
  5. câu thật của chủ (nghe nhịp, đừng thuộc);
  6. chữ của nghề được / không được nói;
  7. mức đùa + khi nào tắt;
  8. có thúc khách không.

  Thêm luật **mượn giọng, không mượn đời tư**. Hình đã điền:
  `docs/vi-du-file-da-dien.md`.
- **Phỏng vấn lấy giọng thật:**
  - xin video / livestream / Zoom / tin thoại của chủ — *trang bán lấy số, nói
    chuyện thật lấy giọng*;
  - hỏi thêm câu cửa miệng, ví dụ chủ hay ví, cách nói chuyện giá, có bảo khách
    *chưa cần mua* không.
- **`hoi-thoai-shop.md` có danh mục 9 nhóm** — mở đầu · chọn · tiền · chuyên
  môn · sau mua · nhóm · khó · bot nói trước · kết.
  - Rút gọn từ 54 tình huống của bot chị Thanh.
  - Tối thiểu 20 tình huống, nhóm A, B, C, G, I mỗi nhóm ≥ 2.
- **Thử giọng với chủ** — cổng mới trước khi mở khách:
  - `scripts/thu_giong.py` / `vps.py thu-giong` cho **bot thật** trả từng tình
    huống, in cạnh câu chủ từng trả;
  - mỗi câu một phiên riêng, không lên Zalo;
  - chủ chấm, sửa đúng chỗ, chạy lại — **xong khi chủ nói "giống" ≥ 8/10**.
  - Đã chạy thật với OpenClaw + máy giả GPT: ba câu, ba phiên riêng, phiên cũ
    không đổi.

**Chưa chạy thật:** giọng thật với GPT thật; chủ thật chấm. Kịch bản: `docs/04`
dòng 100–102.

## 0.4.7 — nhanh hơn, và học thêm từ bot chị Thanh

Đọc lại kỹ repo chị Thanh: so từng file khác nhau, đọc hết 3 skill riêng và các
file nhóm, hội thoại, VPS. Lấy về những gì dùng được cho mọi shop.

- **Trả nhanh hơn:** bot trả khách suy nghĩ `low` (trước `high` — model nghĩ
  lâu trước mỗi tin). Bot của chủ giữ `high`, vì sửa sổ sai một chữ là sai cho
  mọi khách. Đã đo bằng OpenClaw thật + máy giả GPT: request bot khách gửi
  `reasoning.effort: low`, bot chủ `high`. Nhanh hơn bao nhiêu giây thì chưa đo
  — cần mã GPT thật.
- **Bản đồ hội thoại của shop** — `knowledge/hoi-thoai-shop.md` (mới, của shop):
  - mỗi tình huống thật có **sai / đúng** theo đúng chữ chủ;
  - phỏng vấn chủ đề 4 giờ xin **ảnh chụp đoạn chat thật** (5–10 đoạn), không
    chỉ một tin;
  - chủ dạy qua Zalo *"lần sau ai hỏi X thì nói Y"* thì `day-bot` ghi thêm
    tình huống vào đây;
  - `AGENTS.md` đọc file này trước mẫu chung. Đây là cái làm bot chị Thanh nghe
    như người của chị.
- **Phán đoán trong nhóm** — `knowledge/trong-nhom.md` (mới):
  - đọc nhóm trước khi gõ; nhiều người hỏi dồn; một tin ba câu hỏi;
  - có người trả lời sai thì bổ sung, không bẻ mặt;
  - chặn cháy (tài khoản lạ, lộ thông tin riêng, link giả);
  - việc phải kéo ra khỏi nhóm.
- **Skill mới:**
  - `nhip-nhom` — heartbeat nhắc lịch / sự kiện trong sổ vào nhóm, một tin một
    nhóm một ngày, mặc định tắt. Cấu hình ở `USER.md` mục *Nhóm*, ghi lại ở
    `memory/nhom/`.
  - `thong-bao-lich` — chỉ bot của chủ: gửi một thông báo vào nhóm **ngay**,
    đọc lại, chờ gật. Gửi lúc khác / định kỳ vẫn là `giao-viec`.
  - `cham-bai` — **tuỳ chọn** cho shop dạy học. Tắt sẵn, bật bằng
    `dien_config.py --cham-bai`; khung chấm mẫu `knowledge/khung-cham-mau.md`.
  - Đã kiểm bằng OpenClaw thật: bot khách thấy `nhip-nhom`, không thấy
    `thong-bao-lich` / `cham-bai`; bot của chủ thấy cả.
- **Sửa một chỗ sai của chính repo chị Thanh khi mang về:**
  - Bản của chị cho bot tự "chặn cháy" trong nhóm **khi chưa ai gọi**. Nhưng
    plugin Zalo không cho bot thấy tin chưa gọi tên (`requireMention`), nên luật
    đó không chạy được.
  - Bản của mình ghi đúng: chỉ chặn cháy khi đã được gọi vào cuộc. Bot không
    "canh nhóm" được.
- Chưa mang về: **phân tầng khách** (nhóm VIP / thường trả sâu khác nhau) và
  **nhóm điều khiển của chủ**. Riêng của chị Thanh, cần chủ chọn.

**Chưa chạy thật:** nhịp nhóm và thông báo nhóm trên Zalo thật; tốc độ với GPT
thật; chấm bài với bài thật. Kịch bản: `docs/04` dòng 93–99.

## 0.4.6 — 123host + GPT-5.6 Terra, nối VPS bằng mật khẩu, Codex app

Mặc định mới: VPS **123host**, AI **GPT-5.6 Terra** (mã OpenAI API), agent
**Codex app**. Không VNC, không ô SSH key, không PowerShell.

- **Nối VPS bằng mật khẩu root** mà 123host gửi qua email:
  - `vps.py mat-khau --mo` mở Notepad, người dán mật khẩu vào.
  - `vps.py noi <IP> --mat-khau` nối **một lần** (paramiko — tự cài nếu
    thiếu), cài chìa khoá, xoá file mật khẩu.
  - Mật khẩu không in ra màn hình. Sai mật khẩu thì báo chữ thường, giữ file để
    sửa.
- **GPT thay Claude, vẫn nhận cả hai:**
  - `bat_dau.py` nhận mã theo tiền tố: `sk-ant-` → Anthropic, `sk-…` →
    OpenAI.
  - `dien_config.py --nha-ai openai|anthropic`, mặc định openai.
  - Model `openai/gpt-5.6-terra`, dự phòng `openai/gpt-5.4`. Tiết kiệm:
    `openai/gpt-5.6-luna`.
- **Đã chạy thật với OpenClaw 2026.9.4 + máy giả OpenAI API:**
  - onboard bằng `--openai-api-key`, config hợp lệ, `models status` thấy
    openai.
  - Một lượt bot khách đi `/v1/responses`, model `gpt-5.6-terra`, suy luận
    `high`. Công cụ: `read / write / edit / message / view_image /
    session_status`, **không** có quyền chạy lệnh.
  - Bot của chủ có `write / edit / automations / message` khi đúng nick chủ;
    khi không phải nick chủ thì bị lớp `toolsBySender` cắt đúng như thiết kế.
- **Chi phí ghi thật hơn:** một lượt bot khách ≈ 46 nghìn ký tự (đã đo). Ước
  chừng 300–2.000 đồng mỗi tin khách — `CHUAN-BI.md`. Chưa đo bằng tiền thật.
- Docs:
  - `BAT-DAU`: Codex app trước, Claude desktop (cần Git for Windows) sau.
  - `QUY-TRINH` N2 (platform.openai.com, Billing, API keys — khác ChatGPT
    Plus), N3 (123host, mật khẩu, không VNC).
  - `CHUAN-BI`, `PHONG-VAN` M3, `docs/05`, `docs/04` dòng 89–92.

**Chưa chạy thật:** VPS 123host thật (email, có cho đăng nhập mật khẩu không);
mã GPT thật (giọng, độ khôn, tiền thật); Codex app trên Windows thật.

## 0.4.5 — người không rành máy tự dựng được: máy trước, phỏng vấn sau

Người dựng không cần biết PowerShell / Terminal. Nhận zip → mở bằng Claude Code
hoặc Codex → gõ *bắt đầu dựng bot*. Agent chạy mọi lệnh; người chỉ bấm nút theo
lời dẫn, kẹt thì **chụp màn hình gửi agent**.

- **Đổi thứ tự** (`QUY-TRINH`): B0 → **NỐI** (nick Zalo bot, mã AI, VPS, bot
  chạy) → phỏng vấn → `vps.py day-so` → thử. Lúc phỏng vấn bot đã sống, viết
  xong tờ nào thử được ngay.
- **Luật mới cho agent:** không bắt người gõ lệnh; mỗi lần một việc, gọi nút
  đúng chữ trên màn hình; dạy cách chụp màn hình (Windows / Mac / điện thoại);
  ảnh có mã AI thì bảo xoá ảnh + tạo mã mới.
- `scripts/vps.py` (mới) — agent trên máy người dựng điều khiển VPS qua SSH:
  - `khoa` tạo chìa khoá và in dòng để dán vào trang tạo VPS.
  - `noi`, `day-len` đẩy code (VPS đã chạy thì **không** đè sổ).
  - `bat-dau` chạy cả quy trình trên VPS.
  - `gui-ma-ai --mo/--gui`: mã AI đi qua Notepad, không qua chat, không in ra.
  - `lay-qr` kéo ảnh mã đăng nhập về **mở trên màn hình**.
  - `day-so` / `keo-so`: từ chối đè khi chủ vừa dạy bot qua Zalo.
  - `chay` chạy một lệnh bất kỳ trên VPS.
- `bat_dau.py --tu-dong` — không hỏi gì. Tới việc người thì thoát mã 3, kèm
  dòng `TRANG-THAI: {json}` (ma_ai / quet / chu / thu). Đăng nhập Zalo chạy
  nền, sống qua lúc SSH đóng. Mã `NAMI-xxxx` giữ nguyên giữa các lần gọi.
- `BAT-DAU.md` (mới) — trang đầu cho người mua bản zip.
  `scripts/lam_ban_zip.py` — người bán đóng zip từ `git archive`, chặn lọt bí mật.
- Test `test_file_no_that_bi_ignore` không còn đỏ oan khi giao bằng zip (không có `.git`).

Đã chạy thật trong container: `sshd` làm "VPS", user riêng.
- Chạy đủ chuỗi: khoa → dán dòng vào console → noi → day-len → bat-dau (cài máy
  thật, dừng ở mã AI) → gui-ma-ai → bat-dau (onboard + config thật, file mã đã
  xoá ở cả hai đầu).
- Dừng ở quét mã vì container không vào được máy chủ Zalo.
- lay-qr: ảnh khớp từng byte. day-so → chủ sửa trên VPS → day-so từ chối → keo-so.

**Chưa chạy thật:** Windows thật (Notepad, `os.startfile`, `py`); VPS thật ở
nhà cung cấp; điện thoại quét ảnh mã trên màn hình; nhắn mã chủ qua Zalo thật;
gateway làm dịch vụ khi đăng nhập root. Kịch bản: `docs/04` dòng 85–88.

## 0.4.4 — Cloudflare: vào VPS bằng trình duyệt; tra kỹ dots

- `docs/18-cloudflare.md` mới.
  - **Phần 1** — Cloudflare Tunnel + Access, terminal ngay trong trình duyệt:
    người dựng không cần app SSH, VPS đóng được cổng 22. Đóng cổng chỉ **sau
    khi** đã vào được, luôn giữ console nhà cung cấp làm dự phòng. Đã kiểm lệnh
    `cloudflared service install` (bản 2026.10.0).
  - **Phần 2** — cho bot sống trên Cloudflare (`cloudflare/moltworker`): **chưa
    hỗ trợ**. Đọc mã nguồn thấy dự án ghi *experimental*, ghim OpenClaw
    2026.3.23 + Node 22 (template cần 2026.9.4 + Node 24), tốn ≈ $34,5/tháng.
    Bản chụp lưu phiên lên R2 chỉ chạy khi **bấm tay**, nên container khởi động
    lại là mất phiên Zalo. Các bài hướng dẫn nói "tự sao lưu mỗi 5 phút" là
    viết theo bản cũ.
- `docs/17` thêm mục **dots — đã tra kỹ**: máy cloud không có sudo / Docker,
  không có Zalo, không nối được VPS không màn hình (cần app desktop), gói Pro /
  Business Premium, chưa xác nhận có ở Việt Nam, tuần đầu nhiều lỗi. Dùng làm
  người dựng phần chữ được; làm chỗ bot sống thì không.

**Chưa chạy thật:** tunnel + terminal trình duyệt + quét QR trong tab;
moltworker với Zalo; dots.

## 0.4.3 — dựng bằng app chat (Cowork, ChatGPT Work, dots), chuyển sổ sang VPS

**App chat làm được phần chữ, không làm được chỗ bot sống.** Claude Cowork,
ChatGPT Work, OpenAI dots hỏi chủ + điền sổ được (B0–B3). Gateway 24/7 giữ phiên
Zalo thì không: phiên cloud của Cowork xoá khi xong, dots không có sudo / systemd.
Bot vẫn ở VPS. Tra web 12/10/2026, tin bên thứ ba — `docs/17` ghi rõ.

Mới:

- `docs/17-dung-bang-app-chat.md` — bảng ba app, **câu mở đầu dán sẵn** (các app
  này không chắc tự nạp `CLAUDE.md`; không dán thì dễ đọc `AGENTS.md` rồi tưởng
  mình là Nami), và **sáu cách chuyển sổ**: GitHub · gói dán · zip kéo thả · zip
  qua Drive · trang tải của nhà VPS · làm luôn trên VPS. Có mục cấm (pastebin,
  transfer.sh, nhóm chat — gói có giá vốn, hoa hồng).
- `scripts/dong_goi.py` — gói đúng sổ shop (tờ có dấu `FILE CỦA SHOP`, `SOUL.md`,
  hai skill, `knowledge/wiki/`) thành một khối chữ dán được, hoặc `--zip`. Không
  bao giờ gói `.env`, `memory/`, config đã điền, `AGENTS.md`.
- `scripts/mo_goi.py` — mở gói trên VPS: kiểm sha256 trước khi ghi (dán thiếu thì
  không ghi gì), chặn `..` / symlink / `scripts/` / `config/`, giữ bản cũ ở
  `.ban-cu/`, làm lại chỉ mục.
- `kiem_tra_may.py` có dòng *Sổ shop đã có chữ* — bắt lỗi dựng máy xong mà quên
  chuyển sổ.

Đã chạy thật trong container: hai bản sao repo, sửa sổ ở A, dán khối (kèm rác,
CRLF, thụt lề) vào B → sổ khớp, chỉ mục B xanh; đường zip cũng vậy; gói bị sửa
một ký tự hoặc thiếu đuôi → từ chối, không ghi gì.

**Chưa chạy thật:** mở repo bằng Cowork / ChatGPT Work / dots; kết nối GitHub /
Drive của từng app; dán gói qua cửa sổ SSH thật. Kịch bản: `docs/04` dòng 83–84,
`docs/17` mục *Thử*.

## 0.4.2 — dựng máy một lệnh, chỉ dừng ở bốn việc của người

Người dựng gõ **một** lệnh `python3 scripts/bat_dau.py` (tự gọi `scripts/cai_dat.sh`). Máy
làm hết phần máy; chỉ dừng ở **① dán mã AI · ② quét mã · ③ nhắn mã `NAMI-xxxx`
từ nick chủ · ④ nhắn thử**. Đứt giữa chừng → gõ lại đúng lệnh đó, chạy tiếp.
Tiến độ ở `~/.openclaw/zalo-cskh-tien-do.json` (ngoài repo).

Script mới (chạy riêng được khi chỉ cần sửa một bước):

- `scripts/cai_dat.sh` — Node v24.21.0 (kiểm SHA256 trước khi giải nén),
  OpenClaw + plugin ghim 2026.9.4, Python ≥ 3.9, swap 2 GB cho máy ≤ 1 GB,
  giờ Việt Nam. Hỏi trước khi đụng swap / múi giờ; không có người ngồi trước
  máy thì không tự làm. npm 11 bỏ qua script cài của gói → `--allow-scripts=openclaw`.
- `scripts/quet_ma.py` — plugin **không** in QR ra terminal: nó ghi ảnh
  `openclaw-zalouser-qr-<profile>.png` (quyền 0600) và log `Scan QR image: <path>`
  (đọc mã nguồn plugin). Script đọc ảnh đó (giải PNG bằng stdlib), vẽ QR ngay
  trong cửa sổ SSH. Hết `scp`. `docs/14` gỡ mục *chưa xác minh*.
- `scripts/lay_sender_id.py` — senderId chủ không đọc log: chủ nhắn một mã
  ngẫu nhiên, script tìm đúng cuộc trò chuyện riêng có mã đó trong sổ phiên,
  tự gộp config.
- `scripts/kiem_tra_may.py` — soi cả máy xanh / đỏ, dòng đỏ kèm cách sửa. Bắt
  được cả cảnh báo `all DMs will be dropped` mà `config validate` vẫn exit 0.

Sửa:

- **Báo nhầm ở 0.4.0:** khách *không* dùng chung một cuộc trò chuyện. Lõi
  OpenClaw mặc định `dmScope: "main"`, nhưng plugin `zalouser` ép
  `per-channel-peer`. Đã sửa lại config mẫu, `QUY-TRINH`, `docs/10`, `docs/16`.
  Vẫn ghi `dmScope` rõ trong config cho chắc.
- `dien_config.py --chi-xem` in câu hỏi lẫn vào stdout → JSON hỏng. Câu hỏi nay
  ra stderr.

Đã chạy thật trong container: `cai_dat.sh` trên máy có Node 22 sai bản (cài
đúng bản, chạy lại không hại); QR thật giải đúng từng ô, bản vẽ terminal chụp
lại quét ra đúng nội dung; `lay_sender_id` nhặt đúng người từ sổ phiên thật;
`bat_dau` lần 2 bỏ qua bước đã xong, không hỏi lại mã.

**Chưa chạy thật:** điện thoại quét màn hình terminal; tin Zalo thật vào
`lay_sender_id`; gateway làm dịch vụ systemd; giọng bot với Claude thật.
Kịch bản thử: `docs/04` dòng 78–82.

## 0.4.1 — chạy lượt bot thật (model giả), bịt hai chỗ hở

OpenClaw 2026.9.4 chạy **lượt bot thật** (`openclaw agent --local`), model thay
bằng máy chủ giả API Claude ghi lại từng request. Thấy đúng thứ Claude sẽ thấy:
prompt nền, tool từng agent. Kết quả đầy đủ: `docs/16-day-bot.md` mục *Đã kiểm
thế nào*.

Kiểm config không bắt được, chạy thật mới thấy:

- **OpenClaw tự thêm `apply_patch`** đi kèm `write`/`edit` cho bot khách. Nay
  `main.tools.deny: ["apply_patch"]`. Test cũ kiểm chữ trong config nên tưởng
  đã không có.
- **Bot chủ có `terminal`, `portal`, `dashboard`** (nhóm `group:ui`) dù profile
  `coding` không liệt kê. Nay cấm `group:ui` toàn cục.
- **Dấu hiệu "mình là bot chủ" sai:** `AGENTS.md` và `day-bot` dựa vào việc có
  tool ghi — nhưng bot khách cũng có `write` (ghi phiếu). Nay neo vào
  `automations`, tool duy nhất chỉ bot chủ có.

Đã chạy và đạt: bot khách gọi `exec` / `automations` / `terminal` bị OpenClaw
từ chối; bot chủ ghi đúng thư mục repo; sửa sổ lượt sau thấy ngay; khách B
không thấy chuyện khách A.

## 0.4.0 — chạy thật lần đầu: vá lỗ an toàn, chủ dạy bot qua Zalo

Bot chị Thanh (shop coaching) là lần đầu template chạy trên máy thật. Mọi thứ
dưới đây đã kiểm lại bằng chính OpenClaw **2026.9.4** + plugin zalouser
2026.9.4 trên Node v24.21.0: `config validate`, `security audit`, hàm định tuyến
của OpenClaw, `skills list` theo từng agent. Không chỉ đọc docs nữa — 0.3.0 đọc
docs và sai.

**Shop đang chạy bản cũ: cập nhật ngay.** Kéo bản mới rồi chạy
`python3 scripts/lam_chi_muc.py` và `python3 scripts/dien_config.py`
(`docs/15-cap-nhat.md`).

### Lỗi đang chạy ngoài kia — bản cũ có hết

- ~~**Mọi khách nhắn riêng dùng CHUNG một phiên.**~~ **Báo nhầm — xem 0.4.2.**
  Lõi OpenClaw mặc định `dmScope: "main"` thật, nhưng plugin zalouser tự đổi
  thành `per-channel-peer` cho tin Zalo. Nay vẫn ghi rõ `per-channel-peer`.
- **Bot trả khách có `exec` trên VPS.** Template không đặt `tools` → OpenClaw
  dùng profile `coding`: shell, `apply_patch`, web, hẹn giờ, đổi gateway, đọc
  phiên người khác. `security audit` cho config cũ: **4 critical**. Nay bot khách
  `minimal` + đọc/ghi/gửi tin/xem ảnh; toàn cục cấm shell, cấm `elevated`.
- **Tự học bật sẵn.** `skills.workshop.autonomous.mode` mặc định `auto`: ai gõ
  *"từ giờ luôn…"* — kể cả khách — cũng thành skill. Nay `off`. Cùng lý do, tắt
  `dreaming` và `memoryFlush` (tự chép chat vào `MEMORY.md`, file nạp nền).
- **Hai lỗi config làm bot chết** (`agents.defaults.identity` → gateway không
  lên; `open` thiếu `allowFrom: ["*"]` → rơi hết tin khách, vẫn báo *valid*).
- **Bot không thấy `persona.md`, `INDEX.md`, `TOOLS.md`.** OpenClaw chỉ nạp
  `AGENTS.md`, `SOUL.md`, `IDENTITY.md`, `USER.md`, `MEMORY.md` (đã kiểm trong
  code). Bản cũ tưởng bảy file. `lam_chi_muc.py` nay chép persona + chỉ mục vào
  một khối cuối `AGENTS.md`; `sim/nen.py` dùng đúng danh sách năm file.
- Sửa file workspace **không cần khởi động lại** — OpenClaw đọc lại mỗi lượt.
  Bản cũ (và runbook shop đầu tiên) bảo phải restart.

### Mới: chủ dạy bot, giao việc qua Zalo

Chủ nhắn **riêng**, nói thường: *"từ giờ ship 25k"*, *"9h mai nhắc chị gọi chị
Lan"*. Skill `day-bot` (sửa sổ, thêm luật, đổi giọng, duyệt đề xuất của
`hoc-lai`, lùi lại) và `giao-viec` (hẹn giờ qua tool `automations`, luôn giờ
VN). Nhắc lại + chờ gật trước mọi thao tác; nhật ký ở `memory/nhat-ky-sua/`.

Khoá ở **tầng máy**: hai agent (`main` khách / `admin` chủ), `bindings` khớp
senderId chủ trong tin riêng, `commands.ownerAllowFrom` (code tự gỡ hẹn giờ
với người không phải chủ), `main.skills` không có hai skill này,
`toolsBySender` làm lớp hai. Trong nhóm không ai dạy được. Giới hạn thật — ghi
không khoá được theo thư mục nếu không có Docker — ở `docs/16-day-bot.md`.

Bẫy tìm ra lúc dựng: nhiều agent thì `agents.defaults.workspace` bị hiểu là
thư mục **gốc** → agent chạy trong `<gốc>/main`, rỗng. Nay đặt workspace ở từng
agent; có test.

### Mới: dựng cho người không rành kỹ thuật

`python3 scripts/dien_config.py` — ba câu hỏi (tên bot, senderId chủ, tiết
kiệm?), gộp bằng `openclaw config patch` (giữ token gateway + mã AI), đổi tên ở
`IDENTITY.md` + config cùng lúc, chạy `validate` và dịch warning ra chữ thường.
Chặn sẵn: gõ số điện thoại thay senderId, tên có ngoặc kép.

### Model

Ghim `anthropic/claude-opus-5` (mạnh nhất mà 2026.9.4 hỗ trợ cho chat, có xem
ảnh), dự phòng `claude-sonnet-5`, `thinkingDefault: "high"`. Không dùng bí danh
`opus` — tự trượt sang đời mới khi nâng OpenClaw. Opus 5.5 (mới hơn, rẻ hơn)
**chưa** chạy được trên 2026.9.4: OpenClaw giấu model đời mới tới khi có bản hỗ
trợ.

### Bài học từ nhóm lớp thật (đã có ở các commit trước trong bản này)

Luật im trong nhóm vào nền · số chỉ từ sổ, không từ tin cũ · đọc thêm mặc
định là không · cấm hứa còn suất / giữ chỗ · test hết cứng (shop điền giá, xoá
tờ thừa, đổi tên vẫn xanh) · runbook VPS (senderId, swap, RHEL 8, GPG).

**Chưa chạy thật:** tin Zalo thật đi qua `bindings` vào `admin`; việc hẹn giờ
thật gửi tới `user:` / `group:`; dạy bot rồi bot khách nói theo ở tin kế.
Kịch bản `docs/04-kich-ban-thu.md` dòng 66–77.

## 0.3.1 — mở cửa cho Codex và Antigravity

**Thêm `GEMINI.md`.** Cửa vào cho Gemini / Antigravity — trước đây thiếu, hai
agent đó rơi thẳng vào `AGENTS.md` mà không có gì đỡ.

**`AGENTS.md` đổi tiêu đề** từ *Harness — Nami trên Zalo* thành
*Não bot Zalo (Nami) — KHÔNG phải hướng dẫn cho coding agent*. Lý do: Codex và
nhiều agent khác tự nạp `AGENTS.md` theo chuẩn chung, mà trong repo này tên đó
đã là não con bot (OpenClaw nạp workspace đúng tên đó nên **không đổi tên
được**). Agent nào chỉ liếc H1 sẽ hiểu ngược. Tám dòng đầu nay chỉ đích danh
cửa của từng agent. **Nội dung não bot không đổi một chữ** — `<policy>` và mọi
mục dưới giữ nguyên.

**`README.md` · `CHUAN-BI.md` · `HUONG-DAN-AGENT.md`** nay nêu đủ năm agent:
Claude Code · Cursor · Codex · Antigravity · Copilot. Trước chỉ nói Cursor và
Claude Code, khách dùng Codex đọc xong tưởng template không hợp.
`HUONG-DAN-AGENT.md` có bảng *agent → file nó nạp*.

**Chưa chạy thật:** hai cửa mới chưa mở bằng Codex và Antigravity thật. Việc
phải làm trước khi tin: mở repo bằng từng cái, gõ *dựng bot cho shop mình*, xem
nó có nhảy vào `dung-bot/QUY-TRINH.md` và **không** xưng là Nami không.

## 0.3.0 — repo template, và key config đã xác minh

**Đã hết đoán về OpenClaw.** Tải package npm `openclaw@2026.9.4` (nó mang theo
nguyên thư mục `docs/`) và đối chiếu từng key. Mọi key trong template đều đúng.
**(Sai — xem 0.4.0. Đối chiếu docs không bắt được; chạy `config validate` mới bắt được.)**
`docs/05` khối *Đã test với* hết `[CHỜ NGƯỜI BÁN]`.

**Ba chỗ phải sửa trong config mẫu:**

- `groupAllowFrom` trống = **mọi người trong nhóm đã cho phép đều gọi được bot**,
  và nó **không** tự lấy `allowFrom`. Với CSKH thường đúng ý, nhưng phải biết.
- Khoá trong `channels.zalouser.groups` phải là **ID nhóm**, không phải tên.
  Khớp theo tên cần `dangerouslyAllowNameMatching` — đừng bật.
- `"*"` cần `enabled: true`.

**Node có ràng buộc bản:** `>=24.16.0 <25` hoặc `>=26.1.0`. Node 22/23/25 thì
cài xong bot không chạy. `CHUAN-BI.md` nay có nhắc.

**Gộp tin dồn:** đã kiểm, **không có key nào cho người dùng**. Luật nằm ở
`AGENTS.md`, bot xử bằng phán đoán.

**Mở cho ngành dịch vụ.** Thêm ba tờ sổ `lo-trinh` · `ai-phu-hop` ·
`sau-khi-xong`; `ghi-don` tách hai hình dạng (bán hàng / khóa học–dịch vụ);
`TRANG-MAU.md` dạy **xóa tờ không dùng** rồi chạy lại chỉ mục.

**Luật mới: không hứa kết quả.** Bot được nói *cái shop làm*, không được nói
*cái sẽ xảy ra với người này*. Ba chỗ nguy: sức khỏe/thẩm mỹ, tiền/nghề,
thi cử/giấy tờ.

**Mốc giờ trên phiếu chốt `YYYY-MM-DD HH:MM`.** Trước đây không ghi định dạng —
bot ghi *"10h ngày 9/9"* thì heartbeat không đọc được và follow-up **im vĩnh
viễn mà không báo lỗi**.

**Thêm `sim/`** — giả lập chạy luật máy không cần nick, và CI chạy nó mỗi lần
push. `LICENSE` độc quyền: dùng được, không bán lại.

## 0.2.0 — chưa chạy thật

Vẫn **chưa chạy trên nick Zalo thật**. Xem mục 0.1.0 về việc phải làm trước khi bán.

**Đổi hành vi bot — đọc kỹ nếu đang chạy bản cũ:**

- **Bot được lầy**, và chuyện ngoài shop **mở hẳn**. Luật cũ *một nhịp rồi kéo
  về shop* đã bỏ. Kèm ba rào mới: công tắc tắt hài, bảy nhóm không dám, luật
  nhóm. Tất cả ở `knowledge/vui-va-ngoai-le.md`.
  Shop nghề trang trọng: ghi một dòng vào `persona.md` → *Giọng — mức vui*.
- **Nhóm vẫn `requireMention`** — không đổi.
- **Khách xin số tài khoản / QR → bot không đưa**, bàn giao. `gui_qr` / `gui_stk`
  vào danh sách không-có của `TOOLS.md`.
- **Sáu tình huống mới** trong `knowledge/tinh-huong.md`: xin STK, gọi Zalo,
  món shop không bán, chửi bậy/quấy rối, thu hồi tin, ngày nghỉ.

**Trường mới — phải điền lại:**

- `USER.md`: **Ngày nghỉ / Tết**. Chưa điền thì follow-up và heartbeat **không
  rào được** — bot sẽ nhắn khách vào mùng 1.
- `knowledge/wiki/public/gio-truc.md`: mục *Ngày nghỉ*, khớp với `USER.md`.
- `knowledge/persona.md`: mục *Giọng — mức vui*. Để trống = giữ mặc định.
- `memory/phieu/MAU.md`: `ban_giao`, `ban_giao_luc`, `ban_giao_ve`.
- `knowledge/logic/ma-tran.json`: `tach_khi` thêm `quay_roi`; `followup` thêm
  `ngay_nghi_khong_gui`; `phieu` thêm `tran_ky_tu` / `khong_bao_gio_bo` /
  `thu_tu_hy_sinh`.

**Đổi chỗ file:**

- Quy trình dựng B0→B7 chuyển từ `.claude/skills/khoi-tao/SKILL.md` sang
  **`dung-bot/QUY-TRINH.md`**. Skill cũ còn lại làm con trỏ.
- Thêm cửa vào cho Cursor (`.cursor/rules/`) và Copilot (`.github/`).

## 0.1.0 — chưa chạy thật

Bản đầu. **Chưa chạy trên nick Zalo thật.** Toàn bộ kho chữ có test
(`python3 -m unittest discover -s tests`), nhưng test chỉ chứng minh file khớp
nhau, không chứng minh bot sống. Trước khi bán: chạy hết `docs/04-kich-ban-thu.md`
và `docs/14-vps-headless.md` trên máy thật, rồi điền khối *Đã test với* trong
`docs/05-thiet-lap.md`.

Có gì:

- Bot Nami trên nick Zalo cá nhân (OpenClaw + plugin `zalouser`)
- Giọng, cách tư vấn, 15 skill CSKH, phiếu khách theo Zalo ID
- Sổ shop dạng wiki + chỉ mục sinh tự động
- Ba tầng prompt, khối `<policy>`, vòng học cuối ngày, sổ tin nợ khách
- Tool `tra_don` (tắt sẵn), MCP Google Drive (tắt sẵn)
- Quy trình dựng B0→B7 cho coding agent bất kỳ
