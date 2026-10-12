#!/usr/bin/env python3
"""Quét mã đăng nhập Zalo ngay trong cửa sổ SSH — không phải tải ảnh về.

    python3 scripts/quet_ma.py

Plugin @openclaw/zalouser (2026.9.4) KHÔNG in mã QR ra terminal: nó ghi ảnh
`openclaw-zalouser-qr-<profile>.png` vào thư mục tạm và in dòng
`Scan QR image: <đường dẫn>` (đã đọc trong mã nguồn plugin). Trên VPS không
màn hình, người dựng phải `scp` ảnh về — mà mã hết hạn nhanh.

Script này chạy `openclaw channels login --channel zalouser`, bắt dòng đó, giải
mã PNG bằng thư viện chuẩn (không cài gì thêm) và vẽ QR bằng ký tự khối ngay
trên màn hình. Mã đổi thì vẽ lại.

    python3 scripts/quet_ma.py --anh duong/dan/qr.png    # chỉ vẽ một ảnh có sẵn
"""

from __future__ import annotations

import argparse
import re
import shutil
import struct
import subprocess
import sys
import zlib
from pathlib import Path

DONG_QR = re.compile(r"Scan QR image:\s*(\S+\.png)", re.I)
VIEN = 4   # vùng trắng quanh mã, chuẩn QR đòi tối thiểu 4 ô


class LoiAnh(Exception):
    pass


# ── Giải mã PNG — stdlib ──────────────────────────────────────────────────────

def _paeth(a: int, b: int, c: int) -> int:
    p = a + b - c
    pa, pb, pc = abs(p - a), abs(p - b), abs(p - c)
    if pa <= pb and pa <= pc:
        return a
    return b if pb <= pc else c


def doc_png(data: bytes) -> tuple[int, int, list[list[float]]]:
    """Trả (rộng, cao, độ sáng 0..1 từng điểm). Hỗ trợ xám / RGB / bảng màu /
    có kênh alpha, độ sâu 1–8 bit, đủ năm bộ lọc dòng. Không hỗ trợ xen kẽ."""
    if data[:8] != b"\x89PNG\r\n\x1a\n":
        raise LoiAnh("không phải file PNG")
    pos, idat, plte, trns = 8, b"", None, None
    w = h = depth = ctype = interlace = None
    while pos < len(data):
        (n,) = struct.unpack(">I", data[pos:pos + 4])
        kind = data[pos + 4:pos + 8]
        body = data[pos + 8:pos + 8 + n]
        pos += 12 + n
        if kind == b"IHDR":
            w, h, depth, ctype, _, _, interlace = struct.unpack(">IIBBBBB", body)
        elif kind == b"PLTE":
            plte = body
        elif kind == b"tRNS":
            trns = body
        elif kind == b"IDAT":
            idat += body
        elif kind == b"IEND":
            break
    if w is None:
        raise LoiAnh("PNG thiếu IHDR")
    if interlace:
        raise LoiAnh("PNG xen kẽ (interlaced) — chưa hỗ trợ")
    kenh = {0: 1, 2: 3, 3: 1, 4: 2, 6: 4}.get(ctype)
    if kenh is None:
        raise LoiAnh(f"kiểu màu PNG lạ: {ctype}")
    if depth == 16:
        raise LoiAnh("PNG 16 bit — chưa hỗ trợ")
    raw = zlib.decompress(idat)
    bpp = max(1, kenh * depth // 8)           # byte mỗi điểm, cho bộ lọc
    dong_byte = (w * kenh * depth + 7) // 8
    out, truoc, i = [], bytearray(dong_byte), 0
    for _ in range(h):
        loc = raw[i]
        dong = bytearray(raw[i + 1:i + 1 + dong_byte])
        i += 1 + dong_byte
        for x in range(dong_byte):
            a = dong[x - bpp] if x >= bpp else 0
            b = truoc[x]
            c = truoc[x - bpp] if x >= bpp else 0
            if loc == 1:
                dong[x] = (dong[x] + a) & 0xFF
            elif loc == 2:
                dong[x] = (dong[x] + b) & 0xFF
            elif loc == 3:
                dong[x] = (dong[x] + ((a + b) >> 1)) & 0xFF
            elif loc == 4:
                dong[x] = (dong[x] + _paeth(a, b, c)) & 0xFF
            elif loc != 0:
                raise LoiAnh(f"bộ lọc dòng lạ: {loc}")
        out.append(_sang_dong(dong, w, depth, ctype, kenh, plte, trns))
        truoc = dong
    return w, h, out


def _gia_tri(dong: bytearray, w: int, kenh: int, depth: int) -> list[int]:
    if depth == 8:
        return list(dong[:w * kenh])
    vals, moi_byte = [], 8 // depth
    mask = (1 << depth) - 1
    for x in range(w * kenh):
        byte = dong[x // moi_byte]
        dich = 8 - depth * (x % moi_byte + 1)
        vals.append((byte >> dich) & mask)
    return vals


def _sang_dong(dong, w, depth, ctype, kenh, plte, trns) -> list[float]:
    v = _gia_tri(dong, w, kenh, depth)
    toi = (1 << depth) - 1
    sang = []
    for x in range(w):
        p = v[x * kenh:(x + 1) * kenh]
        if ctype == 3:
            if plte is None:
                raise LoiAnh("PNG bảng màu thiếu PLTE")
            r, g, b = plte[p[0] * 3:p[0] * 3 + 3]
            alpha = trns[p[0]] / 255 if trns and p[0] < len(trns) else 1.0
            y = (0.299 * r + 0.587 * g + 0.114 * b) / 255
        elif ctype in (0, 4):
            y = p[0] / toi
            alpha = p[1] / toi if ctype == 4 else 1.0
        else:
            y = (0.299 * p[0] + 0.587 * p[1] + 0.114 * p[2]) / toi
            alpha = p[3] / toi if ctype == 6 else 1.0
        sang.append(y * alpha + (1 - alpha))   # trong suốt = nền trắng
    return sang


# ── Từ điểm ảnh ra ô QR ───────────────────────────────────────────────────────

def _chay(dong: list[bool]) -> list[tuple[bool, int, int]]:
    """(màu, vị trí đầu, độ dài) của từng đoạn liền màu trên một dòng."""
    out, x = [], 0
    while x < len(dong):
        bd = x
        while x < len(dong) and dong[x] == dong[bd]:
            x += 1
        out.append((dong[bd], bd, x - bd))
    return out


def _mau_dinh_vi(den: list[list[bool]]) -> list[tuple[float, float, float]]:
    """Tâm (x, y) và cỡ ô của mọi chỗ cắt ngang mẫu định vị: đen-trắng-đen-trắng-
    đen tỉ lệ 1:1:3:1:1. Khung viền, chữ, logo không có tỉ lệ này — đó là cách
    máy quét QR thật tìm mã trong một ảnh có thứ khác."""
    thay = []
    for y, dong in enumerate(den):
        r = _chay(dong)
        for k in range(len(r) - 4):
            seg = r[k:k + 5]
            if not (seg[0][0] and not seg[1][0] and seg[2][0] and not seg[3][0] and seg[4][0]):
                continue
            tong = sum(s[2] for s in seg)
            o = tong / 7
            if o < 1:
                continue
            ky_vong = (1, 1, 3, 1, 1)
            if all(abs(s[2] - kv * o) <= max(0.5 * o, 1) for s, kv in zip(seg, ky_vong)):
                thay.append((seg[0][1] + tong / 2, y + 0.5, o))
    return thay


def _gom(diem: list[tuple[float, float, float]]) -> list[tuple[float, float, float]]:
    """Gom các chỗ cắt gần nhau thành từng mẫu định vị (tâm trung bình)."""
    nhom: list[list[tuple[float, float, float]]] = []
    for d in diem:
        for g in nhom:
            gx = sum(p[0] for p in g) / len(g)
            gy = sum(p[1] for p in g) / len(g)
            if abs(d[0] - gx) <= 3.5 * d[2] and abs(d[1] - gy) <= 3.5 * d[2]:
                g.append(d)
                break
        else:
            nhom.append([d])
    return [(sum(p[0] for p in g) / len(g), sum(p[1] for p in g) / len(g),
             sum(p[2] for p in g) / len(g), len(g)) for g in nhom]


def _doc_dung(den: list[list[bool]], t) -> bool:
    """Cột qua tâm cũng phải là đen-trắng-đen-trắng-đen 1:1:3:1:1, tâm ở khối giữa."""
    x, y, o = int(t[0]), int(t[1]), t[2]
    if not (0 <= x < len(den[0])):
        return False
    cot = [den[r][x] for r in range(len(den))]
    for mau, bd, dai in [(m, b, d) for m, b, d in _chay(cot)]:
        if mau and bd <= y < bd + dai:      # khối đen chứa tâm = khối 3 ô
            if abs(dai - 3 * o) > max(1.5 * o, 1.5):
                return False
            tren = [s for s in _chay(cot[:bd])][-2:]
            duoi = [s for s in _chay(cot[bd + dai:])][:2]
            if len(tren) < 2 or len(duoi) < 2:
                return False
            ok = [(not tren[1][0]), tren[0][0], (not duoi[0][0]), duoi[1][0]]
            dai4 = [tren[1][2], tren[0][2], duoi[0][2], duoi[1][2]]
            return all(ok) and all(abs(d - o) <= max(0.5 * o, 1) for d in dai4)
    return False


def ra_o(w: int, h: int, sang: list[list[float]]) -> list[list[bool]]:
    """Ma trận ô QR (True = đen), dựa vào ba mẫu định vị ở ba góc."""
    den = [[s < 0.5 for s in dong] for dong in sang]
    if not any(any(d) for d in den):
        raise LoiAnh("ảnh trắng trơn — không thấy mã")
    # Dữ liệu ngẫu nhiên đôi khi có tỉ lệ 1:1:3:1:1 theo chiều NGANG. Mẫu định vị
    # thật thì đúng tỉ lệ cả chiều DỌC qua tâm — kiểm cả hai, như máy quét thật.
    g = [t for t in _gom(_mau_dinh_vi(den)) if _doc_dung(den, t)]
    g = sorted(g, key=lambda t: -t[3])[:3]
    if len(g) < 3:
        raise LoiAnh("không tìm thấy đủ ba mẫu định vị ở ba góc")
    tl = min(g, key=lambda t: t[0] + t[1])
    tr = max(g, key=lambda t: t[0] - t[1])
    bl = max(g, key=lambda t: t[1] - t[0])
    co = sum(t[2] for t in g) / 3
    n = round((tr[0] - tl[0]) / co) + 7
    if n < 21 or (n - 17) % 4:
        # cỡ QR hợp lệ là 21, 25, 29…; lệch thì đo lại theo chiều dọc
        n2 = round((bl[1] - tl[1]) / co) + 7
        n = n2 if n2 >= 21 and (n2 - 17) % 4 == 0 else n
    co_x = (tr[0] - tl[0]) / (n - 7)
    co_y = (bl[1] - tl[1]) / (n - 7)
    x0 = tl[0] - 3.5 * co_x
    y0 = tl[1] - 3.5 * co_y
    o = []
    for r in range(n):
        yy = min(h - 1, max(0, int(y0 + (r + 0.5) * co_y)))
        o.append([den[yy][min(w - 1, max(0, int(x0 + (c + 0.5) * co_x)))] for c in range(n)])
    return o


def ve(o: list[list[bool]], mau: bool = True) -> str:
    """Hai ô dọc một ký tự ▀. Có màu thì ép nền trắng / chữ đen — quét được cả
    khi terminal đang nền tối."""
    n = len(o)
    m = [[False] * (n + 2 * VIEN) for _ in range(VIEN)]
    m += [[False] * VIEN + dong + [False] * VIEN for dong in o]
    m += [[False] * (n + 2 * VIEN) for _ in range(VIEN + 1)]   # +1 cho đủ cặp
    dong_ra = []
    for y in range(0, n + 2 * VIEN, 2):
        tren, duoi = m[y], m[y + 1]
        if mau:
            s = []
            for a, b in zip(tren, duoi):
                s.append(f"\x1b[{30 if a else 97};{40 if b else 107}m▀")
            dong_ra.append("".join(s) + "\x1b[0m")
        else:
            dong_ra.append("".join(
                " " if not a and not b else "█" if a and b else "▀" if a else "▄"
                for a, b in zip(tren, duoi)))
    return "\n".join(dong_ra)


def ve_file(duong: Path, mau: bool = True) -> str:
    w, h, s = doc_png(duong.read_bytes())
    return ve(ra_o(w, h, s), mau)


# ── Chạy đăng nhập ────────────────────────────────────────────────────────────

LOI_DAN = """
Mở Zalo trên điện thoại đang đăng nhập NICK BOT (không phải nick chủ),
bấm biểu tượng quét mã, đưa camera vào hình dưới đây. Mã hết hạn nhanh —
quét ngay. Không quét được: phóng to cửa sổ terminal, hoặc chụp màn hình
gửi cho chủ quét từ ảnh.
"""


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="Quét mã đăng nhập Zalo ngay trên terminal.")
    ap.add_argument("--anh", help="chỉ vẽ một ảnh QR có sẵn rồi thoát")
    ap.add_argument("--khong-mau", action="store_true", help="vẽ không dùng màu ANSI")
    ap.add_argument("--openclaw", default=shutil.which("openclaw") or "openclaw")
    a = ap.parse_args(argv)
    mau = not a.khong_mau

    if a.anh:
        try:
            print(ve_file(Path(a.anh), mau))
        except (OSError, LoiAnh) as e:
            print(f"✗ Không vẽ được: {e}", file=sys.stderr)
            return 1
        return 0

    try:
        p = subprocess.Popen([a.openclaw, "channels", "login", "--channel", "zalouser"],
                             stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, bufsize=1)
    except FileNotFoundError:
        print("✗ Không thấy lệnh openclaw — chạy scripts/cai_dat.sh trước.", file=sys.stderr)
        return 1
    da_ve = None
    for dong in p.stdout:
        m = DONG_QR.search(dong)
        if not m:
            print(dong, end="")
            continue
        duong = Path(m.group(1))
        try:
            hinh = ve_file(duong, mau)
        except (OSError, LoiAnh) as e:
            print(f"\n✗ Không vẽ được mã trên terminal ({e}). Tải ảnh về mà quét:\n"
                  f"  scp <user>@<vps>:{duong} .\n")
            continue
        if da_ve:
            print("\n── Mã mới (mã cũ đã hết hạn) ──")
        print(LOI_DAN)
        print(hinh)
        print(f"\n(ảnh gốc: {duong})\n")
        da_ve = duong
    p.wait()
    if p.returncode == 0:
        print("✓ Đăng nhập xong. Kiểm: openclaw directory self --channel zalouser")
    return p.returncode


if __name__ == "__main__":
    raise SystemExit(main())
