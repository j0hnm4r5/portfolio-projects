from PIL import Image, ImageFont, ImageDraw
import numpy as np

im = Image.open(r'siteImages/buildable.tif')
# im = im.convert('RGB')

width  = im.size[0]
height = im.size[1]

pixels = im.load()

islands = Image.new('P', (width, height))
island_pixels = islands.load()

pixelmap = np.zeros((width, height, 3), dtype='int16')

pixel_list = []
for y in range(height):
	for x in range(width):
		# print pixels[x,y]
		if pixels[x, y] == 0:
			# print "BLACK"
			pixelmap[y, x] = 0

		if (pixels[x, y] == 255) or (pixels[x, y] == 1):
			# print "WHITE"
			pixelmap[y, x] = 255

y = 1
while y < height - 1:
	x = 1
	while x < width - 1:
		if pixelmap[y, x][0] == 0:
			count = 0
			# Check if bordered by white
			n = pixelmap[y - 1, x][0]
			if n == 255:
				count += 1
			s = pixelmap[y + 1, x][0]
			if s == 255:
				count += 1
			e = pixelmap[y, x + 1][0]
			if e == 255:
				count += 1
			w = pixelmap[y, x - 1][0]
			if w == 255:
				count += 1
			# print n,s,e,w
			if count > 3:
				island_pixels[x, y] = 255
				# print "RED"
		x += 1
	y += 1

islands.save('siteImages/buildableIslands.tif')
print "saved"