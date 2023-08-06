from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class WagtailSbFontawesomeConfig(AppConfig):
    name = "wagtail_sb_fontawesome"
    verbose_name = _("Wagtail FontAwesome")
    default_auto_field = "django.db.models.BigAutoField"
