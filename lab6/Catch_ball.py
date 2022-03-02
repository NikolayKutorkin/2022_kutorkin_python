import pygame
from pygame.draw import *
from random import randint
from numpy import sin, cos, pi

pygame.init()

FPS = 60
screen = pygame.display.set_mode((1200, 700))

RED = (255, 0, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
GREEN = (0, 255, 0)
MAGENTA = (255, 0, 255)
CYAN = (0, 255, 255)
BLACK = (0, 0, 0)
COLORS = [RED, BLUE, YELLOW, GREEN, MAGENTA, CYAN]
l = 4


def new_ball():
    '''рисует новый шарик '''
    screen.fill(BLACK)
    x = randint(100, 1100)
    y = randint(100, 650)
    r = randint(30, 100)
    color = COLORS[randint(0, 5)]
    circle(screen, color, (x, y), r)
    pygame.display.update()
    angle = randint(0, 360)
    return [x, y, r, color, angle]


def move_ball(ball):
    x = ball[0]
    y = ball[1]
    r = ball[2]
    color = ball[3]
    angle = ball[4]
    circle(screen, (0, 0, 0), (x, y), r + 5)
    ball[0] += l * cos(ball[4] * pi / 180)
    ball[1] += l * sin(ball[4] * pi / 180)
    circle(screen, color, (x, y), r)
    pygame.display.update()
    return [x, y, r, color, angle]


pygame.display.update()
clock = pygame.time.Clock()
finished = False


score = 0
box = []
# 0 , 1 , 2,     3,     4.
# xb, yb, r, color, angle = new_ball()
# xb, yb, r, color, angle = new_ball()
for i in range(7):
    ball = new_ball()
    box.append(ball)
pygame.display.update()
while not finished:
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            print('Score: ', score)
            finished = True
        elif event.type == pygame.MOUSEBUTTONDOWN:
            for ball in box:
                x, y = event.pos
                if (x - ball[0]) ** 2 + (y - ball[1]) ** 2 <= ball[2] ** 2:
                    print('Nice')
                    score += 100
                    xb, yb, r, color, angle = new_ball()
                    ball[0] = xb
                    ball[1] = yb
                    ball[2] = r
                    ball[3] = color
                    ball[4] = angle

                else:
                    print('Ha')
    # screen.fill(BLACK)
    for ball in box:
        if ball[0] < ball[2] + 2 or ball[0] > 1200 - ball[2] - 2:
            if 270 > ball[4] > 90:
                ball[4] = randint(-50, 50)
            else:
                ball[4] = randint(130, 230)
            ball = move_ball(ball)
            ball = move_ball(ball)
            ball = move_ball(ball)

        if ball[1] < ball[2] + 2 or ball[1] > 700 - ball[2] - 2:
            if 0 < ball[4] < 180:
                ball[4] = randint(220, 320)
            else:
                ball[4] = randint(40, 140)
            ball = move_ball(ball)
            ball = move_ball(ball)
            ball = move_ball(ball)
        ball = move_ball(ball)
            # xb, yb, r, color = move_ball(xb, yb, r, color, angle)
pygame.quit()
