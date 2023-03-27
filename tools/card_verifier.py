from os import listdir
from PIL import Image

dimensions = {}

for file in listdir("./tools/out"):
    image = Image.open(f"./tools/out/{file}")
    dims = (image.width, image.height)
    if dims not in dimensions:
        dimensions[dims] = 0
    dimensions[dims] += 1


print("\n".join([f"{k}: {v//6}" for k, v in dimensions.items()]))