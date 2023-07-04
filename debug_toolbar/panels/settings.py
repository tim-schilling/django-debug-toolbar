from django.conf import settings
from django.utils.translation import gettext_lazy as _
from django.views.debug import get_default_exception_reporter_filter

from debug_toolbar.panels import Panel
from debug_toolbar.utils import pprint

get_safe_settings = get_default_exception_reporter_filter().get_safe_settings


class SettingsPanel(Panel):
    """
    A panel to display all variables in django.conf.settings
    """

    template = "debug_toolbar/panels/settings.html"

    nav_title = _("Settings")

    def title(self):
        return _("Settings from %s") % settings.SETTINGS_MODULE

    def generate_stats(self, request, response):
        self.record_stats(
            {
                "settings": [
                    (key, pprint(value))
                    for key, value in sorted(get_safe_settings().items())
                ]
            }
        )
