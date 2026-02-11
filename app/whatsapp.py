from __future__ import annotations
import urllib.parse

def whatsapp_chat_url(phone: str, message: str) -> str:
    """Creates WhatsApp deep link. Works for WhatsApp app on Android and WhatsApp Web on desktop."""
    # wa.me expects digits only (no +). We'll strip non-digits.
    digits = "".join([c for c in phone if c.isdigit()])
    text = urllib.parse.quote(message or "")
    return f"https://wa.me/{digits}?text={text}"
