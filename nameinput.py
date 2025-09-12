import pygame
from only_hero import load_image
import sys


pygame.init()
COLOR_INACTIVE = pygame.Color('lightskyblue3')
COLOR_ACTIVE = pygame.Color('dodgerblue2')
FONT = pygame.font.Font(None, 32)
WIND_SIZE = WIND_WIDTH, WIND_HEIGHT = 1500, 900
screen = pygame.display.set_mode(WIND_SIZE)
clock = pygame.time.Clock()
FPS = 50
#screen = pygame.display.set_mode(WIND_SIZE)

def terminate():
    pygame.quit()
    sys.exit()


class InputBox:
    def __init__(self, x, y, w, h, text=''):
        self.rect = pygame.Rect(x, y, w, h)
        self.color = COLOR_INACTIVE
        self.text = text
        self.txt_surface = FONT.render(text, True, self.color)
        self.active = False
    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            # If the user clicked on the input_box rect.
            if self.rect.collidepoint(event.pos):
                # Toggle the active variable.
                self.active = not self.active
            else:
                self.active = False
            # Change the current color of the input box.
            self.color = COLOR_ACTIVE if self.active else COLOR_INACTIVE
        if event.type == pygame.KEYDOWN:
            if self.active:
                if event.key == pygame.K_RETURN:
                    print(self.text)
                    self.text = ''
                elif event.key == pygame.K_BACKSPACE:
                    self.text = self.text[:-1]
                else:
                    self.text += event.unicode
                # Re-render the text.
                self.txt_surface = FONT.render(self.text, True, self.color)
    def update(self):
        # Resize the box if the text is too long.
        width = max(200, self.txt_surface.get_width()+10)
        self.rect.w = width
    def draw(self, screen):
        # Blit the text.
        screen.blit(self.txt_surface, (self.rect.x+5, self.rect.y+5))
        # Blit the rect.
        pygame.draw.rect(screen, self.color, self.rect, 2)


def getting_name():
    intro_text = ("Введите своё имя:", (550, 350))
    skale = 0.1
    while skale * WIND_WIDTH < WIND_WIDTH * 0.25:
        skale += 1.25 / FPS
        fon = pygame.transform.scale(load_image('rec.png'), (int(WIND_WIDTH * skale), int(WIND_HEIGHT * skale)))
        screen.blit(fon, (int(WIND_WIDTH - (WIND_WIDTH * skale))//2, int(WIND_HEIGHT - (WIND_HEIGHT * skale))//2))
        pygame.display.flip()
        clock.tick(FPS)

    font = pygame.font.Font(None, 25)
    string_rendered = font.render(intro_text[0], True, pygame.Color('white'))
    intro_rect = string_rendered.get_rect()
    intro_rect.x, intro_rect.y = intro_text[1][0] * 0.75 + WIND_WIDTH * 0.125, intro_text[1][1] * 0.75 + WIND_HEIGHT * 0.125
    screen.blit(string_rendered, intro_rect)

    btm_main = pygame.sprite.Sprite()
    btms = pygame.sprite.Group()
    btms.add(btm_main)
    btm_main.image = load_image('name.png')
    btm_main.rect = btm_main.image.get_rect().move((600, 450))

    input_box1 = InputBox(600, 400, 140, 32)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.pos[0] > 600 and event.pos[0] < 662:
                    if event.pos[1] > 450 and event.pos[1] < 488:
                        #print(input_box1.text)
                        if input_box1.text != '':
                            return input_box1.text

            input_box1.handle_event(event)

        input_box1.update()
        input_box1.draw(screen)
        btms.draw(screen)
        screen.blit(string_rendered, intro_rect)
        pygame.display.flip()
        clock.tick(FPS)
        screen.blit(fon, ((WIND_WIDTH - (WIND_WIDTH * skale)) // 2, (WIND_HEIGHT - (WIND_HEIGHT * skale)) // 2))



def main():
    clock = pygame.time.Clock()
    input_boxes = []
    getting_name()

    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        pygame.display.flip()
        clock.tick(30)


if __name__ == '__main__':
    main()
    pygame.quit()