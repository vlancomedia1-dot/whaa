from __future__ import annotations

def is_android() -> bool:
    try:
        import kivy  # noqa: F401
        from kivy.utils import platform
        return platform == "android"
    except Exception:
        return False

def open_url(url: str) -> None:
    """Open URL in platform-appropriate way."""
    if is_android():
        try:
            from jnius import autoclass  # type: ignore
            PythonActivity = autoclass("org.kivy.android.PythonActivity")
            Intent = autoclass("android.content.Intent")
            Uri = autoclass("android.net.Uri")

            activity = PythonActivity.mActivity
            intent = Intent(Intent.ACTION_VIEW, Uri.parse(url))
            activity.startActivity(intent)
            return
        except Exception:
            # Fallback to webbrowser below
            pass

    import webbrowser
    webbrowser.open(url)
