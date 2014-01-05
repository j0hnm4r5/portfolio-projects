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


def black():
    return (0,0,0)

def white():
    return (255,255,255)

def random_gray() :
    g = random.uniform(0,255)
    return (g,g,g)

def random_color():
    return (random.uniform(0,255),random.uniform(0,255),random.uniform(0,255))


clear()

distance = 10
centerX = windowX/2
point_list = [(centerX,0)]
y = 0
x = centerX

i = 0
t = 0

while (1==1):
    y = 0
    while (y<=windowY):
        if t == 0:
            x = centerX + i
            y += distance
            point_list.append((x,y))
            i += random.uniform(-10,10)
            t = 1
        else :
            x = centerX - i
            y += distance
            point_list.append((x,y))
            i += random.uniform(-10,10)
            t = 0

        pygame.draw.lines(screen, black(), False, point_list, 1)
        pygame.display.flip()
    input(pygame.event.get())


