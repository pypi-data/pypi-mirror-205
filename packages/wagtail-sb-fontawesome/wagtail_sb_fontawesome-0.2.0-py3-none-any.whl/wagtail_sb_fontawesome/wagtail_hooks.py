from django.templatetags.static import static
from django.utils.html import format_html

from .compat import hooks


@hooks.register("insert_global_admin_css")
def fontawesome_css():
    return format_html(
        '<link rel="stylesheet" href="{}">',
        static("fontawsome/css/font-awesome.min.css"),
    )
