from PIL import Image, ImageFont, ImageDraw, ImageOps
import numpy as np

im = Image.open("siteImages/BlockIslandHeightMapLarge.tif")

width  = im.size[0]
height = im.size[1]

pixels = im.load()

pixel_list = []
for y in range(height):
	for x in range(width):
		pixel_list.append(pixels[x, y])
		
pixelmap = np.array(pixel_list).reshape((width, height))
normalmap = np.zeros((width, height, 3), dtype='int16')

bg = Image.new("RGB", (width, height))
bg_pixels = bg.load()

y = 0
while y < height:
	x = 0
	while x < width:
		z = pixelmap[y][x]
		if (x < width / 2) and (y < width / 2):

			vect1_x = 1
			vect1_y = 0
			vect1_z = z - pixelmap[y][x+1]

			vect2_x = 0 
			vect2_y = 1
			vect2_z = z - pixelmap[y+1][x]

			vect1 = [vect1_x, vect1_y, vect1_z]
			vect2 = [vect2_x, vect2_y, vect2_z]

			normalmap[y][x] = np.cross(vect1, vect2)

		if (x >= width / 2) and (y < width / 2):

			vect1_x = 1
			vect1_y = 0
			vect1_z = z - pixelmap[y][x-1]

			vect2_x = 0 
			vect2_y = 1
			vect2_z = z - pixelmap[y+1][x]

			vect1 = [vect1_x, vect1_y, vect1_z]
			vect2 = [vect2_x, vect2_y, vect2_z]

			normalmap[y][x] = np.cross(vect1, vect2)

		if (x < width / 2) and (y >= width / 2):

			vect1_x = 1
			vect1_y = 0
			vect1_z = z - pixelmap[y][x+1]

			vect2_x = 0 
			vect2_y = 1
			vect2_z = z - pixelmap[y-1][x]

			vect1 = [vect1_x, vect1_y, vect1_z]
			vect2 = [vect2_x, vect2_y, vect2_z]

			normalmap[y][x] = np.cross(vect1, vect2)

		if (x >= width / 2) and (y >= width / 2):
			
			vect1_x = 1
			vect1_y = 0
			vect1_z = z - pixelmap[y][x-1]

			vect2_x = 0 
			vect2_y = 1
			vect2_z = z - pixelmap[y-1][x]

			vect1 = [vect1_x, vect1_y, vect1_z]
			vect2 = [vect2_x, vect2_y, vect2_z]

			normalmap[y][x] = np.cross(vect1, vect2)

		px = abs(normalmap[y][x])

		# bg_pixels[x, y] = (int(abs(x)), int(abs(y)), int(abs(z)))
		bg_pixels[x, y] = (px[0], px[1], px[2])
		x += 1
	y += 1


minim = normalmap.min()
maxim = normalmap.max()
im_range = maxim - minim

new_range = 255

for y in range(height):
	for x in range(width):

		orig_val_x = bg_pixels[x,y][0]
		new_x = (((orig_val_x - minim) * new_range) / im_range)

		orig_val_y = bg_pixels[x,y][1]
		new_y = (((orig_val_y - minim) * new_range) / im_range)

		bg_pixels[x, y] = (new_x, new_y, 255)


# bg.show()
bg.save('siteImages/BInormalmap.tif')
