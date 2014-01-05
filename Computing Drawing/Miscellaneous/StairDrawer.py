import rhinoscriptsyntax as rs
import math

#########################
# CLASSES AND FUNCTIONS #
#########################


class Room(object):

	def __init__(self, room_name, room_guid):
		self.room_name = room_name
		self.room_guid = room_guid
		self.room_attachments = [room_guid]
		print "Made " + str(self.room_name) + "!"

	def assignLeftLanding(self, landing_left_guid, stair_left_edge):
		self.landing_left_guid = landing_left_guid
		self.stair_left_edge = stair_left_edge
		self.room_attachments.append(landing_left_guid)
		self.room_attachments.append(stair_left_edge)
		print "Assigned left landing!"

	def assignRightLanding(self, landing_right_guid, stair_right_edge):
		self.landing_right_guid = landing_right_guid
		self.stair_right_edge = stair_right_edge
		self.room_attachments.append(landing_right_guid)
		self.room_attachments.append(stair_right_edge)
		print "Assigned right landing!"

	def move(self, dx, dy, dz):
		rs.MoveObjects(self.room_attachments, (dx, dy, dz))
		print "Moved room!"


def drawStairs(static_room, moving_room):
	start_coord = rs.PointCoordinates(static_room.stair_right_edge)
	end_coord = rs.PointCoordinates(moving_room.stair_left_edge)

	dX = abs(end_coord[0] - start_coord[0])
	print "Original dX = " + str(dX)

	dZ = abs(end_coord[2] - start_coord[2])
	print "Original dZ = " + str(dZ)

	remainder_run = dX % run
	print remainder_run

	if remainder_run != 0:
		if start_coord[2] < end_coord[2]:
			if remainder_run < run - remainder_run:
				moving_room.move(-remainder_run, 0, 0)
				end_coord = rs.PointCoordinates(moving_room.stair_left_edge)
			else:
				moving_room.move(run - remainder_run, 0, 0)
				end_coord = rs.PointCoordinates(moving_room.stair_left_edge)
		else:
			if remainder_run < rise - remainder_run:
				moving_room.move(run - remainder_run, 0, 0)
				end_coord = rs.PointCoordinates(moving_room.stair_left_edge)
			else:
				moving_room.move(-remainder_run, 0, 0)
				end_coord = rs.PointCoordinates(moving_room.stair_left_edge)

	dX = abs(end_coord[0] - start_coord[0])
	print "Adjusted dX = " + str(dX)

	number_runs = int(dX/run)
	print "Number of Treads = " + str(number_runs)

	if start_coord[2] < end_coord[2]:
		moving_room.move(0, 0, number_runs * rise - dZ)
	else:
		moving_room.move(0, 0, -number_runs * rise + dZ)

	dZ = abs(end_coord[2] - start_coord[2])
	print "Adjusted dZ = " + str(dZ)

	rise_vector = rs.VectorCreate((0,0,rise), (0,0,0))
	run_vector = rs.VectorCreate((run,0,0), (0,0,0))

	step_pointlist = [static_room.stair_right_edge]

	if start_coord[2] < end_coord[2]:
		if dZ < 12:
			for step in range(number_runs):
				step_pointlist.append(rs.CopyObject(step_pointlist[-1], rise_vector))
				step_pointlist.append(rs.CopyObject(step_pointlist[-1], run_vector))
		else:
			for step in range(number_runs):
				step_pointlist.append(rs.CopyObject(step_pointlist[-1], rise_vector))
				step_pointlist.append(rs.CopyObject(step_pointlist[-1], run_vector))
			print "Too many stairs!"
	else:
		if dZ < 12:
			for step in range(number_runs):
				step_pointlist.append(rs.CopyObject(step_pointlist[-1], rs.VectorReverse(rise_vector)))
				step_pointlist.append(rs.CopyObject(step_pointlist[-1], run_vector))
		else:
			for step in range(number_runs):
				step_pointlist.append(rs.CopyObject(step_pointlist[-1], rs.VectorReverse(rise_vector)))
				step_pointlist.append(rs.CopyObject(step_pointlist[-1], run_vector))
			print "Too many stairs!"

	rs.AddCurve(step_pointlist, 1)
	rs.DeleteObjects(step_pointlist)
	print "Drew stairs!"


#########################
#       VARABLES        #
#########################

rise = 7.5 #in
run = 11 #in

stair_slope = math.degrees(math.atan(rise/run))
rise = rise/12
run = run/12

#########################
#         CODE          #
#########################

# room = Room("Bedroom", rs.GetObject("Pick room:", 16)) #3D
# room.assignLanding(rs.GetObject("Pick landing:", 8), rs.GetObject("Pick stair edge of landing:", 4)) #3D

room1 = Room("Room One", rs.GetObject("Pick Room One:", 4)) #2D
room1.assignLeftLanding(rs.GetObject("Pick left landing:", 4), rs.GetObject("Pick stair edge of landing:", 1)) #2D
room1.assignRightLanding(rs.GetObject("Pick right landing:", 4), rs.GetObject("Pick stair edge of landing:", 1)) #2D

room2 = Room("Room Two", rs.GetObject("Pick Room Two:", 4)) #2D
room2.assignLeftLanding(rs.GetObject("Pick left landing:", 4), rs.GetObject("Pick stair edge of landing:", 1)) #2D
room2.assignRightLanding(rs.GetObject("Pick right landing:", 4), rs.GetObject("Pick stair edge of landing:", 1)) #2D

room3 = Room("Room Two", rs.GetObject("Pick Room Three:", 4)) #2D
room3.assignLeftLanding(rs.GetObject("Pick left landing:", 4), rs.GetObject("Pick stair edge of landing:", 1)) #2D
room3.assignRightLanding(rs.GetObject("Pick right landing:", 4), rs.GetObject("Pick stair edge of landing:", 1)) #2D

drawStairs(room1, room2)
drawStairs(room2, room3)

