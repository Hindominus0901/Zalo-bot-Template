# Một file cấu hình OpenClaw — mẫu gộp

Người dựng đọc. Chủ shop: làm theo [`05-thiet-lap.md`](05-thiet-lap.md) (họ
bấm nút, quét mã). File này = **một chỗ** nhìn `openclaw.json` sau khi merge.

Hai mảnh nguồn (đừng sửa lệch nhau rồi quên gộp):

| Mảnh | File | Việc |
|---|---|---|
| Nick Zalo + hai agent + rào an toàn | [`config/openclaw.zalouser.example.json5`](../config/openclaw.zalouser.example.json5) | Nguồn duy nhất. Điền bằng `scripts/dien_config.py` |
| Drive | [`config/mcp.example.json5`](../config/mcp.example.json5) | Tắt sẵn. Có `command` mẫu |

Merge vào `~/.openclaw/openclaw.json` trên **máy Gateway**. Workspace = đường dẫn
**tuyệt đối** thư mục shop. Đừng commit file thật, cookie, QR, token.

Tom cá nhân hay để `pairing`. Shop **không** copy pairing — khách lạ phải nhắn
được.

## Mẫu gộp — một nguồn duy nhất

**Đừng chép config từ trang này.** Nguồn duy nhất là
[`config/openclaw.zalouser.example.json5`](../config/openclaw.zalouser.example.json5),
và cách dễ nhất là để script điền hộ:

```bash
python3 scripts/dien_config.py
```

Script hỏi tên bot, senderId của chủ, đường dẫn repo — rồi ghi file và tự chạy
`openclaw config validate`. Bản 0.3.0 từng chép config ra ba trang docs, ba bản
lệch nhau, và cả ba cùng sai một key. Một nguồn thì không lệch được.

File đó có những khối này — đọc để hiểu, không phải để chép:

| Khối | Làm gì | Bỏ đi thì |
|---|---|---|
| `session.dmScope: "per-channel-peer"` | Mỗi khách một cuộc hội thoại | Với Zalo thì plugin vẫn tự tách phiên; kênh khác (nếu thêm) sẽ **chung một phiên** |
| `skills.workshop.autonomous.mode: "off"` | Tắt tự học | Ai gõ *“từ giờ luôn…”* — kể cả khách — cũng thành skill |
| `commands.ownerAllowFrom` | Ai là chủ, **code** kiểm | Không ai là chủ → không dạy bot, không giao việc được |
| `tools` (toàn cục) | Cấm shell, cấm đổi gateway, cấm ghi ra ngoài repo | Bot có `exec` trên VPS giữ cookie Zalo |
| `dreaming` / `memoryFlush` tắt | Không tự chép chat vào `MEMORY.md` | Chữ khách vào file nạp nền của mọi khách |
| `channels.zalouser` | `open` + `allowFrom: ["*"]`, nhóm phải gọi tên | Thiếu `"*"` = rơi hết tin khách, không báo lỗi |
| `agents.entries.main` | Bot trả **khách**: đọc, ghi phiếu, gửi tin, xem ảnh | — |
| `agents.entries.admin` | Bot nói với **chủ**: dạy bot, giao việc | Chủ không dạy được qua Zalo |
| `bindings` | Chủ nhắn riêng → admin; còn lại → main | Chủ cũng thành khách |

Cả hai agent dùng **chung một workspace**: chủ dạy ở admin thì bot khách thấy
ngay lượt sau. Chi tiết dạy bot: [`16-day-bot.md`](16-day-bot.md).

Drive (tắt sẵn) merge riêng từ `config/mcp.example.json5`:

```json5
{
  mcp: {
    servers: {
      gdrive: {
        enabled: false,
        command: "npx",
        args: ["-y", "@modelcontextprotocol/server-gdrive"],
        env: { GDRIVE_OAUTH_PATH: "${GDRIVE_OAUTH_PATH}" },
        toolFilter: { include: ["search*", "read*", "list*", "get*"] },
      },
    },
  },
}
```

`enabled: false` + chưa login = **không gọi** `mcp_drive`. Không thêm Apify / X
để lấy giá.

## Drive: Cursor, Gateway, hay gửi tay

```
File gốc nằm đâu?
        │
        ├─ Chủ gửi file / link mở được không cần login
        │     → cất knowledge/raw/ + dòng NGUON.md
        │
        ├─ Đang dựng trong Cursor, Drive đã bật trong Settings
        │     → coding agent lấy đúng file họ chỉ → raw/
        │
        ├─ Bot / Gateway cần tự lấy file sau này
        │     → login Drive trên máy Gateway, rồi enabled: true
        │     → openclaw mcp doctor --probe
        │
        └─ Drive cần login mà phiên này chưa login
              → dừng. Xin file tay. Không bịa nội dung Drive.
```

Lúc **chat khách**: bot không gọi Drive. Số → tờ `wiki/public/`. Ảnh khách →
`doc_anh`. Thiếu → `ghi_thieu` + `bao_chu`.

Chi tiết bus: [`11-mcp-ung-dung.md`](11-mcp-ung-dung.md).

## Sau khi merge

1. `openclaw doctor` (và `gateway status`).
2. Quét QR nick **riêng** — [`05-thiet-lap.md`](05-thiet-lap.md).
3. Thử từ nick khác: [`04-kich-ban-thu.md`](04-kich-ban-thu.md).

`openclaw doctor --fix` có thể chuyển `HEARTBEAT.md` vào DB. **Giữ file
workspace làm nguồn** — xem `HEARTBEAT.md`.

---

## Gộp tin dồn — kiểm trước khi thêm key

Khách Việt gõ 4–6 tin ngắn liên tiếp. Xử ở tầng gateway (chờ họ im rồi mới đẩy
một lượt cho model) **rẻ và chắc hơn** để model tự phán đoán.

**Đã kiểm trên bản 2026.9.4: KHÔNG có key gộp tin dồn cho người dùng.** Trong
package chỉ có `createChannelInboundDebouncer` — thứ dành cho người viết plugin,
không phải key trong `openclaw.json`.

Nên luật gộp tin nằm ở `AGENTS.md` (mục *Tin dồn và nhịp gửi*), bot xử bằng phán
đoán. Chấp nhận được, chỉ là không chắc bằng máy.

Bản sau có thể thêm — kiểm trên máy mình trước khi thêm bất cứ key nào:

```bash
openclaw config schema | grep -i "debounce\|batch\|behavior"
```

**Không thấy thì đừng thêm.** Config lạ có thể bị nuốt im lặng và mình tưởng đã
bật.

Cùng luật đó cho *đang soạn* / *đã xem* và chia tin: có key thì bật, không có thì
để `AGENTS.md` lo.

Có thật trên 2026.9.4: `channels.zalouser.mediaMaxMb` (chặn cỡ file gửi ra) và
`channels.zalouser.dangerouslyAllowNameMatching` — **đừng bật cái thứ hai**, nó
cho phép khớp nhóm theo tên thay vì ID.

---

## Kiểm mọi key, không chỉ key gộp tin

Kỷ luật ở mục trên áp cho **tất cả** key trong file này, không riêng chuyện gộp
tin: `channels.zalouser.dmPolicy`, `allowFrom`, `groupPolicy`,
`groups."*".requireMention`, `agents.defaults.workspace`,
`agents.entries.main.identity.name`, `mentionPatterns`.

Merge xong **luôn chạy** — trước khi bật gateway:

```bash
openclaw config validate
```

Đọc **hết** kết quả, không chỉ dòng đầu. Hai kiểu lỗi:

- *Unrecognized key* → config hỏng, gateway không lên. Đặt key sai chỗ (hay gặp
  nhất: `identity` nằm trong `defaults`).
- Dòng **warning** dưới chữ `Config valid` → config chạy được nhưng **sai**. Hay
  gặp nhất: `dmPolicy="open" but allowFrom does not include "*"; all DMs will be
  dropped` — bot sống mà mọi khách nhắn riêng đều rơi. Lệnh vẫn ra exit 0, nên
  **đừng tin chữ "valid"**, đọc warning.

Bản 0.3.0 của template **đã sai cả hai** dù tự nhận "đã đối chiếu từng key" —
vì chỉ so với tài liệu, không chạy `validate`. Lần chạy thật đầu tiên mới lộ.
Bài học: **chạy, đừng đọc**.

Không thấy key trong bản đang cài → `openclaw config schema` tìm tên mới, rồi
sửa lại file này cho đúng máy của mình. Đừng chép mù từ tài liệu này.

Bản đã test: `05-thiet-lap.md` mục *Đã test với*.

