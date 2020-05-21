import random

import pygame

from sprites import bloom_sprite

pygame.init()
FPS = 60
width, height = 1200, 800
clock = pygame.time.Clock()
screen = pygame.display.set_mode((width, height))


class SmokeParticle:
    def __init__(self, sc, x, y, force):
        self.cycle = 1000
        self.sc = sc
        self.x = x
        self.y = y
        self.force = force
        self.r_y_c = []
        self.r_x_c = []
        self.wcoords = []
        self.count = []
        self.colors = []
        for c in range(self.force):
            self.r_y_c.append(random.randint(0, 30) - 15)
            self.r_x_c.append(random.randint(0, 20) - 10)
            self.wcoords.append(random.randint(10, 30))
            self.count.append(random.randint(0, 1))
            color = random.randint(20, 25)
            self.colors.append((color, color, color))

    def action(self):
        self.cycle -= 1
        if self.cycle <= 0:
            self.reload_plus()
            self.cycle = 1000
        try:
            for c in range(len(self.r_y_c)):
                if self.count[c] // 3 <= self.wcoords[c] + 50 // 3:
                    if self.count[c] <= 50:
                        pygame.draw.rect(self.sc, self.colors[c],
                                         (self.x + self.r_x_c[c] - (self.wcoords[c]) // 2,
                                          self.y + self.r_y_c[c], self.wcoords[c],
                                          self.wcoords[c]))
                    else:
                        pygame.draw.rect(self.sc, self.colors[c],
                                         (self.x + self.r_x_c[c] - (
                                                     self.wcoords[c] - (self.count[c] // 3) + 50 // 3) // 2,
                                          self.y + self.r_y_c[c], self.wcoords[c] - (self.count[c] // 3) + 50 // 3,
                                          self.wcoords[c] - (self.count[c] // 3) + 50 // 3))
                self.r_y_c[c] -= 1
                self.count[c] += 1
        except BaseException:
            pass
        for c in range(self.force):
            self.r_y_c.append(random.randint(0, 30) - 15)
            self.r_x_c.append(random.randint(0, 20) - 10)
            self.wcoords.append(random.randint(10, 30))
            self.count.append(random.randint(0, 1))
            color = random.randint(20, 25)
            self.colors.append((color, color, color))

    def reload_plus(self):
        self.r_y_c = []
        self.r_x_c = []
        self.wcoords = []
        self.count = []
        self.colors = []

    def update_pos(self, newx, newy):
        self.x = newx
        self.y = newy


class FireParticle:
    def __init__(self, sc, x, y, force):
        self.cycle = 1000
        self.sc = sc
        self.x = x
        self.y = y
        self.force = force
        self.r_y_c = []
        self.r_x_c = []
        self.wcoords = []
        self.count = []
        self.colors = []
        for c in range(self.force):
            self.r_y_c.append(random.randint(0, 16) - 8)
            self.r_x_c.append(random.randint(0, 10) - 5)
            self.wcoords.append(random.randint(5, 10))
            self.count.append(random.randint(0, 1))
            self.colors.append((255, 250, 125))

    def action(self):
        self.cycle -= 1
        if self.cycle <= 0:
            self.reload_plus()
            self.cycle = 1000
        try:
            for c in range(len(self.r_y_c)):
                if self.count[c] <= self.wcoords[c]:
                    pygame.draw.rect(self.sc, (self.colors[c][0], self.colors[c][1] - self.count[c] * 15,
                                               self.colors[c][2] - self.count[c] // 2 * 15),
                                     (self.x + self.r_x_c[c] - (self.wcoords[c] - self.count[c]) // 2,
                                      self.y + self.r_y_c[c], self.wcoords[c] - int(self.count[c]),
                                      self.wcoords[c] - int(self.count[c])))
                self.r_y_c[c] -= 1
                self.count[c] += 0.3
        except BaseException:
            pass
        for c in range(self.force):
            self.r_y_c.append(random.randint(0, 16) - 8)
            self.r_x_c.append(random.randint(0, 10) - 5)
            self.wcoords.append(random.randint(5, 10))
            self.count.append(random.randint(0, 1))
            self.colors.append((255, 250, 125))

    def reload_plus(self):
        self.r_y_c = []
        self.r_x_c = []
        self.wcoords = []
        self.count = []
        self.colors = []

    def update_pos(self, newx, newy):
        self.x = newx
        self.y = newy


class Explotion:
    def __init__(self, sc, w=10, r=50, end=False, color_circle=(255, 255, 255), color_rect=(255, 255, 255)):
        self.sc = sc
        self.r = r
        self.w = w
        self.end = end
        self.count = 0
        self.load = 0
        self.xcoords = []
        self.ycoords = []
        self.wcoords = []
        self.circle_color = color_circle
        self.rect_color = color_rect
        for c in range(15):
            self.xcoords.append(random.randint(0, 6) - 3)
            self.ycoords.append(random.randint(0, 6) - 3)
            self.wcoords.append(random.randint(5, 25))

    def action(self, x, y):
        self.count += 1
        self.load += 1
        if self.end or self.count == 40:
            pass
        try:
            if self.w != 0:
                pygame.draw.circle(self.sc, self.circle_color, (x, y), self.r, self.w)
        except BaseException:
            pass
        try:
            for c in range(15):
                if self.count <= self.wcoords[c]:
                    pygame.draw.rect(self.sc, self.rect_color, (x + self.xcoords[c] * self.count ** 2 // 10,
                                                                y + self.ycoords[c] * self.count ** 2 // 10,
                                                                self.wcoords[c] - self.count,
                                                                self.wcoords[c] - self.count))
        except BaseException:
            pass
        self.r += 3
        self.w -= 1
        self.rect_color = (self.rect_color[0], self.rect_color[1] - 5, self.rect_color[2] - 10)
        if self.w == 0:
            self.end = True

    def reload(self):
        self.count = 0
        self.r = 50
        self.w = 10
        self.load = 0
        self.xcoords = []
        self.ycoords = []
        self.wcoords = []
        self.rect_color = (255, 255, 255)
        for c in range(15):
            self.xcoords.append(random.randint(0, 6) - 3)
            self.ycoords.append(random.randint(0, 6) - 3)
            self.wcoords.append(random.randint(5, 25))


class CircleMenu:
    def __init__(self, sc, board=None, pos_x=0, pos_y=0):
        self.active = False
        self.pressed = False
        self.pos = pos_x, pos_y
        self.sc = sc

    def render(self):
        if self.active:
            screen.blit(bloom_sprite, (self.pos[0] - 50, self.pos[1] - 50))

    def change_coords(self, pos):
        self.pos = pos
        self.board_pos = None  # board_tile(self.pos)

    def get_coords(self):
        return self.pos


# part_test1 = Explotion(screen, 10, 50, False, (255, 255, 255), (255, 255, 255))
# part_test2 = FireParticle(screen, 200, 200, 3)
# part_test3 = SmokeParticle(screen, 400, 300, 1)
# particlesOneShoots = [part_test1]
# particlesStatic = [part_test2, part_test3]
# cm = CircleMenu(screen)
# a, b = 0, 0
# while True:
#     for event in pygame.event.get():
#         if event.type == pygame.QUIT:
#             pygame.quit()
#             exit(0)
#         if event.type == pygame.MOUSEMOTION:
#             pass
#         if event.type == pygame.MOUSEBUTTONDOWN:
#             a, b = event.pos
#
#             # нужно обрабатывать при использовании
#
#             if event.button == 1:
#                 pass
#                 cm.active = False
#                 part_test1.reload()
#             if event.button == 2 or event.button == 3:
#                 cm.active = True
#                 cm.change_coords((a, b))
#     screen.fill((40, 40, 40))
#
#     # нужно обрабатывать всегда
#     for particle in particlesOneShoots:
#         particle.action(a, b)
#     for particle in particlesStatic:
#         particle.action()
#     cm.render()
#
#     screen.blit(bloom_sprite.image, (150, 150))
#
#     pygame.display.flip()
#     clock.tick(FPS)
