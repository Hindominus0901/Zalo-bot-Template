# Cập nhật template — giữ phần shop đã điền

Dành cho **người dựng**. Chỉ cần đọc khi tác giả template ra bản mới và shop
muốn lấy về.

Vấn đề: chủ shop điền **đè lên chính file của template** (giá vào `wiki/public/gia.md`,
tên vào `IDENTITY.md`…). Nên `git pull` sẽ đụng vào đúng nội dung shop. Không có
cách nào tránh hoàn toàn — nhưng biết trước file nào là của ai thì gỡ nhanh.

---

## File nào của ai

### Của shop — luôn giữ bản của mình

Mỗi file này mang một dòng đánh dấu ở đầu:

```
<!-- FILE CỦA SHOP — giữ bản của bạn khi cập nhật template -->
```

- `IDENTITY.md`
- `USER.md`
- `MEMORY.md`
- `knowledge/persona.md`
- `knowledge/wiki/INDEX.md`
- `knowledge/wiki/public/ban-gi.md`
- `knowledge/wiki/public/bao-hanh.md`
- `knowledge/wiki/public/con-hang.md`
- `knowledge/wiki/public/dat-lich.md`
- `knowledge/wiki/public/dia-chi.md`
- `knowledge/wiki/public/doi-tra.md`
- `knowledge/wiki/public/gia.md`
- `knowledge/wiki/public/gio-truc.md`
- `knowledge/wiki/public/hoa-don-vat.md`
- `knowledge/wiki/public/kiem-hang.md`
- `knowledge/wiki/public/ship.md`
- `knowledge/wiki/public/si-ctv.md`
- `knowledge/wiki/public/thanh-toan.md`
- `knowledge/wiki/internal/gia-von-hoa-hong.md`
- `knowledge/wiki/internal/xu-khach-kho.md`

Tác giả template **không sửa nội dung** mấy file này nữa sau bản đầu — chỉ sửa
tờ mẫu `knowledge/wiki/TRANG-MAU.md` nếu cần thêm tờ mới.

### Một phần của shop — đọc kỹ chỗ conflict

| File | Phần của shop |
|---|---|
| `SOUL.md` | Mục cuối *"Shop này — điền lúc phỏng vấn"*. Phần trên là giọng nền, **nên lấy bản mới** |
| `skills/khai-thac/SKILL.md` | Khối câu hỏi khai thác của shop. Phần còn lại là luật chung |
| `skills/ghi-don/SKILL.md` | Bước đặt riêng của shop, nếu có |

Ba file này conflict thì **giữ phần shop, lấy phần còn lại từ bản mới**.

### Của template — luôn lấy bản mới

Mọi thứ còn lại: `AGENTS.md`, `TOOLS.md`, `BOOT.md`, `HEARTBEAT.md`, `docs/`,
`dung-bot/`, `scripts/`, `tests/`, và các `skills/*/SKILL.md` không nằm trong
bảng trên.

Sửa mấy file này ở bản shop = tự làm khó mình lần cập nhật sau. Cần đổi hành vi
bot thì đổi qua `USER.md` / wiki / persona, không đổi qua harness.

### Không bao giờ đụng tới

`memory/` và `knowledge/raw/` — dữ liệu khách, đã bị git ignore, không đi theo
bản cập nhật.

---

## Cách kéo bản mới

Lần đầu, thêm repo gốc làm remote thứ hai:

```
git remote add template <đường-dẫn-repo-gốc>
```

Mỗi lần cập nhật:

```
git checkout -b thu-ban-moi        # đừng làm thẳng trên nhánh đang chạy
git fetch template
git merge template/main
```

Conflict thì theo bảng trên. Xong:

```
python3 scripts/lam_chi_muc.py     # bản mới có thể thêm tờ wiki
python3 -m unittest discover -s tests -v
```

Test xanh **và** chạy lại vài dòng trong `docs/04-kich-ban-thu.md` trên nick
thật, rồi mới trộn về nhánh chính. Đừng cập nhật rồi để đó — bot đang chạy thật.

Bot đang sống thì `openclaw gateway restart` sau khi trộn xong: `AGENTS.md`,
`SOUL.md`, `TOOLS.md` là nền prompt, đổi giữa phiên là lệch (`docs/12`).

---

## Đọc gì trước khi cập nhật

`CHANGELOG.md` ở gốc. Nếu bản mới đổi thứ shop đang phụ thuộc (tên trường phiếu,
tên tool, tên tờ wiki) thì nó phải ghi ở đó. Không ghi = coi như không đổi.

Không muốn cập nhật thì **đừng cập nhật**. Bản đang chạy vẫn chạy — không có
gì hết hạn.
