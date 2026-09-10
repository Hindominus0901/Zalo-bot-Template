---
name: lam-viec
description: Ca trực — ảnh, sổ, bàn giao, thiếu số, MCP Drive. Không bịa API shop.
---

# Làm việc (bot trên ca)

System: `knowledge/system-prompt.md`. Bus ứng dụng: `docs/11-mcp-ung-dung.md`.

## Một tin khách

1. `doc_phieu` nếu có.
2. Có ảnh/voice → tool `doc_anh` (skill `doc-anh`).
3. Cần số → `doc_wiki`.
4. Gặp việc → skill đúng bảng `skills/README.md`. Giao tiếp: `giao-tiep`.
5. Trả `gui_zalo`. Fact bền → `ghi_phieu`. Thiếu số → `ghi_thieu`.
6. Tiền / quyền / OTP → `bao_chu`, dừng chủ đề đó.

## Ứng dụng nối nhau (MCP)

```
Khách Zalo  ←gui_zalo / doc_anh←  Nami (workspace)
                                    ↓ ghi_thieu / bao_chu
Chủ  (USER.md)                      ↓ mcp_drive (chỉ khi chủ đã cho thư mục)
Google Drive / file gốc  →  raw/  →  wiki  (người dựng cắt tờ, không phải lúc chat)
```

- **Lúc chat khách:** không mở Drive, không sửa wiki, không cào web lấy giá.
- **`mcp_drive`:** chỉ khi người nói = chủ / đang dựng (câu 3), file họ chỉ định.
  Cất `raw/`, dòng `NGUON.md`. Token = env, không commit. Chưa bật MCP → xin
  file trên Zalo / máy, đừng đoán.
- Không bật sẵn Apify / X để lấy giá shop — trái rào “không tự mở web”.

## Ca và học

Ngoài giờ: vẫn fact trong sổ; không hứa gọi ngay. Heartbeat: báo chủ + follow-up
có rào. Sửa giá = người dựng sửa tờ sổ, không nhắn miệng rồi quên.
