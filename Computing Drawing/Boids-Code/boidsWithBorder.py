import rhinoscriptsyntax as rs
import random, math

"""
For each agent, for each increment of time:
a) Avoid crowding local flockmates. Steer to keep a minimum distance between each agent and the ones around it. In flocking models, a boid (bird/droid) reacts only to flockmates within a certain neighborhood around itself; there is no global steering intelligence. The neighborhood is defined by a distance from the center of the boid and the angle around it, measured by its direction of travel.
b) Align towards the average heading of local flockmates.
c) Cohere to the flock: move toward the center of mass of local flockmates. The center of mass is the average position of all the agents.
"""

class Boid(object):

	SZ_radius = 10
	NZ_radius = 25
	NZ_angle = 270

	heading_factor = .5
	separation_factor = 1.5
	alignment_factor = 2
	cohesion_factor = .5
	avoidance_factor = 1.5
	node_factor = .5

	def __init__(self, guid, heading, obstacles, nodes):
		""" CREATE A BOID """

		self.guid = guid

		self.position = rs.PointCoordinates(self.guid)
		self.heading = heading

		self.obstacles = obstacles
		self.nodes = nodes

		self.SZ_neighbors = []
		self.NZ_neighbors = []

		self.NZ_avg_heading = []
		self.NZ_center_of_mass = []

		self.separation_vector = (0,0,0)
		self.alignment_vector = (0,0,0)
		self.cohesion_vector = (0,0,0)
		self.avoidance_vector = (0,0,0)
		self.node_vector = (0,0,0)

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

		if len(self.obstacles) == 1:

			avoidance_line = rs.VectorUnitize(self.heading)
			avoidance_line = rs.VectorScale(avoidance_line, Boid.SZ_radius)
			avoidance_line = rs.AddLine(self.position, rs.PointAdd(self.position, avoidance_line))

			ccx = rs.CurveCurveIntersection(avoidance_line, self.obstacles[0])
			if ccx != None:
				centroid = rs.CurveAreaCentroid(self.obstacles[0])
				centroid_distance = rs.Distance(self.position, centroid[0])
				self.avoidance_vector = rs.VectorCreate(centroid[0], self.position)
				if centroid_distance < 75:
					self.avoidance_vector = rs.VectorScale(self.avoidance_vector, Boid.avoidance_factor)
				else:
					self.avoidance_vector = rs.VectorScale(self.avoidance_vector, centroid_distance/10)
			else:
				self.avoidance_vector = (0,0,0)

			rs.DeleteObject(avoidance_line)

	def spin(self):
		""" CIRCLE AROUND NODES """

		node_vector_list = []
		self.node_vector = (0,0,0)

		distance = 1000
		i = 0
		for node in self.nodes:
			temp_distance = rs.Distance(node, self.position)
			if temp_distance < distance:
				distance = temp_distance
				j = i
			i += 1

		self.node_vector = rs.VectorCreate(self.position, self.nodes[j])
		self.node_vector = rs.VectorRotate(self.node_vector, 90, (0,0,1))
		self.node_vector = rs.VectorScale(self.node_vector, Boid.node_factor)


	def update_heading(self):
		""" AVERAGE SEPARATION, ALIGNMENT, AND COHESION VECTORS """

		self.separate()
		self.align()
		self.cohere()
		self.avoid()
		self.spin()

		self.heading = rs.VectorAdd(self.heading, self.separation_vector)
		self.heading = rs.VectorAdd(self.heading, self.alignment_vector)
		self.heading = rs.VectorAdd(self.heading, self.cohesion_vector)
		self.heading = rs.VectorAdd(self.heading, self.avoidance_vector)
		self.heading = rs.VectorAdd(self.heading, self.node_vector)
		self.heading = rs.VectorDivide(self.heading, 5)
		self.heading = rs.VectorScale(self.heading, Boid.heading_factor)

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

def fill(surface):
	box = rs.BoundingBox(surface)

	# number = rs.GetReal("Number of Points:", 50)
	number = 50

	pointlist = []

	i=0
	while i<number:
		x = random.uniform(box[0][0],box[6][0])
		y = random.uniform(box[0][1],box[6][1])
		z = random.uniform(box[0][2],box[6][2])
		point = rs.AddPoint(x,y,z)
		pointlist.append(point)
		i+=1

	return pointlist

def make_nodes(obstacles, node_number):
	nodes = []
	box = rs.BoundingBox(obstacles[0])
	i=0
	while i<node_number:
		x = random.uniform(box[0][0],box[6][0])
		y = random.uniform(box[0][1],box[6][1])
		z = random.uniform(box[0][2],box[6][2])
		node = rs.AddPoint(x,y,z)
		rs.ObjectLayer(node, "Nodes")
		nodes.append(node)
		i+=1
	return nodes



def Main():
	obstacles = rs.GetObjects("Pick Bounding Object", 12, preselect=True)
	population_pts = fill(obstacles[0])

	node_number = random.randint(0,5)
	# node_number = 2
	nodes = make_nodes(obstacles, node_number)

	if node_number == 0:
		steps = 250
	else:
		steps = 100

	initial_heading = rs.VectorCreate((random.uniform(0,10),random.uniform(0,10),0), (0,0,0))

	population = []
	i = 0
	while i < len(population_pts):
		population.append(Boid(population_pts[i], initial_heading, obstacles, nodes))
		i += 1


	for t in range(steps):
		for boid in population:
			boid.update(population)


	for boid in population:
		boid.draw_path()



Main()