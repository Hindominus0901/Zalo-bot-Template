#!/usr/bin/env bash
# Sinh knowledge/wiki/INDEX.md từ frontmatter của các tờ trong wiki/public/.
# Chạy sau mỗi lần thêm / xóa / đổi tên tờ. Sửa số bên trong tờ thì không cần chạy.
set -euo pipefail
cd "$(dirname "$0")/.."
exec python3 scripts/lam_chi_muc.py "$@"
