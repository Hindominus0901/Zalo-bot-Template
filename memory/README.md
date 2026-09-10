# Nhật ký ngày — vòng học của shop

Mỗi ngày một file: `memory/YYYY-MM-DD.md`. OpenClaw tự đọc hôm nay + hôm qua.

**Ghi:** câu khách mà wiki không có số; bàn giao; SĐT vừa xin (thu-lead); việc còn mở. Nguyên văn nếu được.
**Không ghi:** số CK, CCCD, mật khẩu, cả ảnh. SĐT chỉ vài số cuối nếu cần nhận diện.

File ngày bị git ignore (tránh lộ khách). Shop private muốn giữ thì `git add -f`.

Mẫu:

```markdown
# 2026-09-09

## Câu chưa có số trong wiki
- ~14h nick …123: "ship Đà Nẵng bao nhiêu"

## Bàn giao
- ~15h ảnh CK — đã báo người trong USER.md

## Việc mở
- Chờ chủ chốt phí Đà Nẵng
```

Fact shop bền (giá, ship) → trang wiki, không nhét vào đây.
Bài học vận hành bền (“khách hay hỏi ship tỉnh”) → `MEMORY.md`, ngắn.

---

## `memory/no-tra-loi.md` — sổ tin còn nợ khách

Zalo cá nhân **không gửi bù** tin lúc gateway tắt, khác webhook OA. Tin tới lúc
máy chết là mất luôn và không ai biết. File này là chỗ biết.

Nhận tin → thêm một dòng. Trả xong → **xóa dòng đó ngay**. File rỗng là đúng.
File chưa tồn tại cũng đúng — tạo khi có dòng đầu tiên.

```
{senderId} | {giờ nhận} | {vài chữ đầu của tin}
```

```
1234567890 | 2026-09-10 14:32 | ship đà nẵng bao nhiêu
```

**Không ghi:** nội dung đầy đủ, ảnh, số CK, SĐT đủ số. Vài chữ đủ nhận ra việc là được.

Bật máy lại thì `BOOT.md` xử: nợ trong 12h thì trả một tin xin lỗi, cũ hơn thì
chỉ báo chủ. File này bị git ignore như cả `memory/` — trong đó có chữ của khách.

