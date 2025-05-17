#!/usr/bin/env bash
set -euo pipefail

USER_AGENT_HEADER='User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:131.0) Gecko/20100101 Firefox/131.0'

SHEET_URL=$(curl -sL 'https://forger.tall-tales.info/' \
  -H "$USER_AGENT_HEADER" \
  | grep "const SHEET_URL" \
  | sed -E "s/.*'(https:[^']+)'.*/\1/")

if [ -z "$SHEET_URL" ]; then
  printf "No SHEET_URL found\n" >&2
  exit 1
fi
printf "SHEET_URL: %s\n" "$SHEET_URL"

mkdir -p daily-scrape
outfile="daily-scrape/$(date +"%Y-%m-%d").json"

if ! curl -sL "$SHEET_URL" \
  -H "$USER_AGENT_HEADER" \
  | jq > "$outfile"; then
  printf "Failed to scrape %s\n" "$SHEET_URL" >&2
  exit 1
fi
printf "Saved data to \"%s\"\n" "$outfile"
