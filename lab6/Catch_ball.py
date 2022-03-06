import pygame
from pygame.draw import *
from random import randint, choice

# from pygame.examples.prevent_display_stretching import event

pygame.init()

HEIGHT = 600
WIDTH = 1200
N = 2  # Количесво шаров
FPS = 30
COUNTER = 0
screen = pygame.display.set_mode((WIDTH, HEIGHT))
MAX_SPEED = 50
MIN_SPEED = 20
g = 10

RED = (255, 0, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
GREEN = (0, 255, 0)
MAGENTA = (255, 0, 255)
CYAN = (0, 255, 255)
BLACK = (0, 0, 0)
COLORS = [RED, BLUE, YELLOW, GREEN, MAGENTA, CYAN]


def new_ball():
    """создаёт новый шарик """
    x = randint(100, WIDTH - 100)
    y = randint(100, HEIGHT - 100)
    r = randint(10, 100)
    v_x = choice([-1, 1]) * randint(MIN_SPEED, MAX_SPEED)
    v_y = choice([-1, 1]) * randint(MIN_SPEED, MAX_SPEED)
    color = COLORS[randint(0, 5)]
    return [x, y, r, v_x, v_y, color, 'ball']


def new_square():
    a = randint(30, 100)
    x = randint(100, WIDTH - a - 100)
    y = randint(100, HEIGHT - a - 100)
    v_x = choice([-1, 1]) * randint(MIN_SPEED, MAX_SPEED)
    v_y = choice([-1, 1]) * randint(MIN_SPEED, MAX_SPEED)
    color = COLORS[randint(0, 5)]
    return [x, y, a, v_x, v_y, color, 'square']


def rendering_(object):
    """отрисовывает новый шарик """
    if object[6] == 'ball':
        circle(screen, object[5], (object[0], object[1]), object[2])
    elif object[6] == 'square':
        rect(screen, object[5], (object[0], object[1], object[2], object[2]))


def moving_(object):
    """перемещаю новый шарик """
    t = 0.1
    if object[6] == 'ball':
        object[0] = object[0] + object[3] * t  # x + v_x * t
        object[1] = object[1] + object[4] * t  # y + v_y * t
    elif object[6] == 'square':
        object[0] += object[3] * t  # x + v_x * t
        object[1] += object[4] * t + g * t ** 2 / 2  # y + v_y * t
        object[4] += g * t
    return object


def reborn_(object):
    if object[6] == 'ball':
        object[0] = randint(100, WIDTH - 100)  # x
        object[1] = randint(100, HEIGHT - 100)  # y
        object[2] = randint(10, 100)  # r
        object[3] = choice([-1, 1]) * randint(MIN_SPEED, MAX_SPEED)  # v_x
        object[4] = choice([-1, 1]) * randint(MIN_SPEED, MAX_SPEED)  # v_y
        object[5] = COLORS[randint(0, 5)]  # color
    if object[6] == 'square':
        object[0] = randint(100, WIDTH - 100)  # x
        object[1] = randint(100, HEIGHT - 100)  # y
        object[2] = randint(30, 100)  # a
        object[3] = choice([-1, 1]) * randint(MIN_SPEED, MAX_SPEED)  # v_x
        object[4] = choice([-1, 1]) * randint(MIN_SPEED, MAX_SPEED)  # v_y
        object[5] = COLORS[randint(0, 5)]  # color
    return object


def hitting_the_wall(object):
    """проверяет шарик на соудорение со стеной и возращает новые данные шарика"""
    # [x, y, r, v_x, v_y, color]
    # [0, 1, 2,   3,   4,     5]
    border_control(object)
    if object[6] == 'ball':
        if WIDTH <= object[0] + object[2] or object[0] - object[2] <= 0:
            object[3] = -1 * object[3] / abs(object[3]) * randint(5, 20)
            object[4] = choice([-1, 1]) * randint(MIN_SPEED, MAX_SPEED)
            return object

        elif HEIGHT <= object[1] + object[2] or object[1] - object[2] <= 0:
            object[4] = -1 * object[4] / abs(object[4]) * randint(5, 20)
            object[3] = choice([-1, 1]) * randint(MIN_SPEED, MAX_SPEED)
            return object
        else:
            return object
    elif object[6] == 'square':

        if WIDTH <= object[0] + object[2] or object[0] <= 0:
            object[3] = -1 * object[3] / abs(object[3]) * randint(MIN_SPEED * 2, MAX_SPEED * 2)
            return object

        elif HEIGHT <= object[1] + object[2] or object[1] <= 0:
            object[4] = -1 * object[4] / abs(object[4]) * randint(MIN_SPEED * 2, MAX_SPEED * 2)
            return object


def border_control(object):
    if object[6] == 'ball':
        if object[0] < object[2]:
            object[0] = object[2]
        if object[0] > WIDTH - object[2]:
            object[0] = WIDTH - object[2]
        if object[1] < object[2]:
            object[1] = object[2]
        if object[1] > HEIGHT - object[2]:
            object[1] = HEIGHT - object[2]
    elif object[6] == 'square':

        if object[0] < 0:
            object[0] = 0
        if object[0] > WIDTH - object[2]:
            object[0] = WIDTH - object[2]
        if object[1] < 0:
            object[1] = 0
        if object[1] > HEIGHT - object[2]:
            object[1] = HEIGHT - object[2]
    return object


def score_(object):
    score = 0
    if object[6] == 'ball':
        if (object[0] - event.pos[0]) ** 2 + (object[1] - event.pos[1]) ** 2 <= object[2] ** 2:
            reborn_(object)
            score = 100

    elif object[6] == 'square':
        if 0 <= event.pos[0] - object[0] <= object[2] and 0 <= event.pos[1] - object[1] <= object[2]:
            reborn_(object)
            score = 300

    return score


pygame.display.update()
clock = pygame.time.Clock()
finished = False
box = []
Score = 0

for i in range(N):
    box.append(new_ball())

box.append(new_square())

while not finished:
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            finished = True
        elif event.type == pygame.MOUSEBUTTONDOWN:
            for ball in box:
                Score += int(score_(ball))

    for ball in box:
        moving_(ball)
        hitting_the_wall(ball)
        rendering_(ball)

    pygame.display.update()
    screen.fill(BLACK)
pygame.quit()

print('Your score: ', Score)
print('Write your name: ')
name = input()
bests = []
with open('Lists of the best of the best.txt') as f:
    for line in f:
        a = line.rstrip()
        a = a.split()
        bests.append(a)

with open('Lists of the best of the best.txt', 'w') as file:
    check = 0
    for i in range(len(bests)):
        if str(name) == bests[i][0]:
            print(int(bests[i][1]))
            if Score <= int(bests[i][1]):
                check = 1
                break
            else:
                bests.pop(i)

    if check == 0:
        for i in range(len(bests)):
            if Score > int(bests[i][1]):
                Score = str(Score)
                bests.insert(i, [name, Score])
                break
            if i == len(bests) - 1:
                Score = str(Score)
                bests.append([name, Score])

    for element in bests:
        element[1] = str(element[1])
        print(' '.join(element), file=file)

print('THANK YOU FOR PLAYING THIS M I N D - B L O W I N G GAME')
