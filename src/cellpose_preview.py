from pathlib import Path

import numpy as np
import tifffile as tiff
import matplotlib.pyplot as plt

from cellpose import models

PROJECT = Path(__file__).resolve().parent.parent

DATA_DIR = PROJECT / "data" / "01"
FIGURE_DIR = PROJECT / "figure"

model = models.CellposeModel(
    gpu=False
)

files = sorted(DATA_DIR.glob("*.tif"))

frames = [
    0,
    len(files)//2,
    len(files)-1
]

fig, ax = plt.subplots(
    len(frames),
    3,
    figsize=(15,15)
)

for row, idx in enumerate(frames):

    img = tiff.imread(files[idx])

    masks, flows, styles = model.eval(
        img,
        channels=[0,0]
    )

    n_cells = masks.max()

    print(
        f"{files[idx].stem}: {n_cells} cells"
    )

    ax[row,0].imshow(
        img,
        cmap="gray"
    )
    ax[row,0].set_title(
        f"{files[idx].stem} Raw"
    )

    ax[row,1].imshow(
        masks,
        cmap="tab20"
    )
    ax[row,1].set_title(
        f"Mask ({n_cells})"
    )

    ax[row,2].imshow(
        img,
        cmap="gray"
    )

    ax[row,2].contour(
        masks,
        colors="red",
        linewidths=0.5
    )

    ax[row,2].set_title(
        "Overlay"
    )

    for c in range(3):
        ax[row,c].axis("off")

plt.tight_layout()

plt.savefig(
    FIGURE_DIR /
    "cellpose_preview.png",
    dpi=300
)
