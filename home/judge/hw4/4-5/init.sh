#!/usr/bin/env bash
BASEDIR="$(dirname -- "${BASH_SOURCE[0]}")"
cd "$BASEDIR" || return
python3 -m pip install -r src/requirements.txt
