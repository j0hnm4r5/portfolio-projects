import rhinoscriptsyntax as rs
import random

surface = rs.GetObject("Pick Bounding Object", 12, preselect=True)

box = rs.BoundingBox(surface)

number = rs.GetReal("Number of Points:", 50)

i=0
while i<number:
	x = random.uniform(box[0][0],box[6][0])
	y = random.uniform(box[0][1],box[6][1])
	z = random.uniform(box[0][2],box[6][2])
	point = rs.AddPoint(x,y,z)
	i+=1
