import pygame
import pytmx

WIND_SIZE = WIND_HEIGHT, WIND_WIDTH = 1600, 900
FPS = 60
MAPS_DIR = 'тайлы'
TILE_SIZE = 64


class Room:
    def __init__(self, filename):
        self.map = pytmx.load_pygame(f"{MAPS_DIR}/{filename}")
        self.height = self.map.height
        self.width = self.map.width
        self.tile_size = self.map.tilewidth

    def render(self, screen, pos):
        for y in range(self.height):
            for x in range(self.width):
                image = self.map.get_tile_image(x, y, 0)
                screen.blit(image, (x * self.tile_size - pos[0], y * self.tile_size - pos[1]))

    def get_tile_id(self, pos):
        return self.map.tiledgidmap[self.map.get_tile_gid(*pos, 0)] - 1


def main():
    pygame.init()
    screen = pygame.display.set_mode(WIND_SIZE)

    room = Room('1.tmx')
    pos = [0, 0]

    clock = pygame.time.Clock()
    running = True
    gameover = False

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:

                if event.key == 119:
                    pos[1] -= 10
                elif event.key == 100:
                    pos[0] += 10
                elif event.key == 115:
                    pos[1] += 10
                elif event.key == 97:
                    pos[0] -= 10
        screen.fill((8, 10, 10))
        room.render(screen, pos)
        pygame.draw.circle(screen, (255, 0, 0), (800, 450), 5)
        pygame.display.flip()
        clock.tick(FPS)


main()
