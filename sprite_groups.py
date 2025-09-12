import pygame


all_sprites = pygame.sprite.Group()
horizontal_borders = pygame.sprite.Group()
vertical_borders = pygame.sprite.Group()
hero_sprite = pygame.sprite.Group()
floor_sprites = pygame.sprite.Group()
item_group = pygame.sprite.Group()
enemu_bullets = pygame.sprite.Group()
hero_bullets = pygame.sprite.Group()
enemus = pygame.sprite.Group()
death = pygame.sprite.Group()
item_list = []
wep_list = []
entity_list = []
enemy_list = []
spawn = []
rooms = []
KILLS = 0


def clear():
    for i in horizontal_borders:
        i.kill()
    for i in vertical_borders:
        i.kill()
    for i in floor_sprites:
        i.kill()
    for i in item_group:
        i.kill()
    for i in enemu_bullets:
        i.kill()
    for i in hero_bullets:
        i.kill()
    for i in enemus:
        i.kill()
    for i in death:
        i.kill()
    item_list.clear()
    wep_list.clear()
    entity_list.clear()
    enemy_list.clear()
    spawn.clear()