
from collections import OrderedDict
from django.core.cache import cache

from debug_toolbar import settings as dt_settings


class DebugToolbarStore:

    def __init__(self):
        self.max_cache_size = dt_settings.get_config()["RESULTS_CACHE_SIZE"]

    def store(self, store_id, toolbar):
        raise NotImplementedError

    def all(self):
        raise NotImplementedError

    def clear(self):
        raise NotImplementedError


class MemoryStore(DebugToolbarStore):
    """The default in-memory store for the debug toolbar."""
    def __init__(self):
        super().__init__()
        self._store = OrderedDict()

    def store(self, store_id, toolbar):
        self._store[store_id] = toolbar
        for _ in range(self.max_cache_size, len(self._store)):
            self._store.popitem(last=False)

    def fetch(self, store_id):
        return self._store.get(store_id)

    def all(self):
        return self._store.items()

    def clear(self):
        for key in list(self._store.keys()):
            del self._store[key]


class CacheStore(DebugToolbarStore):
    cache_prefix = "__debug__."
    cache_list_key = cache_prefix + "stores"

    @classmethod
    def serialize_toolbar(cls, toolbar):
        x = {
            "stats": toolbar.stats,
            "server_timing_stats": toolbar.server_timing_stats,
            "enabled_panels": [panel.panel_id for panel in toolbar.panels if panel.enabled]
        }
        print(x)
        return x

    @classmethod
    def deserialize_toolbar(cls, data):
        from debug_toolbar.toolbar import DebugToolbar
        panel_classes = [
            panel_class
            for panel_class in reversed(DebugToolbar.get_panel_classes())
            if str(panel_class.panel_id) in data['enabled_panels']
        ]
        print([str(panel_class.panel_id) for panel_class in DebugToolbar.get_panel_classes()])
        toolbar = DebugToolbar(None, None, panel_classes=panel_classes)
        toolbar.stats = data["stats"]
        toolbar.server_timing_stats = data["server_timing_stats"]
        return toolbar

    @classmethod
    def __store_key(cls, store_id):
        return cls.cache_prefix + store_id

    def store(self, store_id, toolbar):
        # Store already exists.
        existing_keys = cache.get(self.cache_list_key, [])
        key = self.__store_key(store_id)
        cache.set(key, self.serialize_toolbar(toolbar))
        cache.set(self.cache_list_key, [key] + existing_keys[:self.max_cache_size - 1])
        cache.delete_many(existing_keys[self.max_cache_size - 1:])

    def fetch(self, store_id):
        return self.deserialize_toolbar(cache.get(self.__store_key(store_id)))

    def all(self):
        existing_keys = cache.get(self.cache_list_key, [])
        if existing_keys:
            return [
                (cache_key.replace(self.cache_prefix, ''), self.deserialize_toolbar(value))
                for cache_key, value in cache.get_many(existing_keys).items()
            ]
        else:
            return []

    def clear(self):
        existing_keys = cache.get(self.cache_list_key, [])
        if existing_keys:
            cache.delete_many(existing_keys)
