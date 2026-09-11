# Lịch sử template

Đọc trước khi kéo bản mới. Cách kéo: [`docs/15-cap-nhat.md`](docs/15-cap-nhat.md).

Bản nào đổi thứ shop đang phụ thuộc — tên trường phiếu, tên tool, tên tờ wiki,
tên file — **phải ghi ở đây**. Không ghi = coi như không đổi.

## 0.3.0 — repo template, và key config đã xác minh

**Đã hết đoán về OpenClaw.** Tải package npm `openclaw@2026.9.4` (nó mang theo
nguyên thư mục `docs/`) và đối chiếu từng key. Mọi key trong template đều đúng.
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
