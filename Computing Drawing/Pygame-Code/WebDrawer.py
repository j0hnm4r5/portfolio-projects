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
            filePath = './image'+str(int(time.time()))+'_'+str(fileCount) + '.jpg'
            print 'now saving image' + filePath
            pygame.image.save(screen, filePath)
            fileCount = fileCount+1


#Code below here ----------------------------------------------


black = (0,0,0)

white = (255,255,255)

clear()

all_points = []

while (1==1):
    pos = pygame.mouse.get_pos()
    x1 = pos[0]
    y1 = pos[1]

    i = 0
    while i<len(all_points):
        x2 = all_points[i][0]
        y2 = all_points[i][1]
        dist = math.sqrt((x2-x1)**2+(y2-y1)**2)
        if dist < 100:
            pygame.draw.line(screen, black, pos, (x2,y2), 1)
        i += 1

    pygame.display.flip()


    input(pygame.event.get())
    all_points.append(pos)
    time.sleep(.05)


