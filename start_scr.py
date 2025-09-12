import pygame
from PyQt5.QtWidgets import QDialog, QApplication
from PyQt5 import uic, QtWidgets
from only_hero import load_image
from nameinput import getting_name, InputBox
import sys
import sqlite3


FPS = 50
WIND_SIZE = WIND_WIDTH, WIND_HEIGHT = 1500, 900
clock = pygame.time.Clock()
screen = pygame.display.set_mode(WIND_SIZE)


def terminate():
    pygame.quit()
    sys.exit()

def start_screen():
    skale = 0.1
    while skale * WIND_WIDTH < WIND_WIDTH:
        skale += 1.25 / FPS
        fon = pygame.transform.scale(load_image('start.png'), (int(WIND_WIDTH * skale), int(WIND_HEIGHT * skale)))
        screen.blit(fon, (int(WIND_WIDTH - (WIND_WIDTH * skale))//2, int(WIND_HEIGHT - (WIND_HEIGHT * skale))//2))
        pygame.display.flip()
        clock.tick(FPS)

    btm_quest = pygame.sprite.Sprite()
    btms = pygame.sprite.Group()
    btms.add(btm_quest)
    btm_quest.image = load_image('help.png', -1)
    btm_quest.rect = btm_quest.image.get_rect().move((570, 300))
    btms.draw(screen)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.pos[0] > 570 and event.pos[0] < 610:
                    if event.pos[1] > 300 and event.pos[1] < 358:
                        name = help_screen()
                        return name
                if event.pos[0] > 50 and event.pos[0] < 470:
                    if event.pos[1] > 255 and event.pos[1] < 370:
                        print('play')
                        name = getting_name()
                        print(name)
                        return name

                    elif event.pos[1] > 450 and event.pos[1] < 590:
                        name = records()
                        return name

                    elif event.pos[1] > 645 and event.pos[1] < 815:
                        print('esc')
                        terminate()


        pygame.display.flip()
        clock.tick(FPS)

def records():
    con = sqlite3.connect("game.sqlite")
    cur = con.cursor()
    result = cur.execute("""SELECT * FROM records""").fetchall()
    if not result:
        result = [['Данных нет', 0]]

    skale = 0.1
    while skale * WIND_WIDTH < WIND_WIDTH:
        skale += 1.25 / FPS
        fon = pygame.transform.scale(load_image('rec.png'), (int(WIND_WIDTH * skale), int(WIND_HEIGHT * skale)))
        screen.blit(fon, (int(WIND_WIDTH - (WIND_WIDTH * skale))//2, int(WIND_HEIGHT - (WIND_HEIGHT * skale))//2))
        pygame.display.flip()
        clock.tick(FPS)
    font = pygame.font.Font(None, 50)
    btm_rerun = pygame.sprite.Sprite()
    btms = pygame.sprite.Group()
    btms.add(btm_rerun)
    btm_rerun.image = load_image('menue.png')
    btm_rerun.rect = btm_rerun.image.get_rect().move((55, 750))
    #print(btm_main.rect, btm_rerun.rect)

    string_rendered = font.render('ЛИДЕРЫ', True, pygame.Color('red'))
    intro_rect = string_rendered.get_rect()
    intro_rect.x, intro_rect.y = 100, 50
    x, y, add = 50, 100, 50
    screen.blit(string_rendered, intro_rect)

    result = sorted(result, key=lambda x: -1 * x[1])
    max_len = max([len(str(i[0])) for i in result])
    print(max_len)
    c = 10

    for line in result:
        if line[0] == 'Данных нет':
            string_rendered = font.render(line[0], True, pygame.Color('white'))
        else:
            help_str = ' '*(max_len-len(str(line[0])))
            s = str(line[0]) + help_str
            print(s)
            string_rendered = font.render(f'{s}   {line[1]} очков', True, pygame.Color('white'))
        if c == 0:
            break
        intro_rect = string_rendered.get_rect()
        intro_rect.x, intro_rect.y = x, y + add
        add += 50
        screen.blit(string_rendered, intro_rect)
        c -= 1
    btms.draw(screen)
    con.commit()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.pos[0] > 55 and event.pos[0] < 255:
                    if event.pos[1] > 750 and event.pos[1] < 800:
                        name = start_screen()
                        return name

        pygame.display.flip()
        clock.tick(FPS)



def help_screen():
    skale = 0.1
    while skale * WIND_WIDTH < WIND_WIDTH:
        skale += 1.25 / FPS
        fon = pygame.transform.scale(load_image('question.png'), (int(WIND_WIDTH * skale), int(WIND_HEIGHT * skale)))
        screen.blit(fon, (int(WIND_WIDTH - (WIND_WIDTH * skale))//2, int(WIND_HEIGHT - (WIND_HEIGHT * skale))//2))
        pygame.display.flip()
        clock.tick(FPS)

    btm_quest = pygame.sprite.Sprite()
    btms = pygame.sprite.Group()
    btms.add(btm_quest)
    btm_quest.image = load_image('name.png')
    btm_quest.rect = btm_quest.image.get_rect().move((100, 700))
    btms.draw(screen)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.pos[0] > 100 and event.pos[0] < 164:
                    if event.pos[1] > 700 and event.pos[1] < 736:
                        name = start_screen()
                        return name


        pygame.display.flip()
        clock.tick(FPS)



def main():
    pygame.init()
    #app = QApplication(sys.argv)
    running = True
    start_screen()
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
    #sys.exit(app.exec())


#main()