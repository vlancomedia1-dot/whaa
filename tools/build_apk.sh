#!/usr/bin/env bash
set -euo pipefail
buildozer android debug
echo "APK generated under ./bin/"
