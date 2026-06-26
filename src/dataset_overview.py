from pathlib import Path

import tifffile as tiff
import matplotlib.pyplot as plt

PROJECT = Path(__file__).resolve().parent.parent

DATA_DIR = PROJECT / "data" / "01"
FIGURE_DIR = PROJECT / "figure"

files = sorted(DATA_DIR.glob("*.tif"))

frames = [
    0,
    len(files)//2,
    len(files)-1
]

fig, ax = plt.subplots(
    1,
    3,
    figsize=(15,5)
)

for i, idx in enumerate(frames):

    img = tiff.imread(files[idx])

    ax[i].imshow(img,cmap="gray")

    ax[i].set_title(
        files[idx].stem
    )

    ax[i].axis("off")

plt.tight_layout()

plt.savefig(
    FIGURE_DIR /
    "dataset_overview.png",
    dpi=300
)
