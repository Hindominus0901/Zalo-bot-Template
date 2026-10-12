#!/usr/bin/env python3
"""Lấy senderId Zalo của chủ — không phải đọc log.

    python3 scripts/lay_sender_id.py

Hiện một mã ngắn (ví dụ NAMI-4821). Chủ nhắn đúng mã đó cho nick bot, từ nick
của chủ. Script tìm cuộc trò chuyện vừa có mã đó và lấy senderId ra, rồi gộp
vào config (`dien_config.py --chu`).

Cần gateway đang chạy — tin phải được nhận thì mới có cuộc trò chuyện.

Cách tìm (đã kiểm trên OpenClaw 2026.9.4 + plugin zalouser 2026.9.4):
- Tin riêng Zalo đi vào phiên tên `agent:<agent>:zalouser:direct:<senderId>`
  (plugin định tuyến với peer.id = senderId; phiên tách theo từng người).
- `openclaw sessions --agent <a> --json` liệt kê phiên + chỗ lưu (SQLite).
- Mã được xác nhận bằng cách đọc SQLite đó ở chế độ CHỈ ĐỌC. Cấu trúc khác đi
  (OpenClaw bản khác) thì chỉ nhận khi có đúng MỘT cuộc trò chuyện mới, và hỏi lại.
"""

from __future__ import annotations

import argparse
import json
import re
import secrets
import shutil
import sqlite3
import subprocess
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
KHOA = re.compile(r"^agent:[^:]+:zalouser:(?:[^:]+:)?direct:(\d{6,25})$")


def sinh_ma() -> str:
    return f"NAMI-{secrets.randbelow(9000) + 1000}"


def ung_vien(phien: list[dict], tu_ms: int) -> list[tuple[str, str]]:
    """(senderId, khoá phiên) của mọi phiên Zalo riêng có hoạt động từ `tu_ms`."""
    ra = []
    for s in phien:
        m = KHOA.match(str(s.get("key", "")))
        if not m:
            continue
        luc = s.get("lastInteractionAt") or s.get("updatedAt") or 0
        try:
            luc = int(luc)
        except (TypeError, ValueError):
            continue
        if luc >= tu_ms:
            ra.append((m.group(1), s["key"]))
    return ra


def co_ma(sqlite_path: str, khoa: str, ma: str) -> bool | None:
    """True/False nếu đọc được; None nếu không đọc được (cấu trúc lạ, khoá file…)."""
    try:
        c = sqlite3.connect(f"file:{sqlite_path}?mode=ro", uri=True, timeout=2)
        try:
            dong = c.execute(
                "SELECT 1 FROM transcript_events te "
                "JOIN session_windows sw ON sw.session_id = te.session_id "
                "WHERE sw.session_key = ? AND te.event_json LIKE ? LIMIT 1",
                (khoa, f"%{ma}%")).fetchone()
            return dong is not None
        finally:
            c.close()
    except sqlite3.Error:
        return None


def phien_cua(oc: str, agent: str) -> tuple[list[dict], str | None]:
    r = subprocess.run([oc, "sessions", "--agent", agent, "--json", "--active", "60"],
                       capture_output=True, text=True)
    if r.returncode != 0:
        return [], None
    try:
        d = json.loads(r.stdout)
    except json.JSONDecodeError:
        return [], None
    return d.get("sessions", []), d.get("path")


def tim(oc: str, ma: str, tu_ms: int, agents=("main", "admin")) -> tuple[str | None, list[str]]:
    """Trả (senderId chắc chắn, các senderId chưa xác nhận được)."""
    chua_ro: list[str] = []
    for ag in agents:
        ds, kho = phien_cua(oc, ag)
        for sid, khoa in ung_vien(ds, tu_ms):
            kq = co_ma(kho, khoa, ma) if kho else None
            if kq:
                return sid, []
            if kq is None and sid not in chua_ro:
                chua_ro.append(sid)
    return None, chua_ro


def ten_bot() -> str:
    m = re.search(r"\*\*Name:\*\*\s*(.+)", (ROOT / "IDENTITY.md").read_text(encoding="utf-8"))
    return m.group(1).strip() if m else "Nami"


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="Lấy senderId Zalo của chủ bằng một mã ngắn.")
    ap.add_argument("--openclaw", default=shutil.which("openclaw") or "openclaw")
    ap.add_argument("--cho", type=int, default=600, help="chờ tối đa bao nhiêu giây (mặc định 600)")
    ap.add_argument("--khong-dien", action="store_true", help="chỉ in senderId, không gộp config")
    ap.add_argument("--ma", help="dùng mã có sẵn (để thử)")
    a = ap.parse_args(argv)

    ma = a.ma or sinh_ma()
    tu_ms = int(time.time() * 1000) - 5000
    print(f"""
Từ NICK ZALO CỦA CHỦ (không phải nick bot), nhắn đúng chữ này cho nick bot:

        {ma}

Bot có thể trả lời một câu — kệ nó. Đang chờ (tối đa {a.cho // 60} phút)…
""")
    het = time.time() + a.cho
    chua_ro: list[str] = []
    while time.time() < het:
        sid, chua_ro = tim(a.openclaw, ma, tu_ms)
        if sid:
            break
        time.sleep(3)
    else:
        sid = None

    if not sid and len(chua_ro) == 1:
        # Không đọc được nội dung (OpenClaw bản khác) — chỉ có một người vừa nhắn.
        tl = input(f"Thấy đúng một người vừa nhắn (senderId {chua_ro[0]}) nhưng không đọc "
                   f"được tin để chắc. Có phải chủ vừa nhắn {ma} không? c/k: ").strip().lower()
        sid = chua_ro[0] if tl.startswith("c") else None
    if not sid:
        if len(chua_ro) > 1:
            print("✗ Có nhiều người cùng nhắn, không đọc được tin để biết ai là chủ. "
                  "Thử lại lúc vắng, hoặc lấy tay: docs/14-vps-headless.md mục "
                  "'Lấy senderId và groupId'.", file=sys.stderr)
        else:
            print("✗ Chưa thấy tin. Kiểm: gateway đang chạy (openclaw gateway status), "
                  "nick bot đã đăng nhập (scripts/quet_ma.py), chủ nhắn đúng mã.", file=sys.stderr)
        return 1

    print(f"✓ senderId của chủ: {sid}")
    if a.khong_dien:
        return 0
    r = subprocess.run([sys.executable, str(ROOT / "scripts" / "dien_config.py"),
                        "--ten", ten_bot(), "--chu", sid, "--openclaw", a.openclaw])
    return r.returncode


if __name__ == "__main__":
    raise SystemExit(main())
