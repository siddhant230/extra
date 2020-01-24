import pygame
from pygame.locals import *
import sys
import math
import random
from scipy.spatial import distance
from ann import network

rocket_image='rocket.png'
alien_image='alien.png'
bullet_image='bullet.png'

width=400
height=400
score=0
start=False

class Rocket:
    def __init__(self,brain=None):
        self.x=width//2
        self.y=int(0.9956*height)
        self.change=1
        self.score=0
        self.bullet=Bullet(self.x,self.y)
        if brain!=None:
            self.brain=brain
        else:
            self.brain=network([4,10,3])
        self.img=pygame.image.load(rocket_image).convert_alpha()

    def update(self,shift):
        self.x += self.change * shift
        if self.x<0:
            self.x=0
        elif self.x>width-5:
            self.x=width-5

    def think(self):
        best=99999999
        closest=None
        for a in aliens:
            if a.y-self.y < best:
                closest=a
        if self.bullet.state=='FIRE':
            state=1
        else:
            state=0
        inp_val=[self.x,closest.y,self.bullet.y,(self.bullet.change-closest.change)**2]
        opt=self.brain.predict(inp_val)
        return opt

    def show(self):
        screen.blit(self.img,(self.x,self.y))


class Bullet:
    def __init__(self,x,y):
        self.x=x+10
        self.y=y-10
        self.state='REST'
        self.change=10
        self.img=pygame.image.load(bullet_image).convert_alpha()

    def update(self):
        self.y-=self.change
        if self.y<=0:
            self.state='REST'

    def show(self):
        screen.blit(self.img,(self.x,self.y))


class Alien:
    def __init__(self):
        self.x=random.randint(5,width-25)
        self.y=random.randint(10,30)
        self.change=0.5
        self.img=pygame.image.load(alien_image).convert_alpha()

    def update(self):
        if self.x >= width or self.x<5:
            self.change*=-1
            self.y+=random.randint(25,40)
        self.x += self.change

    def collision(self,x,y):
        thresh=35
        dist=math.sqrt(math.pow((self.x-x),2)+math.pow((self.y-y),2))
        if dist<thresh:
            return True
        else:
            return False

    def show(self):
        screen.blit(self.img,(self.x,self.y))

def create_new_population(savedbirds=None):
    global rockets
    rockets=[]
    if savedbirds != None:
        total_score = 0
        for b in savedbirds:
            total_score += b.score

        fittest = None
        for b in savedbirds:
            b.fitness = b.score / total_score
            if fittest == None:
                fittest = b
            elif b.fitness > fittest.fitness:
                fittest = b

        for i in range(population):
            if fittest.score<-5:
                obj = Rocket()
            elif random.random() > 0.2:
                obj = Rocket(brain=fittest.brain)
                obj.brain.mutation(0.4)
            else:
                obj = Rocket()
            rockets.append(obj)
    else:
        for i in range(population):
            obj = Rocket()
            rockets.append(obj)

aliens=[]
rockets=[]
pygame.init()
shift=0
population=10
screen=pygame.display.set_mode((500,500),0,32)
screen.fill((110, 0, 200))
myfont = pygame.font.SysFont("Comic Sans MS", 30)
found=False
gen=0
while True:
    for e in pygame.event.get():
        if e.type==KEYDOWN:
            if e.key==K_q:
                pygame.quit()
                sys.exit()
            if e.key==K_c:
                start=True
                for _ in range(population):
                    r=Rocket()
                    rockets.append(r)

                for _ in range(20):
                    aliens.append(Alien())

    if start:
        screen.fill((110, 0, 200))

        for r in rockets:

            thought=r.think()
            if thought==0:
                shift=-0.2
            elif thought==1:
                shift=0.2
            elif thought==2:
                r.score-=0.8
                r.bullet.state='FIRE'

            for i in range(len(aliens)-1,-1,-1):
                if aliens[i].collision(r.x,r.y):
                    r.score=-99999999

                if aliens[i].collision(r.bullet.x,r.bullet.y):
                    r.score+=5
                    r.bullet=None
                    r.bullet=Bullet(r.x,r.y)
                    aliens.pop(i)
                    found=True
                    break
            if not found:
                r.score-=0.002
            found=False

            for alien in aliens:
                alien.update()
                alien.show()

            if r.bullet.state=='FIRE':
                r.bullet.update()
                r.bullet.show()

            if r.bullet.state=='REST':
                r.bullet=Bullet(r.x,r.y)

            if len(aliens)==0:
                gen+=1
                print('###########')
                for _ in range(20):
                    aliens.append(Alien())
                pygame.display.set_caption('GEN : {}'.format(gen))
                create_new_population(rockets)

            r.update(shift=shift)
            r.show()

    else:
        lab2 = myfont.render("Enter c to Continue" , 1, (255,255,255))
        screen.blit(lab2, (10,30))

    pygame.display.update()
