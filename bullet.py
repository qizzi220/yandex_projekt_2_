from random import randint

import pygame
import math

W_SIZE = 500, 350


class Bullet:
    def __init__(self, pos, color=pygame.Color('white'), speed=10, vector=math.pi * 3 / 4, radius=10, rico=9999):
        self.speed = speed
        self.rico = rico
        self.pos = pos
        self.vect = [math.cos(vector), math.sin(vector)]
        self.radius = radius
        self.color = color

    def move(self):
        self.pos = (self.pos[0] + int(self.vect[0] * 4), self.pos[1] - int(self.vect[1] * 4))
        self.board_out()

    def board_out(self):
        if self.pos[0] - self.radius < 0:
            self.pos = (self.radius, self.pos[1])
            self.vect[0] *= -1
        elif self.pos[0] + self.radius > W_SIZE[0]:
            self.pos = (W_SIZE[0] - self.radius, self.pos[1])
            self.vect[0] *= -1
        if self.pos[1] - self.radius < 0:
            self.pos = (self.pos[0], self.radius)
            self.vect[1] *= -1
        elif self.pos[1] + self.radius > W_SIZE[1]:
            self.pos = (self.pos[0], W_SIZE[1] - self.radius)
            self.vect[1] *= -1


def moves():
    for i in bullets:
        i.move()


def render(scr):
    scr.fill((0, 0, 0))
    for i in bullets:
        pygame.draw.circle(scr, i.color, i.pos, i.radius, 0)
    pygame.display.update()


pygame.init()
pygame.display.set_caption('Шарики')
running = True
screen = pygame.display.set_mode(W_SIZE)
bullets = []
clock = pygame.time.Clock()
while running:
    for event in pygame.event.get():
        if event.type == pygame.MOUSEBUTTONUP:
            color = [randint(0, 255), randint(0, 255), randint(0, 255)]
            bullets.append(Bullet(event.pos, color, math.pi))
        if event.type == pygame.QUIT:
            running = False
    moves()
    render(screen)
    clock.tick(60)