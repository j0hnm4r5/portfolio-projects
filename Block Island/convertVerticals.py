import rhinoscriptsyntax as rs

objs = rs.ObjectsByLayer('VERTICALS')

for obj in objs:
	pt = rs.BoundingBox(obj)[0]
	rs.CopyObject(repl, pt)
