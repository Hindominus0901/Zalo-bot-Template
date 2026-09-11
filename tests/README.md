# tests — khớp chữ trong repo, không phải bot sống

Chạy từ gốc repo:

    python3 -m unittest discover -s tests -v
Windows: thay `python3` bằng `py`.

Không cần pip. Xanh = file bắt buộc có mặt, ma trận khớp markdown, config mẫu
`dmPolicy: open`, không commit khóa. **Không** chứng minh Gateway, Zalo, vision,
hay câu trả lời model.

Nick thật: [`docs/04-kich-ban-thu.md`](../docs/04-kich-ban-thu.md). Tiêu chuẩn
mở khách: [`docs/06-tieu-chuan.md`](../docs/06-tieu-chuan.md).

## Các bộ

| File | Canh gì |
|---|---|
| `test_smoke.py` | File bắt buộc có mặt, không commit khóa, tờ wiki là tờ chờ |
| `test_logic.py` | Ma trận khớp markdown, tool khai đủ, rào trong `<policy>` |
| `test_stress.py` | Mỗi ca khó trong ma trận phải được nói ở đâu đó |
| `test_co_che.py` | Chỉ mục sổ, trần phiếu, ba tầng prompt, sổ tin nợ, bàn giao |
| `test_dong_goi.py` | Cửa vào cho agent lạ, `CHUAN-BI`, file của shop, **link nội bộ** |
| `test_tinh_huong.py` | Sáu tình huống khó, và không có số tài khoản nào lọt vào kho |
| `test_vui.py` | Công tắc tắt hài, bảy nhóm không dám, luật nhóm |
| `test_gia_lap.py` | **Chạy luật thật** qua `sim/` — rào giờ, ngày nghỉ, gộp tin, nền prompt |

Hai test đáng để ý vì chúng bắt lỗi im lặng: `test_dong_goi` quét **mọi link
markdown và mọi đường dẫn trong backtick** — link gãy là agent dựng đi vào ngõ
cụt mà không ai biết. `test_tinh_huong` quét `knowledge/` và `skills/` tìm chuỗi
8–16 chữ số — bot đọc được hai thư mục đó, nên một số tài khoản lọt vào là bot
sẽ đọc cho khách.

