import pygame
import random
import math
from nn import NN
import time
from geneticsManager import Manager
# <div>Bird Icon made by <a href="https://www.flaticon.com/authors/freepik" title="Freepik">Freepik</a> from <a href="https://www.flaticon.com/" title="Flaticon">www.flaticon.com</a></div>

pipesCrossed = 0


class Pipe(pygame.sprite.Sprite):
    GAP = 100

    def __init__(self, x, y):
        self.x = x
        self.y = y  # center of the gap
        self.upRect = pygame.Rect(x, 0, 70, y-self.GAP)
        # height value dosent matter
        self.downRect = pygame.Rect(x, y+20, 70, 600)

    def setX(self, x):
        self.upRect.move_ip(-x, 0)
        self.downRect.move_ip(-x, 0)
        self.x = self.x - x

    def getX(self):
        return self.x

    def getY(self):
        return self.y

    def drawPipe(self, screen):
        pygame.draw.rect(screen, (0, 0, 0), self.upRect)
        pygame.draw.rect(screen, (0, 0, 0), self.downRect)
        pass

    def collides(self, playerRect):
        if self.upRect.colliderect(playerRect.image):
            playerRect.setDone()
        if self.downRect.colliderect(playerRect.image):
            playerRect.setDone()

    def distanceToPipe(self, playerX, playerY):
        xDif = (self.x - playerX)/350.0
        yDif = (self.y - playerY)/300.0
        return [xDif, yDif]


class Player(pygame.sprite.Sprite):
    def __init__(self, nuet=None):
        self.r = random.randint(0, 255)
        self.g = random.randint(0, 255)
        self.b = random.randint(0, 255)
        self.x = 10
        self.y = 300
        self.image = pygame.Rect(self.x, self.y, 40, 40)
        self.done = False
        self.deathTime = -1
        self.nuernet = nuet
        self.curTime = time.time()

    def drawPlayer(self, screen):

        if(self.done == True):
            return
        pygame.draw.rect(screen, (self.r, self.g, 0), self.image)

    def moveY(self, dY):

        if(self.done):
            return
        self.image.move_ip(0, dY)
        self.y += dY
        if((self.y > 600 or self.y < 0) and not self.done):
            self.deathTime = time.time() - currentTime
            self.done = True

    def getY(self):
        return self.y

    def setDone(self):
        if(self.done == True):
            return
        self.deathTime = time.time() - currentTime
        self.done = True

    def checkForGround(self, ground, sky):
        pass
        # if self.image.colliderect(ground) and not self.done:
        #     self.done = True
        #     self.deathTime = time.time() - currentTime
        #     print('done')
        # if self.image.colliderect(sky) and not self.done:
        #     self.done = True
        #     self.deathTime = time.time() - currentTime
        #     print('ss')


pygame.init()
m = Manager()
net = NN(2, 5, 2, 1)

ground = pygame.Rect(-5, 0, 350, 40)
sky = pygame.Rect(-5, 1000, 400, 380)

screen = pygame.display.set_mode((350, 600))
pygame.display.set_caption("flappy bird with feed forward nueral network")
icon = pygame.image.load("bird.png")
pygame.display.set_icon(icon)

currentTime = time.time()

playerXPos = 69
playerYPos = 69
dy = -5  # gravity for bird


onScreenPipes = []
p1 = Pipe(300, 300)

pygame.display.flip()
onScreenPipes.append(p1)
pipeDX = 5


woof = Player()


def isOnScreen(pipe):
    if pipe.getX() < 0:
        return False
    return True


def resetTime():
    global currentTime
    meee = time.time()
    currentTime = meee
    print('s')


def getOnScreenPipes():
    return onScreenPipes


def resetPipes():
    onScreenPipes.clear()
    newPipe = Pipe(300, 300)
    onScreenPipes.append(newPipe)


running = True
while running:
    screen.fill((3, 186, 252))
    woof.moveY(-dy)
    woof.drawPlayer(screen)
    m.act(screen)
    m.checkForGround(ground, sky)
    for p in onScreenPipes:
        #print(p.distanceToPipe(10/350.0, woof.getY()/600.0))
       # out = net.forward_prop(p.distanceToPipe(10/350.0, woof.getY()/600.0))
        # print(out)
        xPos = p.getX()
        p.drawPipe(screen)
        p.collides(woof)
        if xPos < 0:
            pipesCrossed = pipesCrossed + 1
            onScreenPipes.remove(p)
            nHeight = random.randint(100, 500)
            newPipe = Pipe(400, nHeight)
            onScreenPipes.append(newPipe)
            continue

        p.setX(pipeDX)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            quit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                m.printRemaining()
                woof.moveY(-50)

    pygame.display.update()
