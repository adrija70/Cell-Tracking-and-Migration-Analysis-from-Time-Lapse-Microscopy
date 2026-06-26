from pathlib import Path

import tifffile as tiff
import pandas as pd

from skimage.filters import threshold_otsu
from skimage.measure import label
from skimage.measure import regionprops_table

PROJECT = Path(__file__).resolve().parent.parent

DATA_DIR = PROJECT / "data" / "01"
ANALYSIS_DIR = PROJECT / "analysis"

all_frames = []

for frame_id, f in enumerate(
    sorted(DATA_DIR.glob("*.tif"))
):

    img = tiff.imread(f)

    mask = img > threshold_otsu(img)

    labels = label(mask)

    props = regionprops_table(
        labels,
        intensity_image=img,
        properties=[
            "label",
            "area",
            "centroid",
            "mean_intensity"
        ]
    )

    df = pd.DataFrame(props)

    df["frame"] = frame_id

    all_frames.append(df)

final = pd.concat(
    all_frames,
    ignore_index=True
)

final.to_csv(
    ANALYSIS_DIR /
    "cell_measurements.csv",
    index=False
)

print(final.head())
