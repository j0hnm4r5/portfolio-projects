# This script assumes rhino units set to inches and the drawing scaled to the size of the paper
# Everything is drawn with Pen 1

import rhinoscriptsyntax as rs
import time
hpglOut = file('./output' + str(int(time.time())) + '.hpgl', 'w')
allCurves = rs.ObjectsByType(4)

hpglOut.write('IN;\n')
hpglOut.write('SP1;\n')

#first explode any polycurves (that aren't polylines)
for curve in allCurves:
	if (rs.CurveDegree(curve) == 2 or rs.CurveDegree(curve) == 3) and rs.IsPolyCurve(curve):
		rs.ExplodeCurves(curve, True)

allCurves = rs.ObjectsByType(4)

for curve in allCurves:
	if rs.CurveDegree(curve) == 1: #polyline or line
		points = rs.CurveEditPoints(curve)
		#print 'line'
	elif rs.CurveDegree (curve) == 2 or rs.CurveDegree (curve) == 3: #curvy curve
		points = rs.DivideCurveLength(curve, .01)
		#print 'curvy'
	if not points:
		#print 'found one very tiny curve, which is not exported'
		continue
	#pen up to the first point on line
	x = points[0][0]
	y = points[0][1]
	hpglOut.write('PU' + str(int(x*1000)) + ',' + str(int(y*1000)) + ';\n')
	#pen down to every subsequent point
	i = 1
	while i<len(points):
		x = points[i][0]
		y = points[i][1]
		hpglOut.write('PD' + str(int(x*1000)) + ',' + str(int(y*1000)) + ';\n')
		i += 1

hpglOut.write('SP0;\n')
hpglOut.close()