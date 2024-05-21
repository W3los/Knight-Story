import pygame, random
from pygame.locals import *
import os
import math

screenwidth = 1920
screenheight = 1080
pygame.init()
screen = pygame.display.set_mode((screenwidth, screenheight))
clock = pygame.time.Clock()


    


class Player(pygame.sprite.Sprite):  # Character for MOBA game
    def __init__(self):

        
        self.idle = [pygame.image.load(os.path.join("Graphics", f'idle{i}.png')) for i in range(1, 11)]
        self.runright = [pygame.image.load(os.path.join("Graphics", f'run{i}.png')) for i in range(1, 11)]
        self.runleft = [pygame.image.load(os.path.join("Graphics", f'left{i}.png')) for i in range(1, 11)]
        self.idleleftanim = [pygame.image.load(os.path.join("Graphics", f'idleleft{i}.png')) for i in range(1, 11)]
        
        self.x,self.y = screenwidth//2, screenheight//2

        
        self.playerwidth = 45
        self.playerheight = 75

        self.left = False
        self.right = False 
        self.walkcount = 0
        self.idlecount = 0
        self.idleright = True
        self.idleleft = False
        self.resize_player_images()

        self.life = 1
        self.mouse_pos = (screenwidth//2, screenheight//2)

        self.image = self.idle[0]
        self.rect = self.image.get_rect()
        self.rect.center = (self.playerwidth//2, self.playerheight//2)
        self.destination = None
        self.seconds = 0
        self.highscores = open(os.path.join("Highscores","HighscoreMOBA.txt"))
        self.content2 = self.highscores.readline()
        self.highscoreMOBA = float(self.content2)
        self.highscores.close()
        self.score = 0
        

        self.dx = 0
        

    def resize_player_images(self):
        self.idle = [pygame.transform.scale(image, (self.playerwidth, self.playerheight)) for image in self.idle]
        self.runright = [pygame.transform.scale(image, (self.playerwidth, self.playerheight)) for image in self.runright]
        self.runleft = [pygame.transform.scale(image, (self.playerwidth, self.playerheight)) for image in self.runleft]
        self.idleleftanim = [pygame.transform.scale(image, (self.playerwidth, self.playerheight)) for image in self.idleleftanim]

    def animate(self, moving):
        if self.walkcount + 1 >= 30:
            self.walkcount = 0
        if self.idlecount + 1 >= 30:
            self.idlecount = 0

        if moving:
            if self.right:
                self.image = self.runright[self.walkcount // 3]
                self.walkcount += 1
            elif self.left:
                self.image = self.runleft[self.walkcount // 3]
                self.walkcount += 1
        else:
            if self.idleright:
                self.image = self.idle[self.idlecount // 3]
                self.idlecount += 1
            elif self.idleleft:
                self.image = self.idleleftanim[self.idlecount // 3]
                self.idlecount += 1
            self.walkcount = 0
    def move_towards_mouse(self):
        if self.destination:
            self.dx, dy = self.destination[0] - self.rect.centerx, self.destination[1] - self.rect.centery
            dist = (self.dx**2 + dy**2) ** 0.5
            if dist != 0:
                speed = 10 
                self.dx, dy = self.dx / dist, dy / dist
                if dist < speed:  
                    self.x, self.y = self.destination[0], self.destination[1]
                    self.rect.center = (self.x, self.y)
                    self.dx, dy = 0, 0  
                else:
                    self.x += self.dx * speed
                    self.y += dy * speed
                    self.rect.center = (self.x, self.y)


    def update(self):
        self.mouse_pos = pygame.mouse.get_pos()
        moving=False

        if pygame.mouse.get_pressed()[2]:
            self.destination = self.mouse_pos  
            moving = True
        elif self.destination is not None:  
            moving = True
            self.move_towards_mouse() 
        if self.mouse_pos[0] == self.rect.centerx and self.mouse_pos[1] == self.rect.centery:
            moving = False
        if self.dx > 0:
            self.right = True
            self.left = False
            self.idleright = True
            self.idleleft = False
            moving = True
        elif self.dx < 0:
            self.right = False
            self.left = True
            self.idleright = False
            self.idleleft = True
            moving = True
        elif self.dx == 0:
            self.left = False
            self.right = False
            moving = False
        

        
        self.animate(moving)


class Projectiles(pygame.sprite.Sprite):
    def __init__(self, direction, speed):
        super().__init__()
        if direction in ["down"]:
            project_image = pygame.image.load(os.path.join("Graphics","project_down.png")).convert_alpha()
            self.image = pygame.transform.scale(project_image, (20, 40))
            self.rect = self.image.get_rect()
        elif direction in ["up"]:
            project_image = pygame.image.load(os.path.join("Graphics","project_up.png")).convert_alpha()
            self.image = pygame.transform.scale(project_image, (20, 40))
            self.rect = self.image.get_rect()
        elif direction in ["left"]:
            project_image = pygame.image.load(os.path.join("Graphics","project_left.png")).convert_alpha()
            self.image = pygame.transform.scale(project_image, (40, 20))
            self.rect = self.image.get_rect()
        elif direction in ["right"]:
            project_image = pygame.image.load(os.path.join("Graphics","project_right.png")).convert_alpha()
            self.image = pygame.transform.scale(project_image, (40, 20))
            self.rect = self.image.get_rect()
    
        if direction == "down":
            self.rect.x = random.randint(10, screenwidth-10)
            self.rect.y = 0
            self.speed_x = 0
            self.speed_y = speed
        elif direction == "up":
            self.rect.x = random.randint(10, screenwidth-10)
            self.rect.y = screenheight
            self.speed_x = 0
            self.speed_y = -speed
        elif direction == "left":
            self.rect.x = screenwidth
            self.rect.y = random.randint(10, screenheight-10)
            self.speed_x = -speed
            self.speed_y = 0
        elif direction == "right":
            self.rect.x = 0
            self.rect.y = random.randint(10, screenheight-10)
            self.speed_x = speed
            self.speed_y = 0

    def update(self):
        self.rect.y += self.speed_y 
        self.rect.x += self.speed_x 

        # Kill sprie when left window
        if self.rect.top > screenheight or self.rect.bottom < 0 or self.rect.right < 0 or self.rect.left > screenwidth:
            self.kill()

class ChasingProjectile(pygame.sprite.Sprite):
    def __init__(self, player):
        super().__init__()
        original_image = pygame.image.load(os.path.join("Graphics","eye.png")).convert_alpha()
        self.image = pygame.transform.scale(original_image, (50, 50))
        self.rect = self.image.get_rect()

        # Ustawienie pozycji początkowej poza ekranem
        self.rect.x = -self.rect.width
        self.rect.y = random.randint(0, screenheight - self.rect.height)

        self.player = player
        self.creation_time = pygame.time.get_ticks()

    def update(self):
        # Obliczenie wektora kierunku do gracza
        dx = self.player.rect.centerx - self.rect.centerx
        dy = self.player.rect.centery - self.rect.centery

        # Normalizacja wektora
        distance = math.hypot(dx, dy)
        if distance != 0:
            dx /= distance
            dy /= distance

        # Ustawienie prędkości
        speed = 5
        self.rect.x += dx * speed
        self.rect.y += dy * speed

        # Sprawdzenie kolizji z graczem
        if pygame.sprite.collide_rect(self, self.player):
            # Przeniesienie gracza na środek ekranu
            self.player.rect.center = screenwidth // 2, screenheight // 2

        # Sprawdzenie czasu życia projektu
        if pygame.time.get_ticks() - self.creation_time > 10000:
            self.kill()

class Target(pygame.sprite.Sprite):
    def __init__(self):
        self.targetimg = pygame.image.load(os.path.join("Graphics",'target.png'))
        self.crosshairimg = pygame.image.load(os.path.join("Graphics",'crosshair.png'))

        self.targetx = 0
        self.targety = 0
        self.targetsize = [30,60]
        self.targetchar = self.targetimg.get_rect()
        self.targetvalues = []
        self.targets = [[] for i in range(4)]
        self.score = 0
        self.chosenTime = 0
        self.seconds = 10
        self.highscores = open(os.path.join("Highscores","Highscores.txt"))
        self.content = self.highscores.readlines()
        self.highscore10 = int(self.content[0])
        self.highscore30 = int(self.content[1])
        self.highscore60 = int(self.content[2])
        self.highscores.close()

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
    collision = False

    chasing_projectile_timer = 0
    chasing_projectile_group = pygame.sprite.Group()
    max_chasing_projectiles = 2

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


    targetblock = Target()

    player = Player()


    projectile_timer = 0
    

    projectiles_group = pygame.sprite.Group()
    
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
                elif event.key == pygame.K_w and gamedisplay == 10:
                    fpsselector -= 1
                elif event.key == pygame.K_s and gamedisplay == 10:
                    fpsselector += 1

                if event.key == pygame.K_ESCAPE and gamedisplay > 0:
                    gamedisplay = 0
                    targetblock.score = 0
            elif event.type == pygame.MOUSEBUTTONDOWN and gamedisplay == 1:
                targetblock.check_click(event.pos)
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 3:
                player.move_towards_mouse()


    
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

            # FPS
            if(pygame.key.get_pressed()[pygame.K_RETURN] and menuselector == 0):
                screen.blit(fpsbg,(0,0))
                gamedisplay = 10
                
                if fpsselector < 0:
                    fpsselector = 2
                elif fpsselector > 2:
                    fpsselector = 0
                for x in range(0,4):
                    targetblock.targetx = random.randint(70,screenwidth-70)
                    targetblock.targety = random.randint(70,screenheight-70)
                    targetblock.targetsize[0] = random.randint(40,130)
                    targetblock.targetsize[1] = targetblock.targetsize[0]
                    targetblock.targetvalues = [targetblock.targetx,targetblock.targety,targetblock.targetsize[0],targetblock.targetsize[1]]
                    targetblock.targets[x] = (targetblock.targetvalues)
                pygame.time.wait(100)

            # MOBA
            elif(pygame.key.get_pressed()[pygame.K_RETURN] and menuselector == 1):
                gamedisplay = 2
                start_timer_moba = pygame.time.get_ticks()

            # EXIT
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
                pygame.mouse.set_visible(False)
                cursor_img_rect = targetblock.crosshairimg.get_rect()
                gamedisplay = 1
            elif(pygame.key.get_pressed()[pygame.K_RETURN] and fpsselector == 1):
                targetblock.chosenTime = 30
                start_timer = pygame.time.get_ticks()
                pygame.mouse.set_visible(False)
                cursor_img_rect = targetblock.crosshairimg.get_rect()
                gamedisplay = 1
            elif(pygame.key.get_pressed()[pygame.K_RETURN] and fpsselector == 2):
                targetblock.chosenTime = 60
                start_timer = pygame.time.get_ticks()
                pygame.mouse.set_visible(False)
                cursor_img_rect = targetblock.crosshairimg.get_rect()
                gamedisplay = 1
            
            


           

        elif(gamedisplay == 1): # FPS
                screen.blit(fpsbg, (0,0))
                cursor_img_rect.center = pygame.mouse.get_pos()
                textscore = font.render("Score: " + str(targetblock.score), True, (255, 255, 255))
                targetblock.seconds = round(targetblock.chosenTime -((pygame.time.get_ticks()- start_timer)/1000), 3)
                targetblock.targetplace(screen)
                screen.blit(textscore, (10, 10))
                screen.blit(font.render(str(targetblock.seconds), True, (255, 255, 255)), ((screenwidth//2) - 60, screenheight//16))
                screen.blit(targetblock.crosshairimg, cursor_img_rect)
                if(targetblock.seconds < 0):
                    screen.blit(fpsbg, (0,0))
                    if(targetblock.chosenTime == 10 and targetblock.highscore10 < targetblock.score):
                        targetblock.highscore10 = targetblock.score
                        targetblock.highscores = open(os.path.join("Highscores","Highscores.txt"),"w")
                        targetblock.highscores.writelines([str(targetblock.score) + "\n", str(targetblock.highscore30) + "\n", str(targetblock.highscore60) + "\n"])
                        targetblock.highscores.close()
                    if(targetblock.chosenTime == 30 and targetblock.highscore30 < targetblock.score):
                        targetblock.highscore30 = targetblock.score
                        targetblock.highscores = open(os.path.join("Highscores","Highscores.txt"),"w")
                        targetblock.highscores.writelines([str(targetblock.highscore10) + "\n", str(targetblock.score) + "\n", str(targetblock.highscore60) + "\n"])
                        targetblock.highscores.close()
                    if(targetblock.chosenTime == 60 and targetblock.highscore60 < targetblock.score):
                        targetblock.highscore60 = targetblock.score
                        targetblock.highscores = open(os.path.join("Highscores","Highscores.txt"),"w")
                        targetblock.highscores.writelines([str(targetblock.highscore10) + "\n", str(targetblock.highscore30) + "\n", str(targetblock.score) + "\n"])
                        targetblock.highscores.close()
                    screen.blit(font.render("Your score on " + str(targetblock.chosenTime) + " seconds is " + str(targetblock.score), True, (255, 255, 255)), ((screenwidth//2) - 400, screenheight//16))
                    screen.blit(font.render("Highscore on 10 seconds: " + str(targetblock.highscore10), True, (0, 255, 255)), ((screenwidth//2) - 365, screenheight//2.5))
                    screen.blit(font.render("Highscore on 30 seconds: " + str(targetblock.highscore30), True, (0, 255, 255)), ((screenwidth//2) - 365, screenheight//2.2))
                    screen.blit(font.render("Highscore on 60 seconds: " + str(targetblock.highscore60), True, (0, 255, 255)), ((screenwidth//2) - 365, screenheight//1.9))
                    screen.blit(fontreturn.render("Press Escape to return to Main Menu", True, (255, 255, 255)), ((screenwidth//2) - 175, screenheight//1.2))

        elif(gamedisplay == 2): # MOBA
            player.seconds = round(0 +((pygame.time.get_ticks()- start_timer_moba)/1000), 3)
            player.rect.center = player.x, player.y
        
            chasing_projectile_timer += 1
            if chasing_projectile_timer >= 150 and len(chasing_projectile_group) < max_chasing_projectiles:  # Tworzenie co 5 sekund
                chasing_projectile = ChasingProjectile(player)
                chasing_projectile_group.add(chasing_projectile)
                chasing_projectile_timer = 0
            
            projectile_timer += 1
            collisions = pygame.sprite.spritecollide(player, projectiles_group, False) or pygame.sprite.spritecollide(player, chasing_projectile_group, False)
            player.update()

            if (projectile_timer) >= 25: 
                direction = random.choice(["down", "up", "left", "right"])
                speed = random.randint(7, 10)
                projectile = Projectiles(direction, speed)
                projectiles_group.add(projectile)
                projectile_timer = 0  

            chasing_projectile_group.update()  
            projectiles_group.update()
            screen.blit(fpsbg,(0,0))
            screen.blit(font.render(str(player.seconds), True, (255, 255, 255)), ((screenwidth//2) - 60, screenheight//16))
            screen.blit(player.image,player.rect)

            projectiles_group.draw(screen)
            chasing_projectile_group.draw(screen)
            if (collisions):
                collision = True
                player.score = player.seconds
            if(collision):
                screen.blit(fpsbg, (0,0))
                if(player.score > player.highscoreMOBA):
                    player.highscoreMOBA = player.score
                    player.highscores = open(os.path.join("Highscores","HighscoreMOBA.txt"),"w")
                    player.highscores.writelines([str(player.highscoreMOBA)])
                    player.highscores.close()
                player.x = screenwidth//2
                player.y = screenheight//2
                player.mouse_pos = (screenwidth//2, screenheight//2)
                screen.blit(font.render("Your score is " + str(player.score) , True, (255, 255, 255)), ((screenwidth//2) - 270, screenheight//16))
                screen.blit(font.render("Highscore: " + str(player.highscoreMOBA), True, (0, 255, 255)), ((screenwidth//2) - 250, screenheight//2.6))
                screen.blit(fontreturn.render("Press Escape to return to Main Menu", True, (255, 255, 255)), ((screenwidth//2) - 175, screenheight//1.2))
                player.seconds = 0

                for sprite in projectiles_group:
                    sprite.kill()
                for sprites in chasing_projectile_group:
                    sprites.kill()

                

        pygame.display.flip()
main()
