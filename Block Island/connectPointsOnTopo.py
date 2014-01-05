from PIL import Image, ImageDraw
import math
import numpy as np

heightmap = Image.open('siteImages/PixelHeightMap.tif')
goals = Image.open('siteImages/buildableIslands-4side.tif')

width  = heightmap.size[0]
height = heightmap.size[1]

drawn = Image.new('P', (width, height))

pixels_heightmap = heightmap.load()
pixels_goals = goals.load()
pixels_drawn = drawn.load()

pixel_list_heightmap = []
pixel_list_goals = []
pixel_list_drawn = []

for y in range(height):
	for x in range(width):
		pixel_list_heightmap.append(pixels_heightmap[x, y])
		pixel_list_goals.append(pixels_goals[x, y])
		pixel_list_drawn.append(pixels_goals[x, y])

pixelmap_heightmap = np.array(pixel_list_heightmap).reshape((width, height))
pixelmap_goals = np.array(pixel_list_goals).reshape((width, height))
pixelmap_drawn = np.array(pixel_list_goals).reshape((width, height))

goal_coords = []
it = np.nditer(pixelmap_goals, flags=['multi_index'])
while not it.finished:
	if it[0] == 255:
		goal_coords.append(it.multi_index)
	it.iternext()

def distance((x1, y1), (x2, y2)):
	return math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)

# connection_list = []
# for n in range(len(goal_coords)):
# 	connection_list.append(0)
#
# i = 0
# for goal1 in goal_coords:
# 	temp = 9999999
# 	for goal2 in goal_coords:
# 		dist = distance(goal1, goal2)
# 		if dist < temp and dist != 0:
# 			temp = dist
# 			connection_list[i] = (goal1, goal2)
# 	i += 1

connection_dict = {}
for n in range(len(goal_coords)):
	connection_dict[goal_coords[n]] = pixelmap_heightmap[goal_coords[n]]

print connection_dict
connection_list = connection_dict.items()
print connection_list
connection_list = sorted(connection_list, key=lambda value: value[1])
print connection_list


# connection_list = []
# for i, goal in enumerate(goal_coords):
# 	if i > 0:
# 		connection_list.append((goal, goal_coords[i-1]))

drawn_im = ImageDraw.Draw(drawn)

# for i, connection in enumerate(connection_list):
# 	print connection
# 	drawn_im.line((connection_list[i - 1][0][::-1], connection[0][::-1]), fill=128)


def travel(start, end, pixelmap):
	level_threshold = .5
	print start, end
	print pixelmap[start], pixelmap[end]
	start_dist = distance((start), (end))
	current = start

	# for x in range(50):
	while distance(current, end) > 1:
		# check NSEW from current pixel to see what is closer to end
		distance_dict = {}
		distance_dict['N'] = distance((current[0], current[1] - 1), end)
		distance_dict['E'] = distance((current[0] + 1, current[1]), end)
		distance_dict['S'] = distance((current[0], current[1] + 1), end)
		distance_dict['W'] = distance((current[0] - 1, current[1]), end)

		value_dict = {}
		value_dict['N'] = pixelmap[(current[0], current[1] - 1)]
		value_dict['E'] = pixelmap[(current[0] + 1, current[1])]
		value_dict['S'] = pixelmap[(current[0], current[1] + 1)]
		value_dict['W'] = pixelmap[(current[0] - 1, current[1])]

		target = pixelmap[current]
		key, value = min(value_dict.items(), key=lambda (_, v): abs(v - target))
		print target, key, value
		# closest = key

		closest = min(distance_dict, key=distance_dict.get)

		if closest == 'N':
			current = (current[0], current[1] - 1)
		elif closest == 'E':
			current = ((current[0] + 1, current[1]))
		elif closest == 'S':
			current = ((current[0], current[1] + 1))
		else:
			current = ((current[0] - 1, current[1]))

		drawn_im.point(current[::-1], fill=pixelmap[current])

# travel(goal_coords[0], goal_coords[1], pixelmap_heightmap)
# travel(connection_list[0][0], connection_list[1][0], pixelmap_heightmap)
for i, goal in enumerate(connection_list):
	if i != 0:
		travel(connection_list[i - 1][0], goal[0], pixelmap_heightmap)
# for i, goal in enumerate(goal_coords):
# 	if i != 0:
# 		travel(goal_coords[i - 1], goal, pixelmap_heightmap)
for goal in goal_coords:
	drawn_im.point(goal[::-1], fill=255)


drawn.show()
drawn.save('siteImages/travelNESWDownhill.tiff')


