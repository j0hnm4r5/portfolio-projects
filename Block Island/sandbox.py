import rhinoscriptsyntax as rs

replacement = rs.GetObject("Pick replacement")
all_objs = rs.GetObjects("Pick objects to replace")

for obj in all_objs:
	bb = rs.BoundingBox(obj)
	rs.DeleteObject(obj)
	rs.CopyObject(replacement, bb[0])