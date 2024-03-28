
import pygame, random
from pygame.locals import *
import os

screenwidth = 1280
screenheight = 720
pygame.init()
screen = pygame.display.set_mode((screenwidth, screenheight))
clock = pygame.time.Clock()

    


class Player(pygame.sprite.Sprite):  # Character for MOBA game
    def __init__(self):

        self.idle = [pygame.image.load(os.path.join("Graphics",'idle1.png')), pygame.image.load(os.path.join("Graphics",'idle2.png')), pygame.image.load(os.path.join("Graphics",'idle3.png')), pygame.image.load(os.path.join("Graphics",'idle4.png')), pygame.image.load(os.path.join("Graphics",'idle5.png')), pygame.image.load(os.path.join("Graphics",'idle6.png')), pygame.image.load(os.path.join("Graphics",'idle7.png')), pygame.image.load(os.path.join("Graphics",'idle8.png')), pygame.image.load(os.path.join("Graphics",'idle9.png')),pygame.image.load(os.path.join("Graphics",'idle10.png'))]
        self.runright = [pygame.image.load(os.path.join("Graphics",'run1.png')), pygame.image.load(os.path.join("Graphics",'run2.png')), pygame.image.load(os.path.join("Graphics",'run3.png')), pygame.image.load(os.path.join("Graphics",'run4.png')), pygame.image.load(os.path.join("Graphics",'run5.png')), pygame.image.load(os.path.join("Graphics",'run6.png')), pygame.image.load(os.path.join("Graphics",'run7.png')), pygame.image.load(os.path.join("Graphics",'run8.png')), pygame.image.load(os.path.join("Graphics",'run9.png')),pygame.image.load(os.path.join("Graphics",'run10.png'))]
        self.runleft = [pygame.image.load(os.path.join("Graphics",'left1.png')), pygame.image.load(os.path.join("Graphics",'left2.png')), pygame.image.load(os.path.join("Graphics",'left3.png')), pygame.image.load(os.path.join("Graphics",'left4.png')), pygame.image.load(os.path.join("Graphics",'left5.png')), pygame.image.load(os.path.join("Graphics",'left6.png')), pygame.image.load(os.path.join("Graphics",'left7.png')), pygame.image.load(os.path.join("Graphics",'left8.png')), pygame.image.load(os.path.join("Graphics",'left9.png')),pygame.image.load(os.path.join("Graphics",'left10.png'))]
        self.idleleftanim = [pygame.image.load(os.path.join("Graphics",'idleleft1.png')), pygame.image.load(os.path.join("Graphics",'idleleft2.png')), pygame.image.load(os.path.join("Graphics",'idleleft3.png')), pygame.image.load(os.path.join("Graphics",'idleleft4.png')), pygame.image.load(os.path.join("Graphics",'idleleft5.png')), pygame.image.load(os.path.join("Graphics",'idleleft6.png')), pygame.image.load(os.path.join("Graphics",'idleleft7.png')), pygame.image.load(os.path.join("Graphics",'idleleft8.png')), pygame.image.load(os.path.join("Graphics",'idleleft9.png')),pygame.image.load(os.path.join("Graphics",'idleleft10.png'))]

        self.blockwidth = 29
        self.blockheight = 38


        self.x = 10
        self.y = 0


        self.vel_y = 8

        self.left = False
        self.right = False 
        self.walkcount = 0
        self.idlecount = 0
        self.idleright = True
        self.idleleft = False

        self.life = 1

        self.char1 = self.idle[0].get_rect()
        self.char1.x = self.x
        self.char1.y = self.y

        self.gamedisplay = 1



        

        # Need to change from platforms to abilities

        # Collision 
        # for platform in platforms:
        #     if platform.rect.colliderect(self.char1.x + dx, self.char1.y, self.blockwidth, self.blockheight):
        #         dx = 0
        #     if platform.rect.colliderect(self.char1.x, self.char1.y + dy,self.blockwidth, self.blockheight):
        #         if self.vel_y < 0:
        #             dy = platform.rect.bottom - self.char1.top
        #             self.vel_y = 0
        #         elif self.vel_y >= 0:
        #             dy = platform.rect.top - self.char1.bottom
        #             self.vel_y = 0
        #             self.jumping = False
        #             self.jumped = False
        #             self.doublejump = True
                    
		#update player coordinates
        # self.x += dx
        # self.y += dy

        # Window boundaries
        if self.char1.bottom > screenheight:
            self.char1.bottom = screenheight
            dy = 0
            self.life = 0
        elif self.x <= 0:
            self.x = 6
        elif self.x >= screenwidth:
            self.x = screenwidth-6
        

        # Animations
        self.char1.center = (self.x,self.y+self.char1.height/2)
        if self.walkcount + 1 >= 30:
            self.walkcount = 0
        if self.idlecount + 1 >= 30:
            self.idlecount = 0

        if self.right:
            screen.blit(self.runright[self.walkcount//3],self.char1)
            self.walkcount += 1
        elif self.left:
            screen.blit(self.runleft[self.walkcount//3],self.char1)
            self.walkcount += 1
        elif not self.right and self.idleright:
            screen.blit(self.idle[self.idlecount//3],self.char1)  
            self.idlecount += 1
            self.walkcount = 0
        elif not self.left and self.idleleft:
            screen.blit(self.idleleftanim[self.idlecount//3],self.char1)  
            self.idlecount += 1
            self.walkcount = 0



class Target(pygame.sprite.Sprite):
    def __init__(self):
        self.targetimg = pygame.image.load(os.path.join("Graphics",'target.png'))

        self.targetx = 0
        self.targety = 0
        self.targetsize = [30,60]
        self.targetchar = self.targetimg.get_rect()
        self.targetvalues = []
        self.targets = [[] for i in range(4)]
        self.score = 0
        self.chosenTime = 0
        self.seconds = 10

    def targetplace(self,screen):
        for x in range(0,4):
            self.targetchar.center = (self.targets[x][0],self.targets[x][1])
            screen.blit(pygame.transform.scale(self.targetimg,[self.targets[x][2],self.targets[x][3]]),self.targetchar)

    def check_click(self, mouse):
        if(self.seconds > 0):
            for x in range(0,4):
                self.targetchar.center = (self.targets[x][0],self.targets[x][1])
                if self.targetchar.collidepoint(mouse):
                    self.targets.pop(x)
                    self.targetx = random.randint(70,screenwidth-70)
                    self.targety = random.randint(70,screenheight-70)
                    self.targetsize[0] = random.randint(40,130)
                    self.targetsize[1] = self.targetsize[0]
                    self.targetvalues = [self.targetx,self.targety,self.targetsize[0],self.targetsize[1]]
                    self.targets.append(self.targetvalues)
                    self.score += 1




        
        

def main():
    gamedisplay = 0
    menuselector = 0
    fpsselector = 0

    pygame.display.set_caption('MultiTrainer') # Title

    # Fill background
    mainmenu = pygame.image.load(os.path.join("Graphics",'background.png'))
    bg = pygame.image.load(os.path.join("Graphics",'background.png'))
    fpsbg = pygame.image.load(os.path.join("Graphics",'fpsbackground.jpg'))
    bgsize = (screenwidth, screenheight)
    bg = pygame.transform.scale(bg,bgsize)
    fpsbg = pygame.transform.scale(fpsbg,bgsize)
    mainmenu = pygame.transform.scale(mainmenu,bgsize)
   

    # Displaying text
    fonttitle = pygame.font.Font("VeniteAdoremus.ttf", 70)
    font = pygame.font.Font("VeniteAdoremus.ttf", 45)
    fontreturn = pygame.font.Font("VeniteAdoremus.ttf", 15)


    title = fonttitle.render("MultiTrainer", 3, (64, 64, 64))
    titlepos = title.get_rect()
    titlepos.center = (screenwidth//2 , screenheight//2.6)

    fps = font.render("FPS", True, (0, 0, 0))
    fpspos = fps.get_rect()
    fpspos.center = (screenwidth//2 , screenheight//1.63)

    moba = font.render("MOBA", True, (0, 0, 0))
    mobapos = moba.get_rect()
    mobapos.center = (screenwidth//2 , screenheight//1.44)

    typing = font.render("TYPING", True, (0, 0, 0))
    typingpos = typing.get_rect()
    typingpos.center = (screenwidth//2 , screenheight//1.28)

    exit = font.render("EXIT", True, (0, 0, 0))
    exitpos = exit.get_rect()
    exitpos.center = (screenwidth//2 , screenheight//1.16)


    ten = font.render("10 seconds", True, (0, 0, 0))
    tenpos = ten.get_rect()
    tenpos.center = (screenwidth//2 , screenheight//1.65)

    thirty = font.render("30 seconds", True, (0, 0, 0))
    thirtypos = thirty.get_rect()
    thirtypos.center = (screenwidth//2 , screenheight//1.45)

    sixty = font.render("60 seconds", True, (0, 0, 0))
    sixtypos = sixty.get_rect()
    sixtypos.center = (screenwidth//2 , screenheight//1.3)

    # testblock = Block()

    targetblock = Target()

    


    
    # Event loop
    while True:
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_w and gamedisplay == 0:
                    menuselector -= 1
                elif event.key == pygame.K_s and gamedisplay == 0:
                    menuselector += 1
                elif event.key == pygame.K_w and gamedisplay == 10:
                    fpsselector -= 1
                elif event.key == pygame.K_s and gamedisplay == 10:
                    fpsselector += 1

                if event.key == pygame.K_ESCAPE and gamedisplay > 0:
                    gamedisplay = 0
                    targetblock.score = 0
            elif event.type == pygame.MOUSEBUTTONDOWN and gamedisplay == 1:
                targetblock.check_click(event.pos)

    
        if(gamedisplay == 0): # MAIN MENU HERE
            screen.blit(mainmenu, (0,0))
            if menuselector == 0:
                fps = font.render("FPS", True, (255, 0, 0))
                moba = font.render("MOBA", True, (0, 0, 0))
                typing = font.render("TYPING", True, (0, 0, 0))
                exit = font.render("Exit", True, (0, 0, 0))
                mainmenu.blit(fps, fpspos)
                mainmenu.blit(moba, mobapos)
                mainmenu.blit(typing, typingpos)
                mainmenu.blit(exit, exitpos)
            else:
                fps = font.render("FPS", True, (0, 0, 0))
                mainmenu.blit(fps, fpspos)

            if menuselector == 1:
                fps = font.render("FPS", True, (0, 0, 0))
                moba = font.render("MOBA", True, (255, 0, 0))
                typing = font.render("TYPING", True, (0, 0, 0))
                exit = font.render("Exit", True, (0, 0, 0))
                mainmenu.blit(fps, fpspos)
                mainmenu.blit(moba, mobapos)
                mainmenu.blit(typing, typingpos)
                mainmenu.blit(exit, exitpos)
            else:
                moba = font.render("MOBA", True, (0, 0, 0))
                mainmenu.blit(moba, mobapos)

            if menuselector == 2:
                fps = font.render("FPS", True, (0, 0, 0))
                moba = font.render("MOBA", True, (0, 0, 0))
                typing = font.render("TYPING", True, (255, 0, 0))
                exit = font.render("Exit", True, (0, 0, 0))
                mainmenu.blit(exit, exitpos)
                mainmenu.blit(moba, mobapos)
                mainmenu.blit(typing, typingpos)
                mainmenu.blit(fps, fpspos)
            else:
                typing = font.render("TYPING", True, (0, 0, 0))
                mainmenu.blit(typing, typingpos)
    
            if menuselector == 3:
                fps = font.render("FPS", True, (0, 0, 0))
                moba = font.render("MOBA", True, (0, 0, 0))
                typing = font.render("TYPING", True, (0, 0, 0))
                exit = font.render("Exit", True, (255, 0, 0))
                mainmenu.blit(exit, exitpos)
                mainmenu.blit(moba, mobapos)
                mainmenu.blit(typing, typingpos)
                mainmenu.blit(fps, fpspos)
            else:
                exit = font.render("EXIT", True, (0, 0, 0))
                mainmenu.blit(exit, exitpos)
                

            if menuselector < 0:
                menuselector = 3
            elif menuselector > 3:
                menuselector = 0

            # FPS game
            if(pygame.key.get_pressed()[pygame.K_RETURN] and menuselector == 0):
                screen.blit(fpsbg,(0,0))
                gamedisplay = 10
                

                for x in range(0,4):
                    targetblock.targetx = random.randint(70,screenwidth-70)
                    targetblock.targety = random.randint(70,screenheight-70)
                    targetblock.targetsize[0] = random.randint(40,130)
                    targetblock.targetsize[1] = targetblock.targetsize[0]
                    targetblock.targetvalues = [targetblock.targetx,targetblock.targety,targetblock.targetsize[0],targetblock.targetsize[1]]
                    targetblock.targets[x] = (targetblock.targetvalues)
                pygame.time.wait(100)
            elif(pygame.key.get_pressed()[pygame.K_RETURN] and menuselector == 3):
                return


        elif(gamedisplay == 10):
            if(fpsselector == 0):
                ten = font.render("10 seconds", True, (255, 0, 0))
                thirty = font.render("30 seconds", True, (255,255, 255))
                sixty = font.render("60 seconds", True, (255,255, 255))
                screen.blit(ten, tenpos)
                screen.blit(thirty, thirtypos)
                screen.blit(sixty, sixtypos)
            else:
                ten = font.render("10 seconds", True, (255,255, 255))
                screen.blit(ten, tenpos)

            if(fpsselector == 1):
                ten = font.render("10 seconds", True, (255,255, 255))
                thirty = font.render("30 seconds", True, (255, 0, 0))
                sixty = font.render("60 seconds", True, (255,255, 255))
                screen.blit(ten, tenpos)
                screen.blit(thirty, thirtypos)
                screen.blit(sixty, sixtypos)
            else:
                thirty = font.render("30 seconds", True, (255,255, 255))
                screen.blit(thirty, thirtypos)

            if(fpsselector == 2):
                ten = font.render("10 seconds", True, (255,255, 255))
                thirty = font.render("30 seconds", True, (255,255, 255))
                sixty = font.render("60 seconds", True, (255, 0, 0))
                screen.blit(ten, tenpos)
                screen.blit(thirty, thirtypos)
                screen.blit(sixty, sixtypos)
            else:
                sixty = font.render("60 seconds", True, (255,255, 255))
                screen.blit(sixty, sixtypos)
            if(pygame.key.get_pressed()[pygame.K_RETURN] and fpsselector == 0):
                targetblock.chosenTime = 10
                start_timer = pygame.time.get_ticks()
                gamedisplay = 1
            elif(pygame.key.get_pressed()[pygame.K_RETURN] and fpsselector == 1):
                targetblock.chosenTime = 30
                start_timer = pygame.time.get_ticks()
                gamedisplay = 1
            elif(pygame.key.get_pressed()[pygame.K_RETURN] and fpsselector == 2):
                targetblock.chosenTime = 60
                start_timer = pygame.time.get_ticks()
                gamedisplay = 1
            if fpsselector < 0:
                fpsselector = 2
            elif fpsselector > 2:
                fpsselector = 0
            
            


           

        elif(gamedisplay == 1): # FPS HERE
                screen.blit(fpsbg, (0,0))
                textscore = font.render("Score: " + str(targetblock.score), True, (255, 255, 255))
                targetblock.seconds = round(targetblock.chosenTime -((pygame.time.get_ticks()- start_timer)/1000), 3)
                targetblock.targetplace(screen)
                screen.blit(textscore, (10, 10))
                screen.blit(font.render(str(targetblock.seconds), True, (255, 255, 255)), ((screenwidth//2) - 60, screenheight//16))
                if(targetblock.seconds < 0):
                    screen.blit(fpsbg, (0,0))
                    screen.blit(font.render("Your score on " + str(targetblock.chosenTime) + " seconds is " + str(targetblock.score), True, (255, 255, 255)), ((screenwidth//2) - 400, screenheight//16))
                    screen.blit(fontreturn.render("Press Escape to return to Main Menu", True, (255, 255, 255)), ((screenwidth//2) - 175, screenheight//1.2))

                
                

        pygame.display.flip()
main()
