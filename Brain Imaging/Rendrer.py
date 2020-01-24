import numpy as np
from ann import network
from brain_creator import Brain
import pygame
from pygame.locals import *
import sys,random,cv2

def fun(val):
    pass

cv2.namedWindow('panel')
cv2.namedWindow('panel2')
cv2.createTrackbar('mutation','panel2',0,1000,fun)

w,h=320,320
factor=20
pygame.init()
screen=pygame.display.set_mode((w,h),0,32,pygame.HWSURFACE)
myfont = pygame.font.SysFont("Comic Sans MS", 30)

inp=[3,3]
layer=int(w/factor)*int(h/factor)
brain=Brain(layer,inp).brain

##rendering##
layers=len(brain)

def outcome():
    global layers
    brain_opt=[]
    for each_layer in range(layers):
        ##show each of this opt neuron node on screen(only these ones)
        inp_list=[random.random() for _ in range(inp[0])]
        output_of_layer=brain[each_layer].predict(inp_list)[-1]
        mapped_opts=brain_imaging(output_of_layer)
        brain[each_layer].color=mapped_opts
        '''brain_opt.append(mapped_opts)
    return brain_opt'''

def brain_imaging(neuron):
    max_pixel_val=255
    color=[]
    for val in neuron:
        color.append(val[0]*max_pixel_val)
    return color

inp_list=[random.random() for _ in range(inp[0])]
start=False
while True:
    for e in pygame.event.get():
        if e.type==KEYDOWN:
            if e.key==K_q:
                pygame.quit()
                sys.exit()
            if e.key==K_c:
                start=True
    screen.fill((255,255,255))
    mutation_rate=cv2.getTrackbarPos('mutation','panel2') / 1000.0
    if start:
        for b in range(len(brain)):
            out=brain[b].predict(inp_list)[-1]
            brain[b].color=brain_imaging(out)
            x,y=brain[b].y,brain[b].x
            pygame.draw.rect(screen,brain[b].color,(x,y,80,80))
            brain[b].mutation(mutation_rate)
            inp_list=out
    else:
        lab2=myfont.render("Press c to Start", 3, (255,0,0))
        screen.blit(lab2,(20,30))
    pygame.display.update()

