from __future__ import annotations

from kivy.app import App
from kivy.lang import Builder
from kivy.properties import StringProperty, ListProperty
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.clock import Clock

from .contacts import load_contacts_from_csv, Contact
from .platform import open_url
from .whatsapp import whatsapp_chat_url

KV = r'''
#:kivy 2.3.0

<Root>:
    HomeScreen:
    ImportScreen:
    SendScreen:

<HomeScreen>:
    name: "home"
    BoxLayout:
        orientation: "vertical"
        padding: dp(16)
        spacing: dp(12)

        Label:
            text: "WhatsPromo (Python)"
            font_size: "22sp"
            size_hint_y: None
            height: self.texture_size[1] + dp(8)

        Label:
            text: "استيراد أرقام من CSV + إرسال رسالة عبر واتساب"
            halign: "right"
            text_size: self.size
        Widget:

        Button:
            text: "استيراد CSV"
            size_hint_y: None
            height: dp(44)
            on_release: app.root.current = "import"

        Button:
            text: "ابدأ الإرسال"
            size_hint_y: None
            height: dp(44)
            on_release: app.root.current = "send"

        Label:
            text: app.status_text
            color: (0.2, 0.6, 0.2, 1)
            halign: "right"
            text_size: self.size
            size_hint_y: None
            height: self.texture_size[1] + dp(8)

<ImportScreen>:
    name: "import"
    BoxLayout:
        orientation: "vertical"
        padding: dp(16)
        spacing: dp(10)

        Label:
            text: "استيراد CSV"
            font_size: "20sp"
            size_hint_y: None
            height: self.texture_size[1] + dp(8)

        TextInput:
            id: path_in
            hint_text: "مسار ملف CSV (مثال: /sdcard/Download/contacts.csv)"
            multiline: False

        Button:
            text: "تحميل"
            size_hint_y: None
            height: dp(44)
            on_release: app.load_csv(path_in.text)

        Label:
            text: app.import_result
            halign: "right"
            text_size: self.size

        BoxLayout:
            size_hint_y: None
            height: dp(44)
            spacing: dp(10)
            Button:
                text: "رجوع"
                on_release: app.root.current = "home"
            Button:
                text: "انتقال للإرسال"
                on_release: app.root.current = "send"

<SendScreen>:
    name: "send"
    BoxLayout:
        orientation: "vertical"
        padding: dp(16)
        spacing: dp(10)

        Label:
            text: "إرسال عبر واتساب"
            font_size: "20sp"
            size_hint_y: None
            height: self.texture_size[1] + dp(8)

        TextInput:
            id: msg_in
            hint_text: "اكتب الرسالة هنا"
            text: app.message_text
            on_text: app.message_text = self.text

        Label:
            text: "عدد الأرقام: " + str(len(app.phones))
            halign: "right"
            text_size: self.size
            size_hint_y: None
            height: self.texture_size[1] + dp(8)

        ScrollView:
            GridLayout:
                cols: 1
                size_hint_y: None
                height: self.minimum_height
                spacing: dp(6)
                padding: dp(2)
                canvas.before:
                    Color:
                        rgba: (0.95,0.95,0.95,1)
                    Rectangle:
                        pos: self.pos
                        size: self.size

                Label:
                    text: "\n".join(app.phones[:50]) + ("\n..." if len(app.phones) > 50 else "")
                    halign: "left"
                    valign: "top"
                    text_size: self.width, None
                    size_hint_y: None
                    height: self.texture_size[1] + dp(10)
                    color: (0,0,0,1)

        BoxLayout:
            size_hint_y: None
            height: dp(44)
            spacing: dp(10)
            Button:
                text: "فتح واتساب لأول رقم"
                on_release: app.open_first()

            Button:
                text: "فتح واتساب للجميع (واحد واحد)"
                on_release: app.open_all()

        Button:
            text: "رجوع"
            size_hint_y: None
            height: dp(44)
            on_release: app.root.current = "home"
'''

class HomeScreen(Screen):
    pass

class ImportScreen(Screen):
    pass

class SendScreen(Screen):
    pass

class Root(ScreenManager):
    pass

class WhatsPromoApp(App):
    status_text = StringProperty("")
    import_result = StringProperty("")
    message_text = StringProperty("مرحباً! هذا نموذج رسالة تجريبية.")
    phones = ListProperty([])  # list[str]

    def build(self):
        return Builder.load_string(KV)

    def load_csv(self, path: str):
        contacts, errors = load_contacts_from_csv(path)
        self.phones = [c.phone for c in contacts]
        msg = []
        msg.append(f"تم تحميل: {len(self.phones)} رقم")
        if errors:
            msg.append("أخطاء:")
            msg.extend(errors[:10])
            if len(errors) > 10:
                msg.append("...")
        self.import_result = "\n".join(msg)
        self.status_text = f"جاهز: {len(self.phones)} رقم"

    def open_first(self):
        if not self.phones:
            self.status_text = "لا توجد أرقام. استورد CSV أولاً."
            return
        url = whatsapp_chat_url(self.phones[0], self.message_text)
        open_url(url)
        self.status_text = f"تم فتح واتساب للرقم: {self.phones[0]}"

    def open_all(self):
        if not self.phones:
            self.status_text = "لا توجد أرقام. استورد CSV أولاً."
            return
        # Open sequentially with a small delay to avoid freezing UI
        self._open_queue = list(self.phones)
        self.status_text = "بدء الفتح المتسلسل..."
        Clock.schedule_once(self._open_next, 0.2)

    def _open_next(self, *_):
        if not getattr(self, "_open_queue", []):
            self.status_text = "انتهى."
            return
        phone = self._open_queue.pop(0)
        url = whatsapp_chat_url(phone, self.message_text)
        open_url(url)
        self.status_text = f"فتح: {phone} (متبقي {len(self._open_queue)})"
        Clock.schedule_once(self._open_next, 0.8)
