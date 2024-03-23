import pygame as pg
import sys

pg.init()
pg.font.init()
pg.mixer.init()

class Fish:
    def __init__(self, x, y, horizontal, color):
        self.position = pg.Vector2(x, y)
        self.color = color
        self.direction = horizontal
        self.foodBounds:pg.Rect

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


def checkCollisionRecs(r1:pg.Rect, r2:pg.Rect) -> bool:
    if (r1.x + r1.width > r2.x and r1.x < r2.x + r2.width and r1.y + r1.height > r2.y and r1.y < r2.y + r2.height):
        return True
    return False


def DrawPipe(screen, p1:pg.Vector2, p2:pg.Vector2):
    if p1.x == p2.x:
        print("vertical pipe")
    else:
        print("horizontal pipe")


def game(screen_, lvl):
    screen:pg.Surface = screen_
    fps = pg.time.Clock()
    pen = pg.draw
    clickCooldown = True
    food = Food(200,200)
    fish = Fish(500, 300, True,(45, 45, 90))
    #turn format is: up, right, down, left    clockwise openings
    turns = [Turn(300, 300, Vec4Bool(False, True, True, False)), Turn(300, 500, Vec4Bool(True, True, False, True)), Turn(800, 500, Vec4Bool(True, False, True, True)), Turn(800, 300, Vec4Bool(False, True, True, True))]
    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()
        if not pg.mouse.get_pressed()[0]:
            clickCooldown = False
        if (pg.mouse.get_pos()[0]+2 > food.position.x and pg.mouse.get_pos()[0] < food.position.x + 30 and pg.mouse.get_pos()[1] > food.position.y and pg.mouse.get_pos()[1]+2 < food.position.y + 30) and not clickCooldown and pg.mouse.get_pressed()[0]:
            food.grabbed = True
            clickCooldown = True
        if food.grabbed:
            food.position = pg.Vector2(pg.mouse.get_pos()[0]-15, pg.mouse.get_pos()[1]-15)
            if not pg.mouse.get_pressed()[0]:
                food.grabbed = False
        if (fish.direction):
            fish.foodBounds = pg.Rect(fish.position.x - 180, fish.position.y - 45, 390, 110)
        else:
            fish.foodBounds = pg.Rect(fish.position.x - 45, fish.position.y - 180, 110, 390)
        if checkCollisionRecs(pg.Rect(food.position.x, food.position.y, 30, 30), fish.foodBounds):
            if fish.direction:
                fish.position.x -= (fish.position.x - food.position.x) * 0.02
            else:
                fish.position.y -= (fish.position.y - food.position.y) * 0.02
        for turn in turns:
            if fish.direction:
                orientation = pg.Vector2(50, 20)
            else:
                orientation = pg.Vector2(30, 20)
            if checkCollisionRecs(pg.Rect(fish.position.x, fish.position.y, orientation.x, orientation.y), pg.Rect(turn.position.x, turn.position.y, 50, 50)):
                if turn.directions.w:
                    #print("up")
                    if (fish.direction) and checkCollisionRecs(pg.Rect(fish.position.x, fish.position.y, 20, orientation.y), pg.Rect(turn.position.x, turn.position.y, 50, 50)) and checkCollisionRecs(pg.Rect(fish.position.x + 30, fish.position.y, 20, orientation.y), pg.Rect(turn.position.x, turn.position.y, 50, 50)) and checkCollisionRecs(pg.Rect(fish.position.x - 20, fish.position.y - 180, 90, 390), pg.Rect(food.position.x, food.position.y, 30, 30))and not checkCollisionRecs(fish.foodBounds, pg.Rect(food.position.x, food.position.y, 30, 30)):
                        fish.direction = False
                        fish.position.x = turn.position.x + 20
                elif not fish.direction:
                    if fish.position.y < turn.position.y:
                        fish.position.y = turn.position.y
                if turn.directions.x:
                    if (not fish.direction) and checkCollisionRecs(pg.Rect(fish.position.x, fish.position.y, 20, 20), pg.Rect(turn.position.x, turn.position.y, 50, 50)) and checkCollisionRecs(pg.Rect(fish.position.x, fish.position.y+30, 20, 20), pg.Rect(turn.position.x, turn.position.y, 50, 50)) and checkCollisionRecs(pg.Rect(fish.position.x - 180, fish.position.y - 20, 390, 90), pg.Rect(food.position.x, food.position.y, 30, 30))and not checkCollisionRecs(fish.foodBounds, pg.Rect(food.position.x, food.position.y, 30, 30)):
                        fish.direction = True
                        fish.position.y = turn.position.y + 20
                elif fish.direction:
                    if fish.position.x + 50 > turn.position.x + 60:
                        fish.position.x = turn.position.x + 10
                if turn.directions.y:
                    #print("down")
                    if (fish.direction) and checkCollisionRecs(pg.Rect(fish.position.x, fish.position.y, 20, orientation.y), pg.Rect(turn.position.x, turn.position.y, 50, 50)) and checkCollisionRecs(pg.Rect(fish.position.x + 30, fish.position.y, 20, orientation.y), pg.Rect(turn.position.x, turn.position.y, 50, 50)) and checkCollisionRecs(pg.Rect(fish.position.x - 20, fish.position.y - 180, 90, 390), pg.Rect(food.position.x, food.position.y, 30, 30)) and not checkCollisionRecs(fish.foodBounds, pg.Rect(food.position.x, food.position.y, 30, 30)):
                        fish.direction = False
                        fish.position.x = turn.position.x + 20
                        print(fish.direction)
                elif not fish.direction:
                    if fish.position.y + 50> turn.position.y + 60:
                        print("aaaa")
                        fish.position.y = turn.position.y + 10
                if turn.directions.z:
                    if (not fish.direction) and checkCollisionRecs(pg.Rect(fish.position.x, fish.position.y, 20, 20), pg.Rect(turn.position.x, turn.position.y, 50, 50)) and checkCollisionRecs(pg.Rect(fish.position.x, fish.position.y+30, 20, 20), pg.Rect(turn.position.x, turn.position.y, 50, 50)) and checkCollisionRecs(pg.Rect(fish.position.x - 180, fish.position.y - 20, 390, 90), pg.Rect(food.position.x, food.position.y, 30, 30))and not checkCollisionRecs(fish.foodBounds, pg.Rect(food.position.x, food.position.y, 30, 30)):
                        fish.direction = True
                        fish.position.y = turn.position.y + 20
                elif fish.direction:
                    if fish.position.x < turn.position.x:
                        fish.position.x = turn.position.x
        #this needs to go at the end
        if pg.mouse.get_pressed()[0]:
            clickCooldown = True
        #drawing
        screen.fill((255, 255, 255))
        for t in turns:
            screen.blit(t.texture, (t.position.x, t.position.y))
        if fish.direction:
            #pen.rect(screen, (0, 255, 0), fish.foodBounds)
            #pen.rect(screen, (255, 20, 239), pg.Rect(fish.position.x - 20, fish.position.y - 180, 90, 390))
            pen.rect(screen, fish.color, pg.Rect(fish.position.x, fish.position.y, 50, 20))
        else:
            #pen.rect(screen, (0, 255, 0), fish.foodBounds)
            #pen.rect(screen, (255, 20, 239), pg.Rect(fish.position.x - 180, fish.position.y - 20, 390, 90))
            pen.rect(screen, fish.color, pg.Rect(fish.position.x, fish.position.y, 20, 50))
        pen.rect(screen, (0,0,0), pg.Rect(food.position.x, food.position.y, 30, 30))
        pen.rect(screen, (0,255,0), pg.Rect(pg.mouse.get_pos()[0], pg.mouse.get_pos()[1], 2, 2))
        fps.tick(60)
        pg.display.update()

def main():
    screen = pg.display.set_mode((1220, 720))
    pg.display.set_caption("Pyweek 37")
    game(screen, 0)

if __name__ == "__main__":
    main()