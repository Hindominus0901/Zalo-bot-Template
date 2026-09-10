# Lịch sử template

Đọc trước khi kéo bản mới. Cách kéo: [`docs/15-cap-nhat.md`](docs/15-cap-nhat.md).

Bản nào đổi thứ shop đang phụ thuộc — tên trường phiếu, tên tool, tên tờ wiki,
tên file — **phải ghi ở đây**. Không ghi = coi như không đổi.

## 0.1.0 — chưa chạy thật

Bản đầu. **Chưa chạy trên nick Zalo thật.** Toàn bộ kho chữ có test
(`python3 -m unittest discover -s tests`), nhưng test chỉ chứng minh file khớp
nhau, không chứng minh bot sống. Trước khi bán: chạy hết `docs/04-kich-ban-thu.md`
và `docs/14-vps-headless.md` trên máy thật, rồi điền khối *Đã test với* trong
`docs/05-thiet-lap.md`.

Có gì:

- Bot Nami trên nick Zalo cá nhân (OpenClaw + plugin `zalouser`)
- Giọng, cách tư vấn, 15 skill CSKH, phiếu khách theo Zalo ID
- Sổ shop dạng wiki + chỉ mục sinh tự động
- Ba tầng prompt, khối `<policy>`, vòng học cuối ngày, sổ tin nợ khách
- Tool `tra_don` (tắt sẵn), MCP Google Drive (tắt sẵn)
- Quy trình dựng B0→B7 cho coding agent bất kỳ
