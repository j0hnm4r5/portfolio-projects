import rhinoscriptsyntax as rs
import pickle

with open('siteImages/buildable.pkl', 'r') as p:
	buildable = pickle.load(p)
with open('siteImages/height.pkl', 'r') as p:
	elevation = pickle.load(p)

with open('siteImages/buildable_islands.pkl', 'r') as p:
	island = pickle.load(p)

width = len(buildable[0])
height = len(buildable)

x = 0
y = 0
z = 0

def box(x,y,z):
	box = [(x, y, 0), (x, y + 1, 0), (x + 1, y + 1, 0), (x + 1, y, 0), (x, y, z), (x, y + 1, z), (x + 1, y + 1, z), (x + 1, y, z)]
	return box

rs.AddLayer(name="STEEP", color= (255,0,0))
rs.AddLayer(name="FLAT", color=(0,0,0))

iY = 0
while iY < height:
	iX = 0
	while iX < width:
		# print buildable[iY][iX]
		x = iX
		y = iY
		z = elevation[iY][iX] / 10
		if z != 0:
			drawn = rs.AddBox(box(x,y,z))
		else:
			drawn = rs.AddSrfPt([box(x,y,z)[0], box(x,y,z)[1], box(x,y,z)[2], box(x,y,z)[3]])
		if buildable[iY][iX] == 0:
			rs.ObjectLayer(drawn, "FLAT")
			# print "FLAT"
		else:
			rs.ObjectLayer(drawn, "STEEP")
			# print "STEEP"
		iX += 1
	iY += 1