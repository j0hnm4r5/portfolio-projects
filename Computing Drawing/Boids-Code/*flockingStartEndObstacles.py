import rhinoscriptsyntax as rs
import random, math
from operator import itemgetter

"""
For each agent, for each increment of time:
a) Avoid crowding local flockmates. Steer to keep a minimum distance between each agent and the ones around it. In flocking models, a boid (bird/droid) reacts only to flockmates within a certain neighborhood around itself; there is no global steering intelligence. The neighborhood is defined by a distance from the center of the boid and the angle around it, measured by its direction of travel.
b) Align towards the average heading of local flockmates.
c) Cohere to the flock: move toward the center of mass of local flockmates. The center of mass is the average position of all the agents.
"""

class Boid(object):

	SZ_radius = 1
	NZ_radius = 5
	NZ_angle = 270

	separation_factor = 1
	alignment_factor = 1
	cohesion_factor = .1
	avoidance_factor = 10
	striver_factor = 1

	def __init__(self, guid, heading, goal, obstacles):
		""" CREATE A BOID """

		self.guid = guid

		self.position = rs.PointCoordinates(self.guid)
		self.heading = heading

		self.goal = goal

		self.obstacles = obstacles

		self.SZ_neighbors = []
		self.NZ_neighbors = []

		self.NZ_avg_heading = []
		self.NZ_center_of_mass = []

		self.separation_vector = (0,0,0)
		self.alignment_vector = (0,0,0)
		self.cohesion_vector = (0,0,0)
		self.avoidance_vector = (0,0,0)
		self.striver_vector = (0,0,0)

		self.path_pts = []
		self.path_guid = ""
		self.path_pts.append(self.position)

	def get_SZ_neighbors(self, population):
		""" IF AGENT IS WITHIN SZ, MAKE IT AN SZ NEIGHBOR """

		self.SZ_neighbors = []

		for agent in population:
			distance = rs.Distance(self.guid, agent.guid)
			if (distance != 0) and (distance < Boid.SZ_radius):
				self.SZ_neighbors.append(agent)

	def get_NZ_neighbors(self, population):
		""" IF AGENT IS WITHIN NZ, MAKE IT AN NZ NEIGHBOR """

		self.NZ_neighbors = []
		center_cone = rs.VectorReverse(self.heading)

		for agent in population:
			distance = rs.Distance(self.guid, agent.guid)
			if distance != 0:
				agent_angle = rs.VectorAngle(rs.VectorCreate(self.guid, agent.guid), center_cone)
				if (distance < Boid.NZ_radius) and (agent_angle < Boid.NZ_angle / 2):
					self.NZ_neighbors.append(agent)


	def separate(self):
		""" MOVE AWAY FROM NEIGHBORS IN SZ """

		self.separation_vector = (0,0,0)
		if len(self.SZ_neighbors) > 0:

			for neighbor in self.SZ_neighbors:
				self.separation_vector = rs.VectorAdd(rs.VectorCreate(self.position, neighbor.position), self.separation_vector)

			self.separation_vector = rs.VectorDivide(self.separation_vector, len(self.SZ_neighbors))
			self.separation_vector = rs.VectorScale(self.separation_vector, Boid.separation_factor)

	def align(self):
		""" ALIIGN TOWARDS AVERAGE HEADING OF NEIGHBORS """

		self.NZ_avg_heading = (0,0,0)

		if len(self.NZ_neighbors) > 0:
			for neighbor in self.NZ_neighbors:
				self.NZ_avg_heading = rs.VectorAdd(self.NZ_avg_heading, neighbor.heading)

			self.NZ_avg_heading = rs.VectorDivide(self.NZ_avg_heading, len(self.NZ_neighbors))

			self.alignment_vector = rs.VectorScale(self.NZ_avg_heading, Boid.alignment_factor)

	def cohere(self):
		""" MOVE TOWARD THE CENTER OF MASS OF NEIGHBORS """

		self.NZ_center_of_mass = (0,0,0)

		if len(self.NZ_neighbors) > 0:

			for neighbor in self.NZ_neighbors:
				self.NZ_center_of_mass = rs.VectorAdd(self.NZ_center_of_mass, neighbor.position)

			self.NZ_center_of_mass = rs.VectorDivide(self.NZ_center_of_mass, len(self.NZ_neighbors))

			self.cohesion_vector = rs.VectorCreate(self.NZ_center_of_mass, self.position)
			self.cohesion_vector = rs.VectorScale(self.cohesion_vector, Boid.cohesion_factor)

	def avoid(self):
		""" AVOID OBSTACLES """

		if self.obstacles != None:

			avoidance_line = rs.VectorScale(self.heading, Boid.avoidance_factor)
			avoidance_line = rs.AddLine(self.position, rs.PointAdd(self.position, avoidance_line))

			i = 0
			for obstacle in self.obstacles:
				csx = rs.CurveSurfaceIntersection(avoidance_line, obstacle)
				i += 1
				if csx != None:
					break
			else:
				csx = None

			if csx != None:
				centroid = rs.SurfaceAreaCentroid(self.obstacles[i-1])
				centroid = rs.AddPoint(centroid[0])
				self.avoidance_vector = rs.VectorCreate(centroid, self.guid)
				print self.avoidance_vector
				axis = rs.VectorCreate(rs.CurveStartPoint(avoidance_line), rs.CurveEndPoint(avoidance_line))
				self.avoidance_vector = rs.VectorRotate(self.avoidance_vector, 180, axis)
				# print self.avoidance_vector

			else:
				self.avoidance_vector = (0,0,0)

			rs.DeleteObject(avoidance_line)


	def strive(self):
		""" HEAD TOWARDS GOAL """

		self.striver_vector = rs.VectorScale(rs.VectorUnitize(rs.VectorCreate(self.goal, self.position)), Boid.striver_factor)


	def update_heading(self):
		""" AVERAGE SEPARATION, ALIGNMENT, AND COHESION VECTORS """

		self.separate()
		self.align()
		self.cohere()
		self.avoid()
		self.strive()

		self.heading = rs.VectorAdd(self.heading, self.separation_vector)
		self.heading = rs.VectorAdd(self.heading, self.alignment_vector)
		self.heading = rs.VectorAdd(self.heading, self.cohesion_vector)
		self.heading = rs.VectorAdd(self.heading, self.avoidance_vector)
		self.heading = rs.VectorAdd(self.heading, self.striver_vector)
		self.heading = rs.VectorDivide(self.heading, 5)

	def move(self):
		""" MOVE A BOID """

		self.position = rs.PointAdd(self.position, self.heading)
		self.path_pts.append(self.position)
		rs.DeleteObject(self.guid)
		self.guid = rs.AddPoint(self.position)


	def update(self, population):
		""" CHANGE HEADING AND MOVE BOID """

		self.get_SZ_neighbors(population)
		self.get_NZ_neighbors(population)
		self.update_heading()
		self.move()

	def draw_path(self):
		""" DRAW BOID'S PATH """

		if self.path_guid:
			rs.DeleteObject(self.path_guid)
		self.path_guid = rs.AddCurve(self.path_pts)

def main():

	start_line = rs.GetObject("Pick starting line:", 4)
	division_pts = rs.DivideCurve(start_line, 10, False, True)
	population_pts = []
	for pt in division_pts:
		population_pts.append(rs.AddPoint(pt))

	initial_heading = rs.GetObject("Pick initial heading:", 4)
	initial_heading = rs.VectorCreate(rs.CurveEndPoint(initial_heading), rs.CurveStartPoint(initial_heading))

	end_heading = rs.GetObject("Pick end heading:", 4)
	end_heading = rs.VectorCreate(rs.CurveStartPoint(end_heading), rs.CurveEndPoint(end_heading))

	end_line = rs.GetObject("Pick ending line:", 4)
	division_pts = rs.DivideCurve(end_line, 10, False, True)
	goal_pts = []
	for pt in division_pts:
		goal_pts.append(rs.AddPoint(pt))
	easing_goal_pts = rs.CopyObjects(goal_pts, rs.VectorReverse(end_heading))

	obstacles = rs.GetObjects("Pick possible obstacles:", 24)


	population = []
	i = 0
	while i < len(population_pts):
		population.append(Boid(population_pts[i], initial_heading, easing_goal_pts[i], obstacles))
		i += 1

	finished = []
	while len(finished) < len(goal_pts):
		for boid in population:
			if rs.Distance(boid.position, boid.goal) > 2.5:
				boid.update(population)
			else:
				boid.update(population)
				finished.append(boid)
				population.remove(boid)

	coordinate_sum = []
	for boid in finished:
		coordinate_sum.append((boid, boid.position[0] + boid.position[1] + boid.position[2]))

	coordinate_sum = sorted(coordinate_sum, key=itemgetter(1))
	finished, numbers = zip(*coordinate_sum)

	goal_pts.reverse()

	i = 0
	for boid in finished:
		boid.path_pts.append(rs.PointCoordinates(goal_pts[i]))
		i += 1


	for boid in finished:
		boid.draw_path()

	# points = rs.ObjectsByType(1)
	# rs.DeleteObject(points)

main()