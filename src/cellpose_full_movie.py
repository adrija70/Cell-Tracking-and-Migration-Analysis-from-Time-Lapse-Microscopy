from pathlib import Path

import numpy as np
import pandas as pd
import tifffile as tiff

from skimage.measure import regionprops_table

from cellpose import models


ROOT = Path("/home/adrija/projects/Python-based image analysis pipelines/cell tracking")

DATA_DIR = ROOT / "data"
OUT_DIR = ROOT / "analysis"
MASK_DIR = OUT_DIR / "cellpose_masks"

MASK_DIR.mkdir(parents=True, exist_ok=True)

print("Loading Cellpose model...")

model = models.CellposeModel(gpu=False)

records = []

files = sorted(
    (DATA_DIR / "01").glob("t*.tif")
)

print(f"{len(files)} frames found")

for f in files[:5]:
    print(f.name)



for frame_idx, file in enumerate(files):

    print(f"Frame {frame_idx}/{len(files)-1}")

    image = tiff.imread(file)

    masks, flows, styles = model.eval(
        image,
        diameter=None
    )

    np.save(
        MASK_DIR / f"mask_{frame_idx:03d}.npy",
        masks
    )

    props = regionprops_table(
        masks,
        properties=[
            "label",
            "area",
            "centroid",
            "perimeter"
        ]
    )

    df = pd.DataFrame(props)

    df["frame"] = frame_idx

    records.append(df)

    print(
        f"  cells detected: {len(df)}"
    )


all_cells = pd.concat(
    records,
    ignore_index=True
)

csv_path = OUT_DIR / "cellpose_measurements.csv"

all_cells.to_csv(
    csv_path,
    index=False
)

print()
print("Saved:")
print(csv_path)
print()
print("Total objects:")
print(len(all_cells))
