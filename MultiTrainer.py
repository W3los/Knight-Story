import pygame
from pygame.locals import *
import os

screenwidth = 1000
screenheight = 700
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



        

        
        # Collision
        for platform in platforms:
            if platform.rect.colliderect(self.char1.x + dx, self.char1.y, self.blockwidth, self.blockheight):
                dx = 0
            if platform.rect.colliderect(self.char1.x, self.char1.y + dy,self.blockwidth, self.blockheight):
                if self.vel_y < 0:
                    dy = platform.rect.bottom - self.char1.top
                    self.vel_y = 0
                elif self.vel_y >= 0:
                    dy = platform.rect.top - self.char1.bottom
                    self.vel_y = 0
                    self.jumping = False
                    self.jumped = False
                    self.doublejump = True
                    
		#update player coordinates
        self.x += dx
        self.y += dy

        if self.char1.bottom > screenheight:
            self.char1.bottom = screenheight
            dy = 0
            self.life = 0
        elif self.x <= 0:
            self.x = 6
        elif self.x >= screenwidth:
            self.x = screenwidth-6
        

        self.char1.center = (self.x,self.y+self.char1.height/2)
        if self.walkcount + 1 >= 30:
            self.walkcount = 0
        if self.idlecount + 1 >= 30:
            self.idlecount = 0
        if self.jumpcountanim + 1 >= 9:
            self.jumpcountanim = 0    
        if self.fallcountanim + 1 >= 9:
            self.fallcountanim = 0   

        if self.jumping and self.idleright:
            if dy <= 0:
                screen.blit(self.jumpright[self.jumpcountanim//3],self.char1)
                self.jumpcountanim += 1
            elif dy > 0:
                screen.blit(self.fallright[self.fallcountanim//3],self.char1)
                self.fallcountanim += 1
        elif self.jumping and self.idleleft:
            if dy <= 0:
                screen.blit(self.jumpleft[self.jumpcountanim//3],self.char1)
                self.jumpcountanim += 1
            elif dy > 0:
                screen.blit(self.fallleft[self.fallcountanim//3],self.char1)
                self.fallcountanim += 1
        elif self.right:
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



class Flag(pygame.sprite.Sprite):
    def __init__(self):
        self.flagimg = pygame.image.load(os.path.join("Graphics",'flag.png'))

        self.flagx = 0
        self.flagy = 0
        self.flagsize = (30,60)
        self.flagchar = self.flagimg.get_rect()

    def flagplace(self,screen):
        self.flagchar.center = (self.flagx,self.flagy)
        screen.blit(pygame.transform.scale(self.flagimg,self.flagsize),self.flagchar)


        
        

def main():
    gamedisplay = 0
    menuselector = 0
    levelselector = 1
    levelselectorbool = False
    levelselmain = False

    pygame.display.set_caption('MultiTrainer') # Title

    # Fill background
    mainmenu = pygame.image.load(os.path.join("Graphics",'background.png'))
    bg = pygame.image.load(os.path.join("Graphics",'background.png'))
    levelselgraphic = pygame.image.load(os.path.join("Graphics",'background.png'))
    level1img = pygame.image.load(os.path.join("Graphics",'level1.png'))
    bgsize = (screenwidth, screenheight)
    bg = pygame.transform.scale(bg,bgsize)
    mainmenu = pygame.transform.scale(mainmenu,bgsize)
    levelselgraphic = pygame.transform.scale(levelselgraphic,bgsize)

    # Displaying text
    fonttitle = pygame.font.Font("VeniteAdoremus.ttf", 80)
    font = pygame.font.Font("VeniteAdoremus.ttf", 45)


    title = fonttitle.render("MultiTrainer", 3, (64, 64, 64))
    titlepos = title.get_rect()
    titlepos.center = (screenwidth//2 , screenheight//7)

    play = font.render("Play", 3, (0, 0, 0))
    playpos = play.get_rect()
    playpos.center = (screenwidth//2 , screenheight//1.6)

    levelsel = font.render("Select level", 3, (0, 0, 0))
    levelselpos = levelsel.get_rect()
    levelselpos.center = (screenwidth//2 , screenheight//1.3)

    exit = font.render("Exit", 3, (0, 0, 0))
    exitpos = exit.get_rect()
    exitpos.center = (screenwidth//2 , screenheight//1.1)

    level1 = font.render("Level1", 3, (0, 0, 0))
    level1pos = level1.get_rect()
    level1pos.center = (200 , screenheight//5)

    mainmen = font.render("Main menu", 3, (0, 0, 0))
    mainmenpos = mainmen.get_rect()
    mainmenpos.center = (screenwidth//2 , 600)

    mainmenu.blit(title, titlepos)
    mainmenu.blit(play, playpos)
    mainmenu.blit(levelsel, levelselpos)
    mainmenu.blit(exit, exitpos)

    testblock = Block()

    flagblock = Flag()


    
    # Event loop
    while True:
        clock.tick(30)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_w and gamedisplay == 0:
                    menuselector -= 1
                elif event.key == pygame.K_s and gamedisplay == 0:
                    menuselector += 1
                if event.key == pygame.K_d and levelselectorbool and levelselmain == False:
                    levelselector += 1
                elif event.key == pygame.K_a and levelselectorbool and levelselmain == False:
                    levelselector -= 1
                if event.key == pygame.K_w and levelselectorbool:
                    levelselector = 1
                    levelselmain = False
                elif event.key == pygame.K_s and levelselectorbool:
                    levelselmain = True
                if event.key == pygame.K_ESCAPE and gamedisplay > 0:
                    gamedisplay = 0
                    testblock.x = 10

    
        if(gamedisplay == 0): # MAIN MENU HERE
            screen.blit(mainmenu, (0,0))
            if menuselector == 0:
                play = font.render("Play", True, (255, 0, 0))
                levelsel = font.render("Select level", True, (0, 0, 0))
                exit = font.render("Exit", True, (0, 0, 0))
                mainmenu.blit(play, playpos)
                mainmenu.blit(levelsel, levelselpos)
                mainmenu.blit(exit, exitpos)
            else:
                play = font.render("Play", True, (0, 0, 0))
                mainmenu.blit(play, playpos)

            if menuselector == 1:
                play = font.render("Play", True, (0, 0, 0))
                levelsel = font.render("Select level", True, (255, 0, 0))
                exit = font.render("Exit", True, (0, 0, 0))
                mainmenu.blit(exit, exitpos)
                mainmenu.blit(levelsel, levelselpos)
                mainmenu.blit(play, playpos)
            else:
                levelsel = font.render("Select level", True, (0, 0, 0))
                mainmenu.blit(levelsel, levelselpos)

            if menuselector == 2:
                play = font.render("Play", True, (0, 0, 0))
                levelsel = font.render("Select level", True, (0, 0, 0))
                exit = font.render("Exit", True, (255, 0, 0))
                mainmenu.blit(exit, exitpos)
                mainmenu.blit(levelsel, levelselpos)
                mainmenu.blit(play, playpos)
            else:
                exit = font.render("Exit", True, (0, 0, 0))
                mainmenu.blit(exit, exitpos)
                

            if menuselector < 0:
                menuselector = 2
            elif menuselector > 2:
                menuselector = 0

            if(pygame.key.get_pressed()[pygame.K_RETURN] and menuselector == 0):
                gamedisplay = 1
                
                flagblock.flagx = screenwidth - flagblock.flagsize[0]
                flagblock.flagy = 573 - flagblock.flagsize[1] / 1.4
                
                testblock.x = 10
                testblock.y = screenheight- 59 - testblock.blockheight

                platforms = Platform.Level1()
            elif(pygame.key.get_pressed()[pygame.K_RETURN] and menuselector == 1):
                levelselectorbool = True
                gamedisplay = -1
                pygame.time.wait(100)
            
            elif(pygame.key.get_pressed()[pygame.K_RETURN] and menuselector == 2):
                return

        elif(gamedisplay == -1):
            screen.blit(levelselgraphic, (0, 0))
            if levelselector == 1:
                level1 = font.render("Level1", True, (255, 0, 0))
                mainmen = font.render("Main menu", True, (0, 0, 0))
                levelselgraphic.blit(level1, level1pos)
                levelselgraphic.blit(mainmen, mainmenpos)
            else:
                level1 = font.render("Level1", True, (0, 0, 0))
                levelselgraphic.blit(level1, level1pos)


            if levelselmain:
                level1 = font.render("Level1", True, (0, 0, 0))
                mainmen = font.render("Main menu", True, (255, 0, 0))
                levelselgraphic.blit(level1, level1pos)
                levelselgraphic.blit(mainmen, mainmenpos)
            else:
                mainmen = font.render("Main menu", True, (0, 0, 0))
                levelselgraphic.blit(mainmen, mainmenpos)

            if levelselector < 1:
                levelselector = 2
            elif levelselector > 2:
                levelselector = 1


            if(pygame.key.get_pressed()[pygame.K_RETURN] and levelselmain):
                gamedisplay = 0
                pygame.time.wait(100)
            elif(pygame.key.get_pressed()[pygame.K_RETURN] and levelselector == 1):
                gamedisplay = 1
                flagblock.flagx = screenwidth - flagblock.flagsize[0]
                flagblock.flagy = 573 - flagblock.flagsize[1] / 1.4
                testblock.x = 10
                testblock.y = screenheight- 59 - testblock.blockheight
                platforms = Platform.Level1()
                levelselectorbool = False
                pygame.time.wait(100)
           

        elif(gamedisplay == 1): # FIRST LEVEL HERE
            if(testblock.life == 1):
                for platform in platforms:
                    screen.blit(platform.image, platform.rect)
                screen.blit(bg, (0, 0))
                screen.blit(level1img, (0, 0))
                flagblock.flagplace(screen)
                
                testblock.update()

        pygame.display.flip()
main()
