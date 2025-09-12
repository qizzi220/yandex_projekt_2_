import os
import sys
import pygame
import math
from sprite_groups import all_sprites, horizontal_borders, vertical_borders, hero_sprite, floor_sprites, item_group, \
    hero_bullets, enemu_bullets, death, entity_list, enemy_list


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
    def __init__(self, pos, spr, speed=2, vector=math.pi * 3 / 4, rico=1, damage=2):
        self.speed = speed
        self.damage = damage
        self.rico = rico
        self.pos = pos[0] - 12, pos[1] - 12
        self.vect = [math.cos(vector) * speed, math.sin(vector) * speed]
        self.spr = spr
        self.spr.rect.x, self.spr.rect.y = self.pos

    def move(self, hero, KILLS):
        self.pos = (self.pos[0] + self.vect[0] * self.speed, self.pos[1] - self.vect[1] * self.speed)
        self.spr.rect.x, self.spr.rect.y = int(self.pos[0]), int(self.pos[1])
        if len(pygame.sprite.spritecollide(self.spr, vertical_borders, False, pygame.sprite.collide_rect)) != 0:
            if self.rico > 0:
                self.rico -= 1
                self.vect[0] = -self.vect[0]
            else:
                self.spr.kill()
                if self in entity_list:
                    entity_list.remove(self)
        if len(pygame.sprite.spritecollide(self.spr, horizontal_borders, False, pygame.sprite.collide_rect)) != 0:
            if self.rico > 0:
                self.rico -= 1
                self.vect[1] = -self.vect[1]
            else:
                self.spr.kill()
                if self in entity_list:
                    entity_list.remove(self)
        if len(pygame.sprite.spritecollide(self.spr, floor_sprites, False, pygame.sprite.collide_rect)) <= 0:
            self.spr.kill()
            if self in entity_list:
                entity_list.remove(self)
        if self.spr in hero_bullets:
            for i in enemy_list:
                s = pygame.sprite.Group()
                s.add(i)
                if len(pygame.sprite.spritecollide(self.spr, s, False, pygame.sprite.collide_rect)) != 0:
                    print('nne', KILLS)
                    KILLS = i.damaged(2, KILLS)
                    self.spr.kill()
                    if self in entity_list:
                        entity_list.remove(self)
        if self.spr in enemu_bullets:
            s = pygame.sprite.Group()
            s.add(hero)
            if len(pygame.sprite.spritecollide(self.spr, s, False, pygame.sprite.collide_rect)) != 0:
                hero.damaged(2)
                self.spr.kill()
                if self in entity_list:
                    entity_list.remove(self)
        return KILLS

class Weapon(pygame.sprite.Sprite):
    def __init__(self, x, y, sprite, shooting_im, entity_list): # + sprite
        super().__init__(item_group)
        self.mo = item_group
        self.pos = self.x, self.y = x, y
        self.image = load_image('gun.png', -1)
        self.image2 = pygame.transform.flip(self.image, True, False)
        self.new_image = load_image(sprite, -1)
        self.rect = self.new_image.get_rect().move((x, y))
        self.im = shooting_im
        self.entity_list = entity_list
        self.last = pygame.time.get_ticks()

    def shoot(self, group):
        now = pygame.time.get_ticks()
        if now - self.last > 400:
            self.last = pygame.time.get_ticks()
            bullet_sprite = pygame.sprite.Sprite()
            bullet_sprite.image = load_image(self.im, colorkey=-1)
            bullet_sprite.rect = bullet_sprite.image.get_rect()
            group.add(bullet_sprite)
            self.entity_list.append(Bullet(self.fier_point, bullet_sprite, vector=self.last_angle / 180 * math.pi, speed=3))

    def change_coords(self, coords):
        self.pos = self.x, self.y = self.rect.x, self.rect.y = coords[0], coords[1]

    def blitRotate(self, flag, scr, originPos, angle):
        if flag:
            self.last_angle = angle
            image_rect = self.image.get_rect(topleft=(self.pos[0] - originPos[0], self.pos[1] - originPos[1]))
            offset_center_to_pivot = pygame.math.Vector2(self.pos) - image_rect.center
            rotated_offset = offset_center_to_pivot.rotate(-angle)
            rotated_image_center = (self.pos[0] - rotated_offset.x, self.pos[1] - rotated_offset.y)
            self.new_image = pygame.transform.rotate(self.image, angle)
            self.rect = self.new_image.get_rect(center=rotated_image_center)
            scr.blit(self.new_image, self.rect)
            angle = angle + 15
            self.fier_point = self.pos[0] + int(50 * math.cos(angle / 180 * math.pi)), \
                         self.pos[1] - int(50 * math.sin(angle / 180 * math.pi))
        else:
            self.last_angle = angle + 180
            image_rect = self.image2.get_rect(topleft=(self.pos[0] - originPos[0], self.pos[1] - originPos[1]))
            offset_center_to_pivot = pygame.math.Vector2(self.pos) - image_rect.center
            rotated_offset = offset_center_to_pivot.rotate(-angle)
            rotated_image_center = (self.pos[0] - rotated_offset.x, self.pos[1] - rotated_offset.y)
            self.new_image = pygame.transform.rotate(self.image2, angle)
            self.rect = self.new_image.get_rect(center=rotated_image_center)
            scr.blit(self.new_image, self.rect)
            angle = angle - 15
            self.fier_point = self.pos[0] + int(- 50 * math.cos(angle / 180 * math.pi)), \
                              self.pos[1] - int(- 50 * math.sin(angle / 180 * math.pi))
