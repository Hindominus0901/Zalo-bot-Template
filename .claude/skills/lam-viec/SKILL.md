---
name: lam-viec
description: Làm việc dựng bot — file, ảnh, MCP Drive, nối ứng dụng. Không cào web lấy giá.
---

# Làm việc + MCP (coding agent)

Dựng shop: `khoi-tao` B0→B7. Nói với chủ: `giao-tiep`. Bus:
[`docs/11-mcp-ung-dung.md`](../../../docs/11-mcp-ung-dung.md).

## Thứ tự dữ liệu

1. Chủ **nói** hoặc **gửi file/ảnh/link**.
2. Ảnh → đọc chữ (vision / tool `doc_anh` trên file họ gửi). Drive → `mcp_drive`
   nếu MCP đã bật **và** họ chỉ đúng thư mục/file.
3. Cất nguyên `knowledge/raw/` + dòng `NGUON.md`.
4. Cắt tờ `wiki/` — không đẻ số.
5. Config / QR / thử nick = B4–B6, sau khi sổ có chữ.

## MCP giữa ứng dụng

| Ứng dụng | Việc | Khi nào |
|---|---|---|
| **Cursor Google Drive** | Lấy file chủ đã cho vào `raw/` | Họ dán link / chỉ folder; MCP đã đăng nhập |
| **OpenClaw `mcp.servers`** | Bot/gateway đọc cùng Drive lúc dựng hoặc chủ bổ sung | Merge `config/mcp.example.json5`, OAuth, `enabled: true` |
| **Zalo zalouser** | Chat khách + bàn giao chủ | Sau QR; không phải MCP |
| **Workspace file** | Sổ, phiếu, skill | Luôn |

Chưa auth Drive: xin họ gửi file vào chat / máy. **Đừng** gọi MCP rồi bịa.

**Cấm:** Apify / tự mở Facebook / web shop để chép giá. X/Twitter không phải
kho CSKH. Token/cookie không commit, không dán vào chat chủ.

## Kiểm

`python3 -m unittest discover -s tests -v`. Ảnh CK trên nick thử: `04-kich-ban-thu.md`.
`openclaw mcp doctor` (nếu đã thêm server) — fail thì tắt `enabled`, làm bằng file tay.
