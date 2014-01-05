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
            filePath = '/image'+str(int(time.time()))+'_'+str(fileCount) + '.png'
            print 'now saving image' + filePath
            pygame.image.save(screen, filePath)
            fileCount = fileCount+1



#Code below here ----------------------------------------------


def black():
    return (0,0,0)

clear()
radius = 10
width = 0
t = 0
x = 0
y = 0

while (1==1):
    while t<=10:
        x = int(random.uniform(0, windowX))
        y = int(random.uniform(0, windowY))
        r = 0
        g = 0
        b = 0
        radius = int(random.uniform(width, 40))
        pygame.draw.circle(screen, black(), (x,y), radius, width)
        while y>0 and radius>width and r<=255 and g<=255 and b<=255:
            pygame.draw.circle(screen, (r,g,b), (x,y), radius, width)
            radius -= 1
            y -= 3
            r += 15
            g += 1
            b += 1
        pygame.draw.line(screen, black(), (0,0), (x,y), 1)
        pygame.draw.line(screen, black(), (0,windowY), (x,y), 1)
        pygame.draw.line(screen, black(), (windowX,0), (x,y), 1)
        pygame.draw.line(screen, black(), (windowX,windowY), (x,y), 1)
        t += 1

        pygame.display.flip()
    input(pygame.event.get())


