from asgiref.local import Local
from django.conf import settings
from django.utils.translation import gettext_lazy as _, ngettext
from django_salmon.signals import observe_cache_operation

from debug_toolbar.panels import Panel
from debug_toolbar.utils import get_stack_trace, render_stacktrace

# The order of the methods in this list determines the order in which they are listed in
# the Commands table in the panel content.
WRAPPED_CACHE_METHODS = [
    "add",
    "get",
    "set",
    "get_or_set",
    "touch",
    "delete",
    "clear",
    "get_many",
    "set_many",
    "delete_many",
    "has_key",
    "incr",
    "decr",
    "incr_version",
    "decr_version",
]


def _handle_cache_signal(
    sender, instance=None, function_name=None, args=(), time=0, result=None, **extra
):
    panel = CachePanel.current_instance()
    if panel is None or getattr(instance, "_djdt_panel", None) is False:
        return
    alias = getattr(instance, "alias", "unknown")
    panel._store_call_info(
        name=function_name,
        time_taken=time,
        return_value=result,
        args=args,
        kwargs=extra.get("kwargs", {}),
        trace=get_stack_trace(),
        backend=f"{alias} ({sender.__name__})",
    )


class CachePanel(Panel):
    """
    Panel that displays the cache statistics.
    """

    template = "debug_toolbar/panels/cache.html"

    is_async = True

    _context_locals = Local()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.total_time = 0
        self.hits = 0
        self.misses = 0
        self.calls = []
        self.counts = dict.fromkeys(WRAPPED_CACHE_METHODS, 0)

    @classmethod
    def current_instance(cls):
        """
        Return the currently enabled CachePanel instance or None.

        If a request is in process with a CachePanel enabled, this will return that
        panel (based on the current thread or async task).  Otherwise it will return
        None.
        """
        return getattr(cls._context_locals, "current_instance", None)

    @classmethod
    def ready(cls):
        observe_cache_operation.connect(
            _handle_cache_signal, dispatch_uid="djdt_cache_panel"
        )

    def _store_call_info(
        self, name, time_taken, return_value, args, kwargs, trace, backend
    ):
        if name == "get" or name == "get_or_set":
            if return_value is None:
                self.misses += 1
            else:
                self.hits += 1
        elif name == "get_many":
            keys = kwargs["keys"] if "keys" in kwargs else args[0]
            self.hits += len(return_value)
            self.misses += len(keys) - len(return_value)
        self.total_time += time_taken
        self.counts[name] += 1
        self.calls.append(
            {
                "time": time_taken,
                "name": name,
                "args": args,
                "kwargs": kwargs,
                "trace": render_stacktrace(trace),
                "backend": backend,
            }
        )

    # Implement the Panel API

    nav_title = _("Cache")

    @property
    def nav_subtitle(self):
        stats = self.get_stats()
        cache_calls = len(stats.get("calls"))
        return ngettext(
            "%(cache_calls)d call in %(time).2fms",
            "%(cache_calls)d calls in %(time).2fms",
            cache_calls,
        ) % {"cache_calls": cache_calls, "time": stats.get("total_time")}

    @property
    def title(self):
        count = self.get_stats().get("total_caches")
        return ngettext(
            "Cache calls from %(count)d backend",
            "Cache calls from %(count)d backends",
            count,
        ) % {"count": count}

    def enable_instrumentation(self):
        self._context_locals.current_instance = self

    def disable_instrumentation(self):
        if hasattr(self._context_locals, "current_instance"):
            del self._context_locals.current_instance

    def generate_stats(self, request, response):
        self.record_stats(
            {
                "total_calls": len(self.calls),
                "calls": self.calls,
                "total_time": self.total_time,
                "hits": self.hits,
                "misses": self.misses,
                "counts": self.counts,
                "total_caches": len(getattr(settings, "CACHES", ["default"])),
            }
        )

    def generate_server_timing(self, request, response):
        stats = self.get_stats()
        value = stats.get("total_time", 0)
        title = "Cache {} Calls".format(stats.get("total_calls", 0))
        self.record_server_timing("total_time", title, value)
