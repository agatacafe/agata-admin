"""Offline behavior checks; invented URLs only, no network calls."""

import os
from pathlib import Path
import unittest
from unittest.mock import patch

from streamlit.testing.v1 import AppTest

from app import DEFAULT_URLS, SERVICES
from scripts.brand import brand_kit
from scripts.portal_config import valid_app_url

APP = str(Path(__file__).resolve().parents[1] / "app.py")
BLANK = {service.setting: "" for service in SERVICES}


class PortalTests(unittest.TestCase):
    def run_app(self, **settings):
        with patch.dict(os.environ, {**BLANK, **settings}):
            return AppTest.from_file(APP, default_timeout=30).run()

    def test_starts_without_secrets(self):
        app = self.run_app()
        self.assertFalse(app.exception)
        self.assertEqual(app.title[0].value, "Ágata café: administration")
        self.assertEqual([s.value for s in app.subheader[:4]], [s.title for s in SERVICES])
        # Only the confirmed Sales deployment is linked; the others wait for their URLs.
        self.assertEqual([(l.proto.label, l.proto.url) for l in app.get("link_button")],
                         [("Open Sales", DEFAULT_URLS["SALES_APP_URL"])])
        self.assertEqual([b.label for b in app.button if b.disabled],
                         ["Open Inventory", "Open Reconciliation", "Open Equity and contributions"])

    def test_invalid_override_disables_sales_only(self):
        app = self.run_app(SALES_APP_URL="javascript:alert(1)")
        self.assertFalse(app.exception)
        self.assertFalse(app.get("link_button"))

    def test_configured_url_enables_only_its_card(self):
        app = self.run_app(SALES_APP_URL="https://sales.example.com/", INVENTORY_APP_URL="javascript:alert(1)")
        self.assertFalse(app.exception)
        links = app.get("link_button")
        self.assertEqual([(l.proto.label, l.proto.url) for l in links],
                         [("Open Sales", "https://sales.example.com/")])

    def test_rejects_unsafe_urls(self):
        for value in ("javascript:alert(1)", "https://user:pw@example.com", "//example.com", ""):
            self.assertIsNone(valid_app_url(value))

    def test_brand_kit_contains_logos(self):
        import io, zipfile
        names = zipfile.ZipFile(io.BytesIO(brand_kit())).namelist()
        for name in ("agata-bean.svg", "agata-bean-olive.svg", "agata-bean-cream.svg", "guide.json", "reference/wordmark.png"):
            self.assertIn(name, names)


if __name__ == "__main__":
    unittest.main()
