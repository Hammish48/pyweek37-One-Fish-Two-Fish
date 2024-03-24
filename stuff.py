import pygame as pg

class Fish:
    def __init__(self, x, y, horizontal, texture):
        self.position = pg.Vector2(x, y)
        self.texture = texture
        self.rot_t = pg.transform.rotate(self.texture, 90)
        self.direction = horizontal
        self.foodBounds:pg.Rect
        self.freed = False

class Food:
    def __init__(self, x, y):
        self.grabbed = False
        self.position = pg.Vector2(x, y)


class Vec4Bool:
    def __init__(self, w:bool, x:bool, y:bool, z:bool) -> None:
        self.w = w
        self.x = x
        self.y = y
        self.z = z

class Turn:
    def __init__(self, x, y, directions:Vec4Bool) -> None:
        self.position = pg.Vector2(x, y)
        self.directions = directions
        self.texture:pg.surface.Surface
        self.texture = pg.image.load("./assets/pipes/two ends.png").convert()
        count:int = 0
        count += int(directions.w)
        count += int(directions.x)
        count += int(directions.y)
        count += int(directions.z)
        match (count):
            case 1:
                self.texture = pg.image.load("./assets/pipes/dead end.png").convert_alpha()
                if (directions.w):
                    self.texture = pg.transform.flip(self.texture, False, True)
                elif (directions.x):
                    self.texture = pg.transform.rotate(self.texture, -270)
                elif (directions.z):
                    self.texture = pg.transform.rotate(self.texture, -90)
            case 2:
                self.texture = pg.image.load("./assets/pipes/two ends corner.png").convert_alpha()
                if directions.w:
                    self.texture = pg.transform.rotate(self.texture, 180)
                    if directions.x:
                        self.texture = pg.transform.flip(self.texture, True, False)
                elif directions.z:
                    self.texture = pg.transform.flip(self.texture, True, False)
            case 3:
                self.texture = pg.image.load("./assets/pipes/three ends.png").convert_alpha()
                if directions.x and directions.z:
                    self.texture = pg.transform.rotate(self.texture, 90)
                    if directions.y:
                        self.texture = pg.transform.flip(self.texture, False, True)
                elif directions.z:
                    self.texture = pg.transform.flip(self.texture, True, False)
            case 4:
                self.texture = pg.image.load("./assets/pipes/4 way joiner.png").convert()


class LongPipe:
    texture = pg.image.load("./assets/pipes/two ends.png").convert()
    def __init__(self, x, y, endx, endy) -> None:
        self.p1 = pg.Vector2(x, y)
        self.p2 = pg.Vector2(endx, endy)
        self.buffer:pg.Surface
    def initSurface(self) -> None:
        if self.p1.x == self.p2.x:
            length = self.p2.y - self.p1.y
            print(length)
            self.buffer = pg.Surface((60, length))
            remainder = length % 60
            length -= remainder
            length /= 60
            for i in range(int(length+1)):
                self.buffer.blit(self.texture, (0, i*60))
        elif self.p1.y == self.p2.y:
            self.texture = pg.transform.rotate(self.texture, 90)
            length = self.p2.x - self.p1.x
            self.buffer = pg.Surface((length, 60))
            remainder = length % 60
            length -= remainder
            length /= 60
            for i in range(int(length+1)):
                self.buffer.blit(self.texture, ((i*60), 0))
        else:
            print("invalid pipe args")

class End:
    def __init__(self, x, y, swimRight, swimUp) -> None:
        self.position = pg.Vector2(x, y)
        self.sr:bool = swimRight
        self.su:bool = swimUp

