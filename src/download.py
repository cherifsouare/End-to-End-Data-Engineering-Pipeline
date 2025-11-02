"""Download trip data and station coordinates."""

import logging
import zipfile
from concurrent.futures import ThreadPoolExecutor

import pandas as pd
import requests

from src.config import DOWNLOADS_DIR

logger = logging.getLogger(__name__)

# specific settings (only used in this module)
MAX_WORKERS = 3

DOWNLOAD_URLS = [
    "https://divvy-tripdata.s3.amazonaws.com/Divvy_Trips_2018_Q4.zip",
    "https://divvy-tripdata.s3.amazonaws.com/Divvy_Trips_2019_Q1.zip",
    "https://divvy-tripdata.s3.amazonaws.com/Divvy_Trips_2019_Q2.zip",
    "https://divvy-tripdata.s3.amazonaws.com/Divvy_Trips_2019_Q3.zip",
    "https://divvy-tripdata.s3.amazonaws.com/Divvy_Trips_2019_Q4.zip",
    "https://divvy-tripdata.s3.amazonaws.com/Divvy_Trips_2020_Q1.zip",
    # "https://divvy-tripdata.s3.amazonaws.com/Divvy_Trips_2220_Q1.zip", --testing bad url
]

STATION_COORDINATES_URL = (
    "https://data.cityofchicago.org/api/views/bbyy-e7gq/rows.csv?accessType=DOWNLOAD"
)
STATION_COORDINATES_FILENAME = "divvy_stations.csv"


def download_and_extract(url):
    """Download and extract one file."""
    filename = url.split("/")[-1]
    filepath = DOWNLOADS_DIR / filename

    logger.info(f"Downloading {filename}")

    try:
        response = requests.get(url, timeout=120)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        logger.error(f"Failed to download {filename}: {e}")
        raise

    with open(filepath, "wb") as f:
        f.write(response.content)

    # Extract (skip __MACOSX junk files)
    with zipfile.ZipFile(filepath, "r") as zip_ref:
        members = [m for m in zip_ref.namelist() if not m.startswith("__MACOSX")]
        zip_ref.extractall(DOWNLOADS_DIR, members=members)

    filepath.unlink()
    logger.info(f"Successfully processed {filename}")


def download_trip_data():
    """Download all trip files in parallel."""
    logger.info("Starting trip data download")

    with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
        list(executor.map(download_and_extract, DOWNLOAD_URLS))

    logger.info("Trip data download complete")


def download_stations():
    """Download station coordinates."""
    logger.info("Downloading station data")

    try:
        df = pd.read_csv(STATION_COORDINATES_URL)
        df = df.dropna(subset=["Latitude", "Longitude"])

        filepath = DOWNLOADS_DIR / STATION_COORDINATES_FILENAME
        df.to_csv(filepath, index=False)

        logger.info(f"Successfully downloaded {len(df)} stations")
    except Exception as e:
        logger.error(f"Failed to download stations: {e}")
        raise


def download_all():
    """Download all data files."""
    logger.info("Starting download pipeline")

    download_trip_data()
    download_stations()

    logger.info("Download pipeline complete")


if __name__ == "__main__":
    from src.config import setup_logging

    setup_logging()
    download_all()
