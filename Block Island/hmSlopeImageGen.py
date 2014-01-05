from PIL import Image, ImageFont, ImageDraw, ImageOps
import numpy as np

# im = Image.open("siteImages/PixelHeightMap.tif")
im = Image.open("siteImages/BlockIslandHeightMapLarge.tif")

width  = im.size[0]
height = im.size[1]

pixels = im.load()

pixel_list = []
for y in range(height):
	for x in range(width):
		pixel_list.append(pixels[x, y])

		
pixelmap = np.array(pixel_list).reshape((width, height))
normalmap_u = np.zeros(width * height, dtype='int16').reshape((width, height))
normalmap_v = np.zeros(width * height, dtype='int16').reshape((width, height))

y = 1
while y < height - 1:
	x = 1
	while x < width - 1:
		north = pixelmap[y-1][x]
		south = pixelmap[y+1][x]
		normalmap_v[y][x] = abs(north - south)

		east = pixelmap[y][x-1]
		west = pixelmap[y][x+1]
		normalmap_u[y][x] = abs(east - west)
		x += 1
	y += 1

# print pixelmap
# print normalmap_u
# print normalmap_v

slopemap_u = Image.new("P", (width, height))
slopemap_v = Image.new("P", (width, height))
slope_pixels_u = slopemap_u.load()
slope_pixels_v = slopemap_v.load()



for y in range(height):
	for x in range(width):
		slope_pixels_u[x,y] = normalmap_u[y][x]
		slope_pixels_v[x,y] = normalmap_v[y][x]

u_min = normalmap_u.min()
u_max = normalmap_u.max()
u_range = u_max - u_min

v_min = normalmap_v.min()
v_max = normalmap_v.max()
v_range = v_max - v_min

new_range = 255

for y in range(height):
	for x in range(width):

		orig_val_u = slope_pixels_u[x,y]
		new_u = (((orig_val_u - u_min) * new_range) / u_range)

		orig_val_v = slope_pixels_v[x,y]
		new_v = (((orig_val_v - v_min) * new_range) / v_range)

		slope_pixels_u[x,y] = new_u
		slope_pixels_v[x,y] = new_v


# slopemap_u.save('siteImages/slopemap_u.tif')
# slopemap_v.save('siteImages/slopemap_v.tif')

slopemap_u.save('siteImages/BIslopemap_u.tif')
slopemap_v.save('siteImages/BIslopemap_v.tif')