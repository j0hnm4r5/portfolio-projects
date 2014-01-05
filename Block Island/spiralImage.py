from PIL import Image


side_length = 80

im = Image.new('P', (side_length, side_length))
pix = im.load()

center = pix[side_length / 2, side_length / 2]

def make_spiral(start, turns):

	def up(n, x, y):
		for i in range(n):
			pix[x, y + i] = 255
	def right(n, x, y):
		pass
	def down(n, x, y):
		pass
	def left(n, x, y):
		pass

	i = 1
	while i < turns:
		up(i, x, y)
		right(i)
		i += 1
		down(i)
		left(i)
		i += 1
