
# TODO: get 5 closest asteroids
# TODO: calculate neurons...

import pygame
import math
import random
import time
from AI import *
from Bullets import *
from Asteroids import *

pygame.init()

HomingBullets = False
NumBullets = 1
AutoFireDelay = 0.5
RotSpeed = 5
pHealth = 5
width = 1200
height = 600
maxAsteroids = 10  # maximum number of Asteroids, can exist more but can't spawn anymore if above it
points = 0
ShowHitboxes = False
asteroidSpeed = [2, 3, 4]
aSize = [1, 2, 3]  # asteroid size

win = pygame.display.set_mode((width, height))

font = pygame.font.Font('freesansbold.ttf', 32)
text = font.render('Points: {}'.format(points), True, (0, 0, 0), (255, 255, 255))

HP = font.render('Health: {}'.format(pHealth), True, (0, 0, 0), (255, 255, 255))
HPrect = HP.get_rect()
HPrect.center = (width - 100, 50)
textRect = text.get_rect()
textRect.center = (100, 50)
pygame.display.set_caption("Shooter Game")

pSize: int = 50  # size of the player

radian = 0.0174532925
degree = 57.2957795
# ------------------------------------------------------------------------------------------


def getDist(pa, pb):  # Get the distance using pythagoras theory

    if pa[0] > pb[0]:
        a = pa[0] - pb[0]
    else:
        a = pb[0] - pa[0]

    if pa[1] > pb[1]:
        b = pa[1] - pb[1]
    else:
        b = pb[1] - pa[1]

    c = round(math.sqrt(a**2 + b**2))
    return c

# ------------------------------------------------------------------------------------------


allAsteroids = 0
totalAsteroids = 0
listAsteroids = {}


def spawnAsteroid(x=None, y=None, size=None, direction=None):
    global allAsteroids, asteroidSpeed
    r = random.choice([0, 1, 2, 3])

    if x is None and y is None and direction is None:
        if r == 0:  # get a random number between 0-3 witch corresponds with the side (top, bottom, left, right)
            x = width + 100  # then assign x, y and direction
            y = random.randint(-100, height + 100)
            if y > width / 2:
                direction = random.randint(180, 225)
            else:
                direction = random.randint(135, 180)  # right

        if r == 1:
            x = -100
            y = random.randint(-100, height + 100)
            if y > width / 2:
                direction = random.randint(-45, 0)
            else:
                direction = random.randint(0, 45)  # left

        if r == 2:
            x = random.randint(-100, width + 100)
            y = -100
            if x > width / 2:
                direction = random.randint(90, 135)
            else:
                direction = random.randint(45, 90)  # bottom

        if r == 3:
            x = random.randint(-100, width + 100)
            y = height + 100
            if x > width / 2:
                direction = random.randint(-135, -90)
            else:
                direction = random.randint(-90, -45)  # top

        if random.choice([0, 1]) == 1:
            direction = math.atan2(pX-x, pY-y)  # 50% chance to spawn asteroid heading to player

    speed = random.choice(asteroidSpeed)  # set random speed between 4 and 10

    if size is None:
        size = random.choice(aSize)

    listAsteroids['{}asteroid'.format(allAsteroids)] = asteroid(x, y, direction, size, (2 ** size) / 2, speed, 1000, 0, 0)
    # add asteroid
    allAsteroids += 1


# ------------------------------------------------------------------------------------------

def drawAsteroid(x, y, size, T):
    s = size * 25

    x1 = x + (s + 10) * math.cos((0+T) * radian)  # define points
    y1 = y + (s - 3) * math.sin((0+T) * radian)

    x2 = x + (s + 4) * math.cos((45+T) * radian)
    y2 = y + (s + 3) * math.sin((45+T) * radian)

    x3 = x + (s - 9) * math.cos((100+T) * radian)
    y3 = y + (s - 7) * math.sin((100+T) * radian)

    x4 = x + (s + 1) * math.cos((140+T) * radian)
    y4 = y + (s + 0) * math.sin((140+T) * radian)

    x5 = x + (s + 4)* math.cos((180+T) * radian)
    y5 = y + (s + 5)* math.sin((180+T) * radian)

    x6 = x + (s + 5) * math.cos((210+T) * radian)
    y6 = y + (s - 2) * math.sin((210+T) * radian)

    x7 = x + (s + 7) * math.cos((265+T) * radian)
    y7 = y + (s + 1) * math.sin((265+T) * radian)

    x8 = x + s * math.cos((335+T) * radian)
    y8 = y + s * math.sin((335+T) * radian)

    pygame.draw.polygon(win, (255, 255, 255),
                        [(x1, y1), (x2, y2), (x3, y3), (x4, y4), (x5, y5), (x6, y6), (x7, y7), (x8, y8)], 1)
    # draw asteroid


# ------------------------------------------------------------------------------------------

def destroyAsteroid(a):
    global points

    x = listAsteroids.get(a).x
    y = listAsteroids.get(a).y
    direc = listAsteroids.get(a).rotation
    size = listAsteroids.get(a).size

    del listAsteroids[a]  # delete asteroid
    if size != 1:  # if asteroid is not at its smallest size
        spawnAsteroid(x=x, y=y, size=size - 1, direction=direc + 30)  # spawn two new ones at a smaller size
        spawnAsteroid(x=x, y=y, size=size - 1, direction=direc - 30)
    points += 1


listBullets = {}
nBullets = 0


def spawnBullet(x, y, direction):  # create bullet from bullet class and add to dict
    global nBullets
    '''
    newBullet = bullet(x, y, direction, 0)
    listBullets['{}bullet'.format(nBullets)] = newBullet
    nBullets += 1
    '''
    for i in range(NumBullets):
        newBullet = bullet(x, y, direction+round((i+1) * (360/NumBullets)), 0)
        listBullets['{}bullet'.format(nBullets)] = newBullet
        nBullets += 1


def drawPlayer(x, y, rotation):  # calculates triangle points and draws the player
    p1x = x + (pSize / 2 * math.cos(rotation * radian))
    p1y = y + (pSize / 2 * math.sin(rotation * radian))

    p2x = x + (pSize / 2 * math.cos((rotation + 140) * radian))
    p2y = y + (pSize / 2 * math.sin((rotation + 140) * radian))

    p3x = x + (pSize / 2 * math.cos((rotation - 140) * radian))
    p3y = y + (pSize / 2 * math.sin((rotation - 140) * radian))

    pygame.draw.polygon(win, (255, 255, 255), [(p1x, p1y), (p2x, p2y), (p3x, p3y)], 1)


# ------------------------------------------------------------------------------------------

run = True
pX = width / 2  # starting x and y for the player p = player
pY = height / 2
pRotation = 0  # starting rotation for player in degrees, 0 is right
rotSpeed = 0
bulletSpeed = 20
pAccel = 0
wasPressed = 0 # if the space bar was pressed last frame
turnReset = 5
accelReset = 5

# ------------------------------------------------------------------------------------------

while run:

    pygame.time.delay(25)  # framerate
    win.fill((0, 0, 0))

    for event in pygame.event.get():  # if click the red cross, exit
        if event.type == pygame.QUIT:
            run = False
    if pHealth <= 0:
        run = False
    # ------------------------------------------------------------------------------------------
    keys = pygame.key.get_pressed()

    if keys[pygame.K_d]:  # if d key is pressed and so on
        if rotSpeed < 6:
            rotSpeed += 0.4
        turnReset = 5  # turnReset decreases every frame, if it reaches 0 it resets the turning
    elif rotSpeed > 2:  # it is set to 5 every frame the key is pressed
        rotSpeed -= 0.4  # reason: to avoid it getting stuck turning
    elif rotSpeed > 0:
        rotSpeed -= 0.1

    if keys[pygame.K_a]:
        if rotSpeed > -6:
            rotSpeed -= 0.4
        turnReset = 5
    elif rotSpeed < -2:
        rotSpeed += 0.4
    elif rotSpeed < 0:
        rotSpeed += 0.1

    pRotation += rotSpeed

    if keys[pygame.K_w]:
        if pAccel < 10:
            pAccel += 0.4
        accelReset = 5  # same as turnReset
    elif pAccel > 2:
        pAccel -= 0.4
    elif pAccel > 0:
        pAccel -= 0.1

    if keys[pygame.K_s]:
        if pAccel > -10:
            pAccel -= 0.4
        accelReset = 5
    elif pAccel < -2:
        pAccel += 0.4
    elif pAccel < 0:
        pAccel += 0.1

    # ------------------------------------------------------------------------------------------

    turnReset -= 0.1  # decreases every frame
    accelReset -= 0.1
    if turnReset <= 0:
        turnReset = 5
        rotSpeed = 0
    if accelReset <= 0:
        accelReset = 5
        pAccel = 0

    # ------------------------------------------------------------------------------------------

    pX += pAccel * math.cos(pRotation * radian)  # calculates new position based on speed
    pY += pAccel * math.sin(pRotation * radian)

    if pX < 0 - pSize:  # teleports player to other side if out of bounds
        pX = width + pSize
    if pY < 0 - pSize:
        pY = height + pSize
    if pX > width + pSize:
        pX = 0 - pSize
    if pY > height + pSize:
        pY = 0 - pSize

    # ------------------------------------------------------------------------------------------

    if keys[pygame.K_SPACE]:  # if space bar is pressed spawn a bullet
        if wasPressed <= 0:
            spawnBullet(pX, pY, pRotation)
            wasPressed = AutoFireDelay
        elif wasPressed > 0:
            wasPressed -= 0.1
    else:
        wasPressed = 0


    # ------------------------------------------------------------------------------------------

    remove = []
    for b in listBullets:  # for every bullet on screen, calculate its new position, draw it and remove if its too old
        x = listBullets.get(b).x
        y = listBullets.get(b).y
        direc = listBullets.get(b).direction

        listBullets.get(b).x += bulletSpeed * math.cos(direc * radian)
        listBullets.get(b).y += bulletSpeed * math.sin(direc * radian)

        if x < 0 - pSize:
            listBullets.get(b).x = width + pSize  # teleports to other side of screen if it goes off screen
        if y < 0 - pSize:
            listBullets.get(b).y = height + pSize
        if x > width + pSize:
            listBullets.get(b).x = 0 - pSize
        if y > height + pSize:
            listBullets.get(b).y = 0 - pSize

        x = listBullets.get(b).x
        y = listBullets.get(b).y
        pygame.draw.polygon(win, (255, 255, 255),
                            [(x + 2, y + 2), (x + 2, y - 2), (x - 2, y - 2), (x - 2, y + 2)])  # draw bullet

        listBullets.get(b).age += 0.1  # increase age
        if listBullets.get(b).age > 10:  # send old bullets to list
            remove.append(b)

    # ------------------------------------------------------------------------------------------
    totalAsteroids = len(listAsteroids)
    if totalAsteroids < maxAsteroids:
        spawnAsteroid()

    def distGet(n):
        return listAsteroids.get(shortestDistance[n])

    shortestDistance = []
    destroy = []
    aremove = []
    for a in listAsteroids:
        s = listAsteroids.get(a).size * 25
        direc = listAsteroids.get(a).rotation
        speed = listAsteroids.get(a).speed
        listAsteroids.get(a).time += RotSpeed
        listAsteroids.get(a).x += speed * math.cos(direc * radian)
        listAsteroids.get(a).y += speed * math.sin(direc * radian)
        x = listAsteroids.get(a).x
        y = listAsteroids.get(a).y
        drawAsteroid(x, y, listAsteroids.get(a).size, listAsteroids.get(a).time)

        if x < -110 or x > width + 110 or y < -110 or y > height + 110:
            aremove.append(a)

        if listAsteroids.get(a).health <= 0:
            destroy.append(a)

        listAsteroids.get(a).distance = getDist([x, y], [pX, pY])

        listAsteroids.get(a).angle = math.atan2(x-pX, y-pY)  # arctangent2 to calculate angle to player

        if x + s + pSize / 2 > pX > x - s - pSize / 2 and y + s + pSize / 2 > pY > y - s - pSize / 2:
            aremove.append(a)
            pHealth -= 1

        if ShowHitboxes:
            pygame.draw.rect(win, (255, 0, 0), (pygame.Rect(x - s, y - s, s * 2, s * 2)), 1)

        notSmaller = True
        if len(shortestDistance) < 5:
            shortestDistance.append(a)

        # ----------------------------------------------
        smallest = 0
        smallestValue = 999999

        if len(shortestDistance) > 5:
            if distGet(0).distance < listAsteroids.get(a).distance:
                smallest = 0
                smallestValue = distGet(0).distance

            if distGet(1).distance < listAsteroids.get(a).distance:
                if distGet(1).distance < smallestValue:
                    smallestValue = distGet(1).distance
                    smallest = 1

            if distGet(2).distance < listAsteroids.get(a).distance:
                if distGet(2).distance < smallestValue:
                    smallestValue = distGet(2).distance
                    smallest = 2

            if distGet(3).distance < listAsteroids.get(a).distance:
                if distGet(3).distance < smallestValue:
                    smallestValue = distGet(3).distance
                    smallest = 3

            if distGet(4).distance < listAsteroids.get(a).distance:
                if distGet(4).distance < smallestValue:
                    smallestValue = distGet(4).distance
                    smallest = 4

            if smallestValue != 999999:
                del shortestDistance[smallest]
                shortestDistance.append(a)
        # ----------------------------------------------

    for a in aremove:
        if a in listAsteroids:
            del listAsteroids[a]

    for a in destroy:
        if a in listAsteroids:
            destroyAsteroid(a)

    # ------------------------------------------------------------------------------------------

    for b in listBullets:
        bx = listBullets.get(b).x
        by = listBullets.get(b).y
        for a in listAsteroids:
            ax = listAsteroids.get(a).x

            ay = listAsteroids.get(a).y
            s = listAsteroids.get(a).size * 25

            if ax - s < bx < ax + s and ay - s < by < ay + s:
                listAsteroids.get(a).health -= 1
                remove.append(b)
                break

    for b in remove:  # remove bullets in the list
        if b in listBullets:
            del listBullets[b]

    # ------------------------------------------------------------------------------------------

    for r in robots:
        if robots.get(r).delete:
            del robots[r]

    drawPlayer(pX, pY, pRotation)
    if ShowHitboxes:
        pygame.draw.rect(win, (255, 0, 0), (pygame.Rect(pX - pSize / 2, pY - pSize / 2, pSize, pSize)), 1)

    text = font.render('Points: {}'.format(points), True, (0, 0, 0), (255, 255, 255))
    win.blit(text, textRect)
    HP = font.render('Health: {}'.format(pHealth), True, (0, 0, 0), (255, 255, 255))
    win.blit(HP, HPrect)

    maxAsteroids = 10 + math.floor(points / 100)

    asteroidSpeed = [2, 3, 4]
    for i in range(math.floor(points / 200)):
        asteroidSpeed.append(i + 5)
    pygame.display.update()


win.fill((0, 0, 0))

font = pygame.font.Font('freesansbold.ttf', 42)
game_over = font.render('Game Over', True, (255, 255, 255), (0, 0, 0))
GOrect = game_over.get_rect()
GOrect.center = (width/2, height/2)

font = pygame.font.Font('freesansbold.ttf', 32)
finScore = font.render('Final Score: {}'.format(points), True, (255, 255, 255), (0, 0, 0))
finScoreRect = finScore.get_rect()
finScoreRect.center = (width/2, height/2 + 50)

win.blit(game_over, GOrect)
win.blit(finScore, finScoreRect)
pygame.display.update()
time.sleep(5)
