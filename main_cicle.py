from PIL import Image
import os
import sys
import pygame
import math


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

class Bullet:
    def __init__(self, pos, spr, speed=2, vector=math.pi * 3 / 4, rico=9999):
        self.speed = speed
        self.rico = rico
        self.pos = pos
        self.vect = [math.cos(vector) * speed, math.sin(vector) * speed]
        self.spr = spr
        self.spr.rect.x = pos[0]
        self.spr.rect.y = pos[1]

    def move(self):
        self.pos = (self.pos[0] + int(self.vect[0] * 4), self.pos[1] - int(self.vect[1] * 4))
        self.spr.rect.x, self.spr.rect.y = self.pos


class Weapon:
    def __init__(self, x, y, sprite, shooting_im): # + sprite
        self.x, self.y = x, y
        self.spr = sprite
        self.spr.rect.x = x
        self.spr.rect.y = y
        self.im = shooting_im


    def shoot(self, coords, mouse):
        global entity_list, all_sprites
        bullet_sprite = pygame.sprite.Sprite()
        bullet_sprite.image = load_image(self.im, colorkey=-1)
        bullet_sprite.rect = bullet_sprite.image.get_rect()
        all_sprites.add(bullet_sprite)

        delta = (mouse[0] - coords[0], mouse[1] - coords[1])
        cos = delta[1] / math.sqrt(delta[1]**2 + delta[0]**2)
        if delta[0] < 0:
            vec = math.asin(cos) + math.pi
        else:
            vec = math.asin(cos) * -1

        entity_list.append(Bullet(coords, bullet_sprite, vector=vec, speed=2))

    def change_coords(self, coords):
        x, y = coords[0], coords[1]
        self.spr.rect.x, self.spr.rect.y = x + 25, y + 30


class Entity:
    def __init__(self, max_health, sprite, armed=[]): # + sprite
        self.armed = armed
        self.max_health, self.health = max_health, max_health
        self.spr = sprite
        self.V = [0, 0]  # y x

    def equip(self, gun):
        x_e, y_e = self.spr.rect.x, self.spr.rect.y
        x_g, y_g = gun.spr.rect.x, gun.spr.rect.y
        delta = (abs(x_e - x_g + 5), abs(y_e - y_g + 10))
        print(delta)
        if delta[0] < 30 and delta[1] < 30:
            self.armed.append(gun)

    def shoot(self, coords, mouse):
        if self.armed:
            self.armed[0].shoot(coords, mouse)

    def move(self):
        global t, screen
        screen.fill((0, 0, 0))
        x = self.spr.rect.x
        y = self.spr.rect.y
        x_pos, y_pos = (x + self.V[1] * t / 100), (y + self.V[0] * t / 100)
        self.spr.rect.x, self.spr.rect.y = x_pos, y_pos
        if self.armed:
            self.armed[0].change_coords((x_pos, y_pos))

    def change_v(self, yv, xv):
        if yv and not xv:
            self.V = [yv[0], self.V[1]]
        elif xv and not yv:
            self.V = [self.V[0], xv[0]]

    def get_v(self):
        return self.V

    def get_coords(self):
        return self.spr.rect.y, self.spr.rect.x

class Hero(Entity):
    pass



if __name__ == '__main__':
    pygame.init()
    pygame.display.set_caption('игра')
    size = width, height = 400, 400
    screen = pygame.display.set_mode(size)
    fps = 60
    clock = pygame.time.Clock()
    f = False

    entity_list = []
    all_sprites = pygame.sprite.Group()
    hero_sprite = pygame.sprite.Sprite()
    gun_sprite = pygame.sprite.Sprite()

    hero_sprite.image = load_image("hero.png", colorkey=-1)
    gun_sprite.image = load_image('tomato_gun.png', colorkey=-1)

    hero_sprite.rect = hero_sprite.image.get_rect()
    gun_sprite.rect = gun_sprite.image.get_rect()

    hero_sprite.rect.x = 5
    hero_sprite.rect.y = 20

    all_sprites.add(hero_sprite)
    all_sprites.add(gun_sprite)
    all_sprites.draw(screen)

    wep = Weapon(50, 50, gun_sprite, 'tomato_bullet.png')
    hero = Hero(20, hero_sprite)
    wep_list = [wep]
    entity_list.append(hero)

    running = True
    while running:
        pygame.display.flip()
        t = clock.tick()
        for i in entity_list:
            i.move()
        clock.tick(fps)
        all_sprites.draw(screen)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.KEYDOWN and event.key == pygame.K_w:
                hero.change_v([-500], [])
            if event.type == pygame.KEYUP and event.key == pygame.K_w:
                hero.change_v([0], [])

            if event.type == pygame.KEYDOWN and event.key == pygame.K_s:
                hero.change_v([500], [])
            if event.type == pygame.KEYUP and event.key == pygame.K_s:
                hero.change_v([0], [])

            if event.type == pygame.KEYDOWN and event.key == pygame.K_a:
                hero.change_v([], [-500])
            if event.type == pygame.KEYUP and event.key == pygame.K_a:
                hero.change_v([], [0])

            if event.type == pygame.KEYDOWN and event.key == pygame.K_d:
                hero.change_v([], [500])
            if event.type == pygame.KEYUP and event.key == pygame.K_d:
                hero.change_v([], [0])
            if event.type == pygame.MOUSEBUTTONDOWN:
                y, x = hero.get_coords()
                hero.shoot((x + 10, y + 20), event.pos)
            if event.type == pygame.MOUSEBUTTONUP:
                f = False
            if event.type == pygame.KEYUP and event.key == pygame.K_e:
                for i in wep_list:
                    hero.equip(i)

    pygame.quit()

# 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
# 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
 # $ git config --global user.email 'mail@yourmail.ru'