import pygame
import random
import sys
import math

RESOLUTION = (700, 700)

white = (255, 255, 255)


class Player:
    def __init__(self, game):
        self.game = game

        self.comprect = game.spawn
        # self.offset = game.offset
        self.image = pygame.Surface((30, 30))
        self.image.fill((0, 100, 100))
        self.rect = pygame.Rect(self.comprect[0] - game.offset[0], self.comprect[1] - game.offset[1], 30, 30)

        self.movx = [False, False]
        self.movy = [False, False]
        self.velx = 0
        self.vely = 0
        self.running = 1
        self.energy = 69
        self.hp = 100
        self.invincibility = 0

    def update(self):
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                sys.exit()
            elif e.type == pygame.KEYDOWN:
                if e.key == pygame.K_LEFT:
                    self.movx[0] = True
                    self.movx[1] = False
                if e.key == pygame.K_RIGHT:
                    self.movx[0] = False
                    self.movx[1] = True
                if e.key == pygame.K_UP:
                    self.movy[0] = True
                    self.movy[1] = False
                if e.key == pygame.K_DOWN:
                    self.movy[0] = False
                    self.movy[1] = True
                if e.key == pygame.K_RSHIFT and self.energy > 10:
                    self.running = 6
                    self.image.fill((0, 170, 170))
            elif e.type == pygame.KEYUP:
                if e.key == pygame.K_LEFT:
                    self.movx[0] = False
                if e.key == pygame.K_RIGHT:
                    self.movx[1] = False
                if e.key == pygame.K_UP:
                    self.movy[0] = False
                if e.key == pygame.K_DOWN:
                    self.movy[1] = False
                if e.key == pygame.K_RSHIFT:
                    self.running = 1
                    if self.energy > 10:
                        self.image.fill((0, 100, 100))
                    else:
                        self.image.fill((0, 50, 50))


        if self.movx[0] and self.movx[1]:
            self.velx = 0
        elif self.movx[0]:
            self.velx = -1
        elif self.movx[1]:
            self.velx = 1
        else:
            self.velx = 0

        if self.movy[0] and self.movy[1]:
            self.vely = 0
        elif self.movy[0]:
            self.vely = -1
        elif self.movy[1]:
            self.vely = 1
        else:
            self.vely = 0

        self.comprect[0] += self.velx * self.running
        self.comprect[1] += self.vely * self.running

        if self.energy < 70:
            self.energy += 0.02 - (self.running - 1) / 3
        else:
            self.running = 1
            self.energy = 69

        if self.energy < 0:
            self.energy = 0
        elif int(self.energy) == 10 and self.running == 1:
            self.image.fill((0, 100, 100))

        if self.invincibility > 0:
            self.invincibility -= 1

        if self.running > 1.2:
            self.running -= 0.2
        elif self.running > 1:
            if self.energy > 10:
                self.image.fill((0, 100, 100))
            else:
                self.image.fill((0, 50, 50))
            self.running -= 0.2
        else:
            self.running = 1

        if self.comprect[0] < 350:
            self.game.offset[0] = 0
        elif self.comprect[0] > 2050:
            self.game.offset[0] = 1700
        else:
            self.game.offset[0] = self.comprect[0] - 350

        if self.comprect[1] < 350:
            self.game.offset[1] = 0
        elif self.comprect[1] > 2050:
            self.game.offset[1] = 1700
        else:
            self.game.offset[1] = self.comprect[1] - 350

        if self.invincibility > 40:
            self.game.offset[0] += random.randint(-7, 8)
            self.game.offset[1] += random.randint(-8, 8)

        if self.invincibility < 2 and self.running == 1:
            for archer in [self.game.archer, self.game.crazyarcher]:
                for p in archer.arrows.sprites():
                    if self.rect.colliderect(p.rect):
                        self.hp -= 5
                        self.invincibility = 50
            for p in self.game.trapper.arrows.sprites():
                if self.rect.colliderect(p.rect):
                    self.hp -= 10
                    self.invincibility = 70
            for vortal in [self.game.vortal, self.game.vortal2]:
                for p in vortal.slaves.sprites():
                    if self.rect.colliderect(p.rect):
                        self.hp -= 6
                        self.invincibility = 55
            for chaser in [self.game.chaser, self.game.telechaser]:
                if self.rect.colliderect(chaser.rect):
                    self.hp -= 51
                    self.invincibility = 150

        if self.hp < 0:
            self.hp = 100
            # self.game.__init__()
            # I wanna know what it does.
        elif self.hp < 100:
            self.hp += 0.008 * self.energy / 36
        else:
            self.hp = 100

        self.rect.x = self.comprect[0] - self.game.offset[0]
        self.rect.y = self.comprect[1] - self.game.offset[1]

    def draw(self):
        if not 2 < self.running < 4 or not self.invincibility % 6 == 1:
            self.game.screen.blit(self.image, self.rect)


class Vortal:
    def __init__(self, game):
        self.game = game
        self.comprect = [random.randint(0, 2400), random.randint(0, 2400)]
        self.image = pygame.Surface((40, 50))
        self.image.fill((200, 200, 20))
        self.rect = pygame.Rect(self.comprect[0] - game.offset[0], self.comprect[1] - game.offset[1], 30, 30)
        self.mode = 'idle'
        self.slaves = pygame.sprite.Group()
        self.shot_slaves = pygame.sprite.Group()

    def update(self):
        self.slaves.update()
        self.rect.x = self.comprect[0] - self.game.offset[0]
        self.rect.y = self.comprect[1] - self.game.offset[1]
        if self.mode == 'idle':
            if self.game.ticks % 800 == 1:
                self.mode = 'prepare'
        elif self.mode == 'prepare':
            for archer in [self.game.archer, self.game.crazyarcher]:
                try:
                    subject = random.choice(archer.arrows.sprites())
                    if not (subject in self.slaves):
                        subject.remove(archer.arrows)
                        self.slaves.add(subject)
                        subject.source = self
                        subject.speed += 0.5
                        if subject.speed < 4:
                            subject.image.fill((255, 0, 0))
                        else:
                            subject.image.fill((210, 0, 20))
                except IndexError:
                    pass
            if self.game.ticks % 100 == 1:
                self.mode = random.choice(['suck', 'dispa'])
                if self.mode == 'suck':
                    for p in self.slaves.sprites():
                        p.change_course(0, 0)

        elif self.mode == 'dispa':
            for p in self.slaves.sprites():
                p.comprect[0] += (p.comprect[0] - self.comprect[0]) / 450
                p.comprect[1] += (p.comprect[1] - self.comprect[1]) / 450
            if self.game.ticks % 400 == 1:
                self.mode = 'idle2'
        elif self.mode == 'suck':
            touching = 0
            for p in self.slaves.sprites():
                p.comprect[0] += (self.comprect[0] - p.comprect[0]) / 450
                p.comprect[1] += (self.comprect[1] - p.comprect[1]) / 450
                if self.rect.colliderect(p.rect):
                    touching += 1
            if touching == len(self.slaves.sprites()):
                self.mode = 'idle2'
        elif self.mode == 'idle2':
            if self.game.ticks % 100 == 1:
                self.mode = 'disperse'
        elif self.mode == 'disperse':
            if self.game.ticks % 20 == 0 and len(self.slaves.sprites()) != 0:
                held = 0
                if random.randint(0, 100) < 40 or len(self.slaves.sprites()) - len(self.shot_slaves.sprites()) < 8:
                    while held < min(4, len(self.slaves.sprites())):
                        subject = random.choice(self.slaves.sprites())
                        if not self.shot_slaves.has(subject):
                            if held == 0:
                                subject.change_course(0, subject.speed)
                            elif held == 1:
                                subject.change_course(subject.speed, 0)
                            elif held == 2:
                                subject.change_course(0, -subject.speed)
                            else:
                                subject.change_course(-subject.speed, 0)
                            self.shot_slaves.add(subject)
                            held += 1

                        if len(self.slaves.sprites()) - len(self.shot_slaves.sprites()) == 0:
                            break

                else:
                    while held < 8:
                        subject = random.choice(self.slaves.sprites())
                        if self.shot_slaves.has(subject):
                            pass
                        else:
                            if held == 0:
                                subject.change_course(0, subject.speed)
                            elif held == 1:
                                subject.change_course(subject.speed, 0)
                            elif held == 2:
                                subject.change_course(0, -subject.speed)
                            elif held == 3:
                                subject.change_course(-subject.speed, 0)
                            elif held == 4:
                                subject.change_course(subject.speed * 0.8, subject.speed * 0.8)
                            elif held == 5:
                                subject.change_course(subject.speed * 0.8, -subject.speed * 0.8)
                            elif held == 6:
                                subject.change_course(-subject.speed * 0.8, subject.speed * 0.8)
                            elif held == 7:
                                subject.change_course(-subject.speed * 0.8, -subject.speed * 0.8)
                            self.shot_slaves.add(subject)
                            held += 1

            if len(self.slaves.sprites()) - len(self.shot_slaves.sprites()) == 0:
                self.mode = 'idle'

    def draw(self):
        for p in self.slaves.sprites():
            p.draw()
        self.game.screen.blit(self.image, self.rect)


class Trapper:
    def __init__(self, game):
        self.game = game
        self.comprect = [random.randint(game.spawn[0] + 30, 2400), random.randint(0, 2400)]
        self.image = pygame.Surface((30, 30))
        self.image.fill((100, 100, 20))
        self.rect = pygame.Rect(self.comprect[0] - game.offset[0], self.comprect[1] - game.offset[1], 30, 30)
        self.speed = 0.65
        self.mode = 'set'
        self.goal = [2000, 2000]
        self.arrows = pygame.sprite.Group()

    def update(self):
        self.arrows.update()
        if self.mode == 'set':
            try:
                angle = math.degrees(math.atan((self.goal[1] - self.comprect[1]) / (
                            self.goal[0] - self.comprect[0])))
            except ZeroDivisionError:
                angle = 90

            velx = math.sin(90 - angle) * self.speed
            vely = math.sin(angle) * self.speed
            self.comprect[0] += velx + (self.goal[0] - self.comprect[0]) / 400
            self.comprect[1] += vely + (self.goal[1] - self.comprect[1]) / 400
            self.rect.x = self.comprect[0] - self.game.offset[0]
            self.rect.y = self.comprect[1] - self.game.offset[1]

            if self.game.ticks % 50 == 0 or abs(math.sqrt((self.rect.centerx - self.game.player.rect.centerx) ** 2 + (
                    (self.rect.centery - self.game.player.rect.centery) ** 2 + 1))) < 300:
                if self.game.player.velx != 0 or self.game.player.vely != 0:
                    self.goal = [self.game.player.comprect[0] + self.game.player.velx * random.randint(350, 500),
                                 self.game.player.comprect[1] + self.game.player.vely * random.randint(350, 500)]
                else:
                    self.goal = [random.randint(0, 2400), random.randint(0, 2400)]
            if (not 0 < self.comprect[0] < 2400 and not 0 < self.comprect[1] < 2400) or\
                    (not -200 < self.goal[0] < 2600 and not -200 < self.goal[1] < 2600):
                self.goal = [random.randint(0, 2400), random.randint(0, 2400)]
            if self.game.ticks % 200 == 199:
                self.arrows.add(Arrow(self, self.game.player, 0))
                self.arrows.sprites()[-1].image.fill((150, 150, 170))
            if len(self.arrows.sprites()) > 30:
                self.arrows.sprites()[random.randint(0, 10)].kill()
            '''print(abs(math.sqrt((self.rect.centerx - self.game.player.rect.centerx) ** 2 + (
                    (self.rect.centery - self.game.player.rect.centery) ** 2 + 1))),
                  self.rect.centerx - self.game.player.rect.centerx,
                  (self.rect.centery - self.game.player.rect.centery))'''

    def draw(self):
        self.game.screen.blit(self.image, self.rect)
        for p in self.arrows.sprites():
            p.draw()


class Chaser:
    def __init__(self, game, teleporting=False):
        self.game = game
        self.comprect = [random.randint(game.spawn[0] + 30, 2400), random.randint(0, 2400)]
        self.image = pygame.Surface((60, 60))
        if teleporting:
            self.image.fill((10, 10, 200))
        else:
            self.image.fill((20, 20, 20))
        self.rect = pygame.Rect(self.comprect[0] - game.offset[0], self.comprect[1] - game.offset[1], 60, 60)
        self.speed = 0.35
        self.mode = 'chase'
        self.magic = teleporting
        self.goal = [1000, 1000]

    def update(self):
        if self.mode == 'chase':
            try:
                angle = math.degrees(math.atan((self.game.player.comprect[1] - self.comprect[1]) / (
                            self.game.player.comprect[0] - self.comprect[0])))
            except ZeroDivisionError:
                angle = 90

            velx = math.sin(90 - angle) * self.speed
            vely = math.sin(angle) * self.speed
            if self.magic:
                velx += random.randint(-1000, 1001) / 2000
                vely += random.randint(-1000, 1001) / 2000

            if self.magic:
                self.comprect[0] += velx + (self.game.player.comprect[0] + self.game.player.velx * 8 - self.comprect[0]) / 400
                self.comprect[1] += vely + (self.game.player.comprect[1] + self.game.player.vely * 8 - self.comprect[1]) / 400
            else:
                self.comprect[0] += velx + (self.game.player.comprect[0] - self.comprect[0]) / 400
                self.comprect[1] += vely + (self.game.player.comprect[1] - self.comprect[1]) / 400
            self.rect.x = self.comprect[0] - self.game.offset[0]
            self.rect.y = self.comprect[1] - self.game.offset[1]
            if self.game.ticks % 7000 < 100 and random.randint(0, 9999) < 2000 and abs(math.sqrt(
                    (self.rect.centerx - self.game.player.rect.centerx) ** 2 / (
                            (self.rect.centery - self.game.player.rect.centery) ** 2 + 1))) < 900:
                self.goal = [(self.game.player.comprect[0] - self.comprect[0]) * 2.4 + self.game.player.comprect[
                    0] + random.randint(-200, 201),
                             (self.game.player.comprect[1] - self.comprect[1]) * 2.2 + self.game.player.comprect[
                                 1] + random.randint(-200, 201)]
                self.mode = 'charge'
            if self.game.ticks % 598 == 0 and self.magic:
                if random.randint(0, 100) < 30:
                    if random.randint(0, 100) < 40:
                        self.comprect[0] = random.randint(0, 2400)
                        self.comprect[1] = random.randint(0, 2400)
                    else:
                        if random.randint(0, 100) < 55:
                            self.comprect[0] = random.randint(0, 2400)
                        else:
                            self.comprect[1] = random.randint(0, 2400)
                else:
                    if self.game.player.velx != 0:
                        self.comprect[0] = self.game.player.comprect[
                                               0] + self.game.player.velx * self.game.player.running ** 0.7 * 350
                    if self.game.player.vely != 0:
                        self.comprect[1] = self.game.player.comprect[
                                               1] + self.game.player.vely * self.game.player.running ** 0.7 * 350
        else:
            self.comprect[0] += (self.goal[0] - self.comprect[0]) / 300
            self.comprect[1] += (self.goal[1] - self.comprect[1]) / 300
            self.rect.x = self.comprect[0] - self.game.offset[0]
            self.rect.y = self.comprect[1] - self.game.offset[1]
            if self.game.ticks % 4500 < 10:
                self.mode = 'chase'
            elif self.game.ticks % 4000 == 1:
                self.goal = [(self.game.player.comprect[0] - self.comprect[0]) * 2.4 + self.game.player.comprect[
                    0] + random.randint(-200, 201),
                             (self.game.player.comprect[1] - self.comprect[1]) * 2.2 + self.game.player.comprect[
                                 1] + random.randint(-200, 201)]

    def draw(self):
        self.game.screen.blit(self.image, self.rect)


class Archer:
    def __init__(self, game):
        self.game = game
        self.comprect = [random.randint(game.spawn[0] + 30, 2400), random.randint(0, 2400)]
        self.image = pygame.Surface((40, 50))
        self.shadow = pygame.Surface((20, 20))
        self.image.fill((200, 20, 20))
        self.rect = pygame.Rect(self.comprect[0] - game.offset[0], self.comprect[1] - game.offset[1], 30, 30)
        self.speed = 0.3
        self.mode = 'chase'
        self.goal_add = [self.game.player.comprect[0] + random.randint(170, 300) * random.choice([-1, 1]),
                         self.game.player.comprect[0] + random.randint(170, 300) * random.choice([-1, 1])]
        self.arrows = pygame.sprite.Group()
        self.angle = 0

    def update(self):
        if self.mode == 'chase':
            self.comprect[0] += (self.goal_add[0] - self.comprect[0]) / 311
            self.comprect[1] += (self.goal_add[1] - self.comprect[1]) / 315
            self.rect.x = self.comprect[0] - self.game.offset[0]
            self.rect.y = self.comprect[1] - self.game.offset[1]  # - random.randint(95, 101)

            if not 0 < self.goal_add[0] < 2400 or not 0 < self.goal_add[1] < 2400:
                self.goal_add[0] += random.randint(50, 200) * random.choice([-1, 1])
                self.goal_add[1] += random.randint(50, 200) * random.choice([-1, 1])

            if self.rect.collidepoint(self.goal_add[0], self.goal_add[1]):
                self.goal_add[0] += random.randint(9, 30) * random.choice([-1, 1])
                self.goal_add[1] += random.randint(9, 30) * random.choice([-1, 1])

            if self.game.ticks % 3000 == 0:
                self.mode = 'pause'
            elif self.game.player.rect.collidepoint([self.rect.centerx, self.rect.bottom + 60]):
                self.goal_add[0] += random.randint(50, 200) * random.choice([-1, 1])
                self.goal_add[1] += random.randint(50, 200) * random.choice([-1, 1])
            elif abs(math.sqrt((self.rect.centerx - self.game.player.rect.centerx) ** 2 + (
                    (self.rect.centery - self.game.player.rect.centery) ** 2 + 1))) > 420:
                self.goal_add = [self.game.player.comprect[0] + random.randint(170, 300) * random.choice([-1, 1]),
                                 self.game.player.comprect[0] + random.randint(170, 300) * random.choice([-1, 1])]
            elif self.game.ticks % 95 < 3:  # random.choice([105, 100, 175, 200, 275, 200, 300, 300, 70, 100, 80, 85]) == 0:
                self.arrows.add(Arrow(self, self.game.player, 3, height_offset=8))
        else:
            self.rect.x = self.comprect[0] - self.game.offset[0]
            self.rect.y = self.comprect[1] - self.game.offset[1]  # - random.randint(95, 101)
            if self.game.ticks % 300 == 0 or abs(math.sqrt((self.rect.centerx - self.game.player.rect.centerx) ** 2 / (
                    (self.rect.centery - self.game.player.rect.centery) ** 2 + 1))) > 500:
                self.goal_add = [self.game.player.comprect[0] + random.randint(170, 300) * random.choice([-1, 1]),
                                 self.game.player.comprect[0] + random.randint(170, 300) * random.choice([-1, 1])]
                self.mode = 'chase'
            if self.game.ticks % 70 < 3:  # random.choice([175, 80, 75, 100, 175, 100, 100, 100, 70]) < 5:
                self.arrows.add(Arrow(self, self.game.player, 3, height_offset=8))
        self.arrows.update()

    def draw(self):
        try:
            self.angle = math.degrees(math.atan(
                (self.game.player.comprect[1] - self.comprect[1]) / (self.game.player.comprect[0] - self.comprect[0])))
        except ZeroDivisionError:
            if self.game.player.comprect[1] < self.comprect[1]:
                self.angle = 90
            else:
                self.angle = 0

        self.game.screen.blit(self.image, self.rect)
        self.game.screen.blit(self.shadow, (self.rect.x + 10, self.rect.y + 100))
        for p in self.arrows.sprites():
            p.draw()


class SprayArcher(Archer):
    def __init__(self, game):
        super().__init__(game)
        self.image.fill((150, 0, 0))

    def update(self):
        self.comprect[0] += (self.goal_add[0] - self.comprect[0]) / 311
        self.comprect[1] += (self.goal_add[1] - self.comprect[1]) / 315
        self.rect.x = self.comprect[0] - self.game.offset[0]
        self.rect.y = self.comprect[1] - self.game.offset[1] - random.randint(95, 101)

        if not 0 < self.goal_add[0] < 2400 or not 0 < self.goal_add[1] < 2400:
            self.goal_add[0] += random.randint(50, 200) * random.choice([-1, 1])
            self.goal_add[1] += random.randint(50, 200) * random.choice([-1, 1])

        if self.rect.collidepoint(self.goal_add[0], self.goal_add[1]):
            self.goal_add[0] += random.randint(9, 30) * random.choice([-1, 1])
            self.goal_add[1] += random.randint(9, 30) * random.choice([-1, 1])

        if self.game.ticks % 300 == 0 or self.rect.collidepoint(self.goal_add[0], self.goal_add[1]):
            self.goal_add = [self.game.player.comprect[0] + random.randint(170, 300) * random.choice([-1, 1]),
                             self.game.player.comprect[0] + random.randint(170, 300) * random.choice([-1, 1])]
        elif self.game.player.rect.collidepoint([self.rect.centerx, self.rect.bottom + 60]):
            self.goal_add[0] += random.randint(50, 200) * random.choice([-1, 1])
            self.goal_add[1] += random.randint(50, 200) * random.choice([-1, 1])
        elif abs(math.sqrt((self.rect.centerx - self.game.player.rect.centerx) ** 2 / (
                (self.rect.centery - self.game.player.rect.centery) ** 2 + 1))) > 400:
            self.goal_add = [self.game.player.comprect[0] + random.randint(170, 300) * random.choice([-1, 1]),
                             self.game.player.comprect[0] + random.randint(170, 300) * random.choice([-1, 1])]
        elif self.game.ticks % 20 < 3:  # random.choice([105, 100, 175, 200, 275, 200, 300, 300, 70, 100, 80, 85]) == 0:
            self.arrows.add(WeirdArrow(self, self.game.player, 3, height_offset=98))

        self.arrows.update()


class Arrow(pygame.sprite.Sprite):
    def __init__(self, source, target, speed, image=None, height_offset=0):
        super().__init__()
        self.image = image
        self.game = source.game
        self.source = source
        self.image = pygame.Surface((8, 8))
        self.speed = speed ** (random.randint(88, 128) / 100)
        if self.speed < 4:
            self.image.fill((255, 255, 255))
        else:
            self.image.fill((210, 210, 255))

        self.comprect = [source.comprect[0] + 20, source.comprect[1] - height_offset + 20]
        self.rect = pygame.Rect(self.comprect[0] - source.game.offset[0], self.comprect[1] - source.game.offset[1], 16,
                                16)

        try:
            self.angle = (
                math.atan((target.comprect[1] - self.comprect[1] + target.vely * 6 + (source.game.ticks % 2 - 1) * 9) /
                          (target.comprect[0] - self.comprect[0] + target.velx * 6 + (source.game.ticks % 2 - 1) * 9)))
        except ZeroDivisionError:
            if target.comprect[1] < self.comprect[1]:
                self.angle = math.pi / 2
            else:
                self.angle = 0

        if source.comprect[0] < target.comprect[0]:
            self.velx = math.sin(math.pi / 2 - self.angle) * speed
            self.vely = math.sin(self.angle) * speed
        else:
            self.velx = -math.sin(math.pi / 2 - self.angle) * speed
            self.vely = -math.sin(self.angle) * speed

    def update(self):
        self.comprect[0] += self.velx
        self.comprect[1] += self.vely
        self.rect.x = self.comprect[0] - self.game.offset[0]
        self.rect.y = self.comprect[1] - self.game.offset[1]
        if not 0 < self.comprect[0] < 2400 or not 0 < self.comprect[1] < 2400:
            self.kill()
        if self.game.ticks % 3 == 0:
            for t in self.game.town.buildings:
                if self.rect.colliderect(t.rect) and self.speed < 4:
                    self.kill()

    def change_course(self, velx, vely):
        self.velx = velx
        self.vely = vely

    def draw(self):
        self.game.screen.blit(self.image, self.rect)


class WeirdArrow(Arrow):
    def __init__(self, source, target, speed, image=None, height_offset=0):
        super().__init__(source, target, speed, image, height_offset)
        self.comprect = [source.comprect[0] + 20, source.comprect[1] - height_offset + 20]
        self.rect = pygame.Rect(self.comprect[0] - source.game.offset[0], self.comprect[1] - source.game.offset[1], 16,
                                16)

        if random.randint(0, 100) < 51:
            try:
                self.angle = math.degrees(math.atan(
                    (target.comprect[1] - self.source.comprect[1]) / (target.comprect[0] - self.source.comprect[0])))
            except ZeroDivisionError:
                if target.comprect[1] < self.comprect[1]:
                    self.angle = 90
                else:
                    self.angle = 0
        else:
            self.angle = random.randint(-3141, 3142) / 1000

        self.velx = math.sin(90 - self.angle) * speed
        self.vely = math.sin(self.angle) * speed


class EnergyBar:
    def __init__(self, game):
        self.game = game
        self.image = pygame.Surface((98, 8))
        self.bk = pygame.Surface((100, 10))

    def update(self):
        self.image = pygame.Surface((int(98 * (self.game.player.energy / 70)), 8))
        if self.game.player.energy < 10:
            self.image.fill((50, 50, 50))
        elif self.game.player.energy < 95:
            self.image.fill((20, 20, 200))
        else:
            self.image.fill((0, 15, 255))

    def draw(self):
        self.game.screen.blit(self.bk, (8, 8))
        self.game.screen.blit(self.image, (9, 9))


class HealthBar:
    def __init__(self, game):
        self.game = game
        self.image = pygame.Surface((98, 8))
        self.bk = pygame.Surface((100, 10))

    def update(self):
        self.image = pygame.Surface((int(98 * (self.game.player.hp / 100)), 8))
        if self.game.player.hp < 34:
            self.image.fill((200, 50, 50))
        elif self.game.player.hp < 67:
            self.image.fill((150, 150, 50))
        else:
            self.image.fill((10, 255, 50))

        if self.game.player.invincibility % 3 == 1:
            self.image.fill((255, 255, 255))

    def draw(self):
        self.game.screen.blit(self.bk, (8, 20))
        self.game.screen.blit(self.image, (9, 21))


class Tree:
    def __init__(self, game, size, position, image=None, color=(50, 170, 10)):
        self.game = game
        self.image = pygame.Surface(size)
        self.image.fill(color)
        self.size = size
        self.comprect = position
        self.rect = pygame.Rect((self.comprect[0] - self.game.offset[0], self.comprect[1] - self.game.offset[1]) , size)

    def update(self):
        self.rect.x = self.comprect[0] - self.game.offset[0]
        self.rect.y = self.comprect[1] - self.game.offset[1]


class Forest:
    def __init__(self, game):
        self.game = game
        self.derivative = []
        self.buildings = []

        for _ in range(0, random.randint(18, 43)):
            self.buildings.append(Tree(self.game, [40, random.randint(50, 90)], [random.randint(200, 2100), random.randint(200, 2100)]))

    def update(self):
        for b in self.buildings:
            b.update()

    def draw(self):
        for b in self.buildings:
            self.game.screen.blit(b.image, b.rect)


class Game:
    def __init__(self):
        pygame.init()

        self.screen = pygame.display.set_mode(RESOLUTION)
        self.spawn = [350, 350]
        self.offset = [0, 0]

        self.town = Forest(self)
        self.player = Player(self)
        self.chaser = Chaser(self)
        self.telechaser = Chaser(self, True)
        self.archer = Archer(self)
        self.crazyarcher = SprayArcher(self)
        self.vortal = Vortal(self)
        self.vortal2 = Vortal(self)
        self.trapper = Trapper(self)
        self.ground = pygame.Surface((2400, 2400))
        for j in range(0, 120):
            for i in range(0, 120):
                temp_tile = pygame.Surface((20, 20))
                # temp_tile.fill(random.choice([(0, 0, 200), (0, 20, 150), (20, 20, 150), (10, 0, 200), (0, 0, 200)]))
                temp_tile.fill(random.choice([(0, 200, 0), (0, 150, 20), (20, 150, 20), (10, 200, 0), (0, 200, 0)]))
                self.ground.blit(temp_tile, (i * 20, j * 20))

        self.clock = pygame.time.Clock()
        self.ticks = 0

        self.ebar = EnergyBar(self)
        self.hbar = HealthBar(self)

    def exist(self):
        while True:
            self.town.update()
            self.player.update()
            self.chaser.update()
            self.telechaser.update()
            self.archer.update()
            self.crazyarcher.update()
            self.vortal.update()
            self.vortal2.update()
            self.trapper.update()
            print('')

            self.clock.tick(100)
            self.ticks = pygame.time.get_ticks()
            self.ebar.update()
            self.hbar.update()

            self.screen.blit(self.ground, (-self.offset[0], -self.offset[1]))
            self.player.draw()
            self.chaser.draw()
            self.telechaser.draw()
            self.archer.draw()
            self.crazyarcher.draw()
            self.trapper.draw()
            self.vortal.draw()
            self.vortal2.draw()
            self.town.draw()

            self.ebar.draw()
            self.hbar.draw()

            pygame.display.set_caption(str(self.clock.get_fps()))
            pygame.display.flip()


g = Game()
g.exist()
