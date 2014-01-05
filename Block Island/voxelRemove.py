import rhinoscriptsyntax as rs
import random

rs.AddLayer("FOCI")
rs.AddLayer("DELETED")

voxels = rs.ObjectsByLayer("BUILDINGv3")


desired_area = 17000
current_area = len(voxels) * 100
number_to_remove = abs((desired_area - current_area) / 100)



number_of_foci = 6

i = 1
ns = []
while i <= number_of_foci:
	n = random.randint(0, len(voxels)-1)
	while n in ns:
		n = random.randint(0, len(voxels)-1)
	ns.append(n)
	rs.ScaleObject(voxels[n], rs.BoundingBox(voxels[n])[0], (1,1,.1))
	rs.ObjectLayer(voxels[n], "FOCI")
	i += 1

foci = rs.ObjectsByLayer("FOCI")

dels_per_focus = number_to_remove / number_of_foci

for i, focus in enumerate(foci):
	for n in range(int(dels_per_focus / 2)):
		# print ns[i]
		# print voxels[ns[i] + n]
		# print voxels[ns[i] - n]
		rs.ScaleObject(voxels[ns[i] + n], rs.BoundingBox(voxels[ns[i] + n])[0], (1,1,.1))
		rs.ScaleObject(voxels[ns[i] - n], rs.BoundingBox(voxels[ns[i] - n])[0], (1,1,.1))
		rs.ObjectLayer(voxels[ns[i] + n], "DELETED")
		rs.ObjectLayer(voxels[ns[i] - n], "DELETED")