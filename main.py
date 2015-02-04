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

bgr_path = os.path.join('.\materials', 'bgr.png')
car_b_path = os.path.join('.\materials', 'blue_car.png')
car_y_path = os.path.join('.\materials', 'yellow_car.png')

#### SELECTING TEMP
playerCarSkin = car_b_path
AICarSkin = car_y_path

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

class PlayerCar(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        
        self.image = pygame.image.load(playerCarSkin).convert_alpha() #alpha for transparency
        self.rect = self.image.get_rect()
        
        self.lane = 1
        self.x = 0
        self.y = 0
        
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
        self.setLane(1)
        area.blit(self.image, (self.x, self.y))

    def move(self):
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT:
                    if self.lane < 4:
                        self.lane = self.lane + 1
                    else:
                        db('NO LANE')
            
                if event.key == pygame.K_LEFT:
                    if self.lane > 1:
                        self.lane = self.lane - 1
                    else:
                        db('NO LANE')

class AICar(pygame.sprite.Sprite): 
    def __init__(self, rand_lane, speed):
        
        self.image = pygame.image.load(AICarSkin).convert_alpha()
        self.rect = self.image.get_rect()
        
        self.lane = rand_lane
        self.x = 0
        self.y = 0
        self.spd = speed
        self.setLane()
        
        pygame.sprite.Sprite.__init__(self, carList)
        
    def setLane(self):
        if self.lane == 1:
            self.x, self.y = lane1[0], lane1[2]
            self.rect.x, self.rect.y = lane1[0], lane1[2]
        elif self.lane == 2:
            self.x, self.y = lane2[0], lane2[2]
            self.rect.x, self.rect.y = lane2[0], lane2[2]
        elif self.lane == 3:
            self.x, self.y = lane3[0], lane3[2]
            self.rect.x, self.rect.y = lane3[0], lane3[2]
        elif self.lane == 4:
            self.x, self.y = lane4[0], lane4[2]
            self.rect.x, self.rect.y = lane4[0], lane4[2]
            
    def drawObj(self, area):
        #self.setLane(1)
        area.blit(self.image, (self.x, self.y))

    def move_down(self):
        self.y = self.y + self.spd
        self.rect.y = self.y
        
    def kill_self(self):
        del self

stopping = False
#first AI thread
def addAI():
    while not stopping:
        db('spawning')
        #carList.add(AICar(random.randint(1,3)))
        aicar = AICar(random.randint(1,2),random.randint(5,20))
        time.sleep(1.5)
        addAI()
    if stopping == True:
        time.sleep(60)

#second AI thread
def addAI2():
    while not stopping:
        db('spawning2')
        #carList.add(AICar(random.randint(1,3)))
        aicar = AICar(random.randint(3,4),random.randint(5,20))
        time.sleep(1.5)
        addAI2()
    if stopping == True:
        time.sleep(60)
    
pygame.init()
screen = pygame.display.set_mode((800, 600))
pygame.key.set_repeat()


player = PlayerCar()

carList = pygame.sprite.Group()
carList2 = pygame.sprite.Group()

t = Thread(target=addAI)
t.daemon = True
t.start()

t2 = Thread(target=addAI2)
t2.daemon = True
t2.start()

#aicar = AICar(random.randint(1,3))

#carList.add(AICar(1))

clock = pygame.time.Clock()

running = True
while running:
    screen.fill((255,255,255))
    screen.blit(bground, (0,0))
    
    #DRAW OBJECTS
    player.drawObj(screen) #draw player
    for aicar in carList:
        aicar.drawObj(screen)
    
    #CHECK INPUT
    events = pygame.event.get() #get events before moving!!!!
    
    for event in events: ## EXIT GAME
        if event.type == pygame.QUIT:
            db("closing")
            stopping = True
            db("closing sleep")
            time.sleep(1)
            pygame.quit()
            db("closing")
            sys.exit()
    
    ## PLAYER INPUT      
    player.move()
    for aicar in carList:
        aicar.move_down()
    dblong(carList.sprites())

    if pygame.sprite.spritecollide(player, carList, True):
        db("COLLISION")
        
    for aicar in carList:
        if pygame.sprite.spritecollide(aicar, carList2, True):
            db("c")

    for aicar in carList2:
        if pygame.sprite.spritecollide(aicar, carList, True):
            db("c")
        
    for aicar in carList:
        if aicar.rect.y > 520:
            db("removing")
            carList.remove(aicar)
    
    pygame.display.update()
    clock.tick(30)
