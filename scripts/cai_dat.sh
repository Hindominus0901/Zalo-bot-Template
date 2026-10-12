#!/usr/bin/env bash
# Cài máy cho bot — một lệnh, chạy lại không hại.
#
#   bash scripts/cai_dat.sh            # hỏi trước khi thêm swap / đổi múi giờ
#   bash scripts/cai_dat.sh --yes      # đồng ý hết, không hỏi
#   bash scripts/cai_dat.sh --prefix ~/.local   # cài Node / OpenClaw vào chỗ khác
#
# Làm: Node đúng bản (v24.21.0 — bản đã chạy thật), OpenClaw + plugin Zalo đúng
# bản ghim (2026.9.4), kiểm Python, thêm swap cho máy nhỏ, đặt giờ Việt Nam.
# Không làm: nhập mã AI (việc của người — scripts/bat_dau.py hỏi sau).
#
# Linux / Mac. Windows: làm tay theo docs/05-thiet-lap.md.
set -euo pipefail

NODE_BAN="24.21.0"
OC_BAN="2026.9.4"
YES=0
PREFIX=""

while [ $# -gt 0 ]; do
  case "$1" in
    --yes|-y) YES=1 ;;
    --prefix) PREFIX="$2"; shift ;;
    -h|--help) sed -n '2,13p' "$0"; exit 0 ;;
    *) echo "Không hiểu: $1"; exit 2 ;;
  esac
  shift
done

xanh() { printf '✓ %s\n' "$*"; }
nhac() { printf '• %s\n' "$*"; }
do_() { printf '✗ %s\n' "$*" >&2; }
hoi() {   # hoi "câu hỏi" → 0 nếu đồng ý
  [ "$YES" = 1 ] && return 0
  [ -t 0 ] || return 1          # không có người ngồi trước máy → không tự làm
  printf '%s [c/k] ' "$1"; read -r tl
  case "$tl" in c|C|co|có|y|Y|yes) return 0 ;; *) return 1 ;; esac
}

# ── Quyền ghi ────────────────────────────────────────────────────────────────
SUDO=""
if [ "$(id -u)" != 0 ] && command -v sudo >/dev/null 2>&1; then SUDO="sudo"; fi
if [ -z "$PREFIX" ]; then
  if [ "$(id -u)" = 0 ] || [ -n "$SUDO" ]; then PREFIX="/usr/local"; else PREFIX="$HOME/.local"; fi
fi
mkdir -p "$PREFIX" 2>/dev/null || $SUDO mkdir -p "$PREFIX"
if [ -w "$PREFIX" ]; then CHAY=""; else CHAY="$SUDO"; fi

# ── Máy gì ───────────────────────────────────────────────────────────────────
case "$(uname -s)" in
  Linux)  OS=linux ;;
  Darwin) OS=darwin ;;
  *) do_ "Máy $(uname -s) — làm tay theo docs/05-thiet-lap.md"; exit 1 ;;
esac
case "$(uname -m)" in
  x86_64|amd64) ARCH=x64 ;;
  aarch64|arm64) ARCH=arm64 ;;
  *) do_ "Chip $(uname -m) chưa hỗ trợ — làm tay theo docs/05-thiet-lap.md"; exit 1 ;;
esac

# ── 1. Node ──────────────────────────────────────────────────────────────────
node_dung() {   # node_dung <đường dẫn node>
  local v; v="$("$1" --version 2>/dev/null)" || return 1
  v="${v#v}"; local lon="${v%%.*}" r="${v#*.}"; local nho="${r%%.*}"
  { [ "$lon" = 24 ] && [ "$nho" -ge 16 ]; } || { [ "$lon" = 26 ] && [ "$nho" -ge 1 ]; } || [ "$lon" -gt 26 ]
}

NODE_GOC="$(command -v node 2>/dev/null || true)"   # node mà shell của người dựng đang gọi
NODE=""
if command -v node >/dev/null 2>&1 && node_dung "$(command -v node)"; then
  NODE="$(command -v node)"
elif [ -x "$PREFIX/bin/node" ] && node_dung "$PREFIX/bin/node"; then
  NODE="$PREFIX/bin/node"
fi

if [ -n "$NODE" ]; then
  xanh "Node $("$NODE" --version) ($NODE)"
else
  co="$(command -v node 2>/dev/null || true)"
  [ -n "$co" ] && nhac "Node đang có $("$co" --version 2>/dev/null) ở $co — sai bản, cài v$NODE_BAN vào $PREFIX"
  tep="node-v$NODE_BAN-$OS-$ARCH.tar.gz"
  goc="https://nodejs.org/dist/v$NODE_BAN"
  tam="$(mktemp -d)"; trap 'rm -rf "$tam"' EXIT
  echo "  tải $tep…"
  curl -fsSL "$goc/$tep" -o "$tam/$tep"
  curl -fsSL "$goc/SHASUMS256.txt" -o "$tam/SHASUMS256.txt"
  can="$(grep " $tep\$" "$tam/SHASUMS256.txt" | cut -d' ' -f1)"
  if command -v sha256sum >/dev/null 2>&1; then co_sha="$(sha256sum "$tam/$tep" | cut -d' ' -f1)"
  else co_sha="$(shasum -a 256 "$tam/$tep" | cut -d' ' -f1)"; fi
  if [ -z "$can" ] || [ "$can" != "$co_sha" ]; then
    do_ "Tải Node bị lỗi (mã kiểm không khớp) — không cài. Thử lại sau."
    exit 1
  fi
  $CHAY tar -xzf "$tam/$tep" -C "$PREFIX" --strip-components=1
  NODE="$PREFIX/bin/node"
  node_dung "$NODE" || { do_ "Cài xong mà Node vẫn sai bản"; exit 1; }
  xanh "Đã cài Node $("$NODE" --version) vào $PREFIX (đã kiểm mã SHA256)"
fi

# Node đúng bản có thể bị một Node SAI đứng trước trong PATH che mất — script
# này tự dùng đúng bản, nhưng shell của người dựng sau đó vẫn gọi bản sai.
export PATH="$(dirname "$NODE"):$PATH"
if [ -n "$NODE_GOC" ] && [ "$NODE_GOC" != "$NODE" ] && ! node_dung "$NODE_GOC"; then
  dong="export PATH=\"$(dirname "$NODE"):\$PATH\"   # Node cho bot Zalo (scripts/cai_dat.sh)"
  rc="$HOME/.bashrc"; [ "$(basename "${SHELL:-}")" = zsh ] && rc="$HOME/.zshrc"
  if grep -qF "$(dirname "$NODE")" "$rc" 2>/dev/null; then
    nhac "Shell đang gọi Node sai ($NODE_GOC) — đã có dòng sửa trong $rc, mở lại SSH là xong"
  elif hoi "Shell đang gọi Node sai ($NODE_GOC). Tự thêm một dòng vào $rc để lần sau gọi đúng bản?"; then
    printf '\n%s\n' "$dong" >> "$rc"
    xanh "Đã thêm vào $rc — mở lại SSH để có hiệu lực"
  else
    nhac "Shell đang gọi Node sai ($NODE_GOC). Thêm dòng này vào $rc rồi mở lại SSH:"
    echo "    $dong"
  fi
fi
NPM="$(dirname "$NODE")/npm"
OC="$(dirname "$NODE")/openclaw"

# ── 2. OpenClaw ──────────────────────────────────────────────────────────────
if [ -x "$OC" ] && "$OC" --version 2>/dev/null | grep -q "$OC_BAN"; then
  xanh "OpenClaw $OC_BAN"
else
  echo "  cài openclaw@$OC_BAN (vài phút)…"
  # npm 11 mặc định BỎ QUA script cài đặt của gói. Cho riêng openclaw chạy script
  # của nó (dọn file cũ + đánh dấu đã cài xong); các gói con thì không cần.
  nk="$(mktemp)"
  if ! $CHAY "$NPM" install -g --no-fund --no-audit --loglevel=error \
        --allow-scripts=openclaw "openclaw@$OC_BAN" >"$nk" 2>&1; then
    do_ "Cài OpenClaw lỗi:"; tail -20 "$nk" >&2; exit 1
  fi
  rm -f "$nk"
  "$OC" --version | grep -q "$OC_BAN" || { do_ "Cài OpenClaw không xong"; exit 1; }
  xanh "Đã cài OpenClaw $OC_BAN"
fi

# ── 3. Plugin Zalo ───────────────────────────────────────────────────────────
if "$OC" plugins list --json 2>/dev/null | grep -q "\"zalouser\"" && \
   "$OC" plugins list --json 2>/dev/null | tr -d ' \n' | grep -q "\"id\":\"zalouser\"[^}]*\"version\":\"$OC_BAN\""; then
  xanh "Plugin Zalo $OC_BAN"
else
  echo "  cài plugin @openclaw/zalouser@$OC_BAN…"
  "$OC" plugins install "@openclaw/zalouser@$OC_BAN" >/dev/null
  xanh "Đã cài plugin Zalo $OC_BAN"
fi

# ── 4. Python ────────────────────────────────────────────────────────────────
py_dung() { "$1" -c 'import sys; sys.exit(0 if sys.version_info >= (3, 9) else 1)' 2>/dev/null; }
PY=""
for p in python3 python3.13 python3.12 python3.11 python3.10 python3.9; do
  if command -v "$p" >/dev/null 2>&1 && py_dung "$(command -v "$p")"; then PY="$(command -v "$p")"; break; fi
done
if [ -n "$PY" ]; then
  xanh "Python $("$PY" -c 'import platform; print(platform.python_version())') ($PY)"
  [ "$(basename "$PY")" != python3 ] && nhac "python3 của máy cũ quá — các lệnh sau gõ $(basename "$PY") thay cho python3"
else
  do_ "Chưa có Python 3.9 trở lên. RHEL/Alma 8: sudo dnf install -y python3.11 · Ubuntu/Debian: sudo apt install -y python3"
fi

# ── 5. Swap (máy nhỏ) ────────────────────────────────────────────────────────
if [ "$OS" = linux ] && [ -r /proc/meminfo ]; then
  ram_mb=$(( $(awk '/^MemTotal/ {print $2}' /proc/meminfo) / 1024 ))
  swap_mb=$(( $(awk '/^SwapTotal/ {print $2}' /proc/meminfo) / 1024 ))
  if [ "$ram_mb" -le 1200 ] && [ "$swap_mb" -lt 1000 ]; then
    if hoi "Máy chỉ có ${ram_mb} MB RAM, chưa có swap — thêm 2 GB swap để bot không bị tắt giữa chừng?"; then
      $SUDO fallocate -l 2G /swapfile && $SUDO chmod 600 /swapfile && $SUDO mkswap /swapfile >/dev/null \
        && $SUDO swapon /swapfile && echo '/swapfile none swap sw 0 0' | $SUDO tee -a /etc/fstab >/dev/null
      xanh "Đã thêm 2 GB swap"
    else
      nhac "RAM ${ram_mb} MB, không swap — dễ bị tắt giữa chừng"
    fi
  else
    xanh "RAM ${ram_mb} MB, swap ${swap_mb} MB"
  fi
fi

# ── 6. Múi giờ ───────────────────────────────────────────────────────────────
if command -v timedatectl >/dev/null 2>&1 && tz="$(timedatectl show -p Timezone --value 2>/dev/null)"; then
  if [ "$tz" = "Asia/Ho_Chi_Minh" ]; then
    xanh "Múi giờ $tz"
  elif hoi "Máy đang giờ $tz — đổi sang giờ Việt Nam (giờ trực, follow-up tính theo giờ VN)?"; then
    $SUDO timedatectl set-timezone Asia/Ho_Chi_Minh && xanh "Đã đặt giờ Việt Nam"
  else
    nhac "Múi giờ $tz — giờ trực / follow-up sẽ lệch"
  fi
else
  nhac "Không đổi được múi giờ tự động trên máy này — đặt tay giờ Asia/Ho_Chi_Minh"
fi

command -v git >/dev/null 2>&1 || nhac "Chưa có git — cần để kéo bản template mới (docs/15-cap-nhat.md)"

echo
echo "Xong phần máy. Bước tiếp: $(basename "${PY:-python3}") scripts/bat_dau.py"
