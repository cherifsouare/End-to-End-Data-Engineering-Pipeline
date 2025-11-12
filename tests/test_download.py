"""Test download module."""

import re

from src.download import DOWNLOAD_URLS


def test_all_urls_use_https():
    """All URLs should use HTTPS."""
    for url in DOWNLOAD_URLS:
        assert url.startswith("https://")


def test_all_urls_are_zip_files():
    """All URLs should be ZIP files."""
    for url in DOWNLOAD_URLS:
        assert url.endswith(".zip")


def test_all_urls_have_reasonable_year():
    """All URLs should have reasonable year (2013-2025)."""
    for url in DOWNLOAD_URLS:
        match = re.search(r"(\d{4})", url)
        assert match, f"No 4-digit year found in: {url}"

        year = int(match.group(1))
        assert 2013 <= year <= 2025, f"Year {year} out of range in: {url}"
