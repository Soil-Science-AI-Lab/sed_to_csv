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
- pandas>=1.0.0
- numpy>=1.18.0
- python>=3.7

### Setup

1. Clone the repository:

```bash
git clone https://github.com/SotKech/sed-to-csv.git
cd sed-to-csv
```

2. Install dependencies:

```bash
conda env update -f Dependencies.yaml
```
or create an enviroment for this:
```bash
conda env create -f Dependencies.yaml
```


## Input File Format

SED files should follow a similar structure:

```
Comment: 
Version: 2.3 [1.2.6947C]
File Name: \My Documents\Samples2025.01.29\19160B9_00001.sed
Instrument: PSR+3500_SN19160B9 [3]
Detectors: 512,256,256
Measurement: REFLECTANCE
Date: 01/29/2026,01/29/2026
Time: 15:34:22,15:34:38
Temperature (C): 27.26,8.81,-5.44,27.34,8.81,-5.44
Battery Voltage: 7.31,7.35
Averages: 10,10
Integration: 20,50,30,20,50,30
Dark Mode: AUTO,AUTO
Foreoptic: LENS4  {RADIANCE}, LENS4  {RADIANCE}
Radiometric Calibration: RADIANCE
Units: W/m^2/sr/nm
Wavelength Range: 350,2500
Latitude: n/a
Longitude: n/a
Altitude: n/a
GPS Time: n/a
Satellites: n/a
Calibrated Reference Correction File: none
Channels: 2151
Columns [2]:
Data:
Wvl	Reflect. %
 350.0	3.1209
 351.0	3.1289
 352.0	3.1201
...
```

**Requirements:**

- Metadata in `Key: Value` format (one per line)
- A `Data:` line marking the start of spectral data
- Tab-separated columns with headers: `Wvl` (wavelength in nm) and `Reflect. %` (reflectance percentage)

## Output Format

The output CSV has the following structure:

| File | Date | Time | Temperature (C) | 350.0 | 351.0 | 352.0 | ... |
|------|------|------|-----------------|-----|-----|-----|-----|
| 19160B9_00001 | 2026-02-05 | 14:30:45 | 25.5 | 12.34 | 13.45 | 14.56 | ... |
| 19160B9_00002 | 2026-02-05 | 14:31:12 | 25.6 | 12.40 | 13.50 | 14.62 | ... |

- **File**: Sample/file identifier
- **Date, Time, Temperature**: Extracted metadata
- **350.0, 351.0, 352.0, etc.**: Wavelength columns (numbers depend on input data)
- **Values**: Reflectance percentages

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

**Sotirios Kechagias**    
*PhD Student, University of Florida*    
[📩 skechagias@ufl.edu](mailto:skechagias@ufl.edu)

## Citation

If you use this tool in your research, please cite:

```bibtex
@software{sed_to_csv,
  author = {Sotirios Kechagias},
  title = {SED to CSV Converter},
  url = {https://github.com/Soil-Science-AI-Lab/sed-to-csv},
  year = {2026}
}
```

## Changelog

### Version 0.1.0 (2026-04-08)

- Initial release
- Basic SED to CSV conversion
- Metadata extraction
- Wavelength pivoting and sorting
