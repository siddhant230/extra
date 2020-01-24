import pygame
from pygame.locals import *
import sys,random,math

dino_img='dinosaur.png'
tree_img='tree.png'
skate_img='skate.png'

w,h=900,320
class dino:

    def __init__(self):
        self.x=30
        self.y=240
        self.img=pygame.image.load(dino_img).convert_alpha()
        self.skate=pygame.image.load(skate_img).convert_alpha()

    def update(self,boost=0):
        self.y+=boost
        if self.y>=240:
            self.y=240
        elif self.y<=0:
            self.y=0

    def show(self):
        screen.blit(self.img,(self.x,self.y))
        screen.blit(self.skate,(self.x,self.y+35))

class Tree:
    def __init__(self):
        self.x=850
        self.y=250
        self.img=pygame.image.load(tree_img).convert_alpha()

    def update(self):
        self.x-=0.5

    def collision(self):
        if (self.x<=d.x+50 and self.x>=d.x):
            if (d.y+50<self.y):
                return False
            else:
                return True
        else:
            return False


    def show(self):
        screen.blit(self.img,(self.x,self.y))


pygame.init()
screen=pygame.display.set_mode((w,h),0,32)
screen.fill((110,0,200))
myfont = pygame.font.SysFont("Comic Sans MS", 30)
start=False
update=True
jump=False
trees=[]
move=0
while True:
    for e in pygame.event.get():
        if e.type==KEYDOWN:

            if e.key==K_q:
                pygame.quit()
                sys.exit()

            if e.key==K_c:
                start=True
                d=dino()
                trees=[]
                trees.append(Tree())

            if e.key==K_SPACE:
                jump=True
        if e.type==KEYUP:
            if e.key==K_SPACE:
                jump=False

    screen.fill((110,0,200))
    if start:
        move+=1
        for i in range(len(trees)-1,-1,-1):
            tree=trees[i]
            if tree.x<=-5:
                trees.pop(i)
            else:
                if tree.collision():
                    update=False
                if update:
                    tree.update()
                tree.show()
        if update:
            if move%random.randint(250,350)==0:
                trees.append(Tree())

            if jump:
                d.update(boost=-0.7)
            else:
                d.update(boost=1.4)
        d.show()

    pygame.display.update()
