# Khung chấm — mẫu (chỉ dùng khi bật skill `cham-bai`)

Chép file này thành `knowledge/wiki/internal/khung-cham-<loại-bài>.md`, điền
**đúng lời chủ**, rồi chạy lại `scripts/lam_chi_muc.py`. Mỗi loại bài một khung.
Không có khung thì bot vẫn nhận xét, nhưng không kết luận đạt / chưa đạt.

```markdown
---
title: Khung chấm — <loại bài>
summary: "Chấm bài <loại> theo N mục; bot [được / không được] kết luận đạt."
updated: "YYYY-MM-DD"
sources: ["lời chủ, buổi phỏng vấn"]
---

# Khung chấm — <loại bài>

Bot được kết luận đạt / chưa đạt: **có / không** (không = chỉ nhận xét, chủ quyết).

| Mục | Đạt khi | Hay thiếu |
|---|---|---|
| 1. … | … | … |
| 2. … | … | … |

Mốc (xong bài này = qua phần nào): …
```
