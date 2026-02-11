#!/usr/bin/env bash
set -euo pipefail
mkdir -p tools
KEYSTORE="tools/release.keystore"
if [ -f "$KEYSTORE" ]; then
  echo "Keystore already exists: $KEYSTORE"
  exit 0
fi
# Change passwords/alias as you like
keytool -genkeypair -v \
  -keystore "$KEYSTORE" \
  -alias release \
  -keyalg RSA -keysize 2048 -validity 10000 \
  -storepass changeit -keypass changeit \
  -dname "CN=WhatsPromoPy, OU=Dev, O=Dev, L=Riyadh, S=Riyadh, C=SA"
echo "Created $KEYSTORE (password: changeit, alias: release)"
echo "Now update buildozer.spec android.release_* fields."
