"""Download trip data and station coordinates."""

import zipfile
from concurrent.futures import ThreadPoolExecutor

import pandas as pd
import requests

from src.config import (
    DOWNLOAD_URLS,
    DOWNLOADS_DIR,
    MAX_WORKERS,
    STATION_COORDINATES_FILENAME,
    STATION_COORDINATES_URL,
)


def download_and_extract(url):
    """Download and extract one file."""
    filename = url.split("/")[-1]
    filepath = DOWNLOADS_DIR / filename

    # Download
    print(f"Downloading {filename}...")
    response = requests.get(url, timeout=120)
    with open(filepath, "wb") as f:
        f.write(response.content)

    # Extract - skip __MACOSX
    with zipfile.ZipFile(filepath, "r") as zip_ref:
        members = [m for m in zip_ref.namelist() if not m.startswith("__MACOSX")]
        zip_ref.extractall(DOWNLOADS_DIR, members=members)

    # Delete zip
    filepath.unlink()
    print(f"✓ {filename}")


def download_trip_data():
    """Download all trip files."""
    print("\nDownloading trip data...")

    with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
        executor.map(download_and_extract, DOWNLOAD_URLS)


def download_stations():
    """Download stations."""
    print("\nDownloading stations...")

    df = pd.read_csv(STATION_COORDINATES_URL)
    df = df.dropna(subset=["Latitude", "Longitude"])

    filepath = DOWNLOADS_DIR / STATION_COORDINATES_FILENAME
    df.to_csv(filepath, index=False)

    print(f"✓ {len(df)} stations")


def download_all():
    """Download everything."""
    download_trip_data()
    download_stations()
    print("\n✓ Done!")
