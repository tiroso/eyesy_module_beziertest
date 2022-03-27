import pygame
import colorsys
import random

hsvl = [(0,0,0)] * 500
surfaces = [pygame.Surface((10, 10))] * 10

beziers = [[2,360] for _ in range(500)]

#Wie schnell rotieren
# 1: Wieviel Grad drehen, GRADSPEICHER (DO NOT MODIFY), Framesspeicher (DO NOT MODIFY),
rotate = [1,1,0,0]

"""
bezier.py - Calculates a bezier curve from control points. 
 
2007 Victor Blomqvist
Released to the Public Domain
"""
import pygame
from pygame.locals import *

class vec2d(object):
    def __init__(self, x, y):
        self.x = x
        self.y = y    

def compute_bezier_points(vertices, numPoints=None):
    if numPoints is None:
        numPoints = 30
    #if numPoints < 2 or len(vertices) != 4:
    if numPoints < 2:
        return None

    result = []

    b0x = vertices[0][0]
    b0y = vertices[0][1]
    b1x = vertices[1][0]
    b1y = vertices[1][1]
    b2x = vertices[2][0]
    b2y = vertices[2][1]
    b3x = vertices[3][0]
    b3y = vertices[3][1]



    # Compute polynomial coefficients from Bezier points
    ax = -b0x + 3 * b1x + -3 * b2x + b3x
    ay = -b0y + 3 * b1y + -3 * b2y + b3y

    bx = 3 * b0x + -6 * b1x + 3 * b2x
    by = 3 * b0y + -6 * b1y + 3 * b2y

    cx = -3 * b0x + 3 * b1x
    cy = -3 * b0y + 3 * b1y

    dx = b0x
    dy = b0y

    # Set up the number of steps and step size
    numSteps = numPoints - 1 # arbitrary choice
    h = 1.0 / numSteps # compute our step size

    # Compute forward differences from Bezier points and "h"
    pointX = dx
    pointY = dy

    firstFDX = ax * (h * h * h) + bx * (h * h) + cx * h
    firstFDY = ay * (h * h * h) + by * (h * h) + cy * h


    secondFDX = 6 * ax * (h * h * h) + 2 * bx * (h * h)
    secondFDY = 6 * ay * (h * h * h) + 2 * by * (h * h)

    thirdFDX = 6 * ax * (h * h * h)
    thirdFDY = 6 * ay * (h * h * h)

    # Compute points at each step
    result.append((int(pointX), int(pointY)))

    for i in range(numSteps):
        pointX += firstFDX
        pointY += firstFDY

        firstFDX += secondFDX
        firstFDY += secondFDY

        secondFDX += thirdFDX
        secondFDY += thirdFDY

        result.append((int(pointX), int(pointY)))

    return result


def blitRotate(surf, image, pos, originPos, angle):

    # offset from pivot to center
    image_rect = image.get_rect(topleft = (pos[0] - originPos[0], pos[1]-originPos[1]))
    offset_center_to_pivot = pygame.math.Vector2(pos) - image_rect.center
    
    # roatated offset from pivot to center
    rotated_offset = offset_center_to_pivot.rotate(-angle)

    # roatetd image center
    rotated_image_center = (pos[0] - rotated_offset.x, pos[1] - rotated_offset.y)

    # get a rotated image
    rotated_image = pygame.transform.rotate(image, angle)
    rotated_image_rect = rotated_image.get_rect(center = rotated_image_center)

    # rotate and blit the image
    surf.blit(rotated_image, rotated_image_rect)
  
    # draw rectangle around the image
    #pygame.draw.rect(surf, (255, 0, 0), (*rotated_image_rect.topleft, *rotated_image.get_size()),2)


for x in range(0, 500, 1):
    hsvl[x] = (random.randint(0,360),random.randint(0,100),random.randint(0,100))

def hsv2rgb(h,s,v):
    return tuple(round(i * 255) for i in colorsys.hsv_to_rgb(float(h) / 360, float(s) / 100, float(v) / 100))

def hsvcolor(instance,hmin,hmax,hstep,smin,smax,sstep,vmin,vmax,vstep):
    global hsvl
    h = 0
    s = 0
    v = 0
    if bool(random.getrandbits(1)): 
        h = hsvl[instance][0] + random.randint(0,hstep)
        s = hsvl[instance][1] + random.randint(0,sstep)
        v = hsvl[instance][2] + random.randint(0,vstep)
    else:
        h = hsvl[instance][0] - random.randint(0,hstep)
        s = hsvl[instance][1] - random.randint(0,sstep)
        v = hsvl[instance][2] - random.randint(0,vstep)
        
    if h < hmin: h = hmin
    if h > hmax: h = hmax    
    if s < smin: s = smin
    if s > smax: s = smax    
    if v < vmin: v = vmin
    if v > vmax: v = vmax
    
    if hsvl[instance][0] <= (hmin + hstep): h = hsvl[instance][0] + hstep
    if hsvl[instance][0] >= (hmax - hstep): h = hsvl[instance][0] - hstep
    if hsvl[instance][1] <= (smin + sstep): s = hsvl[instance][1] + sstep
    if hsvl[instance][1] >= (smax - sstep): s = hsvl[instance][1] - sstep
    if hsvl[instance][2] <= (vmin + vstep): v = hsvl[instance][2] + vstep
    if hsvl[instance][2] >= (vmax - vstep): v = hsvl[instance][2] - vstep
    
    if h < 0: h = 0
    if h > 360: h = 360
    if s < 0: s = 0
    if s > 100: s = 100
    if v < 0: v = 0
    if v > 100: v = 100
    
    hsvl[instance] = (h,s,v)
    
    rgbcolor = hsv2rgb(h,s,v)

    return rgbcolor
    
def setup(screen, etc) :
    pass

def draw(screen, etc) :
    global beziers,rotate
    
    length = int(etc.knob2*620)
    parts = 4
    partlength = int(length/(parts-1))
    count = int(etc.knob1*4)
    
    
    b=0
    for x in range(0, count, 1):
        control_points = [vec2d(640,360)] * parts
        for y in range(0, parts, 1):
            if y == 0: control_points[y] = vec2d(640,360)
            if y > 0:
                bezierdot = 360 + random.randint((-100-(y*40)),(100+(y*40)))#
                bezierspeed = 5
                if abs(abs(beziers[b][0])-abs(beziers[b][1])) < (bezierspeed*y) + 1: 
                    beziers[b][1] = bezierdot
                if beziers[b][0] > beziers[b][1]: bezierdot = beziers[b][0] - random.randint(0,(bezierspeed*y))
                if beziers[b][0] < beziers[b][1]: bezierdot = beziers[b][0] + random.randint(0,(bezierspeed*y))
                control_points[y] = vec2d(640+(y*partlength),bezierdot)
                beziers[b][0] = bezierdot
            b+=1
        # Unkommentieren für eine hart kodierte bezier linie
        #control_points = [vec2d(640,360), vec2d(807,250), vec2d(974,380), vec2d(1141,520)]
        b_points = compute_bezier_points([(z.x, z.y) for z in control_points])
        surfaces[x] = pygame.Surface((1280, 720), pygame.SRCALPHA)
        pygame.draw.lines(surfaces[x], hsvcolor(x,300,360,3,50,int(etc.knob3*100),2,50,int(etc.knob4*100),2), False, b_points, 10)
        
        # 1: Wieviel Grad drehen, bei wieviel Frames, GRADSPEICHER (DO NOT MODIFY), Framesspeicher (DO NOT MODIFY),

        rotatestep = rotate[0] + int(etc.knob3 *10)
        rotatespeed = rotate[1]
        if rotate[2]>359: rotate[2]=0
        blitRotate(screen, surfaces[x], (640,360), (640,360), int(x*(360/count)+rotate[2]))
        rotate[3]+=1
        if rotate[3]>rotatespeed:
            rotate[2]+=rotatestep
            rotate[3]=0
        
    
