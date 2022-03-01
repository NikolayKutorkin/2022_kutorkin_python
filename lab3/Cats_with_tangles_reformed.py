import pygame
import pygame.draw as dr
from numpy import pi, sin


# Фон
def background(screen, width, height, color1, color2):
    """

    :param screen: - screen
    :param width: - width
    :param height: - height
    :param color1: - color1
    :param color2: - color2
    :return:
    """
    dr.rect(screen, color1, (0, 0, width, height / 2))
    dr.rect(screen, color2, (0, height / 2, width, height / 2))


# Окно - Window
def draw_window(x0, y0, n, color1, color2, screen):
    """
    :param x0: - coordinate
    :param y0: - coordinate
    :param n: - parameter
    :param color1: - color1
    :param color2: - color2
    :param screen: - screen
    :return:
    """
    dr.rect(screen, color1, (x0, y0, 180 / n, 270 / n))
    dr.rect(screen, color2, (x0 + 10 / n, y0 + 10 / n, 75 / n, 75 / n))
    dr.rect(screen, color2, (x0 + 95 / n, y0 + 10 / n, 75 / n, 75 / n))
    dr.rect(screen, color2, (x0 + 10 / n, y0 + 95 / n, 75 / n, 165 / n))
    dr.rect(screen, color2, (x0 + 95 / n, y0 + 95 / n, 75 / n, 165 / n))


# Хвост - Tail
def draw_tail(x0, y0, n, coat_color, screen):
    """

    :param x0: - coordinate
    :param y0: - coordinate
    :param n: - parameter
    :param coat_color: - coat_color
    :param screen: - screen
    :return:
    """
    x_up_tail = 0
    y_up_tail = 30

    dr.arc(screen, coat_color, (x0 + x_up_tail / n, y0 + y_up_tail / n, 400 / n, 160 / n), 0, pi / 2,
           width=int(50 / n))
    dr.arc(screen, coat_color, (x0 + x_up_tail / n, y0 + y_up_tail / n + 1, 400 / n, 160 / n), 0, pi / 2,
           width=int(62 / n))
    x_down_tail = 200
    y_down_tail = -45
    dr.arc(screen, coat_color, (x0 + x_down_tail / n, y0 + y_down_tail / n, 400 / n, 160 / n), pi / 6 + pi,
           pi + pi / 2, width=int(16 / n))
    dr.arc(screen, coat_color, (x0 + x_down_tail / n, y0 + y_down_tail / n - 1, 400 / n, 160 / n), pi / 6 + pi,
           pi + pi / 2, width=int(16 / n))
    dr.arc(screen, 'black', (x0 + x_up_tail / n, y0 + y_up_tail / n, 400 / n, 160 / n), - pi / 42, pi / 2, width=1)
    dr.arc(screen, 'black', (x0 + x_down_tail / n, y0 + y_down_tail / n, 400 / n, 160 / n), pi / 6 + pi,
           pi + pi / 2, width=1)


def draw_mirror_tail(x0, y0, n, coat_color, screen):
    """

    :param x0: - coordinate
    :param y0: - coordinate
    :param n: - parameter
    :param coat_color: - coat_color
    :param screen: - screen
    :return:
    """
    x_up_tail = 0
    y_up_tail = 30
    x = x0 + 34

    dr.arc(screen, coat_color, (2 * x - (x0 + x_up_tail / n) - 400 / n, y0 + y_up_tail / n, 400 / n, 160 / n),
           pi / 2, pi,
           width=int(50 / n))
    dr.arc(screen, coat_color, (2 * x - (x0 + x_up_tail / n) - 400 / n, y0 + y_up_tail / n + 1, 400 / n, 160 / n),
           pi / 2, pi,
           width=int(62 / n))
    x_down_tail = 200
    y_down_tail = -45
    dr.arc(screen, coat_color, (2 * x - (x0 + x_down_tail / n) - 400 / n, y0 + y_down_tail / n, 400 / n, 160 / n),
           pi + pi / 2,
           2 * pi - pi / 6, width=int(16 / n))
    dr.arc(screen, coat_color,
           (2 * x - (x0 + x_down_tail / n) - 400 / n, y0 + y_down_tail / n - 1, 400 / n, 160 / n), pi + pi / 2,
           2 * pi - pi / 6, width=int(17 / n))
    dr.arc(screen, 'black', (2 * x - (x0 + x_up_tail / n) - 400 / n - 2, y0 + y_up_tail / n, 400 / n, 160 / n),
           pi / 2,
           pi + pi / 42, width=1)
    dr.arc(screen, 'black', (2 * x - (x0 + x_down_tail / n) - 400 / n, y0 + y_down_tail / n, 400 / n, 160 / n),
           pi + pi / 2,
           2 * pi - pi / 6, width=1)


#   Тело - Body
def draw_body(x0, y0, n, coat_color, screen):
    """

    :param x0: - coordinate
    :param y0: - coordinate
    :param n: - parameter
    :param coat_color: - coat_color
    :param screen: - screen
    :return:
    """
    dr.ellipse(screen, coat_color, (x0, y0, 266 / n, 130 / n), 0)
    dr.ellipse(screen, (0, 0, 0), (x0, y0, 266 / n, 130 / n), 1)


#   Тело зеркалное - Body mirrored
def draw_mirror_body(x0, y0, n, coat_color, screen):
    """

    :param x0: - coordinate
    :param y0: - coordinate
    :param n: - parameter
    :param coat_color: - coat_color
    :param screen: - screen
    :return:
    """
    x = x0 + 34
    dr.ellipse(screen, coat_color, (2 * x - x0 - 266 / n, y0, 266 / n, 130 / n), 0)
    dr.ellipse(screen, (0, 0, 0), (2 * x - x0 - 266 / n, y0, 266 / n, 130 / n), 1)


# Бедро - Hip
def draw_hip(x0, y0, n, coat_color, screen):
    """

       :param x0: - coordinate
       :param y0: - coordinate
       :param n: - parameter
       :param coat_color: - coat_color
       :param screen: - screen
       :return:
       """
    x_hip = 215
    y_hip = 94
    dr.circle(screen, coat_color, (x0 + x_hip / n, y0 + y_hip / n), 45 / n)
    dr.circle(screen, (0, 0, 0), (x0 + x_hip / n, y0 + y_hip / n), 45 / n, 1)


# Бедро зеркалное - Hip mirrored
def draw_mirror_hip(x0, y0, n, coat_color, screen):
    """

       :param x0: - coordinate
       :param y0: - coordinate
       :param n: - parameter
       :param coat_color: - coat_color
       :param screen: - screen
       :return:
       """
    x_hip = 215
    y_hip = 94
    x = x0 + 34
    dr.circle(screen, coat_color, (2 * x - (x0 + x_hip / n), y0 + y_hip / n), 45 / n)
    dr.circle(screen, (0, 0, 0), (2 * x - (x0 + x_hip / n), y0 + y_hip / n), 45 / n, 1)


# Задняя лапка - BackFoot
def draw_BackFoot(x0, y0, n, coat_color, screen):
    """

    :param x0: - coordinate
    :param y0: - coordinate
    :param n: - parameter
    :param coat_color: - coat_color
    :param screen: - screen
    :return:
    """
    x_back_foot = 236
    y_back_foot = 107
    dr.ellipse(screen, coat_color, (x0 + x_back_foot / n, y0 + y_back_foot / n, 30 / n, 75 / n))
    dr.ellipse(screen, (0, 0, 0), (x0 + x_back_foot / n, y0 + y_back_foot / n, 30 / n, 75 / n), 1)


# Задняя лапка зеркалное - BackFoot mirrored
def draw_mirror_BackFoot(x0, y0, n, coat_color, screen):
    """

    :param x0: - coordinate
    :param y0: - coordinate
    :param n: - parameter
    :param coat_color: - coat_color
    :param screen: - screen
    :return:
    """
    x_back_foot = 236
    y_back_foot = 107
    x = x0 + 34
    dr.ellipse(screen, coat_color, (2 * x - (x0 + x_back_foot / n) - 30 / n, y0 + y_back_foot / n, 30 / n, 75 / n))
    dr.ellipse(screen, (0, 0, 0), (2 * x - (x0 + x_back_foot / n) - 30 / n, y0 + y_back_foot / n, 30 / n, 75 / n),
               1)


# Передние лапки - FrontFoot
def draw_FrontFoot(x0, y0, n, coat_color, screen):
    """

    :param x0: - coordinate
    :param y0: - coordinate
    :param n: - parameter
    :param coat_color: - coat_color
    :param screen: - screen
    :return:
    """
    x_right_front_foot = 0
    y_right_front_foot = 60
    dr.ellipse(screen, coat_color, (x0 + x_right_front_foot / n, y0 + y_right_front_foot / n, 35 / n, 63 / n))
    dr.ellipse(screen, (0, 0, 0), (x0 + x_right_front_foot / n, y0 + y_right_front_foot / n, 35 / n, 63 / n), 1)
    x_left_front_foot = 37
    y_left_front_foot = 106
    dr.ellipse(screen, coat_color, (x0 + x_left_front_foot / n, y0 + y_left_front_foot / n, 73 / n, 40 / n))
    dr.ellipse(screen, (0, 0, 0), (x0 + x_left_front_foot / n, y0 + y_left_front_foot / n, 73 / n, 40 / n), 1)


# Передние лапки зеркалное - FrontFoot mirrored

def draw_mirror_FrontFoot(x0, y0, n, coat_color, screen):
    """

    :param x0: - coordinate
    :param y0: - coordinate
    :param n: - parameter
    :param coat_color: - coat_color
    :param screen: - screen
    :return:
    """
    x_right_front_foot = 0
    y_right_front_foot = 60
    x = x0 + 34
    dr.ellipse(screen, coat_color,
               (2 * x - (x0 + x_right_front_foot / n) - 35 / n, y0 + y_right_front_foot / n, 35 / n, 63 / n))
    dr.ellipse(screen, (0, 0, 0),
               (2 * x - (x0 + x_right_front_foot / n) - 35 / n, y0 + y_right_front_foot / n, 35 / n, 63 / n), 1)
    x_left_front_foot = 37
    y_left_front_foot = 106
    dr.ellipse(screen, coat_color,
               (2 * x - (x0 + x_left_front_foot / n) - 73 / n, y0 + y_left_front_foot / n, 73 / n, 40 / n))
    dr.ellipse(screen, (0, 0, 0),
               (2 * x - (x0 + x_left_front_foot / n) - 73 / n, y0 + y_left_front_foot / n, 73 / n, 40 / n), 1)


def draw_Head(x0, y0, n, coat_color, screen):
    """

    :param x0: - coordinate
    :param y0: - coordinate
    :param n: - parameter
    :param coat_color: - coat_color
    :param screen: - screen
    :return:
    """
    x_head = -20
    y_head = 10
    dr.ellipse(screen, coat_color, (x0 + x_head / n, y0 + y_head / n, 107 / n, 100 / n))
    dr.ellipse(screen, (0, 0, 0), (x0 + x_head / n, y0 + y_head / n, 107 / n, 100 / n), 1)


# Левый глаз - LeftEye
def draw_leftEye(x0, y0, n, eye_color, screen):
    """
    :param x0: - coordinate
    :param y0: - coordinate
    :param n: - parameter
    :param eye_color: - eye_color
    :param screen: - screen
    :return:
    """
    x_left_eye = -2
    y_left_eye = 47
    dr.ellipse(screen, eye_color, (x0 + x_left_eye / n, y0 + y_left_eye / n, 26 / n, 32 / n))
    dr.ellipse(screen, (0, 0, 0), (x0 + x_left_eye / n, y0 + y_left_eye / n, 26 / n, 32 / n), 1)
    x_left_pupil = 11
    y_left_pupil = 47
    dr.ellipse(screen, (0, 0, 0), (x0 + x_left_pupil / n, y0 + y_left_pupil / n, 5 / n, 32 / n))
    x_left_glimmer = 10
    y_left_glimmer = 61
    dr.line(screen, 'white', (x0 + (x_left_glimmer - 9) / n, y0 + (y_left_glimmer - 6) / n),
            (x0 + x_left_glimmer / n, y0 + y_left_glimmer / n), int(5 / n))


def draw_rightEye(x0, y0, n, eye_color, screen):
    """

    :param x0: - coordinate
    :param y0: - coordinate
    :param n: - parameter
    :param eye_color: - eye_color
    :param screen: - screen
    :return:
    """
    a = 45
    x_left_eye = -2
    y_left_eye = 47
    dr.ellipse(screen, eye_color, (x0 + (x_left_eye + a) / n, y0 + y_left_eye / n, 26 / n, 32 / n))
    dr.ellipse(screen, (0, 0, 0), (x0 + (x_left_eye + a) / n, y0 + y_left_eye / n, 26 / n, 32 / n), 1)
    x_left_pupil = 11
    y_left_pupil = 47
    dr.ellipse(screen, (0, 0, 0), (x0 + (x_left_pupil + a) / n, y0 + y_left_pupil / n, 5 / n, 32 / n))
    x_left_glimmer = 10
    y_left_glimmer = 61
    dr.line(screen, 'white', (x0 + (x_left_glimmer - 9 + a) / n, y0 + (y_left_glimmer - 6) / n),
            (x0 + (x_left_glimmer + a) / n, y0 + y_left_glimmer / n), int(5 / n))


# Носик - Nose
def draw_Nose(x0, y0, n, screen):
    """

    :param x0: - coordinate
    :param y0: - coordinate
    :param n: - parameter
    :param screen: - screen
    :return:
    """
    x_nose1 = 30
    y_nose1 = 82
    x_nose2 = 38
    y_nose2 = 82
    x_nose3 = 34
    y_nose3 = 86
    dr.polygon(screen, 'pink', (
        (x0 + x_nose1 / n, y0 + y_nose1 / n), (x0 + x_nose2 / n, y0 + y_nose2 / n),
        (x0 + x_nose3 / n, y0 + y_nose3 / n)))
    dr.polygon(screen, (0, 0, 0), (
        (x0 + (x_nose1 - 1) / n, y0 + y_nose1 / n), (x0 + (x_nose2 + 1) / n, y0 + y_nose2 / n),
        (x0 + x_nose3 / n, y0 + y_nose3 / n)), width=1)
    dr.line(screen, 'black', (x0 + x_nose3 / n, y0 + y_nose3 / n), (x0 + x_nose3 / n, y0 + (y_nose3 + 8) / n))


# Мoрдочка - Muzzle
def draw_Mouth(x0, y0, n, screen):
    """

    :param x0: - coordinate
    :param y0: - coordinate
    :param n: - parameter
    :param screen: - screen
    :return:
    """
    x_muzzle = 22
    y_muzzle = 90
    dr.arc(screen, 'black', (x0 + x_muzzle / n, y0 + y_muzzle / n, 12 / n, 12 / n), 7 * pi / 6, 0)
    dr.arc(screen, 'black', (x0 + (x_muzzle + 12) / n, y0 + y_muzzle / n, 12 / n, 12 / n), pi, 11 * pi / 6)


# Ушки - Ears
def draw_Ears(x0, y0, n, coat_color, screen):
    """

    :param x0: - coordinate
    :param y0: - coordinate
    :param n: - parameter
    :param coat_color: - coat_color
    :param screen: - screen
    :return:
    """
    x_ear1 = 48
    y_ear1 = 18
    x_ear2 = 79
    y_ear2 = 0
    x_ear3 = 74
    y_ear3 = 35

    dr.polygon(screen, coat_color,
               ((x0 + x_ear1 / n, y0 + y_ear1 / n), (x0 + x_ear2 / n, y0 + y_ear2 / n),
                (x0 + x_ear3 / n, y0 + y_ear3 / n)))
    dr.polygon(screen, (0, 0, 0),
               ((x0 + x_ear1 / n, y0 + y_ear1 / n), (x0 + x_ear2 / n, y0 + y_ear2 / n),
                (x0 + x_ear3 / n, y0 + y_ear3 / n)), 1)
    dr.polygon(screen, 'pink',
               ((x0 + (x_ear1 + 5) / n, y0 + y_ear1 / n), (x0 + (x_ear2 - 4) / n, y0 + (y_ear2 + 5) / n),
                (x0 + (x_ear3 - 4) / n, y0 + (y_ear3 - 5) / n)))
    dr.polygon(screen, (0, 0, 0), (
        (x0 + (x_ear1 + 4) / n, y0 + y_ear1 / n), (x0 + (x_ear2 - 3) / n, y0 + (y_ear2 + 4) / n),
        (x0 + (x_ear3 - 3) / n, y0 + (y_ear3 - 4) / n)), 1)

    h = 30
    dr.polygon(screen, coat_color,
               ((x0 + (x_ear1 - h) / n, y0 + y_ear1 / n), (x0 + (x_ear2 - 62 - h) / n, y0 + y_ear2 / n),
                (x0 + (x_ear3 - 52 - h) / n, y0 + y_ear3 / n)))
    dr.polygon(screen, (0, 0, 0),
               ((x0 + (x_ear1 - h) / n, y0 + y_ear1 / n), (x0 + (x_ear2 - 62 - h - 1) / n, y0 + y_ear2 / n),
                (x0 + (x_ear3 - 52 - h) / n, y0 + y_ear3 / n)), 1)
    dr.polygon(screen, 'pink',
               ((x0 + (x_ear1 - 4 - h) / n, y0 + y_ear1 / n), (x0 + (x_ear2 - 58 - h) / n, y0 + (y_ear2 + 5) / n),
                (x0 + (x_ear3 - 48 - h) / n, y0 + (y_ear3 - 5) / n)))
    dr.polygon(screen, (0, 0, 0),
               ((x0 + (x_ear1 - 4 - h) / n, y0 + y_ear1 / n), (x0 + (x_ear2 - 59 - h) / n, y0 + (y_ear2 + 4) / n),
                (x0 + (x_ear3 - 49 - h) / n, y0 + (y_ear3 - 4) / n)), 1)


# Вибриссы - Vibrissae
def draw_Vibrissae(x0, y0, n, screen):
    """

    :param x0: - coordinate
    :param y0: - coordinate
    :param n: - parameter
    :param screen: - screen
    :return:
    """
    x_vibrissae1 = -10
    y_vibrissae1 = 94
    x_vibrissae2 = 20
    y_vibrissae2 = 89
    x_vibrissae3 = 41
    y_vibrissae3 = 79

    # Правая сторона
    dr.arc(screen, 'black', (x0 + x_vibrissae1 / n, y0 + y_vibrissae1 / n, 120 / n, 40 / n), pi / 6, pi / 2)
    dr.arc(screen, 'black', (x0 + x_vibrissae2 / n, y0 + y_vibrissae2 / n, 120 / n, 40 / n), pi / 6 + pi / 6,
           pi / 2 + pi / 6)
    dr.arc(screen, 'black', (x0 + x_vibrissae3 / n, y0 + y_vibrissae3 / n, 120 / n, 40 / n), pi / 6 + 2 * pi / 6,
           pi / 2 + 2 * pi / 6)

    # Левая сторона
    z = 30
    dr.arc(screen, 'black', (x0 + (x_vibrissae1 - z) / n, y0 + y_vibrissae1 / n, 120 / n, 40 / n), pi - pi / 2,
           pi - pi / 6)
    dr.arc(screen, 'black', (x0 + (x_vibrissae2 - z - 60) / n, y0 + y_vibrissae2 / n, 120 / n, 40 / n),
           pi - (pi / 2 + pi / 6), pi - (pi / 6 + pi / 6))
    dr.arc(screen, 'black', (x0 + (x_vibrissae3 - z - 102) / n, y0 + y_vibrissae3 / n, 120 / n, 40 / n),
           pi - (pi / 2 + 2 * pi / 6),
           pi - (pi / 6 + 2 * pi / 6))


# Кошка - Cat
def draw_cat(x0, y0, n, coat_color, eye_color, mirror, screen):
    """

    :param x0: - coordinate
    :param y0: - coordinate
    :param n: - parameter
    :param coat_color: - coat_color
    :param eye_color: - eye_color
    :param mirror: - mirror
    :param screen: - screen
    :return:
    """

    if not mirror:

        draw_tail(x0, y0, n, coat_color, screen)
        draw_body(x0, y0, n, coat_color, screen)
        draw_hip(x0, y0, n, coat_color, screen)
        draw_BackFoot(x0, y0, n, coat_color, screen)
        draw_FrontFoot(x0, y0, n, coat_color, screen)

    else:

        draw_mirror_tail(x0, y0, n, coat_color, screen)
        draw_mirror_body(x0, y0, n, coat_color, screen)
        draw_mirror_hip(x0, y0, n, coat_color, screen)
        draw_mirror_BackFoot(x0, y0, n, coat_color, screen)
        draw_mirror_FrontFoot(x0, y0, n, coat_color, screen)
        x0 += 34 * (2 - 2 / n)

    draw_Head(x0, y0, n, coat_color, screen)
    draw_leftEye(x0, y0, n, eye_color, screen)
    draw_rightEye(x0, y0, n, eye_color, screen)
    draw_Nose(x0, y0, n, screen)
    draw_Mouth(x0, y0, n, screen)
    draw_Ears(x0, y0, n, coat_color, screen)
    draw_Vibrissae(x0, y0, n, screen)


def draw_tangle(x0, y0, n, screen):
    """
    :param x0: - coordinate
    :param y0: - coordinate
    :param n: - parameter
    :param screen: - screen
    :return:
    """
    dr.circle(screen, 'grey', (x0, y0), 40 / n)
    dr.circle(screen, 'black', (x0, y0), 40 / n, width=1)
    dr.arc(screen, (0, 0, 0), (x0, y0, 50 / n, 50 / n), pi / 2 + pi / 6, pi)
    dr.arc(screen, (0, 0, 0), (x0 - 10 / n, y0 - 8 / n, 60 / n, 60 / n), pi / 2 + pi / 6, pi)
    dr.arc(screen, (0, 0, 0), (x0 - 20 / n, y0 - 15 / n, 70 / n, 70 / n), pi / 2 + pi / 6, pi)
    dr.arc(screen, (0, 0, 0), (x0 - 47 / n, y0 - 23 / n, 70 / n, 70 / n), 0, pi / 2)
    dr.arc(screen, (0, 0, 0), (x0 - 50 / n, y0 - 33 / n, 80 / n, 80 / n), 0, pi / 2)


# Нитка - Thread
def draw_thread(x0, y0, n, mirror, screen):
    """

    :param x0: - coordinate
    :param y0: - coordinate
    :param n: - parameter
    :param mirror: - mirror
    :param screen: - screen
    :return:
    """
    if not mirror:
        x_thread = x0 - 20 / n
        y_thread = y0 + 25 / n
        for i in range(0, int(18 / n), 1):
            dr.aaline(screen, 'gray', [x_thread, y_thread], [x_thread - i, y_thread + 3 * sin(i * pi / 5)])
            x_thread -= i
            y_thread += 3 * sin(i * pi / 5)
    else:
        x_thread = x0 + 20 / n
        y_thread = y0 + 25 / n
        for i in range(0, int(18 / n), 1):
            dr.aaline(screen, 'gray', [x_thread, y_thread], [x_thread + i, y_thread + 3 * sin(i * pi / 5)])
            x_thread += i
            y_thread += 3 * sin(i * pi / 5)


def draw_tangle_with_thread(x0, y0, n, mirror, screen):
    """

    :param x0: - coordinate
    :param y0: - coordinate
    :param n: - parameter
    :param mirror: - mirror
    :param screen: - screen
    :return:
    """
    draw_tangle(x0, y0, n, screen)
    draw_thread(x0, y0, n, mirror, screen)


def main():
    pygame.init()

    FPS = 30

    # screen parameters
    width = 400
    height = 600
    color1 = (66, 64, 0)
    color2 = (125, 102, 6)

    # window coordinates
    x1, y1 = 250, 20
    x2, y2 = 200, 20
    x3, y3 = 50, 20

    # cats coordinates
    x01, y01 = 180, 280
    x02, y02 = 100, 370
    x03, y03 = 50, 310
    x04, y04 = 250, 450
    x05, y05 = 140, 480
    x06, y06 = 60, 550
    x07, y07 = 300, 530

    # tangle coordinates
    tx1, ty1 = 340, 500
    tx2, ty2 = 250, 550
    tx3, ty3 = 100, 510
    tx4, ty4 = 340, 400

    # coat colors
    coat_color1 = (182, 86, 35)
    coat_color2 = (181, 181, 181)

    # eye colors
    eye_color1 = (90, 135, 0)
    eye_color2 = (71, 255, 255)

    # window colors
    win_col1 = (240, 240, 255)
    win_col2 = (78, 195, 226)

    # parameters
    n1 = 2
    n2 = 4
    n3 = 1.5
    n4 = 1
    n5 = 2.5

    screen = pygame.display.set_mode((width, height))
    background(screen, width, height, color1, color2)

    draw_window(x1, y1, n3, win_col1, win_col2, screen)
    draw_window(x2, y2, n3, win_col1, win_col2, screen)
    draw_window(x3, y3, n3, win_col1, win_col2, screen)

    draw_cat(x01, y01, n1, coat_color1, eye_color1, False, screen)
    draw_cat(x02, y02, n1, coat_color2, eye_color2, True, screen)
    draw_cat(x03, y03, n2, coat_color1, eye_color1, False, screen)
    draw_cat(x04, y04, n2, coat_color1, eye_color1, True, screen)
    draw_cat(x05, y05, n2, coat_color1, eye_color1, False, screen)
    draw_cat(x06, y06, n2, coat_color2, eye_color2, True, screen)
    draw_cat(x07, y07, n2, coat_color2, eye_color2, False, screen)

    draw_tangle_with_thread(tx1, ty1, n1, True, screen)
    draw_tangle_with_thread(tx2, ty2, n3, False, screen)
    draw_tangle_with_thread(tx3, ty3, n5, True, screen)
    draw_tangle_with_thread(tx4, ty4, n4, False, screen)

    pygame.display.update()
    clock = pygame.time.Clock()
    finished = False

    while not finished:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                finished = True

    pygame.quit()


main()
