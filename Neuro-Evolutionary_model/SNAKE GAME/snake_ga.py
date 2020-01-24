import pygame,time
from pygame.locals import *
import sys,random,math
from ann import network
from scipy.spatial import distance

w,h=400,400
ch=2
class Food:

    def __init__(self):
        self.x=random.randint(20,w-20)
        self.y=random.randint(20,h-20)
        self.radius=10
        self.color=(255,255,255)

    def show(self):
        pygame.draw.circle(screen,self.color,(self.x,self.y),self.radius)


class SnakeBody:

    def __init__(self,head=False,x=w//2,y=h//2,brain=None):
        self.x=x
        self.y=y
        self.side=15
        self.score=1e-50
        if brain!=None:
            self.brain=brain
        else:
            self.brain=network([5,4,4])
        self.color=(0,255,0)

    def update(self,nx=0,ny=0):
        self.x+=nx
        self.y+=ny

    def update_body(self,nx,ny):
        self.x=nx
        self.y=ny

    def found_food(self):
        thresh=20
        dist=distance.euclidean((self.x,self.y),(f.x,f.y))
        if dist<thresh:
            self.score+=(1/dist)
            self.score+=10
            return True
        else:
            self.score+=(1/dist)
            return False

    def collision(self):
        if head.x>0 and head.x<w and head.y>0 and head.y<h:
            return False
        else:
            return True

    def body_touch(self):
        for p in snake:
            if p.x==head.x and p.y==head.y:
                return True
        return False

    def think(self):
        global nx,ny
        nx=0
        ny=0
        d=1/distance.euclidean((self.x,self.y),(f.x,f.y))
        inp_val=[self.x,self.y,f.x,f.y,d]
        opt=self.brain.predict(inp_val)
        if opt==0:
            nx=-ch
            ny=0
        elif opt==1:
            nx=ch
            ny=0
        elif opt==2:
            ny=-ch
            nx=0
        elif opt==3:
            ny=ch
            nx=0
        return (nx,ny)

    def show(self):
        pygame.draw.rect(screen,self.color,(self.x,self.y,self.side,self.side))

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
                obj = SnakeBody(head=True)
            elif random.random() > 0.2:
                obj = SnakeBody(brain=fittest.brain,head=True)
                obj.brain.mutation(0.4)
            else:
                obj = SnakeBody()
            heads.append(obj)
    else:
        for i in range(population):
            obj = SnakeBody(head=True)
            heads.append(obj)

pygame.init()
screen=pygame.display.set_mode((w,h),0,32)
screen.fill((110,0,200))
myfont = pygame.font.SysFont("Comic Sans MS", 30)
start=False
nx,ny=0,0
population=20
foods=[]
heads=[]
move=0
savedHeads=[]
snake=[]
while True:
    for e in pygame.event.get():
        if e.type==KEYDOWN:

            if e.key==K_q:
                pygame.quit()
                sys.exit()

            if e.key==K_c:
                if start==False:
                    for _ in range(5):
                        foods.append(Food())
                    for _ in range(population):
                        heads.append(SnakeBody(head=True))
                    start=True

    screen.fill((110,0,200))
    if start:
        for i in range(len(heads)-1,-1,-1):
            head=heads[i]
            for j in range(len(foods)-1,-1,-1):
                f=foods[j]
                nx,ny=head.think()
                px,py=head.x,head.y
                head.update(nx=nx,ny=ny)

                if head.collision():
                    #head.score=-99999999
                    savedHeads.append(heads.pop(i))
                    snake=[]
                    break

                if head.found_food():
                    foods.pop(j)
                f.show()
            head.show()
        move+=1
        print(len(foods),move)
        if len(foods)==0 or move%600==0:
            move=0
            foods=[]
            for _ in range(5):
                foods.append(Food())
        if len(heads)==0 or move%600==0:
            move=0
            if heads!=[]:
                savedHeads.extend(heads)
                heads=[]
            print('###########@@@@@@@@@@@#############')
            create_new_population(savedHeads)
            savedHeads=[]

        #pygame.display.set_caption('SCORE : {}'.format(head.score))
    else:
        lab2 = myfont.render("Press c to Start", 25, (255, 0, 0))
        screen.blit(lab2,(100,100))
    pygame.display.update()
