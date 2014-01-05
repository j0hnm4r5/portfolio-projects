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
    screen.fill((255, 255, 255))


def input(events):
    for event in events:
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        elif event.type ==  pygame.KEYDOWN and ((event.key == pygame.K_RETURN) or (event.key == pygame.K_KP_ENTER)):
            global fileCount
            screen = pygame.display.get_surface()
            filePath = './image'+str(int(time.time()))+'_'+str(fileCount) + '.png'
            print 'now saving image' + filePath
            pygame.image.save(screen, filePath)
            fileCount = fileCount+1


#Code below here ----------------------------------------------

def create_control_pts(n):
	control_pts = []
	i = 0
	while i<n:
		x = random.randint(0,windowX)
		y = random.randint(0,windowY)
		control_pts.append((x,y))
		i += 1
	return control_pts

def binom_coeff(n, k):
	return math.factorial(n)/(math.factorial(k)*math.factorial(n-k))

def connect_points(pts, color, w):
    first_pt = pts[0]
    i = 1
    while i<len(pts):
        next_pt = pts[i]
        pygame.draw.aaline(screen, color, first_pt, next_pt, w)
        first_pt = next_pt
        i += 1

def bezier(control_pts, color, w):
	n = len(control_pts)
	pointlist = []
	t = 0
	while t<=1:
		prevX = 0
		prevY = 0
		i = 0
		while i<n:
			x = (binom_coeff(n, i) * (1 - t)**(n-i) * t**i * control_pts[i][0]) + prevX
			y = (binom_coeff(n, i) * (1 - t)**(n-i) * t**i * control_pts[i][1]) + prevY
			prevX = x
			prevY = y
			i += 1
		x += t**n * control_pts[n-1][0]
		y += t**n * control_pts[n-1][1]
		pointlist.append((x,y))
		t += .01
	connect_points(pointlist,color,w)

black = (0,0,0)
gray = (150,150,150)

n = 6
control_pts = create_control_pts(n)

clear()

while (1==1):

	bezier(control_pts, black, 2)

	pygame.display.flip()
	input(pygame.event.get())
	clear()