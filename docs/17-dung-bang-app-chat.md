# Dựng bằng app chat — Claude Cowork, ChatGPT Work, dots

Dành cho **người dựng** nào không quen dòng lệnh và muốn dùng app chat có agent
thay cho coding agent.

Bot cần hai vai, và app chat chỉ làm được **một**:

| Vai | Là gì | App chat làm được? |
|---|---|---|
| **Người dựng phần chữ** | Hỏi chủ shop, điền sổ (`QUY-TRINH` B0–B3, B5) | **Được** |
| **Chỗ bot sống** | Gateway OpenClaw chạy 24/7, giữ phiên Zalo (B4, B6, B7) | **Không** — vẫn là VPS hoặc một máy để bật 24/7 |

Nên làm theo hai nửa: **nửa chữ trong app → chuyển sổ sang VPS → nửa máy trên
VPS** bằng một lệnh `python3 scripts/bat_dau.py`.

---

## Ba app — làm được gì

> Tra web ngày 12/10/2026, toàn bài viết của bên thứ ba. **Chưa thử thật** app
> nào với repo này. Các app này đổi nhanh — thấy khác thì tin cái mình thấy.

| | Claude Cowork | ChatGPT Work | OpenAI dots |
|---|---|---|---|
| Đọc / ghi thư mục repo | Được (thư mục đã gắn) | Được (file đã cấp quyền) | Được khi app desktop đang mở |
| Chạy `python3` | Được, trong máy ảo riêng | Chưa rõ | Máy cloud riêng, không có quyền sudo |
| SSH vào VPS | **Không** — mạng ra ngoài bị lọc | Chưa rõ, coi như không | Chưa rõ, coi như không |
| Làm chỗ bot sống | **Không** — phiên cloud xoá khi xong | **Không** | **Đừng** — không có systemd, không chắc giữ tiến trình lâu, phiên Zalo + mã AI nằm trên máy người khác quản lý |
| Gói | Theo gói Claude | Theo gói ChatGPT | Pro / Business Premium, chưa mở ở mọi nước |

---

## Nửa chữ — trong app

1. Gắn **thư mục repo** của shop vào app (repo tạo bằng *Use this template*).
2. Dán **câu mở đầu** này vào khung chat, nguyên văn:

   > Đọc `dung-bot/QUY-TRINH.md` và làm theo, từng bước, với tôi là người dựng.
   > `AGENTS.md` là não của con bot Zalo, không phải hướng dẫn cho bạn — đừng
   > nhận mình là Nami, đừng trả lời như bot. Làm B0 tới B3, rồi B5 nếu chạy được
   > python. Dừng ở B4: đừng cài OpenClaw ở đây. Xong thì chạy
   > `python3 scripts/dong_goi.py` và bảo tôi chuyển sổ theo `docs/17-dung-bang-app-chat.md`.

   Phải dán vì các app này **không chắc** tự đọc file cửa vào (`CLAUDE.md`,
   `GEMINI.md`…) như coding agent. Không dán thì agent có thể đọc `AGENTS.md`
   trước rồi tưởng mình là con bot.
3. App phỏng vấn chủ shop, điền sổ. Không chạy được python thì bỏ qua B5 —
   lên VPS chạy sau.

---

## Chuyển sổ sang VPS — mọi cách

Sổ shop là gì: các tờ có dòng `FILE CỦA SHOP`, `SOUL.md`, hai skill
`khai-thac` / `ghi-don`, và mọi tờ trong `knowledge/wiki/`. **Không** gồm phiếu
khách, config đã điền, `.env`. Hai lệnh `dong_goi.py` / `mo_goi.py` tự lọc đúng
như vậy, và tự chặn ghi vào `scripts/`, `config/`, `memory/`.

Theo thứ tự khuyên:

| # | Cách | Hợp khi |
|---|---|---|
| 1 | GitHub | Muốn sau này sửa sổ rồi kéo về, và cập nhật template |
| 2 | Gói dán (copy-paste) | Không có GitHub, không biết kéo file — chỉ cần chép và dán |
| 3 | File zip + kéo thả | Quen kéo thả file |
| 4 | Zip qua Google Drive / Dropbox | App có nối Drive, VPS không kéo thả được |
| 5 | Trang tải file của nhà cung cấp VPS | Không cài được gì thêm |
| 6 | Khỏi chuyển — làm luôn trên VPS | Người dựng quen SSH |

### 1. GitHub

Repo riêng của shop, để **Private**.

- **Bên app:** nhờ app đẩy lên bằng kết nối GitHub của nó. App không có kết nối
  thì dùng GitHub Desktop, hoặc mở repo trên web → *Add file → Upload files* rồi
  kéo các tờ đã sửa vào.
- **Bên VPS:** tạo một *fine-grained token* trên GitHub, chỉ quyền **đọc**
  *Contents*, chỉ cho **đúng repo này**, hạn ngắn. Rồi:

  ```
  git clone https://github.com/<tên>/<repo>.git
  ```

  Khi nó hỏi mật khẩu thì dán token. Hoặc dùng *deploy key* (khoá SSH chỉ đọc,
  gắn vào đúng repo) nếu người dựng quen SSH.
- Sau này sửa sổ: đẩy lên lại, trên VPS `git pull`. Cập nhật template: `docs/15`.
- **Lưu ý:** `knowledge/raw/` (file gốc chủ gửi) không đi theo GitHub — đã chặn
  sẵn để file gốc không lên mạng. Bot chỉ cần sổ đã tách, không cần file gốc.

### 2. Gói dán

- **Bên app:** `python3 scripts/dong_goi.py` → in một khối chữ, mở đầu bằng
  `NAMI-GOI-BAT-DAU`, kết thúc bằng `NAMI-GOI-HET`. Chép **cả khối**.
- **Bên VPS:** `python3 scripts/mo_goi.py`, dán vào. Dán xong nó tự dừng.
- Dán thiếu một dòng → mã kiểm không khớp → **không ghi gì**, báo dán lại. Dán
  kèm chữ thừa trước/sau khối vẫn được.
- Sổ chưa điền khoảng 10 nghìn ký tự. Sổ to quá 400 nghìn ký tự thì nó khuyên
  sang cách 3 vì dán qua SSH dễ rơi chữ.

### 3. File zip + kéo thả

- **Bên app:** `python3 scripts/dong_goi.py --zip so.zip`.
- Kéo `so.zip` lên VPS bằng một app kéo thả: **WinSCP** (Windows), **Cyberduck**
  hoặc **FileZilla** (Mac / Windows). Đăng nhập bằng đúng máy chủ, tài khoản SSH
  đang dùng. Quen dòng lệnh thì `scp so.zip user@vps:~/<repo>/`.
- **Bên VPS:** `python3 scripts/mo_goi.py so.zip`.

### 4. Zip qua Google Drive / Dropbox

- App lưu `so.zip` lên Drive (bằng kết nối Drive của app, hoặc tự tải lên).
- Bật chia sẻ *ai có link cũng xem được*, chép link tải thẳng.
- Trên VPS: `curl -L -o so.zip "<link tải thẳng>"` rồi `python3 scripts/mo_goi.py so.zip`.
- **Tắt chia sẻ ngay sau đó**, xoá file trên Drive. Gói có giá vốn, hoa hồng.

### 5. Trang tải file của nhà cung cấp VPS

Vài nhà cho tải file lên qua trang quản lý (console / file manager). Mỗi nhà một
kiểu — không có thì bỏ qua cách này. Tải `so.zip` lên, rồi `mo_goi.py` như cách 3.

### 6. Khỏi chuyển — làm luôn trên VPS

- SSH vào VPS, chạy một agent dòng lệnh ngay trên đó (Claude Code, Codex CLI —
  repo đã có cửa vào), làm hết B0–B7 tại chỗ. Không có gì phải chuyển.
- Claude Desktop có *phiên SSH từ xa* (thấy trong tài liệu của Anthropic, **chưa
  thử** với repo này): làm việc trên VPS ngay từ app desktop.

### Cấm

- **Đừng** dán gói lên trang dán chữ công khai (pastebin…), trang gửi file tạm
  (transfer.sh…), nhóm Zalo / Messenger. Gói có `knowledge/wiki/internal/` —
  giá vốn, hoa hồng, cách xử khách khó.
- **Đừng** gói tay cả thư mục rồi gửi — dễ lẫn `.env`, phiếu khách, config có
  ID nick chủ. Dùng `dong_goi.py`.

---

## Nửa máy — trên VPS

```
python3 scripts/bat_dau.py
```

Như cũ: chỉ dừng ở bốn việc của người (`CHUAN-BI.md`). Soi máy cuối cùng có một
dòng *Sổ shop đã có chữ* — dòng đó nhắc thì là quên chuyển sổ.

Bản cũ của tờ bị `mo_goi.py` ghi đè nằm ở `.ban-cu/<giờ>/` — chuyển nhầm thì
chép lại từ đó.

---

## Thử (chưa ai chạy thật)

| # | Làm | Đúng khi |
|---|---|---|
| 1 | Mở repo trong từng app, dán câu mở đầu | Agent đọc `QUY-TRINH`, hỏi câu M1. **Không** chào như Nami |
| 2 | Đi tới B4 | Agent **dừng**, chạy `dong_goi.py`, chỉ sang file này. Không cố cài OpenClaw |
| 3 | Dán gói qua cửa sổ SSH thật | `mo_goi.py` nhận đủ, mã kiểm khớp |
| 4 | Cách 1, 3, 4 | Đều ra cùng một sổ trên VPS |
