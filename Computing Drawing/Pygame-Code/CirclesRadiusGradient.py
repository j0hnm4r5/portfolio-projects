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


# Code below here ----------------------------------------------------------------------------------

clear()

r = 0
g = 0
b = 0

radius = 0
width = 1

while (1 == 1):
	x = 0
	while (x <= windowX):
		y = 0
		while (y <= windowY):
			pygame.draw.circle(screen, (r,g,b), (x,y), (x+y+10)/10, width)
			y += 30
		x += 30

	pygame.display.flip()

	input(pygame.event.get())


