import rhinoscriptsyntax as rs
import sys, os

islands = rs.ObjectsByLayer("ISLAND")

pointlist = []
for island in islands:
	bb = rs.BoundingBox(island)
	point = bb[4]
	pointlist.append(point)

with open('points', 'w') as f:
	f.write("3 \n" + str(len(pointlist)) + "\n")
	for point in pointlist:
		f.write(str(point).replace(",", " ") + '\n')

os.system('qconvex i TO result < points')

with open('result', 'r') as f:
	content = f.readlines()

index_list = []
for line in content:
	line = line.strip(' \n').split(" ")
	index_list.append(line)

index_list = index_list[1:]
for index_set in index_list:
	rs.AddCurve((pointlist[int(index_set[0])], pointlist[int(index_set[1])], pointlist[int(index_set[2])]), 1)
