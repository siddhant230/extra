import pygame,sys
from pygame.locals import  *
import random,cv2,os

def mainer():
    class Block:
        def __init__(self,jumpx,jumpy,img=None,res=None):
            self.x=jumpx
            self.y=jumpy
            self.width=factor
            self.response=res
            if img!=None:
                self.img=pygame.image.load(img).convert_alpha()
            else:
                self.img=None
            self.color=(random.randint(0,255),random.randint(0,255),random.randint(0,255))

        def clicked(self,x,y):
            if (x>self.x and x<self.x+self.width) and (y>self.y and y<self.y+self.width) and self.response!=None:
                return self.response

        def show(self):
            if self.img!=None:
                screen.blit(self.img,(self.x,self.y))
            else:
                pygame.draw.rect(screen,self.color,(self.x,self.y,self.width,self.width))

    w,h=1050,800
    factor=350
    x,y=-1,-1
    pygame.init()
    screen=pygame.display.set_mode((w,h),0,32)
    screen.fill((255,255,255))
    myfont = pygame.font.SysFont("Comic Sans MS", 20)

    layer=int(w/factor)*int(h/factor)
    jumpx=80
    jumpy=0
    blocks=[]

    image=['flappy_dispcopy.png','Motion_dispcopy.png','effect_dispcopy.png','pong_dispcopy.png','smart_dispcopy.png','chatbotcopy.png']
    for i in range(layer):
        if i<len(image):
            img=image[i]
            b=Block(jumpy,jumpx,img=img,res=i)
        else:
            b=Block(jumpy,jumpx)
        blocks.append(b)
        jumpy+=factor
        if jumpy>=w:
            jumpy=0
            jumpx+=factor

    start=True
    while True:
        for e in pygame.event.get():
            if e.type==KEYDOWN:

                if e.key==K_q:
                    pygame.quit()
                    sys.exit()

            if e.type==MOUSEBUTTONDOWN and start:
                x,y=pygame.mouse.get_pos()
            else:
                x,y=-1,-1

        if start:
            for block in blocks:
                response=block.clicked(x,y)
                if response!=None:
                    if response==0:
                        pygame.quit()
                        os.system('python C:\\Users\\tusha\Desktop\\Neuro-Evolutionary_model\\flappy_automate.py')
                        mainer()
                    elif response==1:
                        pygame.quit()
                        os.system('python C:\\Users\\tusha\Desktop\\Neuro-Evolutionary_model\\motion_game.py')
                        mainer()
                    elif response==2:
                        pygame.quit()
                        os.system('python C:\\Users\\tusha\Desktop\\Neuro-Evolutionary_model\\cv2effects.py')
                        mainer()
                    elif response==3:
                        pygame.quit()
                        os.system('python C:\\Users\\tusha\Desktop\\Neuro-Evolutionary_model\\PONG\\pong_bot.py')
                        mainer()
                    elif response==4:
                        pygame.quit()
                        os.system('python C:\\Users\\tusha\Desktop\\Neuro-Evolutionary_model\\smartRockets.py')
                        mainer()
                    elif response==5:
                        pygame.quit()
                        os.system('python C:\\Users\\tusha\Desktop\\Neuro-Evolutionary_model\\chatbotcli.py')
                        mainer()

                block.show()

        label121 = myfont.render('ARTIFICIAL INTELLIGENCE DRIVEN GAMES', 5, (255,5,25))
        screen.blit(label121,(380,20))
        pygame.display.update()

if __name__=='__main__':
    mainer()
