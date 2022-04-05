import math
from random import choice, randint as rnd

import pygame

FPS = 30
g = 2
RED = 0xFF0000
BLUE = 0x0000FF
YELLOW = 0xFFC91F
GREEN = 0x00FF00
MAGENTA = 0xFF03B8
CYAN = 0x00FFCC
BLACK = (0, 0, 0)
WHITE = 0xFFFFFF
GREY = 0x7D7D7D
GAME_COLORS = [RED, BLUE, YELLOW, GREEN, MAGENTA, CYAN]

WIDTH = 800
HEIGHT = 600


def turn(point, angle, ref_point):
    """
    Поворачиает точку на угол относителбно опорной точки
    :param point: координаты поворачиваемой точки
    :param angle: угол поворота
    :param ref_point: опорная точка
    :return: кооридинта точки после поворота
    """
    x1 = -(ref_point[0] - point[0]) * math.cos(angle) - (ref_point[1] - point[1]) * math.sin(angle)
    y1 = -(ref_point[0] - point[0]) * math.sin(angle) + (ref_point[1] - point[1]) * math.cos(angle)
    return x1 + ref_point[0], ref_point[1] - y1


def replacing_coordinates(x0, y0, angle, x, y):
    """
    Замена системы координат
    :param x0: координата x системы координат
    :param y0: координата н системы координат
    :param angle: угол поворота системы координат относительно изначальной
    :param x: координата x точки в изначальной системе координат
    :param y: координата y точки в изначальной системе координат
    :return: кооординаты в новой системе координат
    """
    x1 = (x - x0) * math.cos(angle) + (y - y0) * math.sin(angle)
    y1 = (y - y0) * math.cos(angle) - (x - x0) * math.sin(angle)
    return x1, y1


def dist(x1, y1, x2, y2):
    """
    Расстояние между двумя точкми
    :param x1: координат x первой точки
    :param y1: координат y первой точки
    :param x2: координат x второй точки
    :param y2: координат y второй точки
    :return: расстояние между точками
    """
    distance = math.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)
    return distance


def border_control(figure, x, y, side):
    """
    Контролирует вылет объектов за границы экрана. При вылете телепортирует на границу.
    :param figure: вид фигуры объекта
    :param x: опорная координата x фигуры
    :param y: опорная координата y фигуры
    :param side: характерный размер (радиус для круга, сторона квадрата)
    :return: опорные координты фигуры
    """
    if figure == 'ball':
        if x < side:
            x = side
        if x > WIDTH - side:
            x = WIDTH - side
        if y < side:
            y = side
        if y > HEIGHT - side:
            y = HEIGHT - side
    else:
        if x < 0:
            x = 0
        if x > WIDTH - side:
            x = WIDTH - side
        if y < 0:
            y = 0
        if y > HEIGHT - side:
            y = HEIGHT - side
    return x, y


class Bullet:
    def __init__(self, object_screen, x0, y0):
        """
        Интерфейс снарядов для Gun
        :param object_screen: экран, на котором находится снаряд
        :param x0: начальная координата x снаряда
        :param y0: начальная координата y снаряда
        """
        self.screen = object_screen
        self.x = x0
        self.y = y0
        self.vx = 0
        self.vy = 0
        self.live = 30
        self.square = 0
        self.color = choice(GAME_COLORS)


class Ball(Bullet):
    def __init__(self, object_screen, x0, y0):
        """
        Создаёт снаряд в форме шара.
        """
        super().__init__(object_screen, x0, y0)
        self.r = 15

    def move(self):
        """Переместить мяч по прошествии единицы времени с учётом дейсвия силы притяжения.

        Метод описывает перемещение мяча за один кадр перерисовки. То есть, обновляет значения
        self.x и self.y с учетом скоростей self.vx и self.vy, силы гравитации, действующей на мяч,
        и стен по краям окна.
        """
        if self.vy != 0:
            self.x += self.vx
            self.y -= self.vy + g / 2
            self.vy -= g

        self.x, self.y = border_control('ball', self.x, self.y, self.r)
        if self.y >= HEIGHT - self.r and abs(self.vy) < 11:
            self.vy = 0

        if WIDTH <= self.x + self.r or self.x - self.r <= 0:
            self.vx = -1 * self.vx
        elif HEIGHT <= self.y + self.r or self.y - self.r <= 0:
            self.vy = -1 * (self.vy / 2)
            self.vx = self.vx / 1.4

    def draw(self):
        """
        Рисует шар на экране с чёрной границей.
        :return:
        """
        pygame.draw.circle(self.screen, self.color, (self.x, self.y), self.r)
        pygame.draw.circle(self.screen, 'black', (self.x, self.y), self.r, width=1)

    def hit_test(self, obj):
        """Функция проверяет сталкивалкивается ли данный обьект с целью, описываемой в обьекте obj.
            obj: Обьект, с которым проверяется столкновение. Может быть шаром или квадратом.
            :return:
            Возвращает True в случае столкновения мяча и цели. В противном случае возвращает False.
        """
        if obj.figure == 'ball':
            return dist(self.x, self.y, obj.x, obj.y) < self.r + obj.r
        if obj.figure == 'square':
            center_x = obj.x + obj.a / 2
            center_y = obj.y + obj.a / 2
            corners = [[obj.x, obj.y], [obj.x + obj.a, obj.y],
                       [obj.x, obj.y + obj.a], [obj.x + obj.a, obj.y + obj.a]]

            if dist(self.x, self.y, center_x, center_y) <= self.r + obj.a / 2:
                return True
            else:
                for point in corners:
                    if dist(self.x, self.y, point[0], point[1]) <= self.r:
                        return True

        return False


class Rect(Bullet):
    def __init__(self, object_screen, x0, y0, angle):
        """
        Создаёт прямоуголный снаряд, пулю.
        :param object_screen: экран, на котором находится снаряд
        :param x0: начальная координата x снаряда
        :param y0: начальная координата y снаряда
        :param angle: угол, под которым выстреливается пуля
        """
        super().__init__(object_screen, x0, y0)
        self.an = angle
        self.vx = math.cos(self.an)
        self.vy = math.sin(self.an)
        self.up_side = 10
        self.lateral_side = 10

    def move(self):
        """
        Двигает пулю. Пуля пробивает стенки.
        :return:
        """
        self.x += self.vx
        self.y -= self.vy

    def draw(self):
        """
        Прорисовка пули.
        :return:
        """
        down_left = [self.x, self.y]
        down_right = [down_left[0] + self.up_side, down_left[1]]
        up_left = [down_left[0], -self.lateral_side + down_left[1]]
        up_right = [self.up_side + down_left[0], -self.lateral_side + down_left[1]]

        pygame.draw.polygon(self.screen, self.color, (down_left,
                                                      turn(down_right, self.an, down_left),
                                                      turn(up_right, self.an, down_left),
                                                      turn(up_left, self.an, down_left)))

    def hit_test(self, obj):
        """
        Проверяет пулю на стооклновение с объектом.
        :param obj: Объект может быть шаром(ball), квадратом(square), танком.
        :return: Возвращает True пристолкновении. В ином сслучае False
        """
        up_right = [self.x + self.up_side, self.y]
        if obj.figure == 'ball':
            down_right = [self.x + self.up_side, self.y - self.lateral_side]
            points = [up_right, down_right]
            for point in points:
                d = dist(obj.x, obj.y, point[0], point[1])
                return d <= obj.r

        elif obj.figure == 'square':
            down_right = [self.x + self.up_side, self.y + self.lateral_side]
            points = [up_right, down_right]
            for point in points:
                x = point[0] - obj.x
                y = point[1] - obj.y
                if 0 <= x <= obj.a and 0 <= y <= obj.a:
                    return True
        else:
            down_right = [self.x + self.up_side, self.y - self.lateral_side]
            points = [up_right, down_right]
            for point in points:
                d = dist(obj.x, obj.y, point[0], point[1])
                return d <= obj.lateral_side + 4


class Gun:
    def __init__(self, object_screen, x0, y0):
        """
        Интерфейс орудия.
        :param object_screen: экран, на котром находится орудие
        :param x0: координта x нижнего левого угла
        :param y0: координта y нижнего левого угла
        """
        self.screen = object_screen
        self.f2_power = 10
        self.f2_on = 0
        self.an = 0
        self.color = GREY
        self.bullet_type = 0
        self.x = x0
        self.y = y0
        self.up_side = 15
        self.lateral_side = 6
        self.max_power = 70

    def fire2_start(self):
        self.f2_on = 1

    def fire2_end(self, point, magazine):
        """
        Выстреливает снарядом, добавляя объект снаряда в список magazine
        :param point: точка куда стрелять
        :param magazine: список, в который добляетс новый объект снаряда
        :return:
        """
        if point[0] > self.x:
            self.an = math.atan((self.y - point[1]) / (point[0] - self.x))
        elif point[0] < self.x:
            self.an = math.pi + math.atan((self.y - point[1]) / (point[0] - self.x))
        else:
            if point[1] < self.y:
                self.an = math.pi / 2
            else:
                self.an = 3 * math.pi / 2

        if self.bullet_type == 0:
            new_bullet = Ball(self.screen, self.x, self.y)
        else:
            new_bullet = Rect(self.screen, self.x, self.y, self.an)

        new_bullet.vx = self.f2_power * math.cos(self.an)
        new_bullet.vy = self.f2_power * math.sin(self.an)
        magazine.append(new_bullet)
        self.f2_on = 0
        self.f2_power = 10

    def targeting(self, point):
        """
        Прицеливание. Меняет направление орудия в зависимости от положения мыши
        :param point: точка, в которую направлено орудие
        :return:
        """
        if point[0] > self.x:
            self.an = math.atan((self.y - point[1]) / (point[0] - self.x))
        elif point[0] < self.x:
            self.an = math.pi + math.atan((self.y - point[1]) / (point[0] - self.x))
        else:
            if point[1] < self.y:
                self.an = math.pi / 2
            else:
                self.an = 3 * math.pi / 2
        if self.f2_on:
            self.color = RED
        else:
            self.color = GREY

    def draw(self):
        """
        Прорисовка орудия.
        :return:
        """
        down_left = [self.x, self.y]
        down_right = [down_left[0] + self.up_side, down_left[1]]
        up_left = [down_left[0], -self.lateral_side + down_left[1]]
        up_right = [self.up_side + down_left[0], -self.lateral_side + down_left[1]]

        pygame.draw.polygon(self.screen, self.color, (down_left,
                                                      turn(down_right, self.an, down_left),
                                                      turn(up_right, self.an, down_left),
                                                      turn(up_left, self.an, down_left)))

    def power_up(self):
        """
        Увеличения потенциального импульса снаряда. Также происходит удлинение орудия
        :return:
        """
        if self.f2_on:
            if self.f2_power < self.max_power:
                self.f2_power += 1.5
                self.up_side += 1.5
            self.color = RED
        else:
            self.color = GREY
            self.up_side = 15


class PlayerGun(Gun):
    def __init__(self, object_screen, x0, y0):
        """
        Орудие игрока - это танк. Может двигаться.
        :param object_screen: экран на котором изображается танк
        :param x0: начальная x координата танка
        :param y0: начальная y координата танка

        """
        super().__init__(object_screen, x0, y0)
        self.figure = 'tank'
        self.platform = 20
        self.live = 1

    def change_bullet(self):
        """
        Меняет тип снаряда.
        :return:
        """
        if self.bullet_type == 1:
            self.bullet_type = 0
        else:
            self.bullet_type += 1

    def draw_tank(self):
        """
        Рисует платформу танка, башню.
        :return:
        """
        pygame.draw.circle(self.screen, GREEN, [self.x, self.y], self.lateral_side + 2)
        pygame.draw.rect(self.screen, GREY, [self.x - self.platform / 2, self.y, self.platform, self.lateral_side + 3])

    def move_left(self):
        """
        Движение танка влево.
        :return:
        """
        if self.x > 20:
            self.x -= 20

    def move_right(self):
        """
        Движение танка вправо.
        :return:
        """
        if self.x < WIDTH - 20:
            self.x += 20


class BotGun(Gun):
    def __init__(self, object_screen, x0, y0):
        """
        Создаёт орудие, которое управляется программой.
        :param object_screen:
        :param x0:
        :param y0:
        """
        super().__init__(object_screen, x0, y0)
        self.bullet_type = 1


class Target:
    def __init__(self, object_screen, x0, y0, vx, vy):
        """
        Создаёт мишень.
        :param object_screen: экран, на котором находится мишень
        :param x0: опорная x координата мишени
        :param y0: опорная y координата мишени
        :param vx: начальная скорость по x
        :param vy: начальная скорость по y
        """
        self.screen = object_screen
        self.x = x0
        self.y = y0
        self.live = 1
        self.vx = vx
        self.vy = vy
        self.live = 1


class TargetBall(Target):
    def __init__(self, object_screen, x0, y0, vx, vy):
        """
        Создаёт мишень в форме шара
        :param object_screen: экран, на котором находится мишень
        :param x0: опорная x координата мишени
        :param y0: опорная y координата мишени
        :param vx: начальная скорость по x
        :param vy: начальная скорость по y
        """
        super().__init__(object_screen, x0, y0, vx, vy)
        self.score = 0
        self.r = rnd(10, 50)
        self.figure = 'ball'
        self.color = RED

    def hit(self, points=1):
        """Попадание шарика в цель."""
        self.score += points

    def move(self):
        """Переместить мяч по прошествии единицы времени.

        Метод описывает перемещение мяча за один кадр перерисовки. То есть, обновляет значения
        self.x и self.y с учетом скоростей self.vx и self.vy, силы гравитации, действующей на мяч,
        и стен по краям окна (размер окна 800х600).
        """
        if self.vy != 0:
            self.x += self.vx
            self.y -= self.vy

        self.x, self.y = border_control('ball', self.x, self.y, self.r)

        if WIDTH <= self.x + self.r or self.x - self.r <= 0:
            self.vx = -1 * self.vx
        elif HEIGHT <= self.y + self.r or self.y - self.r <= 0:
            self.vy = -1 * (self.vy / 2)

    def draw(self):
        pygame.draw.circle(self.screen, self.color, (self.x, self.y), self.r)
        pygame.draw.circle(self.screen, 'black', (self.x, self.y), self.r, width=1)


class TargetSquare(Target):
    def __init__(self, object_screen, x, y, vx, vy):
        super().__init__(object_screen, x, y, vx, vy)
        self.points = 0
        self.x = 0
        self.y = 0
        self.a = rnd(60, 70)
        self.figure = 'square'
        self.color = BLUE

    def hit(self):
        pass

    def move(self):

        self.x += self.vx
        self.y -= self.vy + g / 2
        self.vy -= g

        self.x, self.y = border_control('square', self.x, self.y, self.a)

        if WIDTH <= self.x + self.a or self.x <= 0:
            self.vx = -1 * self.vx / abs(self.vx) * rnd(10, 20)

        elif HEIGHT <= self.y + self.a or self.y <= 0:
            if self.vy == 0:
                self.vy = rnd(10, 20)
            else:
                self.vy = -1 * self.vy / abs(self.vy) * rnd(10, 20)

    def draw(self):
        pygame.draw.rect(self.screen, self.color, [self.x, self.y, self.a, self.a])


class Bomber:
    def __init__(self, object_screen, x0):
        """
        Сбрасывает цели вниз.
        :param object_screen:
        :param x0:
        """
        self.screen = object_screen
        self.x = x0
        self.y = 0
        self.vx = 2
        self.up_side = 20
        self.lateral_side = 40

    def move(self):
        self.x += self.vx

        if self.x < 0:
            self.x = 0
        if self.x > WIDTH - self.up_side:
            self.x = WIDTH - self.up_side

        if WIDTH <= self.x + self.up_side or self.x <= 0:
            self.vx = -1 * self.vx

    def draw(self):
        pygame.draw.rect(self.screen, GREY, [self.x, self.y, self.up_side, self.lateral_side])

    def drop(self, type_of_bullet, aim):
        """
        Сбрасывание мишени aim.
        :param type_of_bullet:
        :param aim:
        :return:
        """
        if type_of_bullet == 'ball':
            aim.x = self.x + self.up_side / 2
            aim.y = self.y + self.lateral_side / 2
            aim.vx = self.vx
            aim.vy = rnd(20, 30)

        else:
            aim.x = self.x
            aim.y = self.y + self.lateral_side / 2
            aim.vx = self.vx
            aim.vy = rnd(20, 30)


pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
bullet = 0
bullets = []
targets = []
bots = []
bombers = []
score = 0

clock = pygame.time.Clock()

gun = PlayerGun(screen, 60, 590)

bomber_ball = Bomber(screen, 60)
bomber_square = Bomber(screen, 300)
bombers.append(bomber_ball)
bombers.append(bomber_square)

target1 = TargetBall(screen, 0, 0, 0, 0)
target2 = TargetSquare(screen, 0, 0, 0, 0)
targets.append(target1)
targets.append(target2)

bot1 = BotGun(screen, 0, 100)
bot2 = BotGun(screen, 795, 100)
bot1.max_power = 16
bot2.max_power = 16
bots.append(bot1)
bots.append(bot2)

finished = False
check = 0
flag = 0

bomber_ball.drop('ball', target1)
bomber_square.drop('square', target2)
while not finished:

    screen.fill(WHITE)
    num_of_hits = pygame.font.Font(None, 24)
    text1 = num_of_hits.render(str(score), True, (0, 0, 0))
    screen.blit(text1, (10, 10))

    if gun.live == 1:
        gun.draw()
        gun.draw_tank()
    else:
        flag += 1
        if flag == 80:
            gun.live = 1
            flag = 0
    for bot in bots:
        bot.draw()

    for bomber in bombers:
        bomber.draw()

    for target in targets:
        if target.live == 1:
            target.move()
            target.draw()
        else:
            check += 1
            if check == 50:
                if target.figure == 'ball':
                    bombers[0].drop('ball', target)

                else:
                    bombers[1].drop('square', target)

                target.live = 1
                bullet = 0
                check = 0

    for b in bullets:
        if b.live > 0:
            b.draw()
    pygame.display.update()

    clock.tick(FPS)
    keys = pygame.key.get_pressed()
    if keys[pygame.K_d]:
        if gun.y != 780:
            gun.move_right()
    elif keys[pygame.K_a]:
        if gun.x != 20:
            gun.move_left()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            finished = True
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_b:
                gun.change_bullet()
            if event.key == pygame.K_a:
                if gun.x > 20:
                    gun.move_left()
            if event.key == pygame.K_d:
                if gun.x < 100:
                    gun.move_right()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if gun.live:
                gun.fire2_start()
        elif event.type == pygame.MOUSEBUTTONUP:
            if gun.live:
                gun.fire2_end(event.pos, bullets)
                bullet += 1
        if event.type == pygame.MOUSEMOTION:
            gun.targeting(event.pos)

    for bot in bots:
        if gun.live:
            if not bot.f2_on:
                bot.fire2_start()
            elif bot.f2_power == rnd(0, 17):
                bot.fire2_end([gun.x, gun.y], bullets)
            else:
                bot.targeting([gun.x, gun.y])

    for bomber in bombers:
        bomber.move()

    for i, b in enumerate(bullets):
        if b.live > 0:
            b.move()
            b.live -= 0.2
        else:
            bullets.pop(i)

        for target in targets:
            if b.hit_test(target) and target.live:
                target.live = 0
                target.hit()

        if b.hit_test(gun) and gun.live:
            gun.live = 0

    for bot in bots:
        bot.power_up()
    gun.power_up()

pygame.quit()
