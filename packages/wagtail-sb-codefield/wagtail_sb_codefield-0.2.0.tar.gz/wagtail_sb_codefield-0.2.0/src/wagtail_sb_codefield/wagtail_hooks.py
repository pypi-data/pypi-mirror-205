from django.templatetags.static import static
from django.utils.html import format_html
from wagtail import hooks


@hooks.register("insert_editor_css", order=1)
def codeeditor_css():
    return format_html(
        '<link rel="stylesheet" href="{}">',
        static("wagtail_sb_codefield/css/codefield_wagtail_admin.css"),
    )
