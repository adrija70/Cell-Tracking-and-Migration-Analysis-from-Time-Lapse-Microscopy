from pathlib import Path

import tifffile as tiff
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

PROJECT = Path(__file__).resolve().parent.parent

DATA_DIR = PROJECT / "data" / "01"
ANALYSIS_DIR = PROJECT / "analysis"
FIGURE_DIR = PROJECT / "figure"

records = []

for f in sorted(DATA_DIR.glob("*.tif")):

    img = tiff.imread(f)

    records.append([
        f.name,
        np.mean(img),
        np.std(img)
    ])

df = pd.DataFrame(
    records,
    columns=[
        "frame",
        "mean_intensity",
        "std_intensity"
    ]
)

df.to_csv(
    ANALYSIS_DIR /
    "intensity_metrics.csv",
    index=False
)

plt.figure(figsize=(8,5))

plt.plot(
    df["mean_intensity"]
)

plt.xlabel("Frame")
plt.ylabel("Mean intensity")

plt.tight_layout()

plt.savefig(
    FIGURE_DIR /
    "mean_intensity_vs_time.png",
    dpi=300
)
