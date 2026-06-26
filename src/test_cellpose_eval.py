from pathlib import Path
import tifffile as tiff

from cellpose import models

PROJECT = Path(__file__).resolve().parent.parent

DATA_DIR = PROJECT / "data" / "01"

img_file = sorted(DATA_DIR.glob("*.tif"))[0]

img = tiff.imread(img_file)

print("Image shape:", img.shape)
print("Image dtype:", img.dtype)

model = models.CellposeModel(
    gpu=False
)

print("Model loaded")

result = model.eval(
    img,
    channels=[0, 0]
)

print("Type:", type(result))
print("Length:", len(result))

for i, item in enumerate(result):
    try:
        print(i, type(item), getattr(item, "shape", None))
    except:
        print(i, type(item))

print("DONE")