"""Unit tests for sed_to_csv.converter."""

from __future__ import annotations

import os
import tempfile

import pandas as pd
import pytest

from sed_to_csv.converter import _read_sed_metadata_and_data_start, psr_to_csv

# Path to bundled test data
DATA_DIR = os.path.join(os.path.dirname(__file__), "data")


# ---------------------------------------------------------------------------
# _read_sed_metadata_and_data_start
# ---------------------------------------------------------------------------


class TestReadSedMetadataAndDataStart:
    def test_returns_metadata_dict(self) -> None:
        path = os.path.join(DATA_DIR, "sample_00001.sed")
        meta, _ = _read_sed_metadata_and_data_start(path)
        assert meta["Date"] == "01/29/2026,01/29/2026"
        assert meta["File Name"] == "sample_00001.sed"

    def test_returns_correct_data_start_line(self) -> None:
        path = os.path.join(DATA_DIR, "sample_00001.sed")
        _, data_start = _read_sed_metadata_and_data_start(path)
        # data_start should point to the header row ("Wvl\tReflect. %")
        assert data_start > 0

    def test_raises_on_missing_data_marker(self, tmp_path: pytest.TempPathFactory) -> None:
        bad_file = tmp_path / "bad.sed"
        bad_file.write_text("Key: value\nNo data marker here\n")
        with pytest.raises(ValueError, match="No 'Data:' line found"):
            _read_sed_metadata_and_data_start(str(bad_file))


# ---------------------------------------------------------------------------
# psr_to_csv
# ---------------------------------------------------------------------------


class TestPsrToCsv:
    def test_returns_dataframe(self) -> None:
        df = psr_to_csv(DATA_DIR)
        assert isinstance(df, pd.DataFrame)

    def test_row_count_matches_file_count(self) -> None:
        df = psr_to_csv(DATA_DIR)
        # Two sample .sed files in DATA_DIR
        assert len(df) == 2

    def test_metadata_columns_present(self) -> None:
        df = psr_to_csv(DATA_DIR)
        for col in ("Date", "Time", "Temperature (C)"):
            assert col in df.columns

    def test_wavelength_columns_are_sorted(self) -> None:
        df = psr_to_csv(DATA_DIR)
        wavelength_cols = [c for c in df.columns if c not in ("Date", "Time", "Temperature (C)")]
        assert wavelength_cols == sorted(wavelength_cols)

    def test_index_name_is_file(self) -> None:
        df = psr_to_csv(DATA_DIR)
        assert df.index.name == "File"

    def test_saves_csv_when_out_file_given(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            out = os.path.join(tmp, "out.csv")
            psr_to_csv(DATA_DIR, out)
            assert os.path.isfile(out)
            saved = pd.read_csv(out, index_col="File")
            assert len(saved) == 2

    def test_raises_on_empty_directory(self, tmp_path: pytest.TempPathFactory) -> None:
        with pytest.raises(ValueError, match="No .sed files found"):
            psr_to_csv(str(tmp_path))
