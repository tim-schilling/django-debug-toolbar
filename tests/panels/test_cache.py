from django.core import cache
from django_salmon.signals import observe_cache_operation

from debug_toolbar.panels.cache import CachePanel

from ..base import BaseTestCase


class CachePanelTestCase(BaseTestCase):
    panel_id = CachePanel.panel_id

    def test_recording(self):
        self.assertEqual(len(self.panel.calls), 0)
        cache.cache.set("foo", "bar")
        cache.cache.get("foo")
        cache.cache.delete("foo")
        self.assertFalse(cache.cache.touch("foo"))
        cache.cache.set("foo", "bar")
        self.assertTrue(cache.cache.touch("foo"))
        # Verify that the cache has a valid clear method.
        cache.cache.clear()
        self.assertEqual(len(self.panel.calls), 7)

    def test_recording_caches(self):
        self.assertEqual(len(self.panel.calls), 0)
        default_cache = cache.caches[cache.DEFAULT_CACHE_ALIAS]
        second_cache = cache.caches["second"]
        default_cache.set("foo", "bar")
        second_cache.get("foo")
        self.assertEqual(len(self.panel.calls), 2)

    def test_hits_and_misses(self):
        cache.cache.clear()
        cache.cache.get("foo")
        self.assertEqual(self.panel.hits, 0)
        self.assertEqual(self.panel.misses, 1)
        cache.cache.set("foo", 1)
        cache.cache.get("foo")
        self.assertEqual(self.panel.hits, 1)
        self.assertEqual(self.panel.misses, 1)
        cache.cache.get_many(["foo", "bar"])
        self.assertEqual(self.panel.hits, 2)
        self.assertEqual(self.panel.misses, 2)
        cache.cache.set("bar", 2)
        cache.cache.get_many(keys=["foo", "bar"])
        self.assertEqual(self.panel.hits, 4)
        self.assertEqual(self.panel.misses, 2)

    def test_get_or_set_value(self):
        cache.cache.get_or_set("baz", "val")
        self.assertEqual(cache.cache.get("baz"), "val")
        calls = [
            (call["name"], call["args"], call["kwargs"]) for call in self.panel.calls
        ]
        self.assertEqual(
            calls,
            [
                ("get_or_set", ("baz", "val"), {}),
                ("get", ("baz",), {}),
            ],
        )
        self.assertEqual(
            self.panel.counts,
            {
                "add": 0,
                "get": 1,
                "set": 0,
                "get_or_set": 1,
                "touch": 0,
                "delete": 0,
                "clear": 0,
                "get_many": 0,
                "set_many": 0,
                "delete_many": 0,
                "has_key": 0,
                "incr": 0,
                "decr": 0,
                "incr_version": 0,
                "decr_version": 0,
            },
        )

    def test_get_or_set_does_not_override_existing_value(self):
        cache.cache.set("foo", "bar")
        cached_value = cache.cache.get_or_set("foo", "other")
        self.assertEqual(cached_value, "bar")
        calls = [
            (call["name"], call["args"], call["kwargs"]) for call in self.panel.calls
        ]
        self.assertEqual(
            calls,
            [
                ("set", ("foo", "bar"), {}),
                ("get_or_set", ("foo", "other"), {}),
            ],
        )
        self.assertEqual(
            self.panel.counts,
            {
                "add": 0,
                "get": 0,
                "set": 1,
                "get_or_set": 1,
                "touch": 0,
                "delete": 0,
                "clear": 0,
                "get_many": 0,
                "set_many": 0,
                "delete_many": 0,
                "has_key": 0,
                "incr": 0,
                "decr": 0,
                "incr_version": 0,
                "decr_version": 0,
            },
        )

    def test_insert_content(self):
        """
        Test that the panel only inserts content after generate_stats and
        not the process_request.
        """
        cache.cache.get("café")
        response = self.panel.process_request(self.request)
        # ensure the panel does not have content yet.
        self.assertNotIn("café", self.panel.content)
        self.panel.generate_stats(self.request, response)
        self.reload_stats()
        # ensure the panel renders correctly.
        content = self.panel.content
        self.assertIn("café", content)
        self.assertValidHTML(content)
        # ensure traces aren't escaped
        self.assertIn('<span class="djdt-path">', content)

    def test_generate_server_timing(self):
        self.assertEqual(len(self.panel.calls), 0)
        cache.cache.set("foo", "bar")
        cache.cache.get("foo")
        cache.cache.delete("foo")

        self.assertEqual(len(self.panel.calls), 3)

        response = self.panel.process_request(self.request)
        self.panel.generate_stats(self.request, response)
        self.panel.generate_server_timing(self.request, response)

        stats = self.panel.get_stats()

        expected_data = {
            "total_time": {
                "title": "Cache {} Calls".format(stats["total_calls"]),
                "value": stats["total_time"],
            }
        }

        self.assertEqual(self.panel.get_server_timing_stats(), expected_data)

    def test_backend_alias_is_recorded(self):
        cache.cache.get("foo")
        self.assertEqual(self.panel.calls[0]["backend"], "default (LocMemCache)")

    def test_signal_connected_once(self):
        """
        Confirm that calling ready() multiple times only connects the signal handler once.
        """
        CachePanel.ready()
        CachePanel.ready()
        matching = [
            dispatch_uid
            for (dispatch_uid, _mem_id), *_args in observe_cache_operation.receivers
        ]
        self.assertListEqual(matching, ["djdt_cache_panel"])

    def test_enable_disable_sets_removes_current_instance(self):
        """
        Confirm that repeated enable/disable cycles sets and removes current_instance property.
        """
        self.panel.enable_instrumentation()
        self.assertIsNotNone(self.panel.current_instance())
        self.panel.disable_instrumentation()
        self.assertIsNone(self.panel.current_instance())
