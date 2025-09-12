import random
import time
import pygame
import pytmx
# from win32api import GetSystemMetrics

from start_scr import records, start_screen
from end_scr import end_screen
from Weapon import Weapon
from only_hero import Hero, Spawner, Door
from sprite_groups import all_sprites, horizontal_borders, vertical_borders, hero_sprite, floor_sprites, item_group, \
    enemu_bullets, hero_bullets, death, enemus, entity_list, item_list, wep_list, enemy_list, spawn, rooms, clear, KILLS

WIND_SIZE = WIND_WIDTH, WIND_HEIGHT = 1500, 900
# GetSystemMetrics(0), GetSystemMetrics(1) - 60
FPS = 80

MAPS_DIR = 'тайлы'


class Border(pygame.sprite.Sprite):
    def __init__(self, x1, y1, x2, y2):
        super().__init__(all_sprites)
        if x1 == x2:
            self.add(vertical_borders)
            self.image = pygame.Surface([1, y2 - y1])
            self.rect = pygame.Rect(x1, y1, 1, y2 - y1)
        else:
            self.add(horizontal_borders)
            self.image = pygame.Surface([x2 - x1, 1])
            self.rect = pygame.Rect(x1, y1, x2 - x1, 1)


class Floor(pygame.sprite.Sprite):
    def __init__(self, x, y, size):
        super().__init__(all_sprites, floor_sprites)
        self.rect = pygame.Rect(x, y, size, size)


class Room:
    def __init__(self, filename):
        global TILE_SIZE, K_HEIGHT, K_WIDTH
        self.map = pytmx.load_pygame(f"{MAPS_DIR}/{filename}")
        K_HEIGHT = self.height = self.map.height
        K_WIDTH = self.width = self.map.width
        TILE_SIZE = self.tile_size = self.map.tilewidth
        self.fset = ((WIND_WIDTH - self.width * self.tile_size) // 2, (WIND_HEIGHT - self.height * self.tile_size) // 2)

    def creating_sprites(self):
        for y in range(self.height):
            for x in range(self.width):
                a = self.get_tile_id((x, y))
                if a == 0:
                    Border(x * self.tile_size + self.fset[0], y * self.tile_size + self.fset[1],
                           (1 + x) * self.tile_size + self.fset[0], y * self.tile_size + self.fset[1])
                    Border(x * self.tile_size + self.fset[0], y * self.tile_size + self.fset[1],
                           x * self.tile_size + self.fset[0], (1 + y) * self.tile_size + self.fset[1])
                if a == 1:
                    Border(x * self.tile_size + self.fset[0], y * self.tile_size + self.fset[1],
                           (1 + x) * self.tile_size + self.fset[0], y * self.tile_size + self.fset[1])
                if a == 2:
                    Border(x * self.tile_size + self.fset[0], y * self.tile_size + self.fset[1],
                           (1 + x) * self.tile_size + self.fset[0], y * self.tile_size + self.fset[1])
                    Border((1 + x) * self.tile_size + self.fset[0], y * self.tile_size + self.fset[1],
                           (x + 1) * self.tile_size + self.fset[0], (1 + y) * self.tile_size + self.fset[1])
                if a == 6:
                    Border(x * self.tile_size + self.fset[0], y * self.tile_size + self.fset[1],
                           x * self.tile_size + self.fset[0], (1 + y) * self.tile_size + self.fset[1])
                if a == 8:
                    Border((1 + x) * self.tile_size + self.fset[0], y * self.tile_size + self.fset[1],
                           (x + 1) * self.tile_size + self.fset[0], (1 + y) * self.tile_size + self.fset[1])
                if a == 12:
                    Border(x * self.tile_size + self.fset[0], (1 + y) * self.tile_size + self.fset[1],
                           (1 + x) * self.tile_size + self.fset[0], (1 + y) * self.tile_size + self.fset[1])
                    Border(x * self.tile_size + self.fset[0], y * self.tile_size + self.fset[1],
                           x * self.tile_size + self.fset[0], (1 + y) * self.tile_size + self.fset[1])
                if a == 13:
                    Border(x * self.tile_size + self.fset[0], (1 + y) * self.tile_size + self.fset[1]
                           , (1 + x) * self.tile_size + self.fset[0], (1 + y) * self.tile_size + self.fset[1])
                if a == 14:
                    Border(x * self.tile_size + self.fset[0], (1 + y) * self.tile_size + self.fset[1],
                           (1 + x) * self.tile_size + self.fset[0], (1 + y) * self.tile_size + self.fset[1])
                    Border((1 + x) * self.tile_size + self.fset[0], y * self.tile_size + self.fset[1],
                           (1 + x) * self.tile_size + self.fset[0], (1 + y) * self.tile_size + self.fset[1])
                if a in (3, 4, 5, 9, 10, 11, 15, 16, 17, 18, 21, 22, 23, 7, 27, 28, 29):
                    Floor(x * self.tile_size + self.fset[0], y * self.tile_size + self.fset[1], self.tile_size)

    def render(self, screen):
        for y in range(self.height):
            for x in range(self.width):
                image = self.map.get_tile_image(x, y, 0)
                screen.blit(image, (x * self.tile_size + self.fset[0],
                                    y * self.tile_size + self.fset[1]))

    def get_tile_id(self, pos):
        return self.map.tiledgidmap[self.map.get_tile_gid(*pos, 0)] - 1


def spawn_vawe():
    for i in range(random.randint(3, 5)):
        a = Spawner((random.randint(0, WIND_WIDTH), random.randint(0, WIND_HEIGHT)), 2000)
        while not pygame.sprite.spritecollideany(a, floor_sprites) or \
                pygame.sprite.spritecollideany(a, vertical_borders) or \
                pygame.sprite.spritecollideany(a, horizontal_borders):
            a.kill()
            a = Spawner((random.randint(0, WIND_WIDTH), random.randint(0, WIND_HEIGHT)), 2000)
        spawn.append(a)


def door():
    a = Door((random.randint(0, WIND_WIDTH), random.randint(0, WIND_HEIGHT // 2)))
    while not pygame.sprite.spritecollideany(a, floor_sprites) or \
            pygame.sprite.spritecollideany(a, vertical_borders) or \
            pygame.sprite.spritecollideany(a, horizontal_borders) or \
            pygame.sprite.spritecollideany(a, hero_sprite):
        # or pygame.sprite.spritecollideany(a, entity_list)
        a.kill()
        a = Door((random.randint(0, WIND_WIDTH), random.randint(0, WIND_HEIGHT // 2)))
    return a


def main():
    global rooms, KILLS
    pygame.init()
    screen = pygame.display.set_mode(WIND_SIZE)
    rooms += [Room('1.tmx'), Room('2.tmx'), Room('3.tmx'), Room('4.tmx'), Room('5.tmx')]
    running = True
    new_game = False
    shooot = False
    clock = pygame.time.Clock()
    delta_time = 0
    d = Door((-1000, -1000))
    mouse_pos = (0, 0)  # чтоб работало
    NAME = start_screen()

    room = Room('start.tmx')  # чтоб была первая комнота
    room.creating_sprites()
    hero = Hero(screen, 150, (900, 500), 10, 'jo1.png', 0, True, all_sprites, hero_sprite)
    wep = Weapon(600, 500, 'gun.png', 'H_bullet.png', entity_list)
    wep_list.append(wep)
    vawes = 0
    while running:  # цикл перехода между комнотами
        while not d.perehod and running:  # цикл комнаты
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.KEYDOWN:
                    key = pygame.key.get_pressed()
                    hero.vector_update(key)
                if event.type == pygame.KEYUP:
                    key = pygame.key.get_pressed()
                    hero.vector_update(key)
                if event.type == pygame.MOUSEMOTION:
                    mouse_pos = event.pos
                if event.type == pygame.MOUSEBUTTONUP:
                    shooot = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    shooot = True
                if event.type == pygame.KEYUP and event.key == pygame.K_e:
                    for i in wep_list:
                        hero.equip(i)
                    d.come(hero.pos)
            hero.move()
            if shooot:
                hero.shoot(hero_bullets)
            # collision
            if len(pygame.sprite.spritecollide(hero, horizontal_borders, False, pygame.sprite.collide_rect)) == 0:
                hero.last_pos_y = hero.pos[1]
            else:
                hero.set_pos(hero.pos[0], hero.last_pos_y)
            if len(pygame.sprite.spritecollide(hero, vertical_borders, False, pygame.sprite.collide_rect)) == 0:
                hero.last_pos_x = hero.pos[0]
            else:
                hero.set_pos(hero.last_pos_x, hero.pos[1])
            for i in item_list:
                if len(pygame.sprite.spritecollide(i, hero_sprite, False, pygame.sprite.collide_rect)) != 0:
                    i.hero_col(hero)
                    item_list.remove(i)

            for i in enemy_list:
                s = pygame.sprite.Group()
                s.add(i)
                if len(pygame.sprite.spritecollide(hero, s, False, pygame.sprite.collide_rect)) != 0:
                    hero.damaged(1)
                    i.stop(750)

            for i in entity_list:
                KILLS = i.move(hero, KILLS)

            for i in enemy_list:
                i.creating_vector((hero.rect.x, hero.rect.y))
                i.move()
            for i in spawn:
                i.spawn()
            if not enemy_list and not spawn and vawes > 0:
                spawn_vawe()
                vawes -= 1
            if not enemy_list and not spawn and vawes == 0:
                vawes -= 1
                d = door()
            d.open(hero.pos)
            # переход на другую локу
            screen.fill((8, 10, 10))
            room.render(screen)
            death.draw(screen)
            item_group.draw(screen)
            enemu_bullets.draw(screen)
            hero_bullets.draw(screen)
            enemus.draw(screen)
            hero.img_update(mouse_pos)
            hero_sprite.draw(screen)
            hero.draw_hearts()
            pygame.display.flip()
            clock.tick(FPS)

            if not hero.vul:
                pygame.time.delay(2000)
                new_game = True
                t = pygame.time.get_ticks() // 1000
                # print(KILLS)
                NAME = end_screen(NAME, t - delta_time, hero.mon, KILLS)
                delta_time = t
                KILLS = 0
                rooms = []
                clear()
                room = Room('start.tmx')  # чтоб была первая комнота
                rooms += [Room('1.tmx'), Room('2.tmx'), Room('3.tmx'), Room('4.tmx'), Room('5.tmx')]
                room.creating_sprites()
                hero = Hero(screen, 150, (900, 500), 10, 'jo1.png', 0, True, all_sprites, hero_sprite)
                wep = Weapon(600, 500, 'gun.png', 'H_bullet.png', entity_list)
                wep_list.append(wep)
                vawes = 0
                break

        if not new_game:
            clear()
            room = random.choice(rooms)
            room.creating_sprites()
            vawes = random.randint(2, 5)
            hero.pos = ((random.randint(WIND_WIDTH // 2 - 150, WIND_WIDTH // 2 + 150),
                         random.randint(WIND_HEIGHT // 2 - 150, WIND_HEIGHT // 2 + 150)))
            d = Door((-1000, -1000))
            screen.fill((8, 10, 10))
            pygame.display.flip()
            shooot = False
            d = Door((-1000, -1000))
        else:
            new_game = False
        if running:
            time.sleep(2)


main()
