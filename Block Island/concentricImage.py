from PIL import Image
import itertools

side_length = 20

im = Image.new('P', (side_length, side_length))
pix = im.load()

falloff = 20

center = side_length / 2
help = center * (side_length / center) - 1

pix[center, center] = 255



for n in reversed(range(center)):

	# vertical
	pix[center, n] = (n * falloff)
	pix[center, help - n] = (n * falloff)

	# horizontal
	pix[n, center] = (n * falloff)
	pix[help - n, center] = (n * falloff)

	# diagonal
	pix[n, n] = (n * falloff)
	pix[help - n, n] = (n * falloff)
	pix[n, help - n] = (n * falloff)
	pix[help - n, help - n] = (n * falloff)

	# quadrants
	for i in reversed(range(n)):
		pix[i, n] = (i * falloff)
		pix[n, i] = (i * falloff)
		pix[help - i, n] = (i * falloff)
		pix[help - n, i] = (i * falloff)
		pix[i, help - n] = (i * falloff)
		pix[n, help - i] = (i * falloff)
		pix[help - i, help - n] = (i * falloff)
		pix[help - n, help - i] = (i * falloff)

im.show()
# im.save('siteImages/concentric.tif')