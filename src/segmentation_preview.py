from pathlib import Path

import tifffile as tiff
import matplotlib.pyplot as plt

from skimage.filters import threshold_otsu

PROJECT = Path(__file__).resolve().parent.parent

DATA_DIR = PROJECT / "data" / "01"
FIGURE_DIR = PROJECT / "figure"

img = tiff.imread(
    sorted(DATA_DIR.glob("*.tif"))[0]
)

th = threshold_otsu(img)

mask = img > th

fig, ax = plt.subplots(
    1,
    2,
    figsize=(10,5)
)

ax[0].imshow(
    img,
    cmap="gray"
)

ax[0].set_title("Raw")

ax[1].imshow(
    mask,
    cmap="gray"
)

ax[1].set_title("Mask")

for a in ax:
    a.axis("off")

plt.tight_layout()

plt.savefig(
    FIGURE_DIR /
    "segmentation_preview.png",
    dpi=300
)
