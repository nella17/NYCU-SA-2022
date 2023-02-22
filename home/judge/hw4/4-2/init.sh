#!/usr/bin/env bash
BASEDIR="$(dirname -- "${BASH_SOURCE[0]}")"
cd "$BASEDIR" || return
sudo pkg install -y acme.sh caddy
sudo sysctl net.inet.ip.portrange.reservedhigh=0
