import pprint

class Room(object):
	def __init__(self, use, category, area):
		self.use = use
		self.category = category
		self.area = area
		self.attract = []
		self.repel = []

		self.name = self.use + "_" + self.category

def connect(room1, room2, attract=True):
	if attract == True:
		room1.attract.append(room2.name)
		room2.attract.append(room1.name)
	else:
		room1.repel.append(room2.name)
		room2.repel.append(room1.name)


def make_room(use, category, area, attract=[], repel=[]):
	room_dict['temp'] = Room(use, category, area)
	room_dict[room_dict['temp'].name] = room_dict['temp']
	del room_dict['temp']

room_dict = {}

# HOUSING
make_room('digital', 'house', 600)
make_room('paint', 'house', 600)
make_room('sculpt', 'house', 600)
make_room('write', 'house', 600)
make_room('photo', 'house', 600)

# STUDIO / WORKSHOP
make_room('digital', 'work', 900)
make_room('paint', 'work', 1200)
make_room('sculpt', 'work', 1200)
make_room('write', 'work', 300)
make_room('photo', 'work', 900)

# PUBLIC
make_room('gallery', 'public', 1500)
make_room('lecture', 'public', 1500)
make_room('dining', 'public', 700)
make_room('library', 'public', 600)
make_room('bathroom', 'public', 300)
make_room('education', 'public', 900)
make_room('lobby', 'public', 500)


# ADMINISTRATION
make_room('storage', 'admin', 500)
make_room('office', 'admin', 300)
make_room('kitchen', 'admin', 300)
make_room('mechanical', 'admin', 1500)

# OUTDOOR
make_room('performance', 'outdoor', 1500)
make_room('project', 'outdoor', 1200)
make_room('sculptures', 'outdoor', 2000)
make_room('parking', 'outdoor', 1800)



# CONNECTIONS

# connect work/house
for room1 in room_dict.values():
	if room1.category == 'house':
		for room2 in room_dict.values():
			if room2.category == 'work':
				if room2.use == room1.use:
					connect(room_dict[room1.name], room_dict[room2.name])

connect(room_dict['paint_house'], room_dict['sculpt_house'])
connect(room_dict['paint_work'], room_dict['sculpt_work'])

# repel public/work&house
for room1 in room_dict.values():
	if room1.category == 'house' or room1.category == 'work':
		for room2 in room_dict.values():
			if room2.category == 'public':
				connect(room_dict[room1.name], room_dict[room2.name], False)


connect(room_dict['lobby_public'], room_dict['bathroom_public'])
connect(room_dict['lobby_public'], room_dict['dining_public'])
connect(room_dict['lobby_public'], room_dict['gallery_public'])
connect(room_dict['lobby_public'], room_dict['lecture_public'])
connect(room_dict['lobby_public'], room_dict['education_public'])

connect(room_dict['kitchen_admin'], room_dict['dining_public'])
connect(room_dict['library_public'], room_dict['education_public'])