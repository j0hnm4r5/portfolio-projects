import rhinoscriptsyntax as rs
import random
import itertools

class Square(object):

	def __init__(self, square):

		self.square = square

		self.box = rs.BoundingBox(square)

		self.bottom_left = self.box[0]
		self.bottom_right = self.box[1]
		self.top_right = self.box[2]
		self.top_left = self.box[3]

		global grid_pts
		grid_pts.append(self.bottom_left)
		rs.AddPoint(self.bottom_left)

		self.enclosed_curves = square

		for curve in square:
			if rs.IsCurveClosed(curve) == True:
				self.enclosed_curves.remove(curve)

		self.analysis_grid = []
		self.density_pointlist = []
		self.analysis = []
		self.densest = 0


	def draw_analysis_grid(self):

		grid_sections = 3

		width = rs.Distance(self.bottom_left, self.bottom_right) / grid_sections
		height = rs.Distance(self.bottom_left, self.top_left) / grid_sections

		origin = list(self.bottom_left)

		y = 0
		while y < grid_sections:
			x = 0
			while x < grid_sections:

				plane = rs.PlaneFromFrame(origin, (1,0,0), (0,1,0))
				rect = rs.AddRectangle(plane, width, height)
				self.analysis_grid.append(rect)

				origin[0] += width
				x += 1
			origin[0] = self.bottom_left[0]
			origin[1] += height
			y += 1

		for m in range(0, grid_sections**2):
			self.analysis.append(0)


	def divide_curves(self):

		min_curve_length = 50

		for curve in self.enclosed_curves:
			if rs.CurveLength(curve) > min_curve_length:
				self.density_pointlist.append(rs.DivideCurveLength(curve, min_curve_length, False, True))

		self.density_pointlist = list(itertools.chain.from_iterable(self.density_pointlist)) # flattens list

		for point in self.density_pointlist:
			point = self.density_pointlist.pop(0)
			self.density_pointlist.append(rs.AddPoint(point))


	def analyze(self):

		self.divide_curves()
		self.draw_analysis_grid()

		for point in self.density_pointlist:
			i = 0
			for box in self.analysis_grid:
				in_box = rs.IsObjectInBox(point, rs.BoundingBox(box))
				if in_box == True:
					self.analysis[i] += 1
				i += 1

		self.densest = self.analysis.index(max(self.analysis))

		rs.DeleteObjects(self.analysis_grid)
		rs.DeleteObjects(self.density_pointlist)


	def move(self, move_to):
		vector = rs.VectorCreate(move_to, self.bottom_left)
		rs.MoveObject(self.square, vector)


def sort(population):
	for square in population:
		pass


# myfile = open("/Users/johnmars/Desktop/sort.txt", "w")

grid_width = rs.GetInteger("How many squares wide?")
grid_height = rs.GetInteger("How many squares tall?")
number_in_grid = grid_height * grid_width

grid_pts = []
population = []

for x in range(0, number_in_grid):
	selected = rs.GetObjects("Select one square, then press Enter. Selection Order: L>>R, B>>T in squares of 9", group=True)
	square_object = Square(selected)
	population.append(square_object)
	for curve in selected:
		rs.ObjectLayer(curve, "SELECTED")

population_sort = []

for surface in population:
	surface.analyze()
	population_sort.append((surface.densest, surface))

print str(population_sort)
# myfile.write(str(population_sort))
# myfile.close()

population_sort = sorted(population_sort)


i = 0
for thing in population_sort:
	thing[1].move(grid_pts[i])
	i += 1

