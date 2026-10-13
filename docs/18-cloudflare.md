# Cloudflare — vào VPS bằng trình duyệt, và chuyện cho bot sống trên Cloudflare

Dành cho **người dựng**. Hai việc khác nhau, hay bị gọi chung là "đưa lên
Cloudflare":

| | Việc | Kết luận |
|---|---|---|
| **Phần 1** | Vào VPS qua Cloudflare: terminal ngay trong trình duyệt, đóng cổng SSH | **Nên làm** nếu người dựng không quen app SSH |
| **Phần 2** | Bỏ VPS, cho bot sống trên Cloudflare | **Chưa hỗ trợ** — dùng VPS |

> Tra ngày 13/10/2026. Phần 1 đã kiểm lệnh `cloudflared` 2026.10.0; **chưa thử
> thật** tunnel + terminal trình duyệt với template này. Phần 2 đọc mã nguồn
> `cloudflare/moltworker` (bản 29/3/2026), chưa chạy.

---

## Phần 1 — SSH ngay trên trình duyệt (Cloudflare Tunnel)

Được gì:
- Mở `https://ssh.<tên-miền-của-shop>` trên **bất kỳ** máy nào, kể cả điện thoại,
  là ra cửa sổ dòng lệnh của VPS. Không cài PuTTY, không cần biết `ssh user@ip`.
- Đăng nhập bằng email (mã gửi về email), chỉ email được phép mới vào được.
- VPS **không mở cổng nào ra Internet**. `cloudflared` trên VPS tự nối ra
  Cloudflare, giống cách bot nối ra Zalo.
- `python3 scripts/bat_dau.py` và mã QR (`quet_ma.py`) chạy ngay trong tab đó.

Cần:
- Một **tên miền** đã đưa vào Cloudflare (gói Free của Cloudflare là đủ).
- Tài khoản **Cloudflare Zero Trust**: miễn phí dưới 50 người dùng, nhưng lúc đăng
  ký **phải khai thẻ hoặc PayPal**.

### Từng bước

1. **Cloudflare dashboard → Zero Trust → Networks → Tunnels → Create a tunnel**,
   chọn loại *Cloudflared*, đặt tên (ví dụ `zalo-bot`).
2. Dashboard đưa sẵn một lệnh, dạng:

   ```
   sudo cloudflared service install <MÃ-DÀI>
   ```

   Làm theo hướng dẫn cài `cloudflared` của chính trang đó (chọn đúng Debian /
   Ubuntu / Red Hat), rồi dán lệnh trên vào VPS. Lệnh này cài `cloudflared` thành
   dịch vụ, tự bật lại khi VPS khởi động lại. `<MÃ-DÀI>` là chìa khoá của tunnel:
   **không** dán vào chat, không ghi vào repo.
3. **Public hostname**: subdomain `ssh`, miền của shop. Service: **SSH**, URL
   `localhost:22`.
4. **Zero Trust → Access → Applications → Add → Self-hosted**: hostname
   `ssh.<miền>`. Policy *Allow* chỉ **đúng email** người dựng (+ chủ shop nếu
   cần). **Đừng** để *Everyone*.
5. Trong application đó: **Browser rendering → SSH**.
6. Mở `https://ssh.<miền>` → nhập email → nhập mã → đăng nhập user Linux như
   thường.
7. **Chỉ khi bước 6 đã chạy**, và đã thử lại ở một máy khác, mới đóng cổng 22:

   ```
   sudo ufw allow from 127.0.0.1 to any port 22
   sudo ufw deny 22
   ```

   Đóng cổng **trước** khi vào được bằng trình duyệt là tự khoá mình ngoài.
   Luôn giữ một đường dự phòng: **console web của nhà cung cấp VPS**. Tìm sẵn nó
   trước khi đóng cổng.

### Lưu ý

- Diễn đàn Cloudflare có người báo terminal trình duyệt **lúc được lúc không**.
  Tắc thì vào bằng console nhà cung cấp, hoặc mở lại cổng 22 tạm thời.
- Người quen SSH vẫn đi qua tunnel được bằng `cloudflared access ssh` trong
  `~/.ssh/config`. Không bắt buộc.
- Tunnel không đụng vào bot: bot vẫn nối ra Zalo như cũ. Gỡ tunnel thì bot vẫn chạy.
- Thêm vào checklist quét lại (`docs/14`): người trực chỉ cần gửi chủ shop link
  `ssh.<miền>` + email được phép.

### Thử (chưa ai chạy thật với template)

| # | Làm | Đúng khi |
|---|---|---|
| 1 | Mở `ssh.<miền>` từ điện thoại, email lạ | Bị chặn ở bước email |
| 2 | Email được phép → `python3 scripts/bat_dau.py` tới bước quét mã | Mã QR hiện trong tab, điện thoại khác quét được |
| 3 | Đóng cổng 22, khởi động lại VPS | Vẫn vào được qua `ssh.<miền>`; bot vẫn trả lời |

---

## Phần 2 — Bot sống trên Cloudflare thay VPS: chưa hỗ trợ

Cloudflare có dự án **`cloudflare/moltworker`**: chạy OpenClaw gateway trong
*Sandbox container* của Cloudflare. Đã đọc mã nguồn (bản 29/3/2026):

| | Thực tế |
|---|---|
| Tình trạng | README: *"Experimental … not officially supported and may break without notice"* |
| Bản OpenClaw | Ghim `openclaw@2026.3.23-2` trên Node 22. Template này cần **2026.9.4 + Node 24** → phải tự sửa Dockerfile, chưa ai thử |
| Kênh | README nói Telegram, Discord, Slack. **Không nói Zalo**; cài plugin `zalouser` + quét QR trong container là việc tự làm |
| Máy | `standard-1`: ½ vCPU, 4 GiB RAM, 8 GB đĩa |
| Tiền | README tự tính chạy 24/7 ≈ **$34,5/tháng** (gồm gói Workers Paid $5). VPS rẻ ≈ $5 |
| Giữ phiên | Đĩa container mất khi khởi động lại. Lưu bằng **bản chụp lên R2** — mã nguồn bản này chỉ chụp khi **bấm tay** (nút *sync* trong trang quản trị), không tự chụp định kỳ. Container khởi động lại mà quên bấm → **mất phiên Zalo, phải quét lại**, mất cả phiếu khách mới |
| IP | Máy Cloudflare, IP có thể đổi. zca-js đã cảnh báo nick có thể bị khoá; chưa ai thử Zalo trên Cloudflare |
| Template | `cai_dat.sh`, `bat_dau.py`, `quet_ma.py`, `kiem_tra_may.py`, systemd đều viết cho VPS — **không** dùng được ở đây |

**Kết luận:** đắt hơn VPS khoảng 7 lần, dễ mất phiên Zalo, bản OpenClaw lệch,
không có ai thử. Dùng VPS. Muốn khỏi lo SSH thì làm **phần 1**.

---

## Nguồn (tra 13/10/2026)

- Mã nguồn `github.com/cloudflare/moltworker` (README, `Dockerfile`, `src/persistence.ts`, `src/routes/api.ts`, `wrangler.jsonc`)
- Cloudflare Containers FAQ — developers.cloudflare.com/containers/faq/ (đĩa tạm, mặc định ngủ sau 10 phút)
- Hướng dẫn tunnel + browser SSH: runcloud.io/blog/zero-trust-ssh, blog.iterative.engineering (2024), community.cloudflare.com (lúc được lúc không)
- zca-js README: github.com/RFS-ADRENO/zca-js (cảnh báo khoá nick)
