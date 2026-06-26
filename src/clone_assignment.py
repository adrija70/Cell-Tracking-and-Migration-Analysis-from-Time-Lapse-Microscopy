from pathlib import Path

import pandas as pd
import matplotlib.pyplot as plt

from sklearn.cluster import KMeans

PROJECT_DIR = Path(__file__).resolve().parent.parent

ANALYSIS_DIR = PROJECT_DIR / "analysis"
FIGURE_DIR = PROJECT_DIR / "figures"

FIGURE_DIR.mkdir(exist_ok=True)

tracks = pd.read_csv(
    ANALYSIS_DIR / "tracks_filtered.csv"
)


first_frame = tracks[
    tracks["frame"] == tracks["frame"].min()
].copy()

print("Cells at first frame:", len(first_frame))
# chosen for exploratory clustering
N_CLONES = 8

kmeans = KMeans(
    n_clusters=N_CLONES,
    random_state=42,
    n_init=20
)

first_frame["clone_id"] = kmeans.fit_predict(
    first_frame[["x", "y"]]
)

clone_map = dict(
    zip(
        first_frame["track_id"],
        first_frame["clone_id"]
    )
)

tracks["clone_id"] = tracks["track_id"].map(
    clone_map
)

tracks = tracks.dropna(
    subset=["clone_id"]
)

tracks["clone_id"] = (
    tracks["clone_id"]
    .astype(int)
)


tracks.to_csv(
    ANALYSIS_DIR /
    "tracks_with_clones.csv",
    index=False
)


plt.figure(figsize=(8,8))

scatter = plt.scatter(
    first_frame["x"],
    first_frame["y"],
    c=first_frame["clone_id"],
    s=50
)
# image coordinates
plt.gca().invert_yaxis()

plt.title(
    "Synthetic Clone Assignment"
)

plt.xlabel("X")

plt.ylabel("Y")

plt.colorbar(
    label="Clone ID"
)

plt.tight_layout()

plt.savefig(
    FIGURE_DIR /
    "clone_assignment.png",
    dpi=300
)

plt.show()

print(
    "\nSaved:"
)

print(
    ANALYSIS_DIR /
    "tracks_with_clones.csv"
)
