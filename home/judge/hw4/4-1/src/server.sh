#!/usr/bin/env bash

BASEDIR="$(dirname -- "${BASH_SOURCE[0]}")"
CONFIG="${1?config}"

leave() {
  exit
}
cleanup() {
  for pid in $(jobs -p)
  do
    timeout 1 kill "$pid" &
  done
  wait
  for pid in $(jobs -p)
  do
    kill -9 "$pid" &
  done
  wait
  exit
}
trap leave INT
trap cleanup EXIT

caddy run --config "$CONFIG/Caddyfile" &
"$BASEDIR/server.py" "$@"
wait
