from PIL import Image, ImageFont, ImageDraw

im = Image.open(r'siteImages/PixelHeightMap.tif')

width  = im.size[0]
height = im.size[1]

scale_factor = 20

pixels = im.load()

pixel_list = []
for y in range(height):
	for x in range(width):
		pixel_list.append(pixels[x, y])

new_map = Image.new("P", (width * scale_factor, height * scale_factor))
new_map_width = width * scale_factor
new_map_height = height * scale_factor

draw = ImageDraw.Draw(new_map)

# for x in range(0, new_map_width, scale_factor):
# 	draw.line([(x, 0), (x, new_map_height)], fill=256, width=1)

# for y in range(0, new_map_height, scale_factor):
# 	draw.line([(0, y), (new_map_width, y)], fill=256, width=1)

font = ImageFont.truetype('/Users/johnmars/Library/Fonts/inconsolata.otf', size=int(scale_factor*.6))

i = 0
for y in range(height):
	y *= scale_factor
	for x in range(width):
		x *= scale_factor
		draw.text((x + 1, y + 5), str(pixel_list[i]), font=font, fill=256)
		i += 1

new_map.save('siteImages/PixelHeights.png')
		
