import pygame, sys, os, random, math, time
from pygame.locals import *

fileCount = 0
pygame.init()
windowX = 700
windowY = 800
window = pygame.display.set_mode((windowX, windowY))
pygame.display.set_caption('COMPUTING DRAWING')
screen = pygame.display.get_surface()

def clear():
	screen = pygame.display.get_surface()
	screen.fill((255,255,255))


def input(events):
	for event in events:
		if event.type == QUIT:
			pygame.quit()
			sys.exit()
		elif event.type ==  pygame.KEYDOWN and ((event.key == pygame.K_RETURN) or (event.key == pygame.K_KP_ENTER)):
			global fileCount
			screen = pygame.display.get_surface()
			filePath = './image'+str(int(time.time()))+'_'+str(fileCount) + '.jpg'
			print 'now saving image' + filePath
			pygame.image.save(screen, filePath)
			fileCount = fileCount+1


# Code below here -------------------------------------------------------------------

clear()

def random_color():
	return (random.uniform(0, 255), random.uniform(0, 255), random.uniform(0, 255))
def black():
	return (0, 0, 0)

radius = 50
width = 1

t = 0
w = h = 10

point_list = [(0,0)]

while (1 == 1):
	x = 0
	while (x <= windowX):
		y = 0
		while (y <= windowY):
			if t%10 == 0:
				point_list.append((x,y))

			color = black()

			Rect = pygame.Rect(x, y, w, h)
			pygame.draw.rect(screen, color, Rect, width)

			# pygame.draw.circle(screen, color, (x,y), radius, width)

			t += 5
			y += 50

		x += 30

	pygame.draw.lines(screen, (255,0,0), False, point_list, 2)
	pygame.display.flip()
	input(pygame.event.get())


