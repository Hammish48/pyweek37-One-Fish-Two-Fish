import os
import pathlib
import pygame as pg
pg.init()
pg.font.init()
pg.mixer.init()
screen = pg.display.set_mode((1220, 720))
pg.display.set_caption("Pyweek 37")
print(pathlib.Path(__file__).parent)
os.chdir(pathlib.Path(__file__).parent)
from game import main
main(screen)