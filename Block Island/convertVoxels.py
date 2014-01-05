import rhinoscriptsyntax as rs

repl = rs.GetObjects('Pick Replacement Object')
objs = rs.ObjectsByLayer('FRAMES')

for obj in objs:
	pt = rs.BoundingBox(obj)[0]
	rs.CopyObject(repl, pt)
