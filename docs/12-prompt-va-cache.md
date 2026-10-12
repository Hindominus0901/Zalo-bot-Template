# Ba tầng prompt — đừng làm vỡ cache

Dành cho **người dựng**, không phải chủ shop. Chủ shop không cần đọc file này.

CSKH là loại bot nói nhiều lượt với cùng một người, cùng một đống chữ nền
(giọng, rào, catalog tool, chỉ mục sổ). Model tính tiền phần đầu prompt theo
kiểu: **giống hệt lần trước thì rẻ, lệch một ký tự thì tính lại từ chỗ lệch**.
Nên thứ tự nạp không phải chuyện thẩm mỹ — nó là tiền.

---

## Ba tầng

| Tầng | Gồm gì | Đổi khi nào |
|---|---|---|
| **1. Ổn định** | `AGENTS.md` (gồm `<policy>`) · `SOUL.md` · `IDENTITY.md` | Khi sửa file |
| **2. Bối cảnh** | `USER.md` · `MEMORY.md` · khối *Shop này và sổ* cuối `AGENTS.md` (chép từ `persona.md` + `INDEX.md`) | Khi dựng shop / chủ đổi thông tin |

**Chỉ năm file đó được nạp** — `AGENTS.md`, `SOUL.md`, `IDENTITY.md`, `USER.md`,
`MEMORY.md` (đã kiểm trong code OpenClaw 2026.9.4). Bản template cũ tưởng
`TOOLS.md`, `persona.md`, `INDEX.md` cũng được nạp — không phải. Bot không biết
shop bán gì và tra tờ nào trừ khi tự mở. Vì thế `scripts/lam_chi_muc.py` chép
`persona.md` + bảng chỉ mục vào cuối `AGENTS.md`: thấy ngay, không tốn lượt mở.
| **3. Bay hơi** | phiếu khách · trang wiki vừa đọc · ngày giờ · tin khách | **Mỗi lượt** |

Luật một câu: **tầng 3 không bao giờ nằm trong system prompt.** Nó đi kèm tin
của khách trong lượt đó.

Vì sao: nếu nhét phiếu khách vào system prompt, thì mỗi lượt phiếu đổi một tí là
cả phần đầu prompt lệch, và toàn bộ chỗ rẻ bên trên mất theo.

---

## Ba thứ giết cache — kiểm trước khi sửa prompt

1. **Dấu thời gian** ở tầng 1–2. `Hôm nay là 10/09/2026 14:32` nằm trong
   system prompt là hỏng ngay lượt sau. Cần giờ thì để giờ đi cùng tin khách.
2. **Id ngẫu nhiên / số phiên / số lượt.** Cùng lý do.
3. **Thứ tự không cố định.** Liệt kê tờ wiki, liệt kê skill, liệt kê tool —
   phải luôn cùng một thứ tự (sắp theo tên file). Hôm nay `a, b, c` mai `b, a, c`
   là lệch.

Dấu hiệu vỡ: tiền model không giảm dù khách nhắn liên tục trong một phiên.

---

## Phiếu khách: chụp một lần đầu phiên

Bot **đọc phiếu lúc mở phiên**, giữ nguyên bản chụp đó suốt phiên.

Ghi phiếu giữa phiên vẫn **xuống đĩa ngay** (khỏi mất dữ liệu nếu gateway chết),
nhưng bản trong đầu bot thì giữ nguyên tới hết phiên. Bot vừa ghi cái gì thì nó
tự nhớ trong lượt — không cần đọc lại.

Ngoại lệ duy nhất: khi runtime **nén ngữ cảnh** (hội thoại quá dài, phải tóm tắt
phần cũ). Lúc đó phần đầu prompt vỡ sẵn rồi, nên render lại phiếu là miễn phí.
Nén xong thì chụp lại phiếu.

---

## Sửa file thì bao giờ bot thấy

**Lượt sau.** OpenClaw đọc lại năm file nền **mỗi lượt** (code:
*"refreshing each turn so edits become visible"*) — không cần khởi động lại.
Skill làm mới khi có file `SKILL.md` đổi. Config (`agents`, `tools`, `bindings`…)
tự nạp lại. Chỉ **cài plugin mới** mới cần `openclaw gateway restart`.

Giá phải trả: sửa tầng 1–2 là phần đầu prompt đổi, lượt sau mất cache một lần.
Đừng sửa vặt cả ngày — gom lại sửa một lần.

`knowledge/wiki/public/*.md` thì khác — nội dung trang chỉ nạp khi bot cần
(`doc-wiki`), nằm ở tầng 3. Sửa số trong trang không đụng nền.
Nhưng **thêm, xóa trang hoặc đổi `summary` / `persona.md`** thì phải chạy lại
`scripts/lam_chi_muc.py` — nó viết lại khối nền cuối `AGENTS.md`.

---

## Mỗi lượt bot đọc bao nhiêu

`AGENTS.md` đã chốt: **mặc định không mở file nào**, tối đa 3 khi thật cần.

Đừng đọc cả `knowledge/` mỗi tin. Đừng đọc `hoi-thoai-mau.md` khi khách chỉ hỏi
phí ship. Cái gì hay dùng thì đã nằm sẵn ở tầng 1–2 rồi.
