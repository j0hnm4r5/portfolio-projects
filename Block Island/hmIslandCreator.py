import rhinoscriptsyntax as rs
import pickle

with open('siteImages/buildable_islands.pkl', 'r') as p:
	buildable = pickle.load(p)
with open('siteImages/height.pkl', 'r') as p:
	elevation = pickle.load(p)

width = len(buildable[0])
height = len(buildable)

x = 0
y = 0
z = 0

rs.AddLayer(name="ISLAND", color= (0,0,255))

all_objects = rs.ObjectsByType(24)

i = 0
iY = 0
while iY < height:
	iX = 0
	while iX < width:
		if buildable[iY][iX] == 255:
			# print len(all_objects)
			if rs.ObjectLayer(all_objects[i]) == "STEEP" or rs.ObjectLayer(all_objects[i]) == "FLAT":
				rs.ObjectLayer(all_objects[i], "ISLAND")
		iX += 1
		i += 1
	iY += 1