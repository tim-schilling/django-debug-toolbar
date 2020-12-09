from unittest.mock import patch

from django.test import RequestFactory, override_settings
from django.urls import resolve, reverse

from debug_toolbar.panels.history.forms import HistoryStoreForm
from debug_toolbar.toolbar import DebugToolbar

from ..base import BaseTestCase, IntegrationTestCase

rf = RequestFactory()


class HistoryPanelTestCase(BaseTestCase):
    panel_id = "HistoryPanel"

    def test_disabled(self):
        config = {"DISABLE_PANELS": {"debug_toolbar.panels.history.HistoryPanel"}}
        self.assertTrue(self.panel.enabled)
        with self.settings(DEBUG_TOOLBAR_CONFIG=config):
            self.assertFalse(self.panel.enabled)

    def test_post(self):
        self.request = rf.post("/", data={"foo": "bar"})
        response = self.panel.process_request(self.request)
        self.panel.generate_stats(self.request, response)
        data = self.panel.get_stats()["data"]
        self.assertEqual(data["foo"], "bar")

    def test_post_json(self):
        for data, expected_stats_data in (
            ({"foo": "bar"}, {"foo": "bar"}),
            ("", {}),
        ):
            with self.subTest(data=data):
                self.request = rf.post(
                    "/",
                    data=data,
                    content_type="application/json",
                    CONTENT_TYPE="application/json",  # Force django test client to add the content-type even if no data
                )
                response = self.panel.process_request(self.request)
                self.panel.generate_stats(self.request, response)
                data = self.panel.get_stats()["data"]
                self.assertDictEqual(data, expected_stats_data)

    def test_urls(self):
        self.assertEqual(
            reverse("djdt:history_sidebar"),
            "/__debug__/history_sidebar/",
        )
        self.assertEqual(
            resolve("/__debug__/history_sidebar/").url_name,
            "history_sidebar",
        )
        self.assertEqual(
            reverse("djdt:history_refresh"),
            "/__debug__/history_refresh/",
        )
        self.assertEqual(
            resolve("/__debug__/history_refresh/").url_name,
            "history_refresh",
        )


class HistoryViewsTestCase(IntegrationTestCase):
    @override_settings(DEBUG=True)
    def test_history_panel_integration_content(self):
        """Verify the history panel's content renders properly.."""
        self.assertEqual(len(DebugToolbar.store.all()), 0)

        data = {"foo": "bar"}
        self.client.get("/json_view/", data, content_type="application/json")

        # Check the history panel's stats to verify the toolbar rendered properly.
        self.assertEqual(len(DebugToolbar.store.all()), 1)
        toolbar = list(DebugToolbar.store.all())[0][1]
        content = toolbar.get_panel_by_id("HistoryPanel").content
        self.assertIn("bar", content)

    @override_settings(DEBUG=True)
    def test_history_sidebar_invalid(self):
        response = self.client.post(reverse("djdt:history_sidebar"))
        self.assertEqual(response.status_code, 400)

        data = {
            "store_id": "foo",
            "hash": "invalid",
        }
        response = self.client.post(reverse("djdt:history_sidebar"), data=data)
        self.assertEqual(response.status_code, 400)

    @override_settings(DEBUG=True)
    @patch("debug_toolbar.panels.history.views.DebugToolbar.store.fetch")
    def test_history_sidebar_hash(self, fetch):
        """Validate the hashing mechanism."""
        fetch.return_value.panels = []
        data = {
            "store_id": "foo",
            "hash": "3280d66a3cca10098a44907c5a1fd255265eed31",
        }
        response = self.client.post(reverse("djdt:history_sidebar"), data=data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {})

    @override_settings(DEBUG=True)
    def test_history_sidebar(self):
        """Validate the history sidebar view."""
        self.client.get("/json_view/")
        store_id = list(DebugToolbar.store.all())[0][0]
        data = {
            "store_id": store_id,
            "hash": HistoryStoreForm.make_hash({"store_id": store_id}),
        }
        response = self.client.post(reverse("djdt:history_sidebar"), data=data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            set(response.json().keys()),
            {
                "VersionsPanel",
                "TimerPanel",
                "SettingsPanel",
                "HeadersPanel",
                "RequestPanel",
                "SQLPanel",
                "StaticFilesPanel",
                "TemplatesPanel",
                "CachePanel",
                "SignalsPanel",
                "LoggingPanel",
                "ProfilingPanel",
            },
        )

    @override_settings(DEBUG=True)
    def test_history_refresh_invalid(self):
        response = self.client.post(reverse("djdt:history_refresh"))
        self.assertEqual(response.status_code, 400)

        data = {
            "store_id": "foo",
            "hash": "invalid",
        }
        response = self.client.post(reverse("djdt:history_refresh"), data=data)
        self.assertEqual(response.status_code, 400)

    @override_settings(DEBUG=True)
    def test_history_refresh(self):
        """Verify refresh history response has request variables."""
        data = {"foo": "bar"}
        self.client.get("/json_view/", data, content_type="application/json")
        data = {
            "store_id": "foo",
            "hash": "3280d66a3cca10098a44907c5a1fd255265eed31",
        }
        response = self.client.post(reverse("djdt:history_refresh"), data=data)
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(len(data["requests"]), 1)
        for val in ["foo", "bar"]:
            self.assertIn(val, data["requests"][0]["content"])
