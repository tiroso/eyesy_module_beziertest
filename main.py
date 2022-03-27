import pygame
import colorsys
import random
import bezier

hsvl = [(0,0,0)] * 500
surfaces = [pygame.Surface((10, 10))] * 10

beziers = [[2,360] for _ in range(500)]

#Wie schnell rotieren
# 1: Wieviel Grad drehen, GRADSPEICHER (DO NOT MODIFY), Framesspeicher (DO NOT MODIFY),
rotate = [1,1,0,0]

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
        control_points = [bezier.vec2d(640,360)] * parts
        for y in range(0, parts, 1):
            if y == 0: control_points[y] = bezier.vec2d(640,360)
            if y > 0:
                bezierdot = 360 + random.randint((-100-(y*40)),(100+(y*40)))#
                bezierspeed = 5
                if abs(abs(beziers[b][0])-abs(beziers[b][1])) < (bezierspeed*y) + 1: 
                    beziers[b][1] = bezierdot
                if beziers[b][0] > beziers[b][1]: bezierdot = beziers[b][0] - random.randint(0,(bezierspeed*y))
                if beziers[b][0] < beziers[b][1]: bezierdot = beziers[b][0] + random.randint(0,(bezierspeed*y))
                control_points[y] = bezier.vec2d(640+(y*partlength),bezierdot)
                beziers[b][0] = bezierdot
            b+=1
        # Unkommentieren für eine hart kodierte bezier linie
        #control_points = [bezier.vec2d(640,360), bezier.vec2d(807,250), bezier.vec2d(974,380), bezier.vec2d(1141,520)]
        b_points = bezier.compute_bezier_points([(z.x, z.y) for z in control_points])
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
        
    
