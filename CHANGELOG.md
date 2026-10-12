# Lịch sử template

Đọc trước khi kéo bản mới. Cách kéo: [`docs/15-cap-nhat.md`](docs/15-cap-nhat.md).

Bản nào đổi thứ shop đang phụ thuộc — tên trường phiếu, tên tool, tên tờ wiki,
tên file — **phải ghi ở đây**. Không ghi = coi như không đổi.

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

- **Mọi khách nhắn riêng dùng CHUNG một phiên.** Mặc định OpenClaw
  `session.dmScope: "main"`. Hàm định tuyến cho config cũ: chủ, khách A, khách B
  đều vào `agent:main:main`. Bot trả khách B mà còn nhớ tên, SĐT, đơn của khách
  A. Nay `per-channel-peer`.
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
