from pathlib import Path
import pandas as pd
import numpy as np

PROJECT_DIR = Path(__file__).resolve().parent.parent

df = pd.read_csv(
    PROJECT_DIR /
    "analysis" /
    "tracks_filtered.csv"
)

records = []

for track_id, g in df.groupby("track_id"):

    g = g.sort_values("frame")

    x = g["x"].values
    y = g["y"].values

    step_lengths = np.sqrt(
        np.diff(x)**2 +
        np.diff(y)**2
    )

    path_length = step_lengths.sum()

    displacement = np.sqrt(
        (x[-1]-x[0])**2 +
        (y[-1]-y[0])**2
    )

    persistence = (
        displacement / path_length
        if path_length > 0
        else 0
    )

    mean_speed = (
        step_lengths.mean()
        if len(step_lengths) > 0
        else 0
    )

    records.append([
        track_id,
        len(g),
        path_length,
        displacement,
        persistence,
        mean_speed
    ])

metrics = pd.DataFrame(
    records,
    columns=[
        "track_id",
        "n_frames",
        "path_length",
        "displacement",
        "persistence",
        "mean_speed"
    ]
)

outfile = (
    PROJECT_DIR /
    "analysis" /
    "migration_metrics.csv"
)

metrics.to_csv(outfile,index=False)

print(metrics.describe())
