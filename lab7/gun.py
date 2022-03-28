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


class Ball:
    def __init__(self, screen: pygame.Surface, x=40, y=450):
        """ Конструктор класса ball

        Args:
        x - начальное положение мяча по горизонтали
        y - начальное положение мяча по вертикали
        """
        self.screen = screen
        self.x = x
        self.y = y
        self.r = 10
        self.vx = 0
        self.vy = 0
        self.color = choice(GAME_COLORS)
        self.live = 30

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
        for x in range(obj.x - obj.r, obj.x + obj.r):
            y1 = obj.y + math.sqrt(obj.r ** 2 - (obj.x - x) ** 2)
            y2 = obj.y - math.sqrt(obj.r ** 2 - (obj.x - x) ** 2)
            for y in [y1, y2]:
                if (x - self.x) ** 2 + (y - self.y) ** 2 <= self.r ** 2:
                    return True
        return False


class Gun:
    def __init__(self, screen):
        self.screen = screen
        self.f2_power = 10
        self.f2_on = 0
        self.an = 1
        self.color = GREY

        # Параметры фигуры орудия
        self.down_left = [20, 450]
        self.up_side = 15
        self.lateral_side = 6

    def fire2_start(self, event):
        self.f2_on = 1

    def fire2_end(self, event):
        """Выстрел мячом.

        Происходит при отпускании кнопки мыши.
        Начальные значения компонент скорости мяча vx и vy зависят от положения мыши.
        """
        global balls, bullet
        bullet += 1
        new_ball = Ball(self.screen)
        new_ball.r += 5
        self.an = math.atan((450 - event.pos[1]) / (event.pos[0] - 20))
        new_ball.vx = self.f2_power * math.cos(self.an)
        new_ball.vy = - self.f2_power * math.sin(-self.an)
        balls.append(new_ball)
        self.f2_on = 0
        self.f2_power = 10

    def targetting(self, event):
        """Прицеливание. Зависит от положения мыши."""
        if event:
            self.an = math.atan((450 - event.pos[1]) / (event.pos[0] - 20))
        if self.f2_on:
            self.color = RED
        else:
            self.color = GREY

    def draw(self):
        # FIXIT don't know how to do it
        down_right = [self.down_left[0] + self.up_side, self.down_left[1]]
        up_left = [self.down_left[0], -self.lateral_side + self.down_left[1]]
        up_right = [self.up_side + self.down_left[0], -self.lateral_side + self.down_left[1]]

        pygame.draw.polygon(self.screen, self.color, (self.down_left,
                                                      turn(down_right, self.an, self.down_left),
                                                      turn(up_right, self.an, self.down_left),
                                                      turn(up_left, self.an, self.down_left)))

    def power_up(self):
        if self.f2_on:
            if self.f2_power < 100:
                self.f2_power += 2
                self.up_side += 2
            self.color = RED
        else:
            self.color = GREY
            self.up_side = 15


class Target:
    # self.points = 0
    # self.live = 1
    # self.new_target()
    def __init__(self, screen):
        self.screen = screen
        self.points = 0
        self.live = 1
        self.new_target()

    def new_target(self):
        """ Инициализация новой цели. """
        x = self.x = rnd(600, 780)
        y = self.y = rnd(300, 550)
        r = self.r = rnd(2, 50)
        color = self.color = RED

    def hit(self, points=1):
        """Попадание шарика в цель."""
        self.points += points

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


pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
bullet = 0
balls = []

clock = pygame.time.Clock()
gun = Gun(screen)
target = Target(screen)
finished = False
check = 1

while not finished:

    screen.fill(WHITE)
    num_of_bullets = pygame.font.Font(None, 24)
    text = num_of_bullets.render(str(bullet), True, (0, 0, 0))
    screen.blit(text, (10, 10))
    gun.draw()
    if target.live == 1:
        target.draw()
    else:
        check += 1
        print(check)
        if check == 50:
            target.live = 1
            check = 1

    for b in balls:
        if b.live > 0:
            b.draw()
    pygame.display.update()

    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            finished = True
        elif event.type == pygame.MOUSEBUTTONDOWN:
            gun.fire2_start(event)
        elif event.type == pygame.MOUSEBUTTONUP:
            gun.fire2_end(event)
        elif event.type == pygame.MOUSEMOTION:
            gun.targetting(event)

    for b in balls:
        if b.live > 0:
            b.move()
            b.live -= 0.2
        if b.hittest(target) and target.live:
            target.live = 0
            target.hit()
            target.new_target()

    gun.power_up()

pygame.quit()
