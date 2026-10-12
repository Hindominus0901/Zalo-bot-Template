# Nhật ký sửa sổ qua Zalo

Bot admin ghi vào đây **mỗi lần** chủ dạy bot (`skills/day-bot`). Một file một
ngày: `YYYY-MM-DD.md`. Không ghi được nhật ký = không sửa.

Mỗi lần sửa:

```
## 14:05 — ship.md
Chủ nói: "từ giờ khách hỏi ship Hà Nội thì báo 25k nha"
Đã nhắc lại và được gật: có
Trước: - Nội thành Hà Nội: 30.000đ
Sau:   - Nội thành Hà Nội: 25.000đ
```

Lùi: lấy dòng **Trước** của lần gần nhất, viết lại đúng chỗ, ghi thêm một mục
`lùi`. File thật nằm ngoài git (`.gitignore`) — có lời chủ trong đó.
