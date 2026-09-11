# Một file cấu hình OpenClaw — mẫu gộp

Người dựng đọc. Chủ shop: làm theo [`05-thiet-lap.md`](05-thiet-lap.md) (họ
bấm nút, quét mã). File này = **một chỗ** nhìn `openclaw.json` sau khi merge.

Hai mảnh nguồn (đừng sửa lệch nhau rồi quên gộp):

| Mảnh | File | Việc |
|---|---|---|
| Nick Zalo | [`config/openclaw.zalouser.example.json5`](../config/openclaw.zalouser.example.json5) | `dmPolicy: open`, tên Nami, nhóm phải gọi tên |
| Drive | [`config/mcp.example.json5`](../config/mcp.example.json5) | Tắt sẵn. Có `command` mẫu |

Merge vào `~/.openclaw/openclaw.json` trên **máy Gateway**. Workspace = đường dẫn
**tuyệt đối** thư mục shop. Đừng commit file thật, cookie, QR, token.

Tom cá nhân hay để `pairing`. Shop **không** copy pairing — khách lạ phải nhắn
được.

## Mẫu gộp (chú thích ở trên, JSON5 ở dưới)

Bắt buộc khớp `IDENTITY.md` (`name`). Model agent nên **có mắt** (xem ảnh) —
khách CSKH hay gửi ảnh. Chưa chọn model mắt → ghi `[CHỜ]` trên checklist B4,
đừng bảo nick đã sẵn.

```json5
{
  channels: {
    zalouser: {
      enabled: true,
      dmPolicy: "open",
      groupPolicy: "allowlist",
      groups: {
        "*": { requireMention: true },
      },
    },
  },
  agents: {
    defaults: {
      workspace: "/duong/dan/tuyet/doi/toi/repo-shop",
      identity: { name: "Nami" },
    },
  },
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
tin: `channels.zalouser.dmPolicy`, `groupPolicy`, `groups."*".requireMention`,
`agents.defaults.workspace`, `agents.defaults.identity.name`, `mentionPatterns`.

```bash
openclaw config schema | grep -i dmPolicy
```

Không thấy key → **đừng chép mù từ tài liệu này**. OpenClaw có thể nuốt im lặng
một key lạ, và mình tưởng đã bật. Tìm tên mới bằng `config schema`, rồi sửa lại
file này cho đúng máy của mình.

Bản đã test: `05-thiet-lap.md` mục *Đã test với*.

