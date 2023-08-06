from django.utils.translation import gettext_lazy as _
from django_sb_codefield.fields import CodeField as BaseCodeField

CodemirrorDefaultOptions = {
    "theme": "monokai",
    "lineNumbers": True,
}


class CodeField(BaseCodeField):
    description = _("Code")

    def _get_code_mirror_editor_kwargs(self):
        code_mirror_editor_kwargs = super()._get_code_mirror_editor_kwargs()
        code_mirror_editor_kwargs[
            "script_template"
        ] = "wagtail_sb_codefield/wagtail_tabbed_interface_script.html"

        return code_mirror_editor_kwargs
