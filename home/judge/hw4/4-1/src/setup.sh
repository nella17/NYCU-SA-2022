#!/usr/bin/env bash

DOMAIN="${1?domain}"
CONFIG="${2?config}"
STATIC="${3?static}"

acme.sh \
  --server 'https://ca.nasa.nycu:9000/acme/acme/directory' \
  --ca-path '/etc/ssl/certs' \
  --force \
  --issue -d "$DOMAIN" \
  --standalone \
  --cert-file "$CONFIG/cert.cer" \
  --key-file "$CONFIG/cert.key" \
  --ca-file "$CONFIG/ca.cer" \
  --fullchain-file "$CONFIG/fullchain.cer"

sed -i '' \
  -e "s|domain|$DOMAIN|g" \
  -e "s|static|$STATIC|g" \
  -e "s|config|$CONFIG|g" \
  "$CONFIG/Caddyfile"
