"""Entry point for ``python -m sed_to_csv``."""

from __future__ import annotations

import argparse
import logging
import sys

from sed_to_csv.converter import psr_to_csv


def main() -> None:
    """Parse CLI arguments and run the SED-to-CSV conversion."""
    logging.basicConfig(level=logging.INFO, format="%(message)s")

    parser = argparse.ArgumentParser(
        prog="sed_to_csv",
        description="Convert SED spectral data files to a combined CSV file.",
    )
    parser.add_argument(
        "in_dir",
        help="Directory containing .sed files (searched recursively).",
    )
    parser.add_argument(
        "out_file",
        help="Output CSV file path.",
    )

    args = parser.parse_args()

    try:
        psr_to_csv(args.in_dir, args.out_file)
    except ValueError as exc:
        print(f"Error: {exc}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
