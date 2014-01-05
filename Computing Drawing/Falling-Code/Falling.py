import rhinoscriptsyntax as rs
import random

def weighted_direction(sigma):
	m = random.gauss(0,sigma)
	if 3<m<=4:
		return ((-l,l),"NW","SE")
	elif 2<m<=3:
		return ((-l,0),"W","E")
	elif 1<m<=2:
		return ((-l,-l),"SW","NE")
	elif -1<=m<=1:
		return ((0,-l),"S","N")
	elif -2<=m<-1:
		return ((l,-l),"SE","NW")
	elif -3<=m<-2:
		return ((l,0),"E","W")
	elif -4<=m<-3:
		return ((l,l),"NE","SW")
	else:
		return ((0,l),"N","S")

rs.AddLayer("Curves",(255,0,0))
rs.AddLayer("Line Segments",(0,0,255))

sigma = 1.5
l = 2
curvelist = []
curvelist = rs.GetObjects("Pick lines:", filter=4, preselect=True)
print curvelist


# dx = 0

# while dx<70:

last_direction = weighted_direction(sigma)

x = 0
y = 0

pointlist = [(x,y,0)]
linelist = []

i = 0
while i<100 and y>-70:

	direction = weighted_direction(sigma)

	if direction[1] != last_direction[2]:

		temp_x = x + direction[0][0]
		temp_y = y + direction[0][1]

		pointlist.append((temp_x,temp_y,0))

		curve = rs.AddCurve(pointlist)
		self_ccx = rs.CurveCurveIntersection(curve)

		i = 0
		while i<len(curvelist):
			other_ccx = rs.CurveCurveIntersection(curve,curvelist[i])
			i+=1
		if len(curvelist) == 0:
			other_ccx = None

		if (self_ccx or other_ccx) != None:
			del pointlist[-1]

		else:
			x = temp_x
			y = temp_y
			last_direction = direction

		rs.DeleteObject(curve)

	i+=1

curve = rs.AddCurve(pointlist)
rs.ObjectLayer(curve, "Curves")

curvelist.append(curve)

	# dx+=15
