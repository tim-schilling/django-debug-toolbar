"""
The main DebugToolbar class that loads and renders the Toolbar.
"""

import uuid
from collections import OrderedDict
from functools import lru_cache

from django.apps import apps
from django.core.exceptions import ImproperlyConfigured
from django.template import TemplateSyntaxError
from django.template.loader import render_to_string
from django.urls import path
from django.utils.module_loading import import_string

from debug_toolbar import settings as dt_settings


@lru_cache()
def get_store_class():
    # If SHOW_TOOLBAR_CALLBACK is a string, which is the recommended
    # setup, resolve it to the corresponding callable.
    class_or_path = dt_settings.get_config()["STORE_CLASS"]
    if isinstance(class_or_path, str):
        return import_string(class_or_path)
    else:
        return class_or_path


class DebugToolbar:
    def __init__(self, request, get_response, panel_classes=None):
        self.request = request
        self.config = dt_settings.get_config().copy()
        panels = []
        if not panel_classes:
            for panel_class in reversed(self.get_panel_classes()):
                panel = panel_class(self, get_response)
                panels.append(panel)
                if panel.enabled:
                    get_response = panel.process_request
        else:
            for panel_class in panel_classes:
                panel = panel_class(self, get_response)
                panels.append(panel)
        self.process_request = get_response
        self._panels = OrderedDict()
        while panels:
            panel = panels.pop()
            self._panels[panel.panel_id] = panel
        self.stats = {}
        self.server_timing_stats = {}
        self.store_id = None

    # Manage panels

    @property
    def panels(self):
        """
        Get a list of all available panels.
        """
        return list(self._panels.values())

    @property
    def enabled_panels(self):
        """
        Get a list of panels enabled for the current request.
        """
        return [panel for panel in self._panels.values() if panel.enabled]

    def get_panel_by_id(self, panel_id):
        """
        Get the panel with the given id, which is the class name by default.
        """
        return self._panels[panel_id]

    # Handle rendering the toolbar in HTML

    def render_toolbar(self):
        """
        Renders the overall Toolbar with panels inside.
        """
        if not self.should_render_panels():
            # Store already exists.
            if not self.store_id:
                self.store_id = uuid.uuid4().hex
            self.store.store(self.store_id, self)
        try:
            context = {"toolbar": self}
            return render_to_string("debug_toolbar/base.html", context)
        except TemplateSyntaxError:
            if not apps.is_installed("django.contrib.staticfiles"):
                raise ImproperlyConfigured(
                    "The debug toolbar requires the staticfiles contrib app. "
                    "Add 'django.contrib.staticfiles' to INSTALLED_APPS and "
                    "define STATIC_URL in your settings."
                )
            else:
                raise

    def should_render_panels(self):
        render_panels = self.config["RENDER_PANELS"]
        if render_panels is None:
            render_panels = self.request.META["wsgi.multiprocess"]
        return render_panels

    # Handle storing toolbars in memory and fetching them later on
    store = get_store_class()()

    # Manually implement class-level caching of panel classes and url patterns
    # because it's more obvious than going through an abstraction.

    _panel_classes = None

    @classmethod
    def get_panel_classes(cls):
        if cls._panel_classes is None:
            # Load panels in a temporary variable for thread safety.
            panel_classes = [
                import_string(panel_path) for panel_path in dt_settings.get_panels()
            ]
            cls._panel_classes = panel_classes
        return cls._panel_classes

    _urlpatterns = None

    @classmethod
    def get_urls(cls):
        if cls._urlpatterns is None:
            from . import views

            # Load URLs in a temporary variable for thread safety.
            # Global URLs
            urlpatterns = [
                path("render_panel/", views.render_panel, name="render_panel")
            ]
            # Per-panel URLs
            for panel_class in cls.get_panel_classes():
                urlpatterns += panel_class.get_urls()
            cls._urlpatterns = urlpatterns
        return cls._urlpatterns


app_name = "djdt"
urlpatterns = DebugToolbar.get_urls()
