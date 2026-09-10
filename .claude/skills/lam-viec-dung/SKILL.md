---
name: lam-viec-dung
description: Làm việc dựng bot — file, ảnh, MCP Drive. Không cào web lấy giá.
---

# Làm việc + MCP (coding agent)

Dựng: `khoi-tao` B0→B7. Nói với chủ: `giao-tiep-chu`. Bus:
[`docs/11-mcp-ung-dung.md`](../../../docs/11-mcp-ung-dung.md).
**Không** nhầm với skill bot `skills/lam-viec` (ca chat).

## Thứ tự dữ liệu

1. Chủ **nói** hoặc **gửi file/ảnh/link**.
2. Ảnh → đọc chữ (vision). Drive → `mcp_drive` chỉ khi MCP **enabled** và họ chỉ
   đúng thư mục. Chưa bật = xin file tay.
3. Cất nguyên `knowledge/raw/` + dòng `NGUON.md`.
4. Cắt tờ `wiki/` — không đẻ số.
5. Config / quét mã / thử nick = B4–B6, sau khi sổ có chữ.

## MCP

| Ứng dụng | Khi nào |
|---|---|
| Cursor Google Drive | Họ dán link; MCP đã đăng nhập |
| OpenClaw `mcp.servers` | Merge `config/mcp.example.json5`, OAuth, `enabled: true` |
| Zalo zalouser | Sau quét mã — không phải MCP |
| File workspace | Luôn |

**Cấm:** Apify / tự mở Facebook / web lấy giá. Token không commit.

## Kiểm

`python3 -m unittest discover -s tests -v` = kho chữ khớp, **không** = nick sống.
Nick: `docs/04-kich-ban-thu.md`. `openclaw mcp doctor` fail → `enabled: false`.
