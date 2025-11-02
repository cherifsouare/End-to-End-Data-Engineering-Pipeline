"""Configuration management - SHARED settings only."""

import logging
import os
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()

# Paths (used everywhere)
PROJECT_ROOT = Path(__file__).parent.parent
DOWNLOADS_DIR = PROJECT_ROOT / os.getenv("DOWNLOADS_DIR", "downloads")
DOWNLOADS_DIR.mkdir(exist_ok=True)

# AWS (used by multiple modules)
AWS_REGION = os.getenv("AWS_DEFAULT_REGION", "us-east-1")
S3_BUCKET_NAME = os.getenv("S3_BUCKET_NAME", "divvy-data-pipeline-bucket")

# S3 structure (used by upload, weather, snowflake)
S3_RAW_TRIPS_PREFIX = "raw/trips"
S3_RAW_STATIONS_PREFIX = "raw/stations"
S3_RAW_WEATHER_PREFIX = "raw/weather"


def setup_logging(level=logging.INFO):
    """Configure logging for the application."""
    logging.basicConfig(
        level=level,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        handlers=[logging.StreamHandler()],
    )
