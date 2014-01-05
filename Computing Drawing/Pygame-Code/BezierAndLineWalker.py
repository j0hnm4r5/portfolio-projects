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

t = 0

N = 0
E = 1
S = 2
W = 3

L = 0
C = 1
R = 2

distance = 100

x = int(windowX/2)
y = int(windowY/2)

pointlist = [(x,y)]

while (1==1):

    # Preliminary Direction
    if t==0:
        n = random.randint(0,3)
        if n == N:
            y -= distance
        elif n == E:
            x += distance
        elif n == S:
            y += distance
        else:
            x -+ distance
        pointlist.append((x,y))

    last_pt = pointlist[-1]
    second_last_pt = pointlist[-2]


    if t>0:

        # Determine direction traveled
        if last_pt[1] < second_last_pt[1]:
            direction = N
        if last_pt[0] > second_last_pt[0]:
            direction = E
        if last_pt[1] > second_last_pt[1]:
            direction = S
        if last_pt[0] < second_last_pt[0]:
            direction = E
        # print direction

        # Choose Next Point
        r = random.randint(0,2)
        if r == L:
            if direction == N:
                x -= distance
            elif direction == E:
                y -= distance
            elif direction == S:
                x += distance
            else:
                y += distance
        elif r == C:
            if direction == N:
                y += distance
            elif direction == E:
                x += distance
            elif direction == S:
                y -= distance
            else:
                x -= distance
        else:
            if direction == N:
                x += distance
            elif direction == E:
                y += distance
            elif direction == S:
                x -= distance
            else:
                y -= distance

        pointlist.append((x,y))

    # EITHER LINE OR BEZIER
    # pygame.draw.line(screen, random_color(), pointlist[-2], pointlist[-1], 1)
    bezier(pointlist, random_color(), 1)

    t += 1

    pygame.display.flip()
    input(pygame.event.get())
    # clear()