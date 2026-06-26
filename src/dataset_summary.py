from pathlib import Path
import tifffile as tiff
import pandas as pd

PROJECT = Path(__file__).resolve().parent.parent

DATA_DIR = PROJECT / "data" / "01"
ANALYSIS_DIR = PROJECT / "analysis"

records = []

for f in sorted(DATA_DIR.glob("*.tif")):

    img = tiff.imread(f)

    records.append([
        f.name,
        img.shape[0],
        img.shape[1],
        str(img.dtype)
    ])

df = pd.DataFrame(
    records,
    columns=["file","height","width","dtype"]
)

df.to_csv(
    ANALYSIS_DIR / "dataset_summary.csv",
    index=False
)

print(df.head())
