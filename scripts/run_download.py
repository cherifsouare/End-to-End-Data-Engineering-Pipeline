"""Run download pipeline."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from src.config import setup_logging
from src.download import download_all

if __name__ == "__main__":
    setup_logging()
    download_all()
