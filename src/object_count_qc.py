from pathlib import Path

import tifffile as tiff
import pandas as pd

from skimage.filters import gaussian
from skimage.filters import threshold_otsu

from skimage.morphology import (
    remove_small_objects,
    remove_small_holes
)

from skimage.measure import label

PROJECT = Path(__file__).resolve().parent.parent

DATA_DIR = PROJECT / "data" / "01"

records = []

for frame_id, f in enumerate(
    sorted(DATA_DIR.glob("*.tif"))
):

    img = tiff.imread(f)

    smooth = gaussian(
        img,
        sigma=2
    )

    th = threshold_otsu(
        smooth
    )

    mask = smooth > th

    mask = remove_small_objects(
        mask,
        min_size=300
    )

    mask = remove_small_holes(
        mask,
        area_threshold=200
    )

    labels = label(mask)

    records.append([
        frame_id,
        labels.max()
    ])

df = pd.DataFrame(
    records,
    columns=[
        "frame",
        "n_objects"
    ]
)

print(df)

print()
print(
    "Mean objects/frame:",
    df["n_objects"].mean()
)
