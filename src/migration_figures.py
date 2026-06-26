from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt

PROJECT_DIR = Path(__file__).resolve().parent.parent

tracks = pd.read_csv(
    PROJECT_DIR /
    "analysis" /
    "tracks_filtered.csv"
)

metrics = pd.read_csv(
    PROJECT_DIR /
    "analysis" /
    "migration_metrics.csv"
)

FIG_DIR = PROJECT_DIR / "figures"
FIG_DIR.mkdir(exist_ok=True)


# Figure 1
# Trajectories
plt.figure(figsize=(8,8))

for tid, g in tracks.groupby("track_id"):

    g = g.sort_values("frame")

    plt.plot(
        g["x"],
        g["y"]
    )
# image coordinates
plt.gca().invert_yaxis()

plt.xlabel("X")
plt.ylabel("Y")

plt.title("Cell Trajectories")

plt.tight_layout()

plt.savefig(
    FIG_DIR /
    "trajectory_plot.png",
    dpi=300
)

plt.close()


# Figure 2
# Speed distribution
plt.figure(figsize=(7,5))

plt.hist(
    metrics["mean_speed"],
    bins=10
)

plt.xlabel("Mean speed")

plt.ylabel("Count")

plt.title("Speed Distribution")

plt.tight_layout()

plt.savefig(
    FIG_DIR /
    "speed_distribution.png",
    dpi=300
)

plt.close()


# Figure 3
# Displacement vs Persistence
plt.figure(figsize=(7,6))

plt.scatter(
    metrics["displacement"],
    metrics["persistence"]
)

plt.xlabel("Displacement")

plt.ylabel("Persistence")

plt.title(
    "Displacement vs Persistence"
)

plt.tight_layout()

plt.savefig(
    FIG_DIR /
    "displacement_persistence.png",
    dpi=300
)

plt.close()

print("Finished.")
print(FIG_DIR)
