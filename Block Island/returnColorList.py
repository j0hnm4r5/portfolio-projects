import rhinoscriptsyntax as rs
import pickle

objs = rs.ObjectsByLayer('ROOMS')

color_list = []

for obj in objs:
	color = rs.ObjectColor(obj)
	if not color in color_list:
		color_list.append(color)

quantity_dict = {}
for color in color_list:
	objs = rs.ObjectsByColor(color)
	quantity_dict[color] = len(objs)

n = 0
for item in quantity_dict:
	n += quantity_dict[item]

print n * 100

# with open('colors.pkl', 'w') as f:
	# pickle.dump(color_list, f, -1)