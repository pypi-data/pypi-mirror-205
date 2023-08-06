from django.utils.html import format_html
from wagtail import hooks
from wagtail.contrib.modeladmin.options import ModelAdmin, modeladmin_register

from .cache import get_cached_active_theme, set_cached_active_theme
from .models import Theme


class ThemeAdmin(ModelAdmin):
    model = Theme
    menu_label = "Themes"
    menu_icon = "fa-paint-brush"
    add_to_settings_menu = True
    exclude_from_explorer = False
    list_display = ("name", "active")
    list_filter = ("active",)
    search_fields = ("name",)


modeladmin_register(ThemeAdmin)


@hooks.register("insert_global_admin_css")
def global_admin_css():
    theme = get_cached_active_theme()
    if not theme:
        theme = Theme.get_active_theme()
        set_cached_active_theme(theme)

    return format_html("<style>{}</style>", theme.css_styles)
