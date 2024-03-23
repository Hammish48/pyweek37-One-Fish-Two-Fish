import pygame as pg
import sys
from more_stuff import checkCollisionRecs


def mainMenu(screen:pg.Surface, fps:pg.Clock):
    img = pg.image.load("./assets/menu.png").convert()
    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()
        if pg.mouse.get_pressed()[0] and checkCollisionRecs(pg.Rect(pg.mouse.get_pos()[0],pg.mouse.get_pos()[1], 2, 2), pg.Rect(40, 450, 300, 110)):
            break
        screen.blit(img, (0,0))
        fps.tick(20)
        pg.display.update()


def endMenu(screen:pg.Surface, fps:pg.Clock):
    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()
        screen.fill((0,0,0))
        fps.tick(20)
        pg.display.update()