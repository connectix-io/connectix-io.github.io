#!/usr/bin/env bash
# Checks every local href/src in the site's HTML points at a file that exists.
# External links (http, https, mailto) and in-page anchors are skipped.
#
#     scripts/check-links.sh
set -euo pipefail
cd "$(dirname "$0")/.."

status=0
for page in *.html; do
  grep -oE '(href|src)="[^"]+"' "$page" | sed -E 's/^(href|src)="//; s/"$//' | sort -u | while read -r ref; do
    case "$ref" in
      http://*|https://*|mailto:*|\#*|data:*) continue ;;
    esac
    path="${ref%%#*}"
    path="${path%%\?*}"
    if [ ! -f "$path" ]; then
      echo "$page: missing $ref"
      exit 1
    fi
  done || status=1
done

if [ "$status" -eq 0 ]; then
  echo "all local links and assets resolve"
fi
exit "$status"
