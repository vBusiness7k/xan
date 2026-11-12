#!/usr/bin/env bash
set -euo pipefail
if [[ "${1:-}" == "smoke" ]]; then
  fail=0
  while read -r b; do
    [[ "$b" =~ ^#|^$ ]] && continue
    command -v "$b" >/dev/null || { echo "MISSING $b"; fail=1; }
  done < /usr/local/share/tools.list
  [[ -s /usr/share/seclists/Discovery/Web-Content/common.txt ]] || { echo "MISSING wordlist"; fail=1; }
  exit $fail
fi
exec "$@"
