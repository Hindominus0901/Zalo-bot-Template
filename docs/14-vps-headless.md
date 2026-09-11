# VPS không màn hình — quét mã và chạy 24/7

Dành cho **người dựng**. Chủ shop chỉ cần biết: lát họ giơ điện thoại quét một
mã, và **sẽ phải quét lại** thỉnh thoảng.

`docs/05-thiet-lap.md` viết cho máy có màn hình. File này bù đúng phần thiếu:
máy chủ thuê ngoài, vào bằng SSH, không có trình duyệt, không có màn hình để
hiện mã QR.

---

## Trước tiên: cảnh báo chưa xác minh

Tài liệu này dựa trên **suy đoán về cách OpenClaw in mã QR**, chưa chạy thật
trên VPS. Bước đầu của nhánh B là **tự kiểm** rồi mới đi tiếp — đừng làm theo
mù. Nếu OpenClaw hành xử khác, sửa file này lại cho đúng máy của mình.

Cùng kỷ luật với `docs/10-openclaw-config-mau.md`: kiểm trước, đừng đoán.

---

## Hai nhánh

| | Nhánh A — dựng ở máy có màn hình rồi chuyển | Nhánh B — quét thẳng trên VPS |
|---|---|---|
| Dễ | Dễ hơn nhiều | Khó hơn |
| Rủi ro | **Phiên đăng nhập có thể chết khi đổi máy/IP** | Không có rủi ro đó |
| Quét lại sau này | Vẫn phải làm được trên VPS → cuối cùng vẫn phải học nhánh B | Học một lần |

**Khuyên: làm nhánh B ngay từ đầu.** Nhánh A trì hoãn cái khó chứ không bỏ được
nó — vì cookie sẽ chết và lần quét lại là trên VPS.

---

## Nhánh A — dựng ở máy có màn hình rồi chuyển lên

Chỉ chọn nếu chủ shop cần thấy bot chạy ngay hôm nay.

1. Dựng bình thường theo `docs/05-thiet-lap.md`, quét mã trên máy có màn hình.
2. Thử xong theo `docs/04-kich-ban-thu.md`.
3. Chuyển lên VPS: copy **thư mục repo** (workspace) và **thư mục state OpenClaw**
   (`~/.openclaw/`, có phiên đăng nhập bên trong).
4. Trên VPS: cài OpenClaw cùng bản, `openclaw gateway status`.
5. **Kiểm ngay:** `openclaw directory self --channel zalouser`. Thấy nick bot =
   phiên còn sống. Không thấy = phiên chết vì đổi máy → phải quét lại, sang nhánh B.
6. **Tắt hẳn gateway ở máy cũ.** Hai chỗ cùng cầm một phiên là hỏng cả hai.

Rủi ro thật: Zalo nhìn một nick cá nhân đang ở Hà Nội bỗng đăng nhập từ máy chủ
Singapore. Có thể chỉ rớt phiên, có thể bị soi kỹ hơn. **Chưa kiểm được.** Nên
làm bước 5 **trước** khi mở khách thật, đừng để phát hiện lúc khách đang nhắn.

---

## Nhánh B — quét thẳng trên VPS

### B1. tmux trước, luôn luôn

```bash
tmux new -s zalo
```

SSH rớt giữa lúc đang chờ quét mã là mất phiên login, phải làm lại từ đầu.
Vào lại: `tmux attach -t zalo`.

### B2. Xem OpenClaw in mã kiểu gì

```bash
openclaw plugins install @openclaw/zalouser
openclaw channels login --channel zalouser
```

Nhìn cái nó in ra, rồi theo đúng một trong ba nhánh dưới.

**(a) Mã QR vẽ bằng ký tự ngay trong terminal** — dễ nhất. Phóng to cửa sổ
terminal, giơ điện thoại (đang đăng nhập nick bot) quét thẳng màn hình. Xong.

Mã hiện méo / mất nét: phóng to cửa sổ, giảm cỡ chữ, đổi terminal sang nền
trắng chữ đen. Mã QR cần tương phản, không cần màu.

**(b) Nó ghi ra một file ảnh** — kéo file về máy mình:

```bash
# chạy ở MÁY MÌNH, không phải trên VPS
scp user@vps:/duong/dan/qr.png .
```

Mở ảnh đó lên rồi quét. Cách này an toàn nhất vì không mở cổng nào.

Nếu bí quá thì phục vụ tạm qua HTTP — **chỉ khi hiểu rủi ro**:

```bash
# trên VPS, ở thư mục chứa ảnh
python3 -m http.server 8899 --bind 127.0.0.1
```

Rồi từ máy mình mở đường hầm SSH: `ssh -L 8899:127.0.0.1:8899 user@vps`, vào
`http://127.0.0.1:8899`. **`--bind 127.0.0.1` là bắt buộc** — không có nó là mã
đăng nhập nick Zalo của khách phơi ra Internet. Quét xong `Ctrl+C` ngay.

**(c) Nó in một đường link** — mở link đó trên máy mình.

### B3. Kiểm đã vào chưa

```bash
openclaw channels status --probe
openclaw directory self --channel zalouser
```

Thấy tên nick bot là xong. Thoát tmux: `Ctrl+B` rồi `D`.

### B4. Cho chạy 24/7

```bash
openclaw gateway install     # systemd, tự bật lại khi VPS khởi động lại
openclaw gateway status
```

Đừng để gateway sống trong tmux — VPS reboot là mất. tmux chỉ dùng cho lúc
đăng nhập.

---

## Quét lại — đây là việc lặp, không phải việc một lần

Phần quan trọng nhất của file này.

Phiên đăng nhập zca-js **sẽ chết**. Zalo hết hạn phiên, đổi mật khẩu, đăng nhập
tay trên điện thoại, hoặc Zalo thấy bất thường. Khi đó bot im, và khách nhắn vào
không ai trả.

**Dấu hiệu:** `openclaw channels status --probe` báo kênh không khoẻ, hoặc
`openclaw directory self --channel zalouser` không ra nick.

**`BOOT.md` đã dạy bot ngắt mạch:** login lỗi lặp thì dừng thử, báo chủ **một
lần** rằng cần quét lại mã. Không thử lại mù mỗi nhịp. Nên chủ shop sẽ nhận
được tin — nhưng chỉ một tin, và họ cần biết phải làm gì với nó.

**Quy trình quét lại, viết sẵn cho chủ shop bằng chữ thường:**

1. Báo người dựng (hoặc người trực kỹ thuật).
2. Người đó SSH vào, `tmux new -s zalo`, rồi **đăng xuất trước cho sạch**:

   ```bash
   openclaw channels logout --channel zalouser
   openclaw channels login  --channel zalouser
   ```
3. Chủ shop giơ điện thoại quét — **cùng cách như lần đầu**.
4. `openclaw directory self --channel zalouser` kiểm lại.

Vì bước 3 cần chủ shop có mặt, **đừng quét lại lúc nửa đêm** rồi chờ. Hẹn giờ.

Dán bốn bước này vào chỗ chủ shop tìm được — nhóm nội bộ, hoặc một dòng trong
`USER.md`. Đừng để nó chỉ nằm trong file này.

---

## Mấy thứ VPS hay làm hỏng

- **Đừng đăng nhập nick bot bằng tay trên điện thoại** trong lúc gateway đang
  cầm phiên. Mở Zalo Web bằng nick đó cũng đá phiên của bot ra. Luật này có ở
  `docs/02-kenh-zalouser.md`, trên VPS nó dễ quên hơn vì không ai nhìn thấy bot.
- **Đừng chạy hai gateway cùng một nick** — máy cũ và VPS, hoặc hai VPS. Một
  nick một phiên.
- **Không cần mở cổng nào ra Internet.** Bot chủ động nối ra ngoài, không ai nối
  vào. Cổng duy nhất từng mở là cổng tạm ở B2(b), và nó phải bind `127.0.0.1`.
- **VPS reboot** thì gateway phải tự lên — đó là lý do dùng `gateway install`
  chứ không phải tmux. Kiểm bằng cách reboot thử **trước** khi mở khách.
- **Múi giờ.** VPS thường chạy UTC. Giờ trực và giờ follow-up trong `USER.md` là
  giờ Việt Nam. Đặt `timedatectl set-timezone Asia/Ho_Chi_Minh`, không thì bot
  nhắn follow-up lúc bốn giờ sáng.
- **Ổ đĩa đầy.** `memory/` lớn dần theo ngày. Ngó `df -h` thỉnh thoảng.

---

## Xong nhánh này khi

- [ ] `openclaw directory self --channel zalouser` ra đúng nick bot
- [ ] `openclaw gateway status` báo đang chạy
- [ ] Reboot VPS xong gateway tự lên lại
- [ ] `timedatectl` đúng giờ Việt Nam
- [ ] Chủ shop đã biết bốn bước quét lại, và biết tìm ở đâu
- [ ] Nhắn thử từ nick khác, bot trả (`docs/04-kich-ban-thu.md`)
