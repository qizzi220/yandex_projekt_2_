import os
import sys
import pygame


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


class Heart_item(pygame.sprite.Sprite):
    def __init__(self, pos, item_group):
        super().__init__(item_group)
        self.image = load_image('heart1.png', -1)
        self.rect = self.image.get_rect().move(pos)

    def hero_col(self, hero):
        hero.health += 2
        if hero.hearts_points * 2 < hero.health:
            hero.health = hero.hearts_points * 2
        self.kill()


class Money_item(pygame.sprite.Sprite):
    def __init__(self, pos, item_group):
        super().__init__(item_group)
        self.image = load_image('money.png', -1)
        self.rect = self.image.get_rect().move(pos)

    def hero_col(self, hero):
        hero.mon += 1
        self.kill()