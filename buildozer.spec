[app]
title = WhatsPromoPy
package.name = whatspromopy
package.domain = org.example
source.dir = .
source.include_exts = py,kv,png,jpg,ttf,md,txt,spec
version = 0.1.0

requirements = python3,kivy

orientation = portrait
fullscreen = 0

android.permissions = INTERNET
# If you want to read files from storage on old Android versions, you may need:
# android.permissions = INTERNET,READ_EXTERNAL_STORAGE

android.api = 33
android.minapi = 24
android.ndk = 25b

android.archs = arm64-v8a,armeabi-v7a

# AAB signing (fill these after creating keystore)
# android.release_keystore = tools/release.keystore
# android.release_keystore_passwd = changeit
# android.release_keyalias = release
# android.release_keyalias_passwd = changeit

[buildozer]
log_level = 2
warn_on_root = 1
