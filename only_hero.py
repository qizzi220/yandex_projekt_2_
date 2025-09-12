import os
import random
import sys
import pygame
import math
from Weapon import Bullet
from Items import Heart_item, Money_item
from sprite_groups import all_sprites, horizontal_borders, vertical_borders, hero_sprite, floor_sprites, item_group, \
    enemu_bullets, hero_bullets, death, enemus, entity_list, enemy_list, wep_list, item_list, spawn, clear, KILLS

FPS = 60


def ygol(vect):
    ax, ay = 1, 0
    bx, by = vect
    ma = math.sqrt(ax * ax + ay * ay)
    mb = math.sqrt(bx * bx + by * by) + 0.0001
    sc = ax * bx + ay * (-by)
    res = math.acos(sc / ma / mb) * 180 / math.pi
    if -by <= 0:
        res = 360 - res
    return res, bx >= 0


def load_image(name, colorkey=None):
    fullname = os.path.join('images', name)
    # если файл не существует, то выходим
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    if colorkey is not None:
        image = image.convert()
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    else:
        image = image.convert_alpha()
    return image


class Entity(pygame.sprite.Sprite):
    def __init__(self, speed, pos, health, image, vulnerability=True, *groups):
        super().__init__(*groups)  # спрайт группы
        self.health = health
        self.speed = speed
        self.pos = pos
        self.vul = vulnerability
        self.image = load_image(image, -1)
        self.rect = self.image.get_rect().move(pos)
        self.vect = -1  # вектор передвижения (синус и косинус для скорости по x и y, -1 значит что вектора нет)
        self.s = [0, 1, 2] # для генерации предметов

    def move(self):
        if self.vect != -1:
            vx = math.cos(self.vect) * self.speed
            vy = math.sin(self.vect) * self.speed
            self.pos = self.pos[0] + int(vx / FPS), self.pos[1] - int(vy / FPS)
            self.rect.move_ip(int(vx / FPS), -int(vy / FPS))

    def set_pos(self, x, y):
        self.rect.x, self.rect.y = x, y
        self.pos = x, y

    def damaged(self, damage, KILLS):
        if self.vul:
            self.health -= damage
            if self.health <= 0:
                KILLS += 1
                e = random.choice(self.s)
                print(KILLS)
                if e == 0:
                    a = Money_item((self.pos[0] + 18, self.pos[1] + 30), item_group)
                    item_list.append(a)
                if e == 1:
                    a = Heart_item((self.pos[0] + 10, self.pos[1] + 20), item_group)
                    item_list.append(a)
                self.kill()  # убит
                if self in enemy_list:
                    enemy_list.remove(self)
                # TODO дорисовать смэрт
        return KILLS


class Hero(Entity):
    def __init__(self, screen, speed, pos, health, image, money=0, vulnerability=True, *groups):
        super().__init__(speed, pos, health, image, vulnerability, *groups)
        self.hearts_points = int(self.health / 2)
        self.hearts = [load_image('heart1.png', -1), load_image('heart0.5.png', -1), load_image('heart0.png', -1),
                       load_image('money.png', -1)]
        self.last_pos_y = 0
        self.last_pos_x = 0
        self.armed = []
        self.screen = screen
        self.mon = money
        self.jo = [load_image('jo1.png', -1), load_image('jo2.png', -1), load_image('jo3.png', -1),
                   load_image('jo4.png', -1), load_image('jo5.png', -1), load_image('jo6.png', -1)]
        self.img_update([500, 500])
        self.last_damage = pygame.time.get_ticks()

    def img_update(self, mpos):
        pos = (self.pos[0] + 24, self.pos[1] + 48)
        x = mpos[0] - pos[0]
        y = mpos[1] - pos[1]
        gip = (x ** 2 + y ** 2) ** (1 / 2)
        if not gip:
            gip = 0.0001
        si = y / gip
        co = x / gip
        if 0.5 <= co <= 1:
            if si <= 0:
                self.image = self.jo[2]
            else:
                self.image = self.jo[1]
        elif -0.5 >= co >= -1:
            if si <= 0:
                self.image = self.jo[4]
            else:
                self.image = self.jo[5]
        else:
            if si <= 0:
                self.image = self.jo[3]
            else:
                self.image = self.jo[0]
        self.rect = self.image.get_rect().move(self.pos)
        if self.armed:
            i, left_right = ygol((mpos[0] - pos[0], mpos[1] - pos[1]))
            if left_right:
                self.armed[0].blitRotate(left_right, self.screen, (7, 20), i)
                self.armed[0].change_coords((self.pos[0] + 40, self.pos[1] + 70))
            else:
                self.armed[0].blitRotate(left_right, self.screen, (41, 20), i - 180)
                self.armed[0].change_coords((self.pos[0] + 6, self.pos[1] + 70))

    def vector_update(self, keys):
        self.vect = -1
        if keys[pygame.K_w]:
            self.vect = 0.5 * math.pi
        if keys[pygame.K_a]:
            self.vect = 1 * math.pi
        if keys[pygame.K_d]:
            self.vect = 0 * math.pi
        if keys[pygame.K_s]:
            self.vect = 1.5 * math.pi
        if keys[pygame.K_w] and keys[pygame.K_d]:
            self.vect = 0.25 * math.pi
        if keys[pygame.K_w] and keys[pygame.K_a]:
            self.vect = 0.75 * math.pi
        if keys[pygame.K_s] and keys[pygame.K_a]:
            self.vect = 1.25 * math.pi
        if keys[pygame.K_s] and keys[pygame.K_d]:
            self.vect = 1.75 * math.pi

        if keys[pygame.K_v]:
            self.damaged(1)

    def damaged(self, damage):
        now = pygame.time.get_ticks()
        if self.vul and now - self.last_damage >= 500:
            self.health -= 1
            if self.health <= 0:
                self.kill()  # убит
                img = load_image('jorik.png', -1)
                sp = pygame.sprite.Sprite()
                sp.image = img
                sp.rect = sp.image.get_rect().move((self.pos[0], self.pos[1] + 48))
                death.add(sp)
                self.armed.clear()
                self.vul = False
            self.last_damage = pygame.time.get_ticks()

    def equip(self, gun):
        x_e, y_e = self.rect.x + 24, self.rect.y + 48
        x_g, y_g = gun.rect.x + 20, gun.rect.y + 9
        delta = ((x_e - x_g) ** 2 + (y_e - y_g) ** 2) ** 0.5
        if delta < 60:
            self.armed.append(gun)
            gun.kill()

    def shoot(self, gr):
        if self.armed:
            self.armed[0].shoot(gr)

    def draw_hearts(self):
        h = self.health
        for i in range(self.hearts_points):
            if h - i * 2 >= 2:
                self.screen.blit(self.hearts[0], (25 + i * 35, 25))
            elif h - i * 2 == 1:
                self.screen.blit(self.hearts[1], (25 + i * 35, 25))
            elif h - i * 2 <= 0:
                self.screen.blit(self.hearts[2], (25 + i * 35, 25))
        # рисовка МОНЕТОК
        self.screen.blit(self.hearts[3], (25, 65))
        font = pygame.font.Font(None, 40)
        text = font.render(str(self.mon), True, (255, 255, 255))
        text_x = 65
        text_y = 65
        self.screen.blit(text, (text_x, text_y))

    def move(self):
        if self.vect != -1:
            vx = math.cos(self.vect) * self.speed
            vy = math.sin(self.vect) * self.speed
            self.pos = self.pos[0] + vx / FPS, self.pos[1] - vy / FPS
            self.rect.x, self.rect.y = self.pos[0], self.pos[1]


class Enemy(Entity):  # Максим
    def __init__(self, speed, pos, health, image):
        super().__init__(speed, pos, health, image, True, enemus, all_sprites)
        self.images = [load_image('slime1.png', -1), load_image('slime2.png', -1),
                       load_image('slime3.png', -1), load_image('slime4.png', -1), load_image('slimeD.png', -1)]
        self.images2 = [pygame.transform.flip(i, True, False) for i in self.images]
        self.framer = 0
        self.stoped = 0
        self.last_dmg = pygame.time.get_ticks() - 500

    def creating_vector(self, hero_pos):
        self.framer += 1
        f = self.framer // 20
        if f > 3:
            self.framer = 0
            f = 0
        delta = (hero_pos[0] - self.pos[0], hero_pos[1] + 48 - self.pos[1])
        sin = delta[1] / math.sqrt(delta[1] ** 2 + delta[0] ** 2)
        if delta[0] < 0:
            self.vect = math.asin(sin) + math.pi
            self.image = self.images2[f]
            if pygame.time.get_ticks() - self.last_dmg < 300:
                self.image = self.images2[4]
        else:
            self.vect = - math.asin(sin)
            self.image = self.images[f]
            if pygame.time.get_ticks() - self.last_dmg < 300:
                self.image = self.images[4]

    def move(self):
        now = pygame.time.get_ticks()
        if self.vect != -1 and now > self.stoped:
            vx = math.cos(self.vect) * self.speed
            vy = math.sin(self.vect) * self.speed
            self.pos = self.pos[0] + vx / FPS, self.pos[1] - vy / FPS
            self.rect.x, self.rect.y = int(self.pos[0]), int(self.pos[1])

    def stop(self, time):
        self.stoped = pygame.time.get_ticks() + time

    def damaged(self, damage, KILLS):
        if self.vul:
            self.health -= damage
            self.stop(300)
            self.image = self.images[4]
            self.last_dmg = pygame.time.get_ticks()
            if self.health <= 0:
                KILLS += 1
                e = random.choice(self.s)
                if e == 0:
                    a = Money_item((self.pos[0] + 18, self.pos[1] + 30), item_group)
                    item_list.append(a)
                if e == 1:
                    a = Heart_item((self.pos[0] + 10, self.pos[1] + 20), item_group)
                    item_list.append(a)
                self.kill()  # убит
                if self in enemy_list:
                    enemy_list.remove(self)
        return KILLS
                # TODO дорисовать смэрт


class Shooting_enemy(Entity):  # Максим
    def __init__(self, speed, pos, health, image, shooting_im):
        super().__init__(speed, pos, health, image, True, all_sprites, enemus)  # спрайт группы
        self.vect = -1  # вектор передвижения (синус и косинус для скорости по x и y)
        self.last = pygame.time.get_ticks()
        self.images = [load_image('magikan1.png', -1), load_image('magikan2.png', -1),
                       load_image('magikan3.png', -1), load_image('magikan4.png', -1)]
        self.images2 = [pygame.transform.flip(i, True, False) for i in self.images]
        self.framer = 0
        self.shoot_im = shooting_im
        self.bull = load_image('bullet.png', colorkey=-1)
        self.stoped = 0

    def creating_vector(self, hero_pos):
        now = pygame.time.get_ticks()
        f = (now - self.last) // 500
        if f > 3:
            f = 3
        delta = (hero_pos[0] - self.pos[0], hero_pos[1] - self.pos[1])
        if delta[0] < 0:
            self.image = self.images2[f]
        else:
            self.image = self.images[f]
        if (delta[0] ** 2 + delta[1] ** 2) ** 0.5 > 400:
            sin = delta[1] / math.sqrt(delta[1] ** 2 + delta[0] ** 2)
            if delta[0] < 0:
                self.vect = math.asin(sin) + math.pi
            else:
                self.vect = math.asin(sin) * -1
        else:
            self.vect = -1
            if now - self.last >= 2500:
                self.shoot()
                self.last = pygame.time.get_ticks()
        self.rect = self.image.get_rect().move(*self.pos)

    def move(self):
        now = pygame.time.get_ticks()
        if self.vect != -1 and now > self.stoped:
            vx = math.cos(self.vect) * self.speed
            vy = math.sin(self.vect) * self.speed
            self.pos = self.pos[0] + vx / FPS, self.pos[1] - vy / FPS
            self.rect.x, self.rect.y = int(self.pos[0]), int(self.pos[1])

    def stop(self, time):
        self.stoped = pygame.time.get_ticks() + time

    def shoot(self):
        vec = math.pi * (1 / 6)
        n = random.random() * 2
        coords = (self.pos[0] + 52, self.pos[1] + 31)
        for i in range(12):
            bullet_sprite = pygame.sprite.Sprite()
            bullet_sprite.image = self.bull
            bullet_sprite.rect = bullet_sprite.image.get_rect()
            enemu_bullets.add(bullet_sprite)
            entity_list.append(Bullet(coords, bullet_sprite, vector=vec * i + n, speed=2, rico=0))


class Spawner(pygame.sprite.Sprite):
    def __init__(self, pos, time):
        super().__init__(death, all_sprites)  # спрайт группы
        self.pos = pos
        self.image = load_image('sp.png', -1)
        self.rect = self.image.get_rect().move(pos)
        self.time = time
        self.last = pygame.time.get_ticks()

    def spawn(self):
        if pygame.time.get_ticks() - self.last >= self.time:
            if random.randint(0, 1):
                e = Enemy(100, (self.pos[0] + 10, self.pos[1]), 20, 'slime1.png')
            else:
                e = Shooting_enemy(80, (self.pos[0] + 10, self.pos[1]), 14, 'magikan1.png', 'bullet.png')
            enemy_list.append(e)
            spawn.remove(self)
            self.kill()

class Door(pygame.sprite.Sprite):
    def __init__(self, pos):
        super().__init__(death, all_sprites)  # спрайт группы
        self.pos = pos
        self.images = [load_image('doora1.png', -1), load_image('doora2.png', -1), load_image('doora3.png', -1),
                       load_image('doora4.png', -1), load_image('doora5.png', -1)]
        self.image = self.images[0]
        self.rect = self.image.get_rect().move(pos)
        self.last = pygame.time.get_ticks()
        self.framer = 0
        self.f = True
        self.perehod = False

    def open(self, pos):
        posi = pos[0] + 24, pos[1] + 48
        if ((posi[0] - self.pos[0] - 50) ** 2 + (posi[1] - self.pos[1] - 100) ** 2) ** 0.5 <= 150:
            self.f = False
        else:
            self.f = True
        if not self.f:
            self.framer += 1
            f = self.framer // 20
            if f > 4:
                f = 4
                self.framer = 80
            self.image = self.images[f]
        else:
            self.framer -= 1
            f = self.framer // 20
            if f < 0:
                f = 0
                self.framer = 0
            self.image = self.images[f]

    def come(self, pos):
        posi = pos[0] + 24, pos[1] + 48
        if ((posi[0] - self.pos[0] - 50) ** 2 + (posi[1] - self.pos[1] - 100) ** 2) ** 0.5 <= 150:
            #переход в другую комнату
            self.perehod = True


