import rhinoscriptsyntax as rs
import operator

def min_dist(start, end):
	n_dist = rs.Distance((start[0], start[1] + 1, start[2]), end)
	s_dist = rs.Distance((start[0], start[1] - 1, start[2]), end)
	e_dist = rs.Distance((start[0] + 1, start[1], start[2]), end)
	w_dist = rs.Distance((start[0] - 1, start[1], start[2]), end)
	index, value = min(enumerate((n_dist, s_dist, e_dist, w_dist)), key=operator.itemgetter(1))
	return index

path = rs.GetObjects("Pick blocks along path in order", 16)
path.append(path[0])

height = rs.BoundingBox(path)[6][2]

voxel_list = []
for block in path:
	bb = rs.BoundingBox(block)
	if bb[4][2] != height:
		raiser = rs.AddBox((bb[4], bb[5], bb[6], bb[7], (bb[4][0], bb[4][1], height), (bb[5][0], bb[5][1], height), (bb[6][0], bb[6][1], height), (bb[7][0], bb[7][1], height)))
	voxel = rs.AddBox(((bb[4][0], bb[4][1], height), (bb[5][0], bb[5][1], height), (bb[6][0], bb[6][1], height), (bb[7][0], bb[7][1], height), (bb[4][0], bb[4][1], height + 1), (bb[5][0], bb[5][1], height + 1), (bb[6][0], bb[6][1], height + 1), (bb[7][0], bb[7][1], height + 1)))
	voxel_list.append(voxel)
print len(voxel_list)


for i, voxel in enumerate(voxel_list[:-1]):
	current_voxel = voxel
	current_dist = rs.Distance(rs.BoundingBox(current_voxel)[0], rs.BoundingBox(voxel_list[i + 1])[0])
	while current_dist > 1:
		end = rs.BoundingBox(voxel_list[i + 1])[0]
		start = rs.BoundingBox(current_voxel)[0]
		direction = min_dist(start, end)
		if direction == 0:
			#north
			current_voxel = rs.CopyObject(current_voxel, (0, 1, 0))
		elif direction == 1:
			#south
			current_voxel = rs.CopyObject(current_voxel, (0, -1, 0))
		elif direction == 2:
			#east
			current_voxel = rs.CopyObject(current_voxel, (1, 0, 0))
		else:
			#west
			current_voxel = rs.CopyObject(current_voxel, (-1, 0, 0))
		current_dist = rs.Distance(rs.BoundingBox(current_voxel)[0], rs.BoundingBox(voxel_list[i + 1])[0])

