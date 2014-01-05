import rhinoscriptsyntax as rs
import random

def weighted_direction_3d(sigma):
	m = abs(random.gauss(0,sigma))
	n = random.randint(0,7)
	o = random.randint(0,3)
	if m<=1:
		return ((0,0,l), "U", "D")
	elif 1<m<=2:
		if o == 0:
			return ((0,l,l),"UN","DS")
		elif o == 1:
			return ((l,0,l),"UE","DW")
		elif o == 2:
			return ((0,-l,l),"US","DN")
		elif o == 3:
			return ((-l,0,l),"UW","DE")
	elif 2<m<=3:
		if n == 0:
			return ((-l,l,0),"NW","SE")
		elif n == 1:
			return ((-l,0,0),"W","E")
		elif n == 2:
			return ((-l,-l,0),"SW","NE")
		elif n == 3:
			return ((0,-l,0),"S","N")
		elif n == 4:
			return ((l,-l,0),"SE","NW")
		elif n == 5:
			return ((l,0,0),"E","W")
		elif n == 6:
			return ((l,l,0),"NE","SW")
		else:
			return ((0,l,0),"N","S")
	elif 3<m<=4:
		if o == 0:
			return ((0,l,-l),"DN","US")
		elif o == 1:
			return ((l,0,-l),"DE","UW")
		elif o == 2:
			return ((0,-l,-l),"DS","UN")
		elif o == 3:
			return ((-l,0,-l),"DW","UE")
	else:
		return ((0,0,-l), "D", "U")

l=1
sigma = .01

curvelist = []
surfacelist = []
startpoints = []

pt_id = rs.GetObjects("Pick Points:", 1)
surfacelist = rs.GetObjects("Pick Bounding Surfaces:", 8)

for pt in pt_id:
	startpoints.append(rs.PointCoordinates(pt))
	rs.ObjectLayer(pt, "DRAWN")

for p in startpoints:

	x = p[0]
	y = p[1]
	z = p[2]

	last_direction = ((0,0,-l), "U", "D")
	pointlist = [(x,y,z)]
	linelist = []

	i = 0
	while i<=1000 and z<=10:

		direction = weighted_direction_3d(sigma)
		tried_directions = []
		ok_direction = False


		if (direction[1] != last_direction[2]) and (tried_directions.count(direction) == 0):

			temp_x = x + direction[0][0]
			temp_y = y + direction[0][1]
			temp_z = z + direction[0][2]

			pointlist.append((temp_x,temp_y,temp_z))

			curve = rs.AddCurve(pointlist)
			# self_ccx = rs.CurveCurveIntersection(curve)

			# for c in curvelist:
			# 	other_ccx = rs.CurveCurveIntersection(curve,c)
			# 	if other_ccx != None:
			# 		break
			# else:
			# 	other_ccx = None

			for s in surfacelist:
				csx = rs.CurveSurfaceIntersection(curve,s)
				if csx != None:
					break
			else:
				csx = None

			# self_ccx or other_ccx or
			if (csx) != None:
				tried_directions.append(direction)
				sigma = 1.5
				del pointlist[-1]

			else:
				x = temp_x
				y = temp_y
				z = temp_z
				last_direction = direction
				sigma = .5

			rs.DeleteObject(curve)

		i+=1

	curve = rs.AddCurve(pointlist)
	curvelist.append(curve)