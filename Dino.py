import pygame as py
import random
import datetime
import math
import colorsys
py.init() #init pygame
font = py.font.Font(None, 74) # use default font
display = py.display.set_mode((700, 500)) #make a display with 1000 x 1000
py.display.set_caption("Broom") #set caption to Broom
py.font.init() # init pygame font
loop = True #should the loop run
clock = py.time.Clock()
CactusImg = py.image.load('cactus.png')
CactusHeights = [80, 40, 20, 80, 30]
CactusXpos = []
meters = 0
for i in range(1,5):
    CactusXpos.append(random.randrange(200, 3000))
    
class player:
    x = 20
    y = 480
    yVel = 0
    onGround = False
    alive = True
    def move(self):
        self.y = self.y + self.yVel
    def fall(self):
        if self.y < 480:
            self.y = self.y + 1
    def kill(self):
        self.alive = False
    def checkGround(self):
        if self.y < 480:
            self.onGround = False
            self.yVel += 1
        else:
            self.onGround = True
            self.yVel = 0

dino = player()

def keyInput():
    keys = py.key.get_pressed()
    if keys[py.K_SPACE] and dino.onGround:
        dino.yVel = -20
        
def rainbow():
    h1 = colorsys.hsv_to_rgb((((math.ceil((datetime.datetime.now().timestamp() * 500) / 20)) / 360)), 1, 1)
    (r, g, b) = h1
    r*=255
    g*=255
    b*=255
    r = round(r)
    g = round(g)
    b = round(b)
    return (r, g, b)

def render():
    display.fill((0,0,0))
    text =font.render(str(meters),1,rainbow())
    display.blit(text,(250,10))
    for i, y in zip(CactusXpos, CactusHeights):
        display.blit(CactusImg, (i-15, 480 - y))
    py.draw.rect(display, (255, 255, 255), (dino.x, dino.y, 20, 20))
    py.display.flip()

def renderDeath():
    display.fill((0,0,0))
    text =font.render(str("You died at {} Meters! :(".format(meters)),1,rainbow())
    display.blit(text,(0,250))
    
    py.display.flip()
    
while loop:
    clock.tick(60)
    rainbow()
    for event in py.event.get():
        if event.type == py.QUIT:
            loop = False
            
    keyInput()
    if dino.alive:
        dino.move()
        meters = (meters + 1)
        dino.fall()
        dino.checkGround()
    
    CactusXpos = [x - 10 for x in CactusXpos]
    for x in range(len(CactusXpos)):
        if CactusXpos[x] < 0:
            CactusXpos[x] = random.randrange(640, 5000)
    for x, y in zip(CactusXpos, CactusHeights):
        a = py.Rect((x, 480-y), (30, 100))
        b = py.Rect((dino.x, dino.y), (20, 20))
        if a.colliderect(b):
            dino.kill()
    if dino.alive:
        render()
    else:
        renderDeath()

    
    
    
    
py.quit()