from pathlib import Path
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from tifffile import imread
from scipy.ndimage import center_of_mass

PROJECT_DIR = Path(__file__).resolve().parent.parent

tracks = pd.read_csv(
    PROJECT_DIR / "analysis" / "tracks_filtered.csv"
)

metrics = pd.read_csv(
    PROJECT_DIR / "analysis" / "migration_metrics.csv"
)

FIG_DIR = PROJECT_DIR / "figures"
FIG_DIR.mkdir(exist_ok=True)


# FIGURE 1
# Origin-normalized trajectories
plt.figure(figsize=(7,7))

for tid, g in tracks.groupby("track_id"):

    g = g.sort_values("frame")

    x = g["x"].values
    y = g["y"].values

    x = x - x[0]
    y = y - y[0]

    plt.plot(x, y, lw=2)

plt.axhline(0, ls="--", alpha=0.3)
plt.axvline(0, ls="--", alpha=0.3)

plt.xlabel("ΔX (pixels)")
plt.ylabel("ΔY (pixels)")
plt.title("Origin-normalized Cell Trajectories")

plt.tight_layout()

plt.savefig(
    FIG_DIR / "figure1_origin_normalized_trajectories.png",
    dpi=300
)

plt.close()


# FIGURE 2
# Mean squared displacement
plt.figure(figsize=(7,5))

all_msd = []

for tid, g in tracks.groupby("track_id"):

    g = g.sort_values("frame")

    x = g["x"].values
    y = g["y"].values

    max_lag = min(10, len(g)-1)

    lags = []
    msd = []

    for lag in range(1, max_lag+1):

        dx = x[lag:] - x[:-lag]
        dy = y[lag:] - y[:-lag]

        val = np.mean(dx**2 + dy**2)

        lags.append(lag)
        msd.append(val)

    all_msd.append(msd)

    plt.plot(lags, msd, alpha=0.3)

min_len = min(len(m) for m in all_msd)

avg_msd = np.mean(
    [m[:min_len] for m in all_msd],
    axis=0
)

plt.plot(
    range(1, min_len+1),
    avg_msd,
    linewidth=4,
    label="Mean MSD"
)

plt.xlabel("Lag Time")
plt.ylabel("MSD")
plt.title("Mean Squared Displacement")

plt.legend()

plt.tight_layout()

plt.savefig(
    FIG_DIR / "figure2_MSD.png",
    dpi=300
)

plt.close()


# FIGURE 3
# Track duration distribution
track_lengths = (
    tracks.groupby("track_id")
          .size()
)

plt.figure(figsize=(6,5))

plt.hist(track_lengths, bins=10)

plt.xlabel("Track Length (frames)")
plt.ylabel("Count")

plt.title("Track Duration Distribution")

plt.tight_layout()

plt.savefig(
    FIG_DIR / "figure3_track_duration.png",
    dpi=300
)

plt.close()


# FIGURE 4
# Speed boxplot
plt.figure(figsize=(5,6))

plt.boxplot(
    metrics["mean_speed"]
)

plt.ylabel("Mean Speed")

plt.title("Cell Migration Speed")

plt.tight_layout()

plt.savefig(
    FIG_DIR / "figure4_speed_boxplot.png",
    dpi=300
)

plt.close()


# FIGURE 5
# Speed vs Persistence
plt.figure(figsize=(6,6))

plt.scatter(
    metrics["mean_speed"],
    metrics["persistence"],
    s=80
)

plt.xlabel("Mean Speed")
plt.ylabel("Persistence")

plt.title("Speed vs Persistence")

plt.tight_layout()

plt.savefig(
    FIG_DIR / "figure5_speed_vs_persistence.png",
    dpi=300
)

plt.close()


# FIGURE 6
# Segmentation quality panel
raw = imread(
    PROJECT_DIR /
    "data" /
    "01" /
    "t000.tif"
)

mask = np.load(
    PROJECT_DIR /
    "analysis" /
    "cellpose_masks" /
    "mask_000.npy"
)

overlay = raw.copy()

plt.figure(figsize=(15,5))

plt.subplot(1,3,1)
plt.imshow(raw, cmap="gray")
plt.title("Raw Image")
plt.axis("off")

plt.subplot(1,3,2)
plt.imshow(mask)
plt.title("Cellpose Mask")
plt.axis("off")

plt.subplot(1,3,3)
plt.imshow(raw, cmap="gray")
plt.contour(mask, colors="red", linewidths=0.5)
plt.title("Overlay")
plt.axis("off")

plt.tight_layout()

plt.savefig(
    FIG_DIR / "figure6_segmentation_quality.png",
    dpi=300
)

plt.close()

print()
print("All figures saved to:")
print(FIG_DIR)
