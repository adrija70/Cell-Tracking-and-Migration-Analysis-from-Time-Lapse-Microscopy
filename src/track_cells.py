from pathlib import Path
import pandas as pd
import numpy as np
from scipy.spatial.distance import cdist

PROJECT_DIR = Path(__file__).resolve().parent.parent

df = pd.read_csv(
    PROJECT_DIR /
    "analysis" /
    "cell_measurements_clean.csv"
)

df = df.sort_values(["frame"])

next_track_id = 0
tracks = []

first_frame = df["frame"].min()

current = df[df["frame"] == first_frame].copy()

current["track_id"] = range(len(current))

next_track_id = len(current)

tracks.append(current)

for frame in range(first_frame + 1,
                   df["frame"].max() + 1):

    prev = current

    current = df[df["frame"] == frame].copy()

    prev_xy = prev[["x","y"]].values
    curr_xy = current[["x","y"]].values

    D = cdist(curr_xy, prev_xy)

    assigned_prev = set()
    track_ids = []

    for i in range(len(current)):

        j = np.argmin(D[i])

        if D[i,j] < 80 and j not in assigned_prev:

            track_ids.append(
                prev.iloc[j]["track_id"]
            )

            assigned_prev.add(j)

        else:

            track_ids.append(next_track_id)
            next_track_id += 1

    current["track_id"] = track_ids

    tracks.append(current)

tracks_df = pd.concat(tracks)

outfile = (
    PROJECT_DIR /
    "analysis" /
    "tracks_dataframe.csv"
)

tracks_df.to_csv(outfile,index=False)

print()
print("Saved:", outfile)
print()
print("Unique tracks:",
      tracks_df["track_id"].nunique())
