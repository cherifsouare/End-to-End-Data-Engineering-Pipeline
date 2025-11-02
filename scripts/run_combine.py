import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from src.combine import combine_files

if __name__ == "__main__":
    combine_files()
