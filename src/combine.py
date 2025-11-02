"""Combine trip CSV files into one."""

import pandas as pd

from src.config import COMBINED_FILENAME, DOWNLOADS_DIR, STATION_COORDINATES_FILENAME


def combine_files():
    """Combine all trip CSV files."""
    print("\nFinding trip files...")

    # Get all CSV files except stations and combined
    csv_files = [
        f
        for f in DOWNLOADS_DIR.glob("*.csv")
        if f.name != STATION_COORDINATES_FILENAME and f.name != COMBINED_FILENAME
    ]

    print(f"Found {len(csv_files)} files")

    # Read all files
    print("Reading files...")
    dfs = []
    for f in csv_files:
        print(f"  {f.name}...", end=" ")
        df = pd.read_csv(f)
        dfs.append(df)
        print(f"{len(df):,} rows")

    # Combine
    print("\nCombining...")
    combined = pd.concat(dfs, ignore_index=True)

    # Save
    output = DOWNLOADS_DIR / COMBINED_FILENAME
    combined.to_csv(output, index=False)

    print(f"✓ Saved {len(combined):,} rows to {COMBINED_FILENAME}")
