# Lịch sử template

Đọc trước khi kéo bản mới. Cách kéo: [`docs/15-cap-nhat.md`](docs/15-cap-nhat.md).

Bản nào đổi thứ shop đang phụ thuộc — tên trường phiếu, tên tool, tên tờ wiki,
tên file — **phải ghi ở đây**. Không ghi = coi như không đổi.

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
