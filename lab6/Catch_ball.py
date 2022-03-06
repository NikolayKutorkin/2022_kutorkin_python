import pygame
from pygame.draw import *
from random import randint, choice

# from pygame.examples.prevent_display_stretching import event

pygame.init()

# Настройка параметров
HEIGHT = 600  # Высота скрина
WIDTH = 1200  # Ширина скрина
BALLS_NUMBER = 2  # Количесво шаров
SQUARES_NUMBER = 2  # Количество квадратов
FPS = 30
screen = pygame.display.set_mode((WIDTH, HEIGHT))
MAX_SPEED = 50  # Максимальная скорость шаров и квадратов
MIN_SPEED = 20  # Минимальная скорость шаров и квадратов
g = 10  # Ускорение свободного падения. Сила тяжести действует только на квадраты
SCORE = 0

# Создание палитры
RED = (255, 0, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
GREEN = (0, 255, 0)
MAGENTA = (255, 0, 255)
CYAN = (0, 255, 255)
BLACK = (0, 0, 0)
COLORS = [RED, BLUE, YELLOW, GREEN, MAGENTA, CYAN]


def new_ball():
    """
    Создаёт лист параметров шара.
    :return: Список list параметров шара:
    list[0] - координата х центра шара;
    list[1] - координата y центра шара;
    list[2] - радиус шара;
    list[3] - скорость шара по x;
    list[4] - скорость шара по y;
    list[5] - цвет шара;
    list[6] - тип фигуры (ball). Нужен для того, чтобы функции (rendering_, moving_, и т.д) могли
    распознать фигуру и применить к нему нужную реализацию.
    """
    x = randint(100, WIDTH - 100)
    y = randint(100, HEIGHT - 100)
    r = randint(10, 100)
    v_x = choice([-1, 1]) * randint(MIN_SPEED, MAX_SPEED)
    v_y = choice([-1, 1]) * randint(MIN_SPEED, MAX_SPEED)
    color = COLORS[randint(0, 5)]
    return [x, y, r, v_x, v_y, color, 'ball']


def new_square():
    """
    Создаёт лист с параметрами квадрата.
    :return: Список list параметров квадрата:
    list[0] - координата х центра квадрата;
    list[1] - координата y центра квадрата;
    list[2] - сторона квадрата;
    list[3] - скорость квадрата по x;
    list[4] - скорость квадрата по y;
    list[5] - цвет квадрата;
    list[6] - тип фигуры (square). Нужен для того, чтобы функции (rendering_, moving_, и т.д) могли
    распознать фигуру и применить к нему нужную реализацию.
    """
    side = randint(30, 100)
    x = randint(100, WIDTH - side - 100)
    y = randint(100, HEIGHT - side - 100)
    v_x = choice([-1, 1]) * randint(MIN_SPEED, MAX_SPEED)
    v_y = choice([-1, 1]) * randint(MIN_SPEED, MAX_SPEED)
    color = COLORS[randint(0, 5)]
    return [x, y, side, v_x, v_y, color, 'square']


def rendering_(figure):
    """
    Рисует фигуру в зависимости от её параметров.
    :param figure: Список с параметрами фигуры.
    :return:
    """
    if figure[6] == 'ball':
        # [x, y, r, v_x, v_y, color]
        # [0, 1, 2,   3,   4,     5]
        circle(screen, figure[5], (figure[0], figure[1]), figure[2])
    elif figure[6] == 'square':
        # [x, y, side, v_x, v_y, color]
        # [0, 1, 2,   3,   4,     5]
        rect(screen, figure[5], (figure[0], figure[1], figure[2], figure[2]))


def moving_(figure):
    """
    Изменяет координаты фигуры в зависимости от скорости
    и типа фигуры (каждый тип может двигаться по разным траекториям).
    :param figure: Список с параметрами фигуры.
    """
    t = 0.1
    if figure[6] == 'ball':
        # [x, y, r, v_x, v_y, color]
        # [0, 1, 2,   3,   4,     5]
        figure[0] = figure[0] + figure[3] * t  # x + v_x * t
        figure[1] = figure[1] + figure[4] * t  # y + v_y * t
    elif figure[6] == 'square':
        # [x, y, side, v_x, v_y, color]
        # [0, 1, 2,   3,   4,     5]
        figure[0] += figure[3] * t  # x + v_x * t
        figure[1] += figure[4] * t + g * t ** 2 / 2  # y + v_y * t + g * t**2 / 2
        figure[4] += g * t


def reborn_(figure):
    """
    Задаёт новые случайные параметры для фигуры, сохраняя при этом её тип.
    :param figure: Список с параметрами фигуры.
    :return:
    """
    if figure[6] == 'ball':
        # [x, y, r, v_x, v_y, color]
        # [0, 1, 2,   3,   4,     5]
        figure[0] = randint(100, WIDTH - 100)  # x
        figure[1] = randint(100, HEIGHT - 100)  # y
        figure[2] = randint(10, 100)  # r
        figure[3] = choice([-1, 1]) * randint(MIN_SPEED, MAX_SPEED)  # v_x
        figure[4] = choice([-1, 1]) * randint(MIN_SPEED, MAX_SPEED)  # v_y
        figure[5] = COLORS[randint(0, 5)]  # color
    if figure[6] == 'square':
        # [x, y, side, v_x, v_y, color]
        # [0, 1, 2,   3,   4,     5]
        figure[0] = randint(100, WIDTH - 100)  # x
        figure[1] = randint(100, HEIGHT - 100)  # y
        figure[2] = randint(30, 100)  # a
        figure[3] = choice([-1, 1]) * randint(MIN_SPEED, MAX_SPEED)  # v_x
        figure[4] = choice([-1, 1]) * randint(MIN_SPEED, MAX_SPEED)  # v_y
        figure[5] = COLORS[randint(0, 5)]  # color


def border_control(figure):
    """
    Проверяет фигуры на вылет за границы скрина. Предотвращает застревание в стенах.
    :param figure: Список с параметрами фигуры.
    :return:
    """
    if figure[6] == 'ball':
        # [x, y, r, v_x, v_y, color]
        # [0, 1, 2,   3,   4,     5]
        if figure[0] < figure[2]:
            figure[0] = figure[2]
        if figure[0] > WIDTH - figure[2]:
            figure[0] = WIDTH - figure[2]
        if figure[1] < figure[2]:
            figure[1] = figure[2]
        if figure[1] > HEIGHT - figure[2]:
            figure[1] = HEIGHT - figure[2]
    elif figure[6] == 'square':
        # [x, y, side, v_x, v_y, color]
        # [0, 1, 2,   3,   4,     5]
        if figure[0] < 0:
            figure[0] = 0
        if figure[0] > WIDTH - figure[2]:
            figure[0] = WIDTH - figure[2]
        if figure[1] < 0:
            figure[1] = 0
        if figure[1] > HEIGHT - figure[2]:
            figure[1] = HEIGHT - figure[2]


def hitting_the_wall(figure):
    """
    Проверяет фигуру на соударение со стеной, а также на застревание в стенах
    с помощью функции border_control. При соударении со стеной меняет параметры фигуры,
    не меняя её цвет и тип.
    :param figure: Список с параметрами фигуры.
    :return:
    """
    border_control(figure)
    if figure[6] == 'ball':
        # [x, y, r, v_x, v_y, color]
        # [0, 1, 2,   3,   4,     5]
        if WIDTH <= figure[0] + figure[2] or figure[0] - figure[2] <= 0:
            figure[3] = -1 * figure[3] / abs(figure[3]) * randint(5, 20)
            figure[4] = choice([-1, 1]) * randint(MIN_SPEED, MAX_SPEED)

        elif HEIGHT <= figure[1] + figure[2] or figure[1] - figure[2] <= 0:
            figure[4] = -1 * figure[4] / abs(figure[4]) * randint(5, 20)
            figure[3] = choice([-1, 1]) * randint(MIN_SPEED, MAX_SPEED)

    elif figure[6] == 'square':
        # [x, y, side, v_x, v_y, color]
        # [0, 1, 2,   3,   4,     5]
        if WIDTH <= figure[0] + figure[2] or figure[0] <= 0:
            figure[3] = -1 * figure[3] / abs(figure[3]) * randint(MIN_SPEED, MAX_SPEED)

        elif HEIGHT <= figure[1] + figure[2] or figure[1] <= 0:
            figure[4] = -1 * figure[4] / abs(figure[4]) * randint(MIN_SPEED, MAX_SPEED)


def score_(figure):
    """
    Зачисляет очки за попадание мышью в площадь фигуры. За каждую фигуру могут быть зачислено разное
    количество очков.
    :param figure: Список с параметрами фигуры.
    :return: Количество зачисляемых очков.
    """
    score = 0
    if figure[6] == 'ball':
        if (figure[0] - event.pos[0]) ** 2 + (figure[1] - event.pos[1]) ** 2 <= figure[2] ** 2:
            reborn_(figure)
            score = 100

    elif figure[6] == 'square':
        if 0 <= event.pos[0] - figure[0] <= figure[2] and 0 <= event.pos[1] - figure[1] <= figure[2]:
            reborn_(figure)
            score = 300

    return score


def add_result(name, score):
    """
    Добавляет результат игрока с именем "name" в таблицу лучших.
    :param name: Имя игрока
    :param score: Количество очков, резултат игрока
    :return:
    """
    bests = []  # создание листа для работы сданными из файла
    with open('Lists of the best of the best.txt') as f:
        for string in f:
            temp = string.rstrip()  # избавление от знака '\n' в конце каждой строки
            temp = temp.split()  # преврашение строки в список ('name score' -> ['name', 'score'])
            bests.append(temp)  # добавление пары ['name', 'score'] в список

    with open('Lists of the best of the best.txt', 'w') as file:
        # Проверка совпадения имени
        check = 0
        for j in range(len(bests)):
            if str(name) == bests[j][0]:
                if score <= int(bests[j][1]):  # Если name набрал меньше очков, чем раньше, то весь файл не меняется
                    check = 1  # даёт условие, при котором цикл вставки результата пропускается
                    break
                else:
                    bests.pop(j)  # Если name набрал больше очков, чем раньше, его старый результат удаляется

        # Вставка результата
        if check == 0:
            for k in range(len(bests)):
                # Результат сравнивается сначала с натбольшим результатом списка, потом с меньшим.
                # Как только находится результат, равный или меньший результату name, результат name сразу
                # вставляется выше найденного результата.
                if score >= int(bests[k][1]):
                    score = str(score)
                    bests.insert(k, [name, score])
                    break

        # Вывод полученного списка в файл. Имя и очки разделяюся пробелом
        for element in bests:
            element[1] = str(element[1])
            print(' '.join(element), file=file)


pygame.display.update()
clock = pygame.time.Clock()
finished = False
box = []

for i in range(BALLS_NUMBER):
    box.append(new_ball())
for i in range(SQUARES_NUMBER):
    box.append(new_square())

while not finished:
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            finished = True
        elif event.type == pygame.MOUSEBUTTONDOWN:
            for ball in box:
                SCORE += int(score_(ball))

    for ball in box:
        moving_(ball)
        hitting_the_wall(ball)
        rendering_(ball)

    pygame.display.update()
    screen.fill(BLACK)
pygame.quit()

print('Your score: ', SCORE)
print('Write your name: ')
NAME = input()
add_result(NAME, SCORE)

print('THANK YOU FOR PLAYING THIS M I N D - B L O W I N G GAME')
