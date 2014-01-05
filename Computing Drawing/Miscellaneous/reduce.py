import rhinoscriptsyntax as rs

objects = rs.GetObjects("Pick Objects", preselect=True)
count = rs.GetInteger("Reduce by:", minimum=2, maximum=len(objects))

i = 0
for thing in objects:
	is_reduced = i%count
	if is_reduced == 0:
		rs.DeleteObject(thing)
	i += 1