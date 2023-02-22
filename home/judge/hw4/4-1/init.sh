#!/usr/bin/env bash
BASEDIR="$(dirname -- "${BASH_SOURCE[0]}")"
cd "$BASEDIR" || return
sudo pkg install -y acme.sh caddy rust
sudo sysctl net.inet.ip.portrange.reservedhigh=0
python3 -m pip install -r src/requirements.txt
