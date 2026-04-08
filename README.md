# SED to CSV Converter

Convert spectral reflectance data from SED files to CSV format.

## Overview

This utility processes spectral reflectance measurement files (`.sed` format) and converts them into a consolidated CSV file. It's designed for handling batch processing of spectral data with automatic metadata extraction and wavelength-based pivoting.

## Features

- 🔄 **Recursive Directory Processing** - Automatically finds and processes all `.sed` files in nested directories
- 📊 **Metadata Extraction** - Automatically extracts Date, Time, Temperature, and other metadata from file headers
- 📈 **Wide Format Pivot** - Converts wavelength-reflectance pairs into a wide format where each wavelength becomes a column
- 🔢 **Numerical Sorting** - Wavelength columns are automatically sorted in numerical order
- 📁 **Batch Consolidation** - Combines multiple sample files into a single output CSV
- ⚠️ **Error Handling** - Graceful handling of malformed files and missing data fields

## Installation

### Requirements

- Python 3.7 or higher
- pandas >= 1.0.0
- numpy >= 1.18.0

### Setup

1. Clone the repository:

```bash
git clone https://github.com/SotKech/sed-to-csv.git
cd sed-to-csv
```

2. Install dependencies:

```bash
pip install -r requirements.txt
```

Alternatively, install via setup.py:

```bash
pip install -e .
```

## Usage

### As a Python Module

```python
from sed_to_csv import psr_to_csv

# Basic usage - save to CSV
result = psr_to_csv(
    in_dir="path/to/sed/files",
    out_file="output.csv"
)

# Get dataframe without saving
df = psr_to_csv(in_dir="path/to/sed/files")
print(df)
```

### Command Line

Edit the `if __name__ == "__main__":` block in `sed_to_csv.py` and run:

```bash
python sed_to_csv.py
```

## Input File Format

SED files should follow this structure:

```
File Name: 19160B9_00001
Date: 2026-02-05
Time: 14:30:45
Temperature (C): 25.5
Instrument: Spectrophotometer XYZ
Data:
Wvl	Reflect. %
380	12.34
390	13.45
400	14.56
...
```

**Requirements:**

- Metadata in `Key: Value` format (one per line)
- A `Data:` line marking the start of spectral data
- Tab-separated columns with headers: `Wvl` (wavelength in nm) and `Reflect. %` (reflectance percentage)

## Output Format

The output CSV has the following structure:

| File | Date | Time | Temperature (C) | 380 | 390 | 400 | ... |
|------|------|------|-----------------|-----|-----|-----|-----|
| 19160B9_00001 | 2026-02-05 | 14:30:45 | 25.5 | 12.34 | 13.45 | 14.56 | ... |
| 19160B9_00002 | 2026-02-05 | 14:31:12 | 25.6 | 12.40 | 13.50 | 14.62 | ... |

- **File**: Sample/file identifier
- **Date, Time, Temperature**: Extracted metadata
- **380, 390, 400, etc.**: Wavelength columns (numbers depend on input data)
- **Values**: Reflectance percentages

## API Reference

### `psr_to_csv(in_dir, out_file=None)`

Converts SED files to CSV format.

**Parameters:**

- `in_dir` (str): Root directory to search for `.sed` files (recursive)
- `out_file` (str, optional): Path where CSV output will be saved. If `None`, only returns dataframe

**Returns:**

- `pd.DataFrame`: Combined dataframe with all samples, indexed by file ID

**Raises:**

- `ValueError`: If no `.sed` files found or required data fields are missing

**Example:**

```python
df = psr_to_csv("./samples", "./output/spectra.csv")
print(f"Processed {len(df)} samples")
```

### `_read_sed_metadata_and_data_start(path)`

Internal helper function to extract metadata and locate data section.

**Parameters:**

- `path` (str): Path to a single `.sed` file

**Returns:**

- `tuple`: `(metadata_dict, data_start_line_number)`

**Raises:**

- `ValueError`: If no `Data:` marker found

## Examples

### Example 1: Basic Batch Processing

```python
from sed_to_csv import psr_to_csv

# Process all .sed files in a directory tree
psr_to_csv(
    in_dir="./spectral_data/2026-02-05",
    out_file="./output/2026-02-05_combined.csv"
)
```

### Example 2: Processing with Data Inspection

```python
from sed_to_csv import psr_to_csv

df = psr_to_csv("./samples")

print(f"Shape: {df.shape}")  # (num_samples, num_wavelengths + 4)
print(f"Wavelength range: {df.columns[4]} - {df.columns[-1]}")
print(df.head())

df.to_csv("output.csv")
```

### Example 3: Filtering Results

```python
from sed_to_csv import psr_to_csv

df = psr_to_csv("./samples")

# Filter by temperature
high_temp = df[df["Temperature (C)"].astype(float) > 25.0]

# Get reflectance at specific wavelengths
wavelengths_of_interest = ["450", "550", "650"]
subset = df[["File", "Date"] + wavelengths_of_interest]
```

## Error Handling

The script includes robust error handling:

- **Missing `Data:` marker**: Raises `ValueError` with file path
- **File encoding issues**: Uses `errors="replace"` to handle corrupted characters
- **Missing columns**: Strips whitespace from headers for tolerance
- **No .sed files found**: Raises `ValueError` with search directory

## Troubleshooting

### "No .sed files found under: [path]"

- Verify the directory path is correct
- Ensure files have `.sed` extension (case-sensitive on Linux/Mac)
- Check file permissions

### "No 'Data:' line found in [file]"

- Verify SED file format is correct
- The `Data:` marker must be on its own line
- Check for encoding issues

### Column mismatch errors

- Ensure tab separation in data section
- Verify column headers are exactly `Wvl` and `Reflect. %`
- Check for extra whitespace

## Performance

Processing time depends on:

- Number of files
- Wavelength points per file (typically 300-3000)
- Disk I/O speed

Typical performance:

- 100 files with 1000 wavelengths each: ~2-5 seconds
- 1000 files with 1000 wavelengths each: ~20-50 seconds

## Contributing

Contributions are welcome! Please:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/improvement`)
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Author

**SotKech**

## Citation

If you use this tool in your research, please cite:

```bibtex
@software{sed_to_csv,
  author = {SotKech},
  title = {SED to CSV Converter},
  url = {https://github.com/SotKech/sed-to-csv},
  year = {2026}
}
```

## Support

For issues, questions, or suggestions, please open an [issue](https://github.com/SotKech/sed-to-csv/issues) on GitHub.

## Changelog

### Version 0.1.0 (2026-04-08)

- Initial release
- Basic SED to CSV conversion
- Metadata extraction
- Wavelength pivoting and sorting
