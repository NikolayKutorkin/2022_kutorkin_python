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
    x1 = -(ref_point[0] - point[0]) * math.cos(angle) - (ref_point[1] - point[1]) * math.sin(angle)
    y1 = -(ref_point[0] - point[0]) * math.sin(angle) + (ref_point[1] - point[1]) * math.cos(angle)
    return x1 + ref_point[0], ref_point[1] - y1


def replacing_coordinates(x0, y0, angle, x, y):
    x1 = (x - x0) * math.cos(angle) + (y - y0) * math.sin(angle)
    y1 = (y - y0) * math.cos(angle) - (x - x0) * math.sin(angle)
    return x1, y1


def dist(x1, y1, x2, y2):
    distance = math.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)
    return distance

def border_control():
    pass

class Bullet:
    def __init__(self, object_screen, x0, y0):
        self.screen = object_screen
        self.x = x0
        self.y = y0
        self.vx = 0
        self.vy = 0
        self.live = 30
        self.square = 0
        self.color = choice(GAME_COLORS)


class Ball(Bullet):
    def __init__(self, screen, x0, y0):
        """ Конструктор класса ball

        Args:
        x - начальное положение мяча по горизонтали
        y - начальное положение мяча по вертикали
        """
        super().__init__(screen, x0, y0)
        self.r = 15

    def move(self):
        """Переместить мяч по прошествии единицы времени.

        Метод описывает перемещение мяча за один кадр перерисовки. То есть, обновляет значения
        self.x и self.y с учетом скоростей self.vx и self.vy, силы гравитации, действующей на мяч,
        и стен по краям окна (размер окна 800х600).
        """
        if self.vy != 0:
            self.x += self.vx
            self.y -= self.vy + g / 2
            self.vy -= g

        # Проверка, не вышел ли шар за стенку
        if self.x < self.r:
            self.x = self.r
        if self.x > WIDTH - self.r:
            self.x = WIDTH - self.r
        if self.y < self.r:
            self.y = self.r
        if self.y > HEIGHT - self.r:
            if abs(self.vy) < 11:
                self.vy = 0
            self.y = HEIGHT - self.r

        # Удар о стенку
        if WIDTH <= self.x + self.r or self.x - self.r <= 0:
            self.vx = -1 * self.vx
        elif HEIGHT <= self.y + self.r or self.y - self.r <= 0:
            self.vy = -1 * (self.vy / 2)
            self.vx = self.vx / 1.4

    def draw(self):
        pygame.draw.circle(
            self.screen,
            self.color,
            (self.x, self.y),
            self.r
        )
        pygame.draw.circle(
            self.screen,
            'black',
            (self.x, self.y),
            self.r,
            width=1
        )

    def hittest(self, obj):
        """Функция проверяет сталкивалкивается ли данный обьект с целью, описываемой в обьекте obj.

        Args:
            obj: Обьект, с которым проверяется столкновение.
        Returns:
            Возвращает True в случае столкновения мяча и цели. В противном случае возвращает False.
        """
        if obj.figure == 'ball':
            d = dist(self.x, self.y, obj.x, obj.y)
            return d < self.r + obj.r
        if obj.figure == 'square':
            x = obj.x
            y = obj.y
            a = obj.a
            center_x = x + a / 2
            center_y = y + a / 2
            corners = [[x, y], [x + a, y], [x, y + a], [x + a, y + a]]

            d = dist(self.x, self.y, center_x, center_y)
            if d <= self.r + obj.a / 2:
                return True
            else:
                for point in corners:
                    d = dist(self.x, self.y, point[0], point[1])
                    if d <= self.r:
                        return True

        return False


class Rect(Bullet):
    def __init__(self, screen, x0, y0, angle):
        super().__init__(screen, x0, y0)
        self.an = angle
        self.vx = math.cos(self.an)
        self.vy = math.sin(self.an)

        # Параметры фигуры пули
        self.up_side = 10
        self.lateral_side = 10

    def move(self):
        self.x += self.vx
        self.y -= self.vy

    def draw(self):
        down_left = [self.x, self.y]
        down_right = [down_left[0] + self.up_side, down_left[1]]
        up_left = [down_left[0], -self.lateral_side + down_left[1]]
        up_right = [self.up_side + down_left[0], -self.lateral_side + down_left[1]]

        pygame.draw.polygon(self.screen, self.color, (down_left,
                                                      turn(down_right, self.an, down_left),
                                                      turn(up_right, self.an, down_left),
                                                      turn(up_left, self.an, down_left)))

    def hittest(self, obj):
        if obj.figure == 'ball':
            up_right = [self.x + self.up_side, self.y]
            down_right = [self.x + self.up_side, self.y - self.lateral_side]
            points = [up_right, down_right]
            for point in points:
                d = dist(obj.x, obj.y, point[0], point[1])
                return d <= obj.r

        elif obj.figure == 'square':
            up_right = [self.x + self.up_side, self.y]
            down_right = [self.x + self.up_side, self.y + self.lateral_side]
            points = [up_right, down_right]
            for point in points:
                x = point[0] - obj.x
                y = point[1] - obj.y
                if 0 <= x <= obj.a and 0 <= y <= obj.a:
                    return True
        else:
            up_right = [self.x + self.up_side, self.y]
            down_right = [self.x + self.up_side, self.y - self.lateral_side]
            points = [up_right, down_right]
            for point in points:
                d = dist(obj.x, obj.y, point[0], point[1])
                return d <= obj.lateral_side + 8


class Gun:
    def __init__(self, screen, x0, y0):
        self.screen = screen
        self.f2_power = 10
        self.f2_on = 0
        self.an = 1
        self.color = GREY
        self.bullet_type = 0
        self.x = x0
        self.y = y0

        # Параметры фигуры орудия
        self.down_left = [x0, y0]
        self.up_side = 15
        self.lateral_side = 6

    def fire2_start(self):
        self.f2_on = 1

    def fire2_end(self, point, bullets):
        """Выстрел мячом.

        Происходит при отпускании кнопки мыши.
        Начальные значения компонент скорости мяча vx и vy зависят от положения мыши.
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
        bullets.append(new_bullet)
        self.f2_on = 0
        self.f2_power = 10

    def targetting(self, point):
        """Прицеливание. Зависит от положения мыши."""
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
        down_left = [self.x, self.y]
        down_right = [down_left[0] + self.up_side, down_left[1]]
        up_left = [down_left[0], -self.lateral_side + down_left[1]]
        up_right = [self.up_side + down_left[0], -self.lateral_side + down_left[1]]
        opora = [self.x, self.y - self.lateral_side / 2]
        pygame.draw.polygon(self.screen, self.color, (down_left,
                                                      turn(down_right, self.an, down_left),
                                                      turn(up_right, self.an, down_left),
                                                      turn(up_left, self.an, down_left)))

    def power_up(self):
        if self.f2_on:
            if self.f2_power < 70:
                self.f2_power += 1.5
                self.up_side += 1.5
            self.color = RED
        else:
            self.color = GREY
            self.up_side = 15


class Player_Gun(Gun):
    def __init__(self, screen, x0, y0):
        super().__init__(screen, x0, y0)
        self.figure = 'tank'
        self.live = 1

    def change_bullet(self):
        if self.bullet_type == 1:
            self.bullet_type = 0
        else:
            self.bullet_type += 1

    def draw_tank(self):
        pygame.draw.circle(self.screen, GREEN, [self.x, self.y], self.lateral_side + 2)
        l = 20
        pygame.draw.rect(self.screen, GREY, [self.x - l / 2, self.y, l, self.lateral_side + 3])

    def move_left(self):
        self.x -= 20

    def move_right(self):
        self.x += 20


class Bot_gun(Gun):
    def __init__(self, screen, x0, y0):
        super().__init__(screen, x0, y0)
        self.bullet_type = 1


class Target:
    def __init__(self, screen, x0, y0, vx, vy):
        self.screen = screen
        self.x = x0
        self.y = y0
        self.live = 1
        self.vx = vx
        self.vy = vy
        self.live = 1


class Target_ball(Target):
    def __init__(self, screen, x0, y0, vx, vy):
        super().__init__(screen, x0, y0, vx, vy)
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

        # Проверка, не вышел ли шар за стенку
        if self.x < self.r:
            self.x = self.r
        if self.x > WIDTH - self.r:
            self.x = WIDTH - self.r
        if self.y < self.r:
            self.y = self.r
        if self.y > HEIGHT - self.r:
            self.y = HEIGHT - self.r

        # Удар о стенку
        if WIDTH <= self.x + self.r or self.x - self.r <= 0:
            self.vx = -1 * self.vx
        elif HEIGHT <= self.y + self.r or self.y - self.r <= 0:
            self.vy = -1 * (self.vy / 2)

    def draw(self):
        pygame.draw.circle(
            self.screen,
            self.color,
            (self.x, self.y),
            self.r
        )
        pygame.draw.circle(
            self.screen,
            'black',
            (self.x, self.y),
            self.r,
            width=1
        )


class Target_square(Target):
    def __init__(self, screen, x, y, vx, vy):
        super().__init__(screen, x, y, vx, vy)
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

        if self.x < 0:
            self.x = 0
        if self.x > WIDTH - self.a:
            self.x = WIDTH - self.a
        if self.y < 0:
            self.y = 0
        if self.y > HEIGHT - self.a:
            self.y = HEIGHT - self.a

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
    def __init__(self, screen, x0):
        self.screen = screen
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

    def drop(self, type_of_bullet, target):
        if type_of_bullet == 'ball':
            target.x = self.x + self.up_side / 2
            target.y = self.y + self.lateral_side / 2
            target.vx = self.vx
            target.vy = rnd(20, 30)

        else:
            target.x = self.x
            target.y = self.y + self.lateral_side / 2
            target.vx = self.vx
            target.vy = rnd(20, 30)


pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
bullet = 0
bullets = []
targets = []
bots = []
bombers = []
score = 0

clock = pygame.time.Clock()
gun = Player_Gun(screen, 60, 590)
bomber_ball = Bomber(screen, 60)
bomber_square = Bomber(screen, 300)
bombers.append(bomber_ball)
bombers.append(bomber_square)
target1 = Target_ball(screen, 0, 0, 0, 0)
target2 = Target_square(screen, 0, 0, 0, 0)
targets.append(target1)
targets.append(target2)
bots.append(Bot_gun(screen, 20, 100))
bots.append(Bot_gun(screen, 570, 100))
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
                if gun.x != 20:
                    gun.move_left()
            if event.key == pygame.K_d:
                if gun.y != 780:
                    gun.move_right()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if not check:
                gun.fire2_start()
        elif event.type == pygame.MOUSEBUTTONUP:
            if not check:
                gun.fire2_end(event.pos, bullets)
                bullet += 1
        elif event.type == pygame.MOUSEMOTION:
            gun.targetting(event.pos)

    for i, bot in enumerate(bots):
        if not bot.f2_on:
            bot.fire2_start()
        elif bot.f2_power == rnd(30, 70):
            bot.fire2_end([gun.x, gun.y], bullets)
        else:
            bot.targetting([gun.x, gun.y])

    for bomber in bombers:
        bomber.move()
    for i, b in enumerate(bullets):
        if b.live > 0:
            b.move()
            b.live -= 0.2
        else:
            bullets.pop(i)

        for i, target in enumerate(targets):
            if b.hittest(target) and target.live:
                target.live = 0
                target.hit()

        if b.hittest(gun) and gun.live:
            gun.live = 0

    for bot in bots:
        bot.power_up()
    gun.power_up()

pygame.quit()
