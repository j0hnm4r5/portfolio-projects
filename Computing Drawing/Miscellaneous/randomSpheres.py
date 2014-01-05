import rhinoscriptsyntax as rs
import random

points = rs.GetObjects("Pick Centers", 1)

distances = []

i=0
while i<len(points):
	distances = []
	for pt in points:
		distances.append(rs.Distance(points[i],pt))

	distances.sort()

	r = (distances[0] + distances[1] + distances[2]) / 6
	rs.AddSphere(points[i], r)
	i+=1