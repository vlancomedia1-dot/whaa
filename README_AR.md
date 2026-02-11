# WhatsPromo Python (قالب جاهز) + أداة بناء APK/AAB

هذا مشروع بايثون مبني على **Kivy** ويعمل على:
- **الكمبيوتر** (Windows/Linux/macOS) للتجربة السريعة.
- **أندرويد** عبر **Buildozer** لإخراج **APK** أو **AAB** بسهولة.

> الهدف: تعطيك قاعدة جاهزة تشبه تطبيقات التسويق/الإرسال (استيراد أرقام من CSV + إنشاء رابط واتساب لكل رقم)، مع سكربتات بناء جاهزة.

---

## 1) تشغيله على الكمبيوتر (للتأكد أنه يعمل)

### تثبيت المتطلبات
```bash
python -m venv .venv
source .venv/bin/activate   # على ويندوز: .venv\Scripts\activate
pip install -r requirements.txt
```

### تشغيل
```bash
python main.py
```

---

## 2) بناء APK / AAB (Android)

### المتطلبات (لينكس/WSL هو الأسهل)
- Python 3.10+
- Java (OpenJDK 17 غالباً مناسب)
- Buildozer
- Android SDK/NDK (Buildozer يثبت كثير من الأشياء تلقائياً)

### تثبيت Buildozer
```bash
pip install --upgrade pip
pip install buildozer
```

### تهيئة أول مرة
```bash
buildozer android debug
```
أول بناء قد يأخذ وقت لأنه يحمّل SDK/NDK و Python-for-Android.

### إخراج APK (Debug)
```bash
bash tools/build_apk.sh
```
ستجد الملف في:
`bin/`

### إخراج AAB (Release)
1) جهّز keystore (مرة واحدة):
```bash
bash tools/create_keystore.sh
```
2) ابنِ AAB:
```bash
bash tools/build_aab.sh
```

> ملاحظة: سكربتات `*.sh` تعمل على Linux/WSL. على ويندوز بدون WSL استخدم `tools\build_apk.bat`.

---

## 3) ماذا يفعل التطبيق؟

- شاشة: استيراد CSV (عمود: `phone` أو `number`)
- كتابة رسالة
- إنشاء قائمة أرقام
- زر "فتح واتساب" يفتح المحادثة لكل رقم (على الكمبيوتر يفتح WhatsApp Web، وعلى أندرويد يفتح تطبيق واتساب إن وجد).

---

## 4) تخصيص سريع
- الاسم/الأيقونة/النسخة: في `buildozer.spec`
- الألوان والنصوص: في `app/ui.py`
- منطق CSV: في `app/contacts.py`

---

## 5) استكشاف أخطاء
- إذا فشل بناء أندرويد، شغّل:
```bash
buildozer -v android debug
```
ثم شاركني الخطأ.
