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
point_list = [(0,0)]
distance = 10
x = 0

while (1==1):
    while x<=windowX:
        y = 0
        while y<=windowY:
            pixel = pygame.Rect(x,y,distance,distance)
            pygame.draw.rect(screen, random_gray(), pixel, 0)
            y += distance
        x += distance
    pygame.display.flip()
    input(pygame.event.get())


