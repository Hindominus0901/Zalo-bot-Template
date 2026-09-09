# Kênh: tài khoản Zalo cá nhân — chạy như Tom

**Đã chốt:** bot không phải Zalo Bot Creator, không phải OA. Shop đưa **một nick Zalo
cá nhân**; bot cầm nick đó 24/7, khách nhắn như nhắn cho người.

Cách Tom chạy: OpenClaw Gateway + plugin `@openclaw/zalouser` (login QR, thư viện
`zca-js` in-process). Template này **ngồi lên runtime đó**, không viết lại Python
polling của `agent-cskh-zalo`.

---

## Khách thấy gì

Không có chữ `Bot` trước tên. Không có OA. Một người trong danh bạ / kết bạn /
link `zalo.me/...`. Gõ chữ, thả sticker, gửi ảnh, reply tin — bot trả như người
đang cầm điện thoại: đang soạn, đã xem, có thể thả reaction.

Gợi ý tương tác **không thành nút OA**. Thành:

- 2–3 câu khách gõ y nguyên, cuối tin
- Reply/quote tin họ vừa gửi
- Sticker khi cuộc chat đang vui (không bắt buộc)

---

## So với hai cửa kia

| | Nick cá nhân (Tom / zalouser) | Bot Creator | OA |
|---|---|---|---|
| Khách thấy | Người | `Bot …` | Trang OA |
| Vào nhóm | Như thành viên thật | 3 nhóm, phải @ | Không |
| Nút / list | Không | Chưa chắc | Có |
| Hạn mức 3.000 tin / 50 user | Không áp | Có | Theo gói OA |
| ZNS / nhắn số lạ | Không | Không | Có điều kiện |
| Chính thức | **Không** — mô phỏng Zalo Web | Có | Có |
| Rủi ro nick | **Khóa / hạn chế** nếu Zalo phát hiện tự động | Token bot | Token OA |

Rủi ro nick là thật. **Đã chốt: nick riêng cho bot, số riêng** — không cầm nick
Zalo chính của chủ shop, không gắn ngân hàng / CCCD quan trọng nếu tránh được.

---

## Cài như Tom

1. Máy/VPS chạy OpenClaw Gateway (không tắt — mất socket là mất tin lúc offline;
   `zca-js` không replay tin Zalo chưa kịp đẩy vào hàng đợi).
2. `openclaw plugins install @openclaw/zalouser`
3. `openclaw channels login --channel zalouser` — quét QR bằng app Zalo **của nick bot**
4. Bật kênh. Session cookie lưu trong state OpenClaw; restart gateway không phải
   quét lại trừ khi cookie chết.

### Config CSKH — khác Tom cá nhân

Tom (trợ lý riêng) mặc định `dmPolicy: pairing`: người lạ phải được duyệt. **CSKH
không được thế** — khách mới nhắn vào là phải vào được.

```json5
{
  channels: {
    zalouser: {
      enabled: true,
      dmPolicy: "open",          // khách lạ vào được
      groupPolicy: "allowlist",  // nhóm thì chọn, đừng open hết
      // groups: { "<id>": { enabled: true, requireMention: true } }
    },
  },
}
```

Trong nhóm: mặc định chỉ trả lời khi được @ hoặc khi người ta reply tin của bot.
Tránh đọc cả group rồi nhảy vào mỗi câu.

---

## Template này là gì trên OpenClaw

Không phải bot Python mới. Là **workspace CSKH** thả vào OpenClaw:

| File template | Việc trên OpenClaw |
|---|---|
| `knowledge/giong-noi.md` | `SOUL.md` — giọng |
| `persona.md` (sinh lúc phỏng vấn shop) | Bối cảnh shop + rào tiền/nội bộ |
| `knowledge/wiki/` | Kho số liệu |
| `skills/` | Khai thác, báo giá, ghi đơn, theo đơn, ảnh, phàn nàn, bàn giao |
| `knowledge/khung-khai-thac.md` + `moi-loai-cau-hoi.md` | Nhét vào `AGENTS.md` / skill vận hành |
| `channels.zalouser` | Nick cầm tay |

Workspace Tom (nếu có `SOUL.md` / `IDENTITY.md` trên máy) **trộn giọng vào
`giong-noi.md`** — chưa lấy được vì file không nằm trên GitHub.

---

## Việc kênh này làm được tốt hơn Bot Creator

- Typing + seen trước khi trả lời — đỡ cảm giác máy
- Sticker, ảnh, voice, quote reply
- Không hạn 50 user / 3.000 tin gói Basic
- Tên nick đặt như nhân viên (`Lan nhà hoa`, không cần tiền tố `Bot`)
- Vào nhóm như người, không beta 3 nhóm

Việc **không** làm được: nút bấm OA, ZNS, form, thanh toán trong OA. Gợi ý vẫn là chữ.

---

## Vận hành đừng chủ quan

- Nick bot **không dùng tay song song** trên điện thoại lúc gateway đang cầm session
  (dễ đá cookie, dễ lộ hành vi bot).
- Cookie chết thì quét QR lại trên đúng máy gateway.
- Tin lúc gateway tắt: Zalo personal socket **không gửi bù** như webhook OA. VPS
  24/7 vẫn bắt buộc.
- Rate: đừng bắn tin hàng loạt. CSKH 1-1 bình thường thì ổn hơn broadcast.

Nguồn: [OpenClaw zalouser](https://docs.openclaw.ai/channels/zalouser) ·
[zca-js](https://github.com/rfs-adreno/zca-js) (unofficial, có cảnh báo khóa nick).
