import pygame
from pygame.draw import *
from random import randint
from numpy import sin, cos, pi

pygame.init()

FPS = 10
screen = pygame.display.set_mode((1200, 700))

RED = (255, 0, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
GREEN = (0, 255, 0)
MAGENTA = (255, 0, 255)
CYAN = (0, 255, 255)
BLACK = (0, 0, 0)
COLORS = [RED, BLUE, YELLOW, GREEN, MAGENTA, CYAN]


def new_ball():
    '''рисует новый шарик '''
    x = randint(100, 1100)
    y = randint(100, 900)
    r = randint(10, 100)
    color = COLORS[randint(0, 5)]
    circle(screen, color, (x, y), r)
    return x, y, r, color


def move_ball(x, y, r, color, vector):
    x = x + vector[0]
    y = y + vector[1]
    screen.fill(BLACK)
    circle(screen, color, (x, y), r)
    pygame.display.update()
    return x, y, r, color


pygame.display.update()
clock = pygame.time.Clock()
finished = False

# xb = -1
# yb = -1
# r = 0
score = 0

xb, yb, r, color = new_ball()
l = 4
agle = randint(0, 360)
direction = [l * cos(agle * pi / 180), l * sin(agle * pi / 180)]
pygame.display.update()
while not finished:
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            print('Score: ', score)
            finished = True
        elif event.type == pygame.MOUSEBUTTONDOWN:
            x, y = event.pos
            if (x - xb) ** 2 + (y - yb) ** 2 <= (r ** 2):
                print('Nice')
                score += 100
                screen.fill(BLACK)
                xb, yb, r, color = new_ball()
                l = 0
                agle = randint(0, 360)
                direction = [l * cos(agle * pi / 180), l * sin(agle * pi / 180)]
                pygame.display.update()

            else:
                print('Ha')
    xb, yb, r, color = move_ball(xb, yb, r, color, direction)
    # direction = [l * cos(agle * pi / 180), l * sin(agle * pi / 180)]
    if xb < 20 or xb > 1180:
        if agle < 270 and agle > 90:
            agle = randint(-90, 90)
        else:
            agle = randint(90, 270)
        direction = [l * cos(agle * pi / 180), l * sin(agle * pi / 180)]
        xb, yb, r, color = move_ball(xb, yb, r, color, direction)
    if yb < 20 or yb > 680:
        if agle > 0 and agle < 180:
            agle = randint(180, 360)
        else:
            agle = randint(0, 180)
        direction = [l * cos(agle * pi / 180), l * sin(agle * pi / 180)]
        xb, yb, r, color = move_ball(xb, yb, r, color, direction)
pygame.quit()
