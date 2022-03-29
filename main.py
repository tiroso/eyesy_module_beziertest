import pygame
import colorsys
import random
import itertools
import math
import time


hsvl = [(random.randint(0,360),random.randint(0,100),random.randint(0,100)) for _ in range(100 * 30 * 4)]
beziers = [[random.randint(0,360),random.randint(0,360)] for _ in range(100 * 30)]
rotate = [0,0]
cooldowntimer = [[0,0] for _ in range(100)]
linebuffer=[]
circlebuffer=[]
last_screen = None

def add_to_buffer( array,leng, value ):
    global linebuffer,circlebuffer
    if array == "line":
        if len(linebuffer)==leng and leng>0: linebuffer.pop( 0 )
        linebuffer.append( value )
    if array == "circle":
        if len(circlebuffer)==10000 and leng>0: circlebuffer.pop( 0 )
        circlebuffer.append( value )

def mapFromTo(x,a,b,c,d):
    #x:input value; 
    #a,b:input range
    #c,d:output range
    #y:return value
    try:
        y=(x-a)/(b-a)*(d-c)+c
        return y
    except:
        return 0

def advance(iterator, step):
    next(itertools.islice(iterator, step, step), None)


def tuplewize(iterable, size):
    iterators = itertools.tee(iterable, size)
    for position, iterator in enumerate(iterators):
        advance(iterator, position)
    return zip(*iterators)
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
    global beziers,rotate,cooldowntimer,linebuffer,circlebuffer,last_screen
    
    #Anzahl der Bezier linien
    max_bezier_lines = int(etc.knob1*30) 
    #Maximale Laenge der Bezier linien
    max_bezier_length = 620
    #Lange der Bezierlinien wird durch Audio beeinflusst - 0 deaktiviert - 1 aktiviert
    bezieraudio_length = 1
    bezieraudio_maxvol = int(etc.knob3*16200) 
    bezieraudiocooldown_step = 50
    bezieraudiocooldown_speed = 1
    #Minimal Laenge der Bezier linien
    min_bezier_length = 50
    #Maximal bewegungs innerhalb einer Bezierkurve
    bezier_inner_move = 5
    # starke des beziertrails 0 - 255
    bezier_trail=253
    #wie weit darf sich die bezierkurve von der ujrsprungslinie entfernen
    bezier_max_out = 100
    #jeder abschnitt darf sich um einen faktor mit sich selber sich nochmals weiter entfernen
    bezier_max_out_multi = 40
    # statische bezier lines zum testen - 1 aktiv - 0 inaktiv
    static_bezier_lines = 0 
    #Start Dicke der Bezierlinien
    bezier_start_thickness = 1 
    #Dicke der Bezierlinie nach aussen- Linear nicht exponentiell
    bezier_thicker = 2 
    #Bezier Connectoren sind kreise zwischen den linien- 1 mit kreisen - 0 ohne kreise
    bezier_connector = 1
    #Farbmodus der Bezierblume
    # - 0 Alle Straenge gleiche Farbe
    # - 1 Jeder Strang eine eigene Farbe
    # - 2 Jeder Teilabschnitt jeden Strangs eine eigene Farbe
    # - 3 Audio ausschlag farbe
    bezier_color_mode = 0
    bezier_min_hue=0
    bezier_max_hue=360
    bezier_min_saturation=80
    bezier_max_saturation=100
    bezier_min_value=60
    bezier_max_value=100
    #Farbsettings der Hintergrundfarbe
    bg_min_hue=0
    bg_max_hue=360
    bg_min_saturation=80
    bg_max_saturation=100
    bg_min_value=60
    bg_max_value=100
    #Positionierung der Bezierblume - x-Achse
    bezier_x = etc.xres / 2 
    #Positionierung der Bezierblume - y-Achse
    bezier_y = etc.yres / 2 
    # rotationsparameter - Sprungweite in Grad
    rotatestep = 1 
    #rotationsparameter - Bei wieviel gezaehlten Frames soll gesprungen werden
    rotatespeed = 1 + int(etc.knob2 *29)
    
    
    # DO NOT MODIFY
    bezier_line_counter=0
    bezier_linepart_counter=0
    
    if last_screen==None:
        last_screen = pygame.Surface((1280, 720))
        last_screen = last_screen.convert_alpha()
        last_screen.fill((0, 0, 0, 0))
    working_screen = pygame.Surface((1280, 720))
    working_screen = last_screen.convert_alpha()
    working_screen.fill((0, 0, 0, 0))
    last_screen.set_alpha(bezier_trail)
    working_screen.blit(last_screen, (0,0))
    
    if etc.knob4 < 1.0 and etc.knob4 > 0.0:
        bezier_min_hue=((etc.knob4*360)+1) % 360
        bezier_max_hue=(bezier_min_hue+50) % 360
    if etc.knob4 == 0: 
        bezier_min_hue=((math.sin(time.time()))*360) % 360
        bezier_max_hue=(bezier_min_hue+10) % 360
    
    bgcolor = hsvcolor(len(hsvl)-1,bg_min_hue,bg_max_hue,5,bg_min_saturation,bg_max_saturation,2,bg_min_value,bg_max_value,2)    
    if etc.knob5 < 0.9 and etc.knob5 > 0.0:
        bgcolor=hsv2rgb(((etc.knob5*360)+1) % 360,100,100)
    if etc.knob5 < 1.0 and etc.knob5 >= 0.9:
        bg_min_hue=((math.sin(time.time()))*720) % 360
        bg_max_hue=(bg_min_hue+10) % 360
        bgcolor = hsvcolor(len(hsvl)-1,bg_min_hue,bg_max_hue,5,bg_min_saturation,bg_max_saturation,2,bg_min_value,bg_max_value,2)
    if etc.knob5 ==0.0:
        bgcolor=(0,0,0)
    
    etc.bg_color = bgcolor
    
    #for x in (linebuffer):
        # screen, color, tuple(rotatepoint1),tuple(rotatepoint2), int(lt)
        #pygame.draw.line((xs for xs in x))
        #pygame.draw.line(x[0],x[1],x[2],x[3],x[4])
    
    for x in range(0, max_bezier_lines, 1):
        bezier_length = max_bezier_length
        min_audio_channel = math.floor(x*(100/max_bezier_lines))
        max_audio_channel = math.floor((x+1)*(100/max_bezier_lines))
        avg=0
        for i in range(min_audio_channel, max_audio_channel) :
            avg = abs(etc.audio_in[i]) + avg
        avg = avg / (max_audio_channel-min_audio_channel)
        avg+=1
        if bezier_color_mode == 3:
            bezier_min_hue=mapFromTo(avg,0,bezieraudio_maxvol,bezier_min_hue,bezier_max_hue)
            bezier_max_hue=mapFromTo(avg,0,bezieraudio_maxvol,bezier_min_hue,bezier_max_hue)
        avg = mapFromTo(avg,0,bezieraudio_maxvol,0,max_bezier_length)

        if bezieraudio_length:
            bezier_length = cooldowntimer[x][0]
            if avg > cooldowntimer[x][0]:
                cooldowntimer[x][0]=avg
                cooldowntimer[x][1]=0
                bezier_length = cooldowntimer[x][0]
            if cooldowntimer[x][1] >= bezieraudiocooldown_speed:
                cooldowntimer[x][1]=0
                bezier_length = cooldowntimer[x][0]
                cooldowntimer[x][0]-=bezieraudiocooldown_step
                if cooldowntimer[x][0]<0: cooldowntimer[x][0]=0
            cooldowntimer[x][1]+=1
            
        parts = 4
        if bezier_length<min_bezier_length: bezier_length=min_bezier_length
        partlength = int(bezier_length/(parts-1))
        control_points = [vec2d(bezier_x,bezier_y)] * parts
        for y in range(0, parts, 1):
            if y == 0: control_points[y] = vec2d(bezier_x,bezier_y)
            if y > 0:
                bezierdot = bezier_y + random.randint((-(bezier_max_out)-(y*bezier_max_out_multi)),((bezier_max_out)+(y*bezier_max_out_multi)))#
                if abs(abs(beziers[bezier_line_counter][0])-abs(beziers[bezier_line_counter][1])) < (bezier_inner_move*y) + 1: 
                    beziers[bezier_line_counter][1] = bezierdot
                if beziers[bezier_line_counter][0] > beziers[bezier_line_counter][1]: bezierdot = beziers[bezier_line_counter][0] - random.randint(0,(bezier_inner_move*y))
                if beziers[bezier_line_counter][0] < beziers[bezier_line_counter][1]: bezierdot = beziers[bezier_line_counter][0] + random.randint(0,(bezier_inner_move*y))
                control_points[y] = vec2d(bezier_x+(y*partlength),bezierdot)
                beziers[bezier_line_counter][0] = bezierdot
            bezier_line_counter+=1
        if static_bezier_lines: control_points = [vec2d(640,360), vec2d(807,250), vec2d(974,380), vec2d(1141,520)]
        b_points = compute_bezier_points([(z.x, z.y) for z in control_points])

        if bezier_color_mode == 0:
            color_instance=0
        elif bezier_color_mode == 1:
            color_instance=x
        elif bezier_color_mode == 2:
            color_instance=bezier_linepart_counter
        else:
            color_instance=0
        lt=bezier_start_thickness
        for z in tuplewize(b_points, 2):
            if bezier_color_mode == 2:
                color_instance=bezier_linepart_counter
            bezier_linepart_counter+=1
            lt+=bezier_thicker
            color = hsvcolor(color_instance,bezier_min_hue,bezier_max_hue,5,bezier_min_saturation,bezier_max_saturation,2,bezier_min_value,bezier_max_value,2)
            
            startpoint = pygame.math.Vector2(bezier_x, bezier_y)
            endpoint1 = pygame.math.Vector2(z[0][0]-bezier_x,z[0][1]-bezier_y)
            endpoint2 = pygame.math.Vector2(z[1][0]-bezier_x,z[1][1]-bezier_y)
            rotatepoint1 = startpoint + endpoint1.rotate(int(x*(360/max_bezier_lines))+rotate[0] % 360)
            rotatepoint2 = startpoint + endpoint2.rotate(int(x*(360/max_bezier_lines))+rotate[0] % 360)
            pygame.draw.line(working_screen, color, tuple(rotatepoint1),tuple(rotatepoint2), int(lt))
            add_to_buffer( "line", x*100, (screen, color, tuple(rotatepoint1),tuple(rotatepoint2), int(lt) ))
            if bezier_connector: 
                pygame.draw.circle(working_screen, color, rotatepoint1, int(lt/2)-2)
                add_to_buffer( "circle",x*100*20, (screen, color, rotatepoint1, int(lt/2)-2))
                pygame.draw.circle(working_screen, color, rotatepoint2, int(lt/2)-2)
                add_to_buffer( "circle",x*100*20, (screen, color, rotatepoint2, int(lt/2)-2))
        rotate[1]+=1
        if rotate[1]>=rotatespeed:
            rotate[0]=rotate[0]+rotatestep % 360
            rotate[1]=0
    last_screen = working_screen
    screen.blit(working_screen, (0,0))
