import pygame
from only_hero import load_image
from start_scr import start_screen
import sys
import sqlite3


FPS = 50
WIND_SIZE = WIND_WIDTH, WIND_HEIGHT = 1500, 900
clock = pygame.time.Clock()
screen = pygame.display.set_mode(WIND_SIZE)


def terminate():
    pygame.quit()
    sys.exit()

def end_screen(name, time, money, kills):
    con = sqlite3.connect("game.sqlite")
    cur = con.cursor()
    result = cur.execute("""SELECT score FROM records""").fetchall()
    if not result:
        result = [[0]]
    intro_text = [("ВЫ ПРОИГРАЛИ...опять", (180, 80)),
                  (f"Времени вживых: {time} секунд", (70, 240)),
                  (f"Собрано монеток: {money}", (70, 320)),
                  (f"Умершие враги: {kills}", (70, 400)),
                  (f"Результат: {money*3+kills}", (70, 520)),
                  (f"Рекорд вроде как: {max(result)[0]}", (900, 750))]
                  #(f"Главный экран", (270, 660)),
                  #(f"Начать заново", (270, 750))

    skale = 0.1
    while skale * WIND_WIDTH < WIND_WIDTH * 0.75:
        skale += 1.25 / FPS
        fon = pygame.transform.scale(load_image('end.png'), (int(WIND_WIDTH * skale), int(WIND_HEIGHT * skale)))
        screen.blit(fon, (int(WIND_WIDTH - (WIND_WIDTH * skale))//2, int(WIND_HEIGHT - (WIND_HEIGHT * skale))//2))
        pygame.display.flip()
        clock.tick(FPS)
    font = pygame.font.Font(None, 25)
    btm_main, btm_rerun = pygame.sprite.Sprite(), pygame.sprite.Sprite()
    btms = pygame.sprite.Group()
    btms.add(btm_main, btm_rerun)
    btm_main.image, btm_rerun.image = load_image('menue.png'), load_image('rerun.png')
    btm_main.rect, btm_rerun.rect = btm_main.image.get_rect().move((355, 580)), btm_rerun.image.get_rect().move((355, 670))
    print(btm_main.rect, btm_rerun.rect)
    for line in intro_text:
        string_rendered = font.render(line[0], True, pygame.Color('white'))
        intro_rect = string_rendered.get_rect()
        intro_rect.x, intro_rect.y = line[1][0] * 0.75 + WIND_WIDTH * 0.125, line[1][1]* 0.75 + WIND_HEIGHT * 0.125
        screen.blit(string_rendered, intro_rect)
    btms.draw(screen)
    print('asdsd', name, money)
    cur.execute("""INSERT INTO records(nam, score) VALUES(?, ?)""", (name, money*3+kills))
    con.commit()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.pos[0] > 355 and event.pos[0] < 555:
                    if event.pos[1] > 580 and event.pos[1] < 630:
                        print('main')
                        name = start_screen()
                        return name

                    if event.pos[1] > 670 and event.pos[1] < 720:
                        return name
        pygame.display.flip()
        clock.tick(FPS)


def main():
    pygame.init()
    running = True
    end_screen('dude', 200, 3300, 5)
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

#main()