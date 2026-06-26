from pathlib import Path
import tifffile as tiff

PROJECT = Path(__file__).resolve().parent.parent

DATA_DIR = PROJECT / "data" / "01"

files = sorted(DATA_DIR.glob("*.tif"))

print("Number of frames:", len(files))

print("\nFirst 5 files:")
for f in files[:5]:
    print(f.name)

img = tiff.imread(files[0])

print("\nShape:", img.shape)
print("dtype:", img.dtype)
print("min:", img.min())
print("max:", img.max())
