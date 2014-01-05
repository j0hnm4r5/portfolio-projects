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

def random_gray() :
    g = random.uniform(0,255)
    return (g,g,g)

def random_color():
    return (random.uniform(0,255),random.uniform(0,255),random.uniform(0,255))

def draw_arc(color, x, y, radius, start_deg, end_deg, width):
    rect = (x - radius, y - radius, radius * 2, radius * 2)
    start_rad = math.radians(start_deg)
    end_rad = math.radians(end_deg)

    pygame.draw.arc(screen, color, rect, start_rad, end_rad, width)

clear()

start = -15
end = 30

while (1==1):
    x = -windowX/2
    while (x<=windowX+windowX/2):
        y = 10 * math.cos(math.radians(x))
        pygame.draw.circle(screen, black, (int(x), int(y+(windowY/2))), int(windowY/3), 1)
        # draw_arc(black, x, y+(windowY/2), 100, start+x, end+x, 1)
        x += 10

    pygame.display.flip()
    input(pygame.event.get())


