#Mew's good game
import pygame
import os, sys
import random
import time
from threading import Thread

######################
DEBUG = True
DEBUGL = False
######################

#### SELECTING TEMP
bgr_path = 'materials\m_bgr.png'
playerCarSkin = 'materials\m_blue_car.png'
AICarSkin = 'materials\yellow_car.png'
coinSkin = 'materials\coin.png'
bground = pygame.image.load(bgr_path)

#Set up global lanes as tables
lane1 = {}
lane2 = {}
lane3 = {}
lane4 = {}
start_pos_ai = 0
lane1[0], lane1[1], lane1[2] = 40, 500, start_pos_ai
lane2[0], lane2[1], lane2[2] = 180, 500, start_pos_ai
lane3[0], lane3[1], lane3[2] = 320, 500, start_pos_ai
lane4[0], lane4[1], lane4[2] = 460, 500, start_pos_ai

## other
score_i = 0
lives_i = 3

score = str(score_i)
lives = str(lives_i)
#################### MUST BE ONE OF THE FIRST FUNCTIONS!!
def db(txt):
    global DEBUG
    if DEBUG == True:
        print('debug: ', txt)
    else:
        return None

def dblong(txt):
    global DEBUGL
    if DEBUGL == True:
        print('debug: ', txt)
    else:
        return None
    
####################
db(lane4)
db(lane1[0])

#############

#############

def end_ctrl():
    for event_a in pygame.event.get():
        if event_a.type == pygame.QUIT:
            db("watwat")
            pygame.quit()
            sys.exit()
            
####################################################################################################
class PlayerCar(pygame.sprite.Sprite):
    def __init__(self):
        self.image = pygame.image.load(playerCarSkin).convert_alpha() #alpha for transparency
        self.rect = self.image.get_rect()
        
        self.lane = 1
        self.x = 0
        self.y = 0
        self.speed = 12

        pygame.sprite.Sprite.__init__(self)
        
    def setLane(self, lane):
        if self.lane == 1:
            self.x, self.y = lane1[0], lane1[1]
            self.rect.x, self.rect.y = lane1[0], lane1[1]
        elif self.lane == 2:
            self.x, self.y = lane2[0], lane2[1]
            self.rect.x, self.rect.y = lane2[0], lane2[1]
        elif self.lane == 3:
            self.x, self.y = lane3[0], lane3[1]
            self.rect.x, self.rect.y = lane3[0], lane3[1]
        elif self.lane == 4:
            self.x, self.y = lane4[0], lane4[1]
            self.rect.x, self.rect.y = lane4[0], lane4[1]
        
    def drawObj(self, area):
        #self.setLane(1)
        self.rect.y = 500
        self.y = self.rect.y
        area.blit(self.image, (self.x, self.y))

    def freemove(self):
        if (pygame.key.get_pressed()[pygame.K_LSHIFT]):
            self.speed = 20
        else:
            self.speed = 12
        if (pygame.key.get_pressed()[pygame.K_d]):
            if self.x < 500:
                self.x = self.x + self.speed
                self.rect.x = self.x
        if (pygame.key.get_pressed()[pygame.K_a]):
            if self.x > 0:
                self.x = self.x - self.speed
                self.rect.x = self.x
                    
####################################################################################################
class AICar(pygame.sprite.Sprite): 
    def __init__(self, rand_lane, speed): 
        self.image = pygame.image.load(AICarSkin).convert_alpha()
        self.rect = self.image.get_rect()
        
        self.lane = rand_lane
        self.x = 0
        self.y = 0
        self.spd = speed
        self.setLane(self.lane)
        
        pygame.sprite.Sprite.__init__(self, carList)
        
    def setLane(self, ln):
        if ln == 1:
            self.x, self.y = lane1[0], lane1[2]
            self.rect.x, self.rect.y = lane1[0], lane1[2]
        elif ln == 2:
            self.x, self.y = lane2[0], lane2[2]
            self.rect.x, self.rect.y = lane2[0], lane2[2]
        elif ln == 3:
            self.x, self.y = lane3[0], lane3[2]
            self.rect.x, self.rect.y = lane3[0], lane3[2]
        elif ln == 4:
            self.x, self.y = lane4[0], lane4[2]
            self.rect.x, self.rect.y = lane4[0], lane4[2]
            
    def drawObj(self, area):
        area.blit(self.image, (self.x, self.y))

    def move_down(self):
        self.y = self.y + self.spd
        self.rect.y = self.y
####################################################################################################
        
class Coin(pygame.sprite.Sprite):#this is very similiar to AICar class (basically same, except collision functions)
    def __init__(self, rand_lane, speed):
        self.image = pygame.image.load(coinSkin).convert_alpha()
        self.rect = self.image.get_rect()

        self.lane = rand_lane
        self.x = 0
        self.y = 0
        
        self.spd = speed
        self.setLane(self.lane)
        
        pygame.sprite.Sprite.__init__(self, coinList)

    def setLane(self, ln):
        if ln == 1:
            self.x, self.y = lane1[0] + 17, lane1[2]
            self.rect.x, self.rect.y = lane1[0] + 17, lane1[2]
        elif ln == 2:
            self.x, self.y = lane2[0] + 17, lane2[2]
            self.rect.x, self.rect.y = lane2[0] + 17, lane2[2]
        elif ln == 3:
            self.x, self.y = lane3[0] + 17, lane3[2]
            self.rect.x, self.rect.y = lane3[0] + 17, lane3[2]
        elif ln == 4:
            self.x, self.y = lane4[0] + 17, lane4[2]
            self.rect.x, self.rect.y = lane4[0] + 17, lane4[2]
        
    def drawObj(self, area):
        area.blit(self.image, (self.x, self.y))

    def move_down(self):
        self.y = self.y + self.spd
        self.rect.y = self.y
####################################################################################################

def main_init():
    global score_i, score, lives_i, lives
    #score_i = 0
    lives_i = 3

def write_score(points):
    scores = open('Scores.txt', 'a')
    scores.write(str(time.strftime("%H:%M:%S")) + ' ' + str(time.strftime("%d/%m/%Y")) + ' score: ' + str(points) + "\n")

move_all = True
running = True

## AI SPAWNERZ
stopping = False
#first AI thread (adds cars + coins)
def addAI():
    if move_all == True:
        db('spawning')
        aicar = AICar(random.randint(1,2),random.randint(10,20))
        coin = Coin(random.randint(1,4),random.randint(5,10))
    time.sleep(1)
    addAI()

#second AI thread
def addAI2():
    if move_all == True:
        db('spawning2')
        aicar = AICar(random.randint(3,4),random.randint(10,20))
    time.sleep(1)
    addAI2()

def CheckCollisionsCars():
    if pygame.sprite.spritecollide(player, carList, True):
        db("COLLISION")
        player_lives(-1)
        
    for aicar in carList:
        if pygame.sprite.spritecollide(aicar, carList2, True):
            db("c")
    for aicar in carList2:
        if pygame.sprite.spritecollide(aicar, carList, True):
            db("c")   

def CheckCollisionsCoins():
    if pygame.sprite.spritecollide(player, coinList, True):
        db("COLLECTED COIN")
        addScore(random.randint(1,5))

def addScore(sc):
    global score_i
    score_i = score_i + sc

def player_lives(n):
    global lives_i
    lives_i = lives_i + n
    
pygame.init()
screen = pygame.display.set_mode((800, 600))
icon = pygame.transform.scale(pygame.image.load(coinSkin).convert_alpha(), (32, 32))
pygame.display.set_icon(icon)
pygame.display.set_caption('GuudRally 1.0')

#pygame.key.set_repeat()

carList = pygame.sprite.Group()
carList2 = pygame.sprite.Group()
coinList = pygame.sprite.Group()

#coin = Coin(2, 2)

player = PlayerCar() ## Add player. Just one player.

### AI SPAWNER THREADS ##
t = Thread(target=addAI)
t.daemon = True
t.start()

t2 = Thread(target=addAI2)
t2.daemon = True
t2.start()
#########################

clock = pygame.time.Clock()
while running:
    score = str(score_i)
    lives = str(lives_i)
    
    screen.fill((255,255,255))
    screen.blit(bground, (0,0))


    ## DISPLAY SCORE
    score_font = pygame.font.SysFont("monospace", 20, bold=True)
    p_score = score_font.render("Your score is: " + score, 1, (0,0,0))
    p_lives = score_font.render("Lives left: " + lives, 1, (0,0,0))
    
    screen.blit(p_score, (575,50))
    screen.blit(p_lives, (575,80))

    #CHECK INPUT
    events = pygame.event.get() #get events before moving!!!!
            
    #DRAW OBJECTS
    player.drawObj(screen) #draw player

    for coin in coinList: ##draw Coin
        coin.drawObj(screen)
        
    for aicar in carList: ##draw AI cars
        aicar.drawObj(screen)
    
    ## PLAYER INPUT
    player.freemove()

    ## Make AI cars move down
    for aicar in carList:
        aicar.move_down()
    dblong(carList.sprites())
    ## same for coins
    for coin in coinList:
        coin.move_down()

    ## COLLISON CHECK
    CheckCollisionsCars()
    CheckCollisionsCoins()
                    
    ## Check for cars, travelled too far
    for aicar in carList:
        if aicar.rect.y > 520:
            db("removing")
            carList.remove(aicar)

    ## Check lives
    if lives_i == 0:
        main_init()
        move_all = False
        continue

    if move_all == False:
        score_font_f = pygame.font.SysFont("monospace", 40, bold=True)
        font_quest = pygame.font.SysFont("monospace", 24, bold=True)
        
        p_score_f = score_font_f.render("Your score is: " + score, 1, (0,0,0))
        p_endgame = score_font_f.render("GAME OVER", 1, (0,0,0))
        p_quest = font_quest.render("Press R to restart", 1, (0,0,0))
        
        screen.blit(p_endgame, (250,200))
        screen.blit(p_score_f, (200,250))
        screen.blit(p_quest, (240,300))
        
        carList.empty()
        carList2.empty()
        coinList.empty()
        
        if (pygame.key.get_pressed()[pygame.K_r]):
            write_score(score_i)
            lives_i = 3
            score_i = 0
            move_all = True
            print(move_all)
    
    for event in events: ## EXIT GAME
        if event.type == pygame.QUIT:
            db("closing")
            move_all = False
            stopping = True
            db("closing sleep")
            time.sleep(1)
            pygame.quit()
            db("closing")
            sys.exit()
    
    pygame.display.update()
    clock.tick(30)
