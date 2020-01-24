import pygame
from pygame.locals import *
import cv2,sys,random
from scipy.spatial import distance
import warnings
warnings.filterwarnings('ignore')

def overlap():
    def random_walk():
        if random.random()<0.5:
            rx=random.randint(1,15)
            ry=random.randint(1,15)
        else:
            rx=-1*random.randint(1,15)
            ry=-1*random.randint(1,15)
        return (rx,ry)

    pygame.init()
    pygame.display.set_caption('OVERFLOW')
    screen=pygame.display.set_mode((640,480),0,32)
    screen.fill((255,255,255))
    cap=cv2.VideoCapture(0)
    class point_make:
        def __init__(self):
            self.rx=random.randint(300,350)
            self.ry=random.randint(220,270)
    p_arr=[]
    for i in range(20):
        p_arr.append(point_make())
    while True:
        ##make a cv window
        _,img=cap.read()
        ##picking a blob on pygame window
        for _ in range(60):
            cx,cy=random_walk()
            print('###########',cx,cy)
            for i in range(len(p_arr)):
                px=p_arr[i].rx
                py=p_arr[i].ry
                p_arr[i].rx , p_arr[i].ry = (p_arr[i].rx + cx)%640 , (p_arr[i].ry + cy)%480
                col=img[p_arr[i].ry][p_arr[i].rx][::-1]
                pygame.draw.circle(screen,col,(p_arr[i].rx,p_arr[i].ry),2)
                sx,sy=(p_arr[i].rx,p_arr[i].ry)
                print(sx,sy,'##',px,py)
        #quitting part
        for e in pygame.event.get():
            if e.type==KEYDOWN:
                if e.key==K_q:
                    cap.release()
                    cv2.destroyAllWindows()
                    pygame.quit()
                    mainer()
        pygame.display.update()
cx,cy=1,1
def non_overlap():
    pygame.init()
    pygame.display.set_caption('INFLOW')
    screen=pygame.display.set_mode((640,480),0,32)
    screen.fill((255,255,255))
    cap=cv2.VideoCapture(0)
    class point_make:
        def __init__(self):
            self.rx=random.randint(300,350)
            self.ry=random.randint(220,270)
    p_arr=[]
    for i in range(50):
        p_arr.append(point_make())

    def bounce(x,y):
        global cx,cy
        if x<=0 or x>=635:
            cx*=-1
        if y<=0 or y>=475:
            cy*=-1

    def random_walk():
        if random.random()<0.5:
            rx=random.randint(3,20)
            ry=random.randint(3,20)
        else:
            rx=-1*random.randint(4,20)
            ry=-1*random.randint(4,20)
        return (rx,ry)

    while True:
        ##make a cv window
        _,img=cap.read()
        r=random.randint(1,3)
        ##picking a blob on pygame window
        for _ in range(100):
            vx,vy=random_walk()
            for i in range(len(p_arr)):
                bounce(p_arr[i].rx + vx*cx , p_arr[i].ry + vy*cy )
                p_arr[i].rx,p_arr[i].ry=p_arr[i].rx + vx*cx , p_arr[i].ry + vy*cy
                col=img[p_arr[i].ry][p_arr[i].rx][::-1]
                pygame.draw.circle(screen,col,(p_arr[i].rx,p_arr[i].ry),2)
        #quitting part
        for e in pygame.event.get():
            if e.type==KEYDOWN:
                if e.key==K_q:
                    cap.release()
                    cv2.destroyAllWindows()
                    pygame.quit()
                    mainer()
        pygame.display.update()
def effect():
    pygame.init()
    pygame.display.set_caption('PARTICLE EFFECT')
    screen=pygame.display.set_mode((640,480),0,32)
    screen.fill((255,255,255))
    cap=cv2.VideoCapture(0)
    points=[]
    c=[]
    while True:
        ##make a cv window
        _,img=cap.read()
        ##picking a blob on pygame window
        for i in range(2000):
            rx,ry=random.randint(0,638),random.randint(0,478)
            col=img[ry][rx][::-1]
            c.append(col)
            pygame.draw.circle(screen,col,(rx,ry),1)
            points.append((rx,ry))
        points=[]
        #quitting part
        for e in pygame.event.get():
            if e.type==KEYDOWN:
                if e.key==K_q:
                    cap.release()
                    cv2.destroyAllWindows()
                    pygame.quit()
                    mainer()

        pygame.display.update()
def mainer():
    def euclidean(a,b):
        return distance.euclidean(a,b)

    pygame.init()
    pygame.display.set_caption('DISPLAY PYGAME')
    screen=pygame.display.set_mode((640,480),0,32)
    screen.fill((0,0,0))

    def back():
        class circle:
            def __init__(self):
                self.x=random.randint(0,640)
                self.y=random.randint(0,480)
                self.r=random.randint(5,25)
            def plot(self):
                size = (50, 50)
                blue_image = pygame.Surface(size, pygame.SRCALPHA)
                col=(random.randint(20,255),random.randint(20,255),random.randint(20,255),random.randint(50,90))
                pygame.draw.circle(blue_image,col,(size[0]//2,size[1]//2),self.r)
                screen.blit(blue_image,(self.x,self.y))

        circles=[circle()]
        circles[-1].plot()
        while len(circles)<110:
                c=circle()
                over=True
                for i in range(len(circles)):
                    other=circles[i]
                    dist=euclidean((c.x,c.y),(other.x,other.y))
                    if dist>(other.r+c.r):
                        over=False
                    else:
                        over=True
                        break
                if over==False:
                    circles.append(c)
                    circles[-1].plot()
        pygame.display.update()
    back()
    while True:
        myfont = pygame.font.SysFont("Comic Sans MS", 30)
        label = myfont.render("PRESS o to see Overflow", 3, (255,0,0))
        label2 = myfont.render("PRESS i to see Inflow", 3, (255,0,0))
        label3 = myfont.render("PRESS e to see particle effect", 3, (255,0,0))
        label4 = myfont.render("PRESS q to see QUIT", 3, (255,0,0))
        label5=myfont.render("Press r to change background",3,(255,0,0))
        screen.blit(label,(160,80))
        screen.blit(label2,(160,120))
        screen.blit(label3,(160,160))
        screen.blit(label4,(160,200))
        screen.blit(label5,(160,240))
        for e in pygame.event.get():
            if e.type==KEYDOWN:
                if e.key==K_r:
                    mainer()
                if e.key==K_q:
                    pygame.quit()
                    sys.exit()
                if e.key==K_o:
                    pygame.quit()
                    overlap()
                if e.key==K_i:
                    pygame.quit()
                    non_overlap()
                if e.key==K_e:
                    pygame.quit()
                    effect()
        pygame.display.update()

if __name__=='__main__':
    mainer()
