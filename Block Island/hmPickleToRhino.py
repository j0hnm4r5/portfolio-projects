from PIL import Image
import numpy as np
import pickle

img_buildable = Image.open("siteImages/buildableIslands-1side.tif")

width = img_buildable.size[0]
height = img_buildable.size[1]

pixels = img_buildable.load()

pixel_list = []

for y in range(height):
	for x in range(width):
		pixel_list.append(pixels[x, y])

pixelmap = np.array(pixel_list).reshape((width, height)).tolist()

with open('siteImages/buildable_islands.pkl', 'w') as p:
	pickle.dump(pixelmap, p, -1)



# img_height = Image.open("siteImages/pixelHeightMap.tif")

# width = img_height.size[0]
# height = img_height.size[1]

# pixels = img_height.load()

# pixel_list = []

# for y in range(height):
# 	for x in range(width):
# 		pixel_list.append(pixels[x, y])

# pixelmap = np.array(pixel_list).reshape((width, height)).tolist()

# with open('siteImages/height.pkl', 'w') as p:
# 	pickle.dump(pixelmap, p, -1)