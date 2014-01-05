import rhinoscriptsyntax as rs
import time, os


# ===============================================================

# constants

# ===============================================================


saveframes = True
framestep = 1

rs.EnableRedraw()

curve_list = rs.GetObjects("Pick Curves:", 4)
line_list = []

eye_spacing = 1.5 #in feet


camera_path_l = rs.GetObject("Pick Camera Path:", 4)

start = rs.CurveStartPoint(camera_path_l)
end = rs.AddPoint(start[0]+eye_spacing,start[1],start[2])
distance = rs.VectorCreate(end, start)

camera_path_r = rs.CopyObject(camera_path_l, distance)

rs.DeleteObject(end)

camera_target = rs.GetObject("Pick Camera Target:", 1)


frames = 36


# ===============================================================

# setups

# ===============================================================


for curve in curve_list:
	divide = rs.DivideCurve(curve, frames-1, False, False)

	segment_list = []
	i = 0
	while i<len(divide)-1:
		segment = rs.TrimCurve(curve, (divide[i],divide[i+1]), False)
		segment_list.append(segment)
		i+=1

	segment_list.reverse()
	line_list.append(segment_list)
	rs.DeleteObject(curve)

zipped = zip(*line_list)

camera_locations_l = rs.DivideCurve(camera_path_l, frames)
camera_locations_r = rs.DivideCurve(camera_path_r, frames)


# ===============================================================

# main movie loop

# ===============================================================


frame = 1

for part in zipped:
	rs.ViewCameraTarget("Animation", camera_locations_l[frame-1], camera_target)
	filename = "Z:\\Users\\johnmars\\Desktop\\IMAGES\\"+format(frame,"05")+"_l.ai"
	rs.Command("-_Export _SelAll _Enter " + filename + " _Enter")
	rs.Command("_SelNone")
	rs.ViewCameraTarget("Animation", camera_locations_r[frame-1], camera_target)
	filename = "Z:\\Users\\johnmars\\Desktop\\IMAGES\\"+format(frame,"05")+"_r.ai"
	rs.Command("-_Export _SelAll _Enter " + filename + " _Enter")
	rs.Command("_SelNone")
	for line in part:
		rs.DeleteObject(line)
	frame+=framestep

rs.ViewCameraTarget("Animation", camera_locations_l[frame], camera_target)
filename = "Z:\\Users\\johnmars\\Desktop\\IMAGES\\"+format(frame,"05")+"_l.ai"
rs.Command("-_Export _SelAll _Enter " + filename + " _Enter")
rs.Command("_SelNone")
rs.ViewCameraTarget("Animation", camera_locations_r[frame], camera_target)
filename = "Z:\\Users\\johnmars\\Desktop\\IMAGES\\"+format(frame,"05")+"_r.ai"
rs.Command("-_Export _SelAll _Enter " + filename + " _Enter")
rs.Command("_SelNone")


# ===============================================================

# end main movie loop

# ===============================================================