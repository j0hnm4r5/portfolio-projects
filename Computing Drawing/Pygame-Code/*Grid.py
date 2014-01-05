import pygame, sys, os, random, math, time
from pygame.locals import *

fileCount = 0
pygame.init()
dpi = 72
windowX = 10.5 * dpi
windowY = 12 * dpi
window = pygame.display.set_mode((int(windowX), int(windowY)))
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

def screenshot():
    global fileCount
    screen = pygame.display.get_surface()
    filePath = './image'+str(int(time.time()))+'_'+str(fileCount) + '.png'
    print 'now saving image' + filePath
    pygame.image.save(screen, filePath)
    fileCount = fileCount+1

def random_color():
    return (random.uniform(0, 255), random.uniform(0, 255), random.uniform(0, 255))

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

clear()
while 1==1:
    pointlist = []

    y=0
    while y<=windowY:
        x=0
        row = []
        while x<=windowX:
            if x<windowX/20+10*random.gauss(0,2) or x>windowX-windowX/20+10*random.gauss(0,2):
                row.append((x,y))
            else:
                row.append((x,y + random.gauss(0,y/50)))
            x+=50
        pointlist.append(row)
        y+=20
    # print pointlist[1]
    # print pointlist

    t = 0
    for list in pointlist:
        # connect_points(list, black, 1)
        bezier(list, black, 1)
        t+=1
        # for l in list:
        #     pygame.draw.circle(screen, black, l, 2, 0)



    pygame.display.flip()
    input(pygame.event.get())
    clear()
