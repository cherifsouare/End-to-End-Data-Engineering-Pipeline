"""Configuration management."""

import os
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()

# Paths
PROJECT_ROOT = Path(__file__).parent.parent
DOWNLOADS_DIR = PROJECT_ROOT / os.getenv("DOWNLOADS_DIR", "downloads")
DOWNLOADS_DIR.mkdir(exist_ok=True)

# AWS
AWS_REGION = os.getenv("AWS_DEFAULT_REGION", "us-east-1")
S3_BUCKET_NAME = os.getenv("S3_BUCKET_NAME", "divvy-data-pipeline-bucket")
S3_PROCESSED_PREFIX = "processed/divvy-trips"

# Trip data URLs
DOWNLOAD_URLS = [
    "https://divvy-tripdata.s3.amazonaws.com/Divvy_Trips_2018_Q4.zip",
    "https://divvy-tripdata.s3.amazonaws.com/Divvy_Trips_2019_Q1.zip",
    "https://divvy-tripdata.s3.amazonaws.com/Divvy_Trips_2019_Q2.zip",
    "https://divvy-tripdata.s3.amazonaws.com/Divvy_Trips_2019_Q3.zip",
    "https://divvy-tripdata.s3.amazonaws.com/Divvy_Trips_2019_Q4.zip",
    "https://divvy-tripdata.s3.amazonaws.com/Divvy_Trips_2020_Q1.zip",
]

# Station coordinates
STATION_COORDINATES_URL = (
    "https://data.cityofchicago.org/api/views/bbyy-e7gq/rows.csv?accessType=DOWNLOAD"
)
STATION_COORDINATES_FILENAME = "divvy_stations.csv"

# Settings
MAX_WORKERS = int(os.getenv("MAX_WORKERS", "5"))
COMBINED_FILENAME = "divvy_trips_combined.csv"
