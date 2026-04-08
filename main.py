"""Convert SED spectral data files to CSV format."""

import os
import glob
import pandas as pd


def _read_sed_metadata_and_data_start(path):
    """
    Extract metadata and find where data begins in a SED file.
    
    Args:
        path (str): Path to the .sed file
        
    Returns:
        tuple: (metadata_dict, data_start_line_number)
        
    Raises:
        ValueError: If no "Data:" line is found
    """
    meta = {}
    data_start_line = None

    with open(path, "r", errors="replace") as f:
        for i, line in enumerate(f):
            s = line.strip()

            if s == "Data:":
                data_start_line = i + 1
                break

            if ":" in s:
                k, v = s.split(":", 1)
                meta[k.strip()] = v.strip()

    if data_start_line is None:
        raise ValueError(f"No 'Data:' line found in {path}")

    return meta, data_start_line


def psr_to_csv(in_dir, out_file=None):
    """
    Convert .sed files to a combined CSV file.
    
    Args:
        in_dir (str): Directory containing .sed files (searched recursively)
        out_file (str, optional): Output CSV file path. If None, returns dataframe only
        
    Returns:
        pd.DataFrame: Combined dataframe with all samples
        
    Raises:
        ValueError: If no .sed files found or parsing fails
    """
    dfs = []
    pattern = os.path.join(in_dir, "**", "*.sed")

    for path in glob.glob(pattern, recursive=True):
        abs_path = os.path.abspath(path)
        print(f"Processing: {abs_path}")

        meta, data_start_line = _read_sed_metadata_and_data_start(abs_path)

        df = pd.read_csv(
            abs_path,
            sep="\t",
            header=0,
            skiprows=data_start_line,
            engine="python",
        )

        df.columns = [c.strip() for c in df.columns]

        file_id = meta.get("File Name", os.path.basename(abs_path))

        df = df[["Wvl", "Reflect. %"]].copy()
        df.index = [file_id] * len(df)

        wide = df.pivot(columns="Wvl", values="Reflect. %")
        wide = wide.reindex(sorted(wide.columns), axis=1)

        for key in reversed(["Date", "Time", "Temperature (C)"]):
            wide.insert(0, key, str(meta.get(key, "")).replace(",", " "))

        wide.index.name = "File"
        dfs.append(wide)

    if not dfs:
        raise ValueError(f"No .sed files found under: {in_dir}")

    out = pd.concat(dfs).sort_index()

    if out_file is not None:
        out.to_csv(out_file)
        print(f"Saved: {out_file}")

    return out


if __name__ == "__main__":
    psr_to_csv(
        r"C:\Users\skechagias\Desktop\Samples2026.02.05",
        r"C:\Users\skechagias\Desktop\Samples2026.01.29\spectra-2026.02.05.csv",
    )
