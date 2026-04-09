"""
Convert SED spectral data files to CSV format.

This module processes spectral reflectance data from .sed files (typically from
spectrophotometers) and consolidates them into a single CSV file with metadata
and reflectance measurements organized by wavelength.


Example:
    >>> psr_to_csv(
    ...     "./examples/sample_data",
    ...     "./output/spectra.csv"
    ... )
"""

from __future__ import annotations

import glob
import logging
import os

import pandas as pd

logger = logging.getLogger(__name__)


def _read_sed_metadata_and_data_start(path: str) -> tuple[dict[str, str], int]:
    """
    Extract metadata and find where data begins in a SED file.

    Parses the header section of a .sed file to extract key-value metadata pairs
    (e.g., Date, Time, Temperature) and identifies the line number where the
    actual spectral data begins (marked by "Data:" line).

    Args:
        path (str): Path to the .sed file to parse.

    Returns:
        tuple[dict[str, str], int]: A tuple containing:
            - metadata_dict (dict): Key-value pairs from the file header.
              Keys are stripped of whitespace; values are the content after ":".
            - data_start_line_number (int): Line number (0-indexed) where data
              begins, i.e., the line immediately after "Data:".

    Raises:
        ValueError: If no "Data:" line is found in the file. This indicates
            the file format is invalid or corrupted.

    Note:
        - Lines are read with error handling (errors="replace") to handle
          encoding issues gracefully.
        - Only lines containing ":" are parsed as metadata.
        - The function stops reading after finding "Data:".
    """
    meta: dict[str, str] = {}
    data_start_line: int | None = None

    with open(path, "r", errors="replace") as f:
        for i, line in enumerate(f):
            s = line.strip()

            # Check if we've reached the data section
            if s == "Data:":
                data_start_line = i + 1
                break

            # Parse metadata lines (key: value format)
            if ":" in s:
                k, v = s.split(":", 1)
                meta[k.strip()] = v.strip()

    if data_start_line is None:
        raise ValueError(f"No 'Data:' line found in {path}")

    return meta, data_start_line


def psr_to_csv(in_dir: str, out_file: str | None = None) -> pd.DataFrame:
    """
    Convert .sed files to a combined CSV file with spectral data and metadata.

    Recursively searches for all .sed files in the input directory, extracts
    metadata and reflectance measurements, and consolidates them into a single
    wide-format CSV where:
    - Rows represent individual samples (files)
    - Columns represent wavelengths (with reflectance % values)
    - Metadata columns (Date, Time, Temperature) are prepended

    Wide format explanation: Data is transformed from long format (one row per
    wavelength measurement) to wide format (one row per sample, with wavelengths
    as separate columns). This makes it easier to compare spectral profiles
    across samples.

    Processing steps:
    1. Find all .sed files recursively in in_dir
    2. For each file:
       - Extract metadata (Date, Time, Temperature, etc.)
       - Read spectral data (Wavelength and Reflectance %)
       - Pivot data so wavelengths become columns
    3. Concatenate all samples and sort by file ID
    4. Optionally save to CSV

    Args:
        in_dir (str): Directory containing .sed files. Subdirectories are
            searched recursively.
        out_file (str | None, optional): Path where the output CSV will be saved.
            If None, the dataframe is returned but not saved to disk.
            Default is None.

    Returns:
        pd.DataFrame: Combined dataframe with shape (n_samples, n_wavelengths + 3).
            - Index: File names (from "File Name" metadata or filename)
            - Columns: Date, Time, Temperature (C), then wavelength columns
            - Values: Reflectance percentages

    Raises:
        ValueError: If no .sed files are found in the directory tree.

    Example:
        >>> df = psr_to_csv("./samples")
        >>> df.shape
        (45, 2048)

        >>> psr_to_csv(
        ...     "./samples",
        ...     "./output/combined_spectra.csv"
        ... )
    """
    dfs: list[pd.DataFrame] = []
    pattern: str = os.path.join(in_dir, "**", "*.sed")

    # Process each .sed file found
    for path in glob.glob(pattern, recursive=True):
        abs_path: str = os.path.abspath(path)
        logger.info("Processing: %s", abs_path)

        # Extract metadata and data location
        meta, data_start_line = _read_sed_metadata_and_data_start(abs_path)

        # Read spectral data (tab-separated, starting after metadata)
        df: pd.DataFrame = pd.read_csv(
            abs_path,
            sep="\t",
            header=0,
            skiprows=data_start_line,
            engine="python",
        )

        # Clean column names (remove leading/trailing whitespace)
        df.columns = [c.strip() for c in df.columns]

        # Use "File Name" metadata or fallback to filename
        file_id: str = meta.get("File Name", os.path.basename(abs_path))

        # Keep only wavelength and reflectance columns
        df = df[["Wvl", "Reflect. %"]].copy()
        df.index = [file_id] * len(df)

        # Pivot: convert from long format (one row per wavelength) to wide format
        # (one row per sample, one column per wavelength)
        wide: pd.DataFrame = df.pivot(columns="Wvl", values="Reflect. %")

        # Sort wavelength columns in ascending order
        wide = wide.reindex(sorted(wide.columns), axis=1)

        # Prepend metadata columns (Date, Time, Temperature) in reverse order
        # so they appear in the correct order after insertion
        for key in reversed(["Date", "Time", "Temperature (C)"]):
            wide.insert(0, key, str(meta.get(key, "")).replace(",", " "))

        # Set index name for clarity
        wide.index.name = "File"
        dfs.append(wide)

    # Ensure at least one file was found
    if not dfs:
        raise ValueError(f"No .sed files found under: {in_dir}")

    # Concatenate all samples and sort by file ID
    out: pd.DataFrame = pd.concat(dfs).sort_index()

    # Optionally save to CSV
    if out_file is not None:
        out.to_csv(out_file)
        logger.info("Saved: %s", out_file)

    return out
