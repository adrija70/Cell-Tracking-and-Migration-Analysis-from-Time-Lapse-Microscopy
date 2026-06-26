from pathlib import Path

import tifffile as tiff
import matplotlib.pyplot as plt

from skimage.filters import gaussian
from skimage.filters import threshold_otsu

from skimage.morphology import (
    remove_small_objects,
    remove_small_holes
)

PROJECT = Path(__file__).resolve().parent.parent

DATA_DIR = PROJECT / "data" / "01"
FIGURE_DIR = PROJECT / "figure"

img = tiff.imread(
    sorted(DATA_DIR.glob("*.tif"))[0]
)

# smooth

smooth = gaussian(
    img,
    sigma=2
)

# threshold

th = threshold_otsu(
    smooth
)

mask = smooth > th

# remove tiny noise

mask = remove_small_objects(
    mask,
    min_size=300
)

mask = remove_small_holes(
    mask,
    area_threshold=200
)

fig, ax = plt.subplots(
    1,
    3,
    figsize=(15,5)
)

ax[0].imshow(
    img,
    cmap="gray"
)
ax[0].set_title("Raw")

ax[1].imshow(
    smooth,
    cmap="gray"
)
ax[1].set_title("Smoothed")

ax[2].imshow(
    mask,
    cmap="gray"
)
ax[2].set_title("Filtered Mask")

for a in ax:
    a.axis("off")

plt.tight_layout()

plt.savefig(
    FIGURE_DIR /
    "segmentation_qc.png",
    dpi=300
)
