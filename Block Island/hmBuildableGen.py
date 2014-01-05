from PIL import Image, ImageFont, ImageDraw, ImageOps
import numpy as np

threshold = 20

im_u = Image.open("siteImages/BIslopemap_u.tif")
im_v = Image.open("siteImages/BIslopemap_v.tif")

width  = im_u.size[0]
height = im_u.size[1]

pixels_u = im_u.load()
pixels_v = im_v.load()

pixel_list_u = []
pixel_list_v = []

for y in range(height):
	for x in range(width):
		pixel_list_u.append(pixels_u[x, y])
		pixel_list_v.append(pixels_v[x, y])
		
pixelmap_u = np.array(pixel_list_u).reshape((width, height))
pixelmap_v = np.array(pixel_list_v).reshape((width, height))
buildable = Image.new("P", (width, height), 0)
buildable_px = buildable.load()
	
for y in range(height):
	for x in range(width):
		if pixelmap_u[y, x] > threshold:
			buildable_px[x, y] = 255
		if pixelmap_v[y, x] > threshold:
			buildable_px[x, y] = 255

# buildable.save('siteImages/buildables/buildable_' + str(threshold) + '.png')
# buildable.save('siteImages/BIbuildable.tif')