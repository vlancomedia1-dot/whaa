#!/usr/bin/env bash
set -euo pipefail
# Ensure you configured signing in buildozer.spec before release build
buildozer android release aab
echo "AAB generated under ./bin/"
