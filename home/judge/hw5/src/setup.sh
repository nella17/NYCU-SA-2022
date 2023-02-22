#!/usr/bin/env bash

CONFIG="${1?config}"
STATIC="${2?static}"

sed -i '' \
  -e "s|static|$STATIC|g" \
  -e "s|config|$CONFIG|g" \
  "$CONFIG/Caddyfile"
