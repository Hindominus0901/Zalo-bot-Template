#!/usr/bin/env python3
"""Soi cả máy bot một lệnh — xanh / đỏ, chữ thường, dòng đỏ kèm cách sửa.

    python3 scripts/kiem_tra_may.py

Chỉ ĐỌC: không sửa config, không bật tắt gì. Gateway chưa chạy vẫn soi được
phần tĩnh (bản cài, config, quyền, skill).

Mọi phép kiểm dựa trên output thật của OpenClaw 2026.9.4 (đã chạy để xem khuôn).
"""

from __future__ import annotations

import argparse
import json
import re
import shutil
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
BAN_OPENCLAW = "2026.9.4"


@dataclass
class Dong:
    muc: str          # "ok" | "loi" | "nhac"
    ten: str
    sua: str = ""


def ok(ten): return Dong("ok", ten)
def loi(ten, sua): return Dong("loi", ten, sua)
def nhac(ten, sua=""): return Dong("nhac", ten, sua)


# ── Phép kiểm thuần: nhận output, trả Dong ────────────────────────────────────

def kiem_node(ra: str | None) -> Dong:
    if not ra:
        return loi("Chưa có Node", "chạy: bash scripts/cai_dat.sh")
    m = re.search(r"v?(\d+)\.(\d+)", ra)
    if not m:
        return loi(f"Không đọc được bản Node ({ra.strip()})", "chạy: bash scripts/cai_dat.sh")
    lon, nho = int(m.group(1)), int(m.group(2))
    dung = (lon == 24 and nho >= 16) or (lon == 26 and nho >= 1) or lon > 26
    if dung:
        return ok(f"Node {ra.strip()}")
    return loi(f"Node {ra.strip()} — OpenClaw đòi >=24.16 <25 hoặc >=26.1",
               "chạy: bash scripts/cai_dat.sh (cài v24.21.0, bản đã chạy thật)")


def kiem_openclaw(ra: str | None) -> Dong:
    if not ra:
        return loi("Chưa có OpenClaw", "chạy: bash scripts/cai_dat.sh")
    m = re.search(r"(\d{4}\.\d+\.\d+)", ra)
    ban = m.group(1) if m else ra.strip()
    if ban == BAN_OPENCLAW:
        return ok(f"OpenClaw {ban}")
    return nhac(f"OpenClaw {ban} — template mới thử với {BAN_OPENCLAW}",
                "chạy được thì thôi; lỗi lạ thì cài đúng bản: bash scripts/cai_dat.sh")


def kiem_plugin(plugins_json: str | None) -> Dong:
    try:
        ds = json.loads(plugins_json or "[]")
    except json.JSONDecodeError:
        ds = []
    ds = ds if isinstance(ds, list) else ds.get("plugins", [])
    z = [p for p in ds if p.get("id") == "zalouser"]
    if not z:
        return loi("Chưa cài plugin Zalo", f"openclaw plugins install @openclaw/zalouser@{BAN_OPENCLAW}")
    if str(z[0].get("status")) not in ("loaded", "enabled", "True"):
        return loi(f"Plugin Zalo không chạy ({z[0].get('status')})", "openclaw doctor")
    return ok(f"Plugin Zalo {z[0].get('version')}")


def kiem_validate(ma_thoat: int, ra: str) -> Dong:
    if ma_thoat != 0:
        dau = next((d.strip() for d in ra.splitlines() if "×" in d or "Unrecognized" in d), ra.strip()[:160])
        return loi(f"Config hỏng — gateway sẽ không lên: {dau}",
                   "python3 scripts/dien_config.py (gộp lại config mẫu)")
    if "all DMs will be dropped" in ra:
        return loi("Config chạy được nhưng RƠI HẾT tin khách nhắn riêng (thiếu allowFrom \"*\")",
                   "python3 scripts/dien_config.py")
    if "warning" in ra.lower():
        canh = [d.strip(" !") for d in ra.splitlines() if d.strip().startswith("!")]
        return nhac("Config có cảnh báo: " + "; ".join(canh)[:200])
    return ok("Config hợp lệ, không cảnh báo")


def kiem_cfg(gia_tri: dict) -> list[Dong]:
    """gia_tri: kết quả `openclaw config get <khoá> --json` cho các khoá dưới."""
    out = []
    if gia_tri.get("session.dmScope") == "per-channel-peer":
        out.append(ok("Mỗi khách một cuộc trò chuyện riêng"))
    else:
        out.append(nhac("dmScope chưa đặt per-channel-peer (Zalo vẫn tự tách, nhưng nên ghi rõ)",
                        "python3 scripts/dien_config.py"))
    tools = gia_tri.get("agents.entries.main.tools") or {}
    cap = set(tools.get("alsoAllow") or []) | set(tools.get("allow") or [])
    if tools.get("profile") != "minimal" or cap & {"exec", "process", "automations", "cron", "gateway"}:
        out.append(loi("Bot trả khách có quyền quá rộng (chạy lệnh / hẹn giờ trên máy)",
                       "python3 scripts/dien_config.py"))
    else:
        out.append(ok("Bot trả khách không chạy lệnh máy, không hẹn giờ"))
    chu = gia_tri.get("commands.ownerAllowFrom") or []
    if not chu or any("SENDERID_CHU" in str(x) for x in chu):
        out.append(nhac("Chưa khai nick chủ — chủ chưa dạy bot / giao việc qua Zalo được",
                        "python3 scripts/lay_sender_id.py"))
    else:
        out.append(ok("Đã khai nick chủ — chủ dạy bot được qua tin riêng"))
    return out


def kiem_skill(agent: str, skills_json: str | None, goc: Path) -> Dong:
    try:
        d = json.loads(skills_json or "{}")
    except json.JSONDecodeError:
        return nhac(f"Không đọc được skill của {agent}")
    ws = Path(d.get("workspaceDir") or "")
    if ws.resolve() != goc.resolve():
        return loi(f"Bot {agent} đang chạy ở {ws} — không phải thư mục shop {goc}",
                   "python3 scripts/dien_config.py (đặt workspace cho từng agent)")
    thay = {s["name"] for s in d.get("skills", [])
            if "workspace" in str(s.get("source", "")) and not s.get("blockedByAgentFilter")}
    if not thay:
        return loi(f"Bot {agent} không thấy skill nào của shop", "python3 scripts/dien_config.py")
    chi_chu = {"day-bot", "giao-viec", "thong-bao-lich"}
    if agent == "main" and thay & chi_chu:
        return loi("Bot trả khách thấy skill dạy bot / giao việc", "python3 scripts/dien_config.py")
    if agent == "admin" and not chi_chu <= thay:
        return loi("Bot của chủ thiếu skill dạy bot / giao việc", "python3 scripts/dien_config.py")
    return ok(f"Bot {agent}: đúng thư mục shop, thấy {len(thay)} skill")


def kiem_gateway(status_json: str | None) -> list[Dong]:
    try:
        d = json.loads(status_json or "{}")
    except json.JSONDecodeError:
        return [loi("Không đọc được trạng thái gateway", "openclaw gateway status")]
    out = []
    if (d.get("service") or {}).get("loaded"):
        out.append(ok("Gateway tự bật lại khi máy khởi động lại"))
    else:
        out.append(loi("Gateway chưa cài làm dịch vụ — tắt máy / mất SSH là bot im",
                       "openclaw gateway install"))
    if (d.get("rpc") or {}).get("ok"):
        out.append(ok("Gateway đang chạy"))
    else:
        out.append(loi("Gateway không trả lời — bot đang im", "openclaw gateway restart"))
    return out


def kiem_so(goc: Path) -> Dong:
    """Dựng máy xong mà quên chuyển sổ sang → bot chạy nhưng chẳng biết shop bán gì."""
    chua = [r for r in ("knowledge/wiki/public/ban-gi.md", "knowledge/wiki/public/gia.md")
            if (goc / r).exists() and "[CHỜ CHỦ SHOP]" in (goc / r).read_text(encoding="utf-8")]
    if chua:
        return nhac("Sổ shop chưa điền (" + ", ".join(Path(r).name for r in chua) + ") — bot chưa biết shop bán gì",
                    "điền ở máy khác rồi? chuyển sang: python3 scripts/mo_goi.py (docs/17)")
    return ok("Sổ shop đã có chữ")


def kiem_mui_gio(tz: str | None) -> Dong:
    if tz and ("Ho_Chi_Minh" in tz or tz in ("Asia/Saigon", "+07")):
        return ok(f"Múi giờ {tz}")
    return loi(f"Múi giờ {tz or 'không rõ'} — giờ trực / follow-up sẽ lệch",
               "sudo timedatectl set-timezone Asia/Ho_Chi_Minh")


def kiem_ram(meminfo: str | None) -> Dong:
    if not meminfo:
        return nhac("Không đọc được RAM (không phải Linux?)")
    kb = {k: int(v) for k, v in re.findall(r"^(\w+):\s+(\d+)", meminfo, re.M)}
    ram, swap = kb.get("MemTotal", 0) / 1024 / 1024, kb.get("SwapTotal", 0) / 1024 / 1024
    if ram <= 1.2 and swap < 1:
        return loi(f"RAM {ram:.1f} GB, không có swap — dễ bị tắt giữa chừng",
                   "bash scripts/cai_dat.sh (tự thêm swap 2 GB)")
    return ok(f"RAM {ram:.1f} GB, swap {swap:.1f} GB")


# ── Chạy lệnh thật ────────────────────────────────────────────────────────────

def _chay(*cmd, timeout=60) -> tuple[int, str]:
    try:
        r = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout)
        return r.returncode, r.stdout + r.stderr
    except (FileNotFoundError, subprocess.TimeoutExpired) as e:
        return 127, str(e)


def _json_get(oc: str, khoa: str):
    ma, ra = _chay(oc, "config", "get", khoa, "--json")
    if ma != 0:
        return None
    for thu in (ra.strip(), ra.strip().splitlines()[-1] if ra.strip() else ""):
        try:
            return json.loads(thu)
        except json.JSONDecodeError:
            continue
    return None


def soi(oc: str, goc: Path) -> list[Dong]:
    out = []
    node = shutil.which("node")
    out.append(kiem_node(_chay(node, "--version")[1] if node else None))
    if not shutil.which(oc) and not Path(oc).exists():
        out.append(kiem_openclaw(None))
        return out
    out.append(kiem_openclaw(_chay(oc, "--version")[1]))
    out.append(kiem_plugin(_chay(oc, "plugins", "list", "--json")[1]))
    out.append(kiem_validate(*_chay(oc, "config", "validate")))
    out += kiem_cfg({k: _json_get(oc, k) for k in
                     ("session.dmScope", "agents.entries.main.tools", "commands.ownerAllowFrom")})
    for ag in ("main", "admin"):
        out.append(kiem_skill(ag, _chay(oc, "skills", "list", "--agent", ag, "--json")[1], goc))
    out += kiem_gateway(_chay(oc, "gateway", "status", "--json")[1])
    out.append(kiem_so(goc))
    tz = None
    if shutil.which("timedatectl"):
        ma, ra = _chay("timedatectl", "show", "-p", "Timezone", "--value")
        # Máy không có systemd (container) thì lệnh này in lỗi — đừng lấy lỗi làm tên múi giờ.
        tz = ra.strip() if ma == 0 and "/" in ra.strip() else None
    if not tz:
        try:
            lt = Path("/etc/localtime").resolve().as_posix()
            tz = lt.split("zoneinfo/")[-1] if "zoneinfo/" in lt else None
        except OSError:
            tz = None
    out.append(kiem_mui_gio(tz))
    mem = Path("/proc/meminfo")
    out.append(kiem_ram(mem.read_text() if mem.exists() else None))
    return out


def in_ra(ds: list[Dong]) -> int:
    dau = {"ok": "✓", "loi": "✗", "nhac": "•"}
    for d in ds:
        print(f"{dau[d.muc]} {d.ten}")
        if d.sua and d.muc != "ok":
            print(f"    → {d.sua}")
    so_loi = sum(d.muc == "loi" for d in ds)
    print()
    print("Máy sẵn sàng." if not so_loi else f"Còn {so_loi} chỗ đỏ — sửa theo dòng → ở trên.")
    return 1 if so_loi else 0


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="Soi cả máy bot một lệnh.")
    ap.add_argument("--openclaw", default=shutil.which("openclaw") or "openclaw")
    ap.add_argument("--workspace", default=str(ROOT))
    a = ap.parse_args(argv)
    return in_ra(soi(a.openclaw, Path(a.workspace)))


if __name__ == "__main__":
    raise SystemExit(main())
