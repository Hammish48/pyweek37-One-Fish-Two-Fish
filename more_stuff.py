import pygame as pg

def checkCollisionRecs(r1:pg.Rect, r2:pg.Rect) -> bool:
    if (r1.x + r1.width > r2.x and r1.x < r2.x + r2.width and r1.y + r1.height > r2.y and r1.y < r2.y + r2.height):
        return True
    return False