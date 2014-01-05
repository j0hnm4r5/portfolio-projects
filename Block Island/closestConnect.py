import rhinoscriptsyntax as rs

islands = rs.ObjectsByLayer("ISLAND-4")

pointlist = []
for island in islands:
	bb = rs.BoundingBox(island)
	point = bb[4]
	pointlist.append(point)

for point in pointlist:
	distances = []
	for i, p in enumerate(pointlist):
		dist = rs.Distance(point, p)
		if dist != 0:
			distances.append((i, dist))
	distances = sorted(distances, key=lambda distance: distance[1])
	rs.AddCurve((pointlist[distances[0][0]] , point), 1)
	# rs.AddCurve((pointlist[distances[1][0]] , point), 1)
	# rs.AddCurve((pointlist[distances[2][0]] , point), 1)