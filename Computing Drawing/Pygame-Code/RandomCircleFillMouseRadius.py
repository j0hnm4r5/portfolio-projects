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


def black():
    return (0,0,0)

clear()

width = 1

while (1==1):
    t = 0
    while t<=100:
        x = random.uniform(0, windowX)
        y = random.uniform(0, windowY)
        radius = (pygame.mouse.get_pos()[0]+1)/100
        r = random.uniform(0,255)
        g = random.uniform(0,255)
        b = random.uniform(0,255)
        pygame.draw.circle(screen, (r,g,b), (int(x), int(y)), radius, width)
        t += 1

    pygame.display.flip()
    input(pygame.event.get())


