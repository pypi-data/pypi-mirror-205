try:
    from wagtail import hooks
except ImportError:
    from wagtail.core import hooks


__all__ = [
    "hooks",
]
