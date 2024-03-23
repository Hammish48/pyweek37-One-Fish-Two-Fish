import pygame as pg
import sys
from stuff import *

def checkCollisionRecs(r1:pg.Rect, r2:pg.Rect) -> bool:
    if (r1.x + r1.width > r2.x and r1.x < r2.x + r2.width and r1.y + r1.height > r2.y and r1.y < r2.y + r2.height):
        return True
    return False

def game(screen_, lvl, fps_:pg.Clock, textures:list):
    screen:pg.Surface = screen_
    pen = pg.draw
    clickCooldown = True
    t_red_fish=textures[0]
    t_blue_fish:pg.Surface = textures[1]
    t_green_fish:pg.Surface = textures[2]
    t_yellow_fish:pg.Surface = textures[3]
    t_food:pg.Surface = textures[4]
    food = Food(200,200)
    fishes = []
    turns = []
    pipes = []
    ends = [End(800, 600, False, False), End(200, 200, False, True)]
    food = Food(100, 100)
    match (lvl):
        case 0:
            fishes = [Fish(500, 300, True, t_blue_fish), Fish(300, 400, False, t_red_fish)]
            turns = [Turn(300, 300, Vec4Bool(False, True, True, False)), Turn(300, 500, Vec4Bool(True, True, False, True)), Turn(800, 500, Vec4Bool(True, False, True, True)), Turn(800, 300, Vec4Bool(False, True, True, True)), Turn(800, 600, Vec4Bool(True, False, False, False)), Turn(200, 500, Vec4Bool(True, True, False, False))]
            #turn format is: up, right, down, left    clockwise openings
            pipes = [LongPipe(360, 300, 800, 300), LongPipe(300, 360, 300, 500)]
    for pipe in pipes:
        pipe.initSurface()
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
        freedFishes = 0
        for i,fish in enumerate(fishes):
            if (fish.direction):
                fish.foodBounds = pg.Rect(fish.position.x - 180, fish.position.y - 45, 390, 110)
            else:
                fish.foodBounds = pg.Rect(fish.position.x - 45, fish.position.y - 180, 110, 390)
            if checkCollisionRecs(pg.Rect(food.position.x, food.position.y, 30, 30), fish.foodBounds):
                if i == 0:
                    speed = 0.02
                else:
                    speed = 0.026
                if fish.direction:
                    fish.position.x -= (fish.position.x - food.position.x) * speed
                else:
                    fish.position.y -= (fish.position.y - food.position.y) * speed
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
            if checkCollisionRecs(pg.Rect(fish.position.x, fish.position.y,50, 50), pg.Rect(ends[i].position.x, ends[i].position.y, 50, 50)):
                fish.freed = True
            else:
                fish.freed = False
            if fish.freed:
                freedFishes += 1
        if freedFishes == len(fishes):
            print("you wonded")
            
        #this needs to go at the end
        if pg.mouse.get_pressed()[0]:
            clickCooldown = True
        #drawing
        screen.fill((255, 255, 255))
        for pipe in pipes:
            screen.blit(pipe.buffer, pipe.p1)
        for t in turns:
            screen.blit(t.texture, (t.position.x, t.position.y))
        for i, end in enumerate(ends):
            screen.blit(textures[i+5], end.position)
        for fish in fishes:
            if fish.direction:
                #pen.rect(screen, (0, 255, 0), fish.foodBounds)
                #pen.rect(screen, (255, 20, 239), pg.Rect(fish.position.x - 20, fish.position.y - 180, 90, 390))
                if (food.position.x < fish.position.x + 25):
                    pen.rect(screen, (0, 255, 255), pg.Rect(fish.position.x, fish.position.y, 50, 20))
                    screen.blit(fish.texture, (fish.position.x, fish.position.y))
                else:
                    pen.rect(screen, (0, 255, 255), pg.Rect(fish.position.x, fish.position.y, 50, 20))
                    screen.blit(pg.transform.flip(fish.texture, True, False), (fish.position.x, fish.position.y))
            else:
                #pen.rect(screen, (0, 255, 0), fish.foodBounds)
                #pen.rect(screen, (255, 20, 239), pg.Rect(fish.position.x - 180, fish.position.y - 20, 390, 90))
                if (food.position.y > fish.position.y + 25):
                    pen.rect(screen, (0, 255, 255), pg.Rect(fish.position.x, fish.position.y, 20, 50))
                    screen.blit(fish.rot_t, (fish.position.x, fish.position.y))
                else:
                    pen.rect(screen, (0, 255, 255), pg.Rect(fish.position.x, fish.position.y, 20, 50))
                    screen.blit(pg.transform.flip(fish.rot_t, False, True), (fish.position.x, fish.position.y))
        screen.blit(t_food, food.position)
        pen.rect(screen, (0,255,0), pg.Rect(pg.mouse.get_pos()[0], pg.mouse.get_pos()[1], 2, 2))
        fps_.tick(60)
        pg.display.update()

def main(screen:pg.Surface):
    fps = pg.time.Clock()
    textures = [pg.image.load("./assets/red fish.png").convert_alpha(),
    pg.image.load("./assets/blue fish.png").convert_alpha(),
    pg.image.load("./assets/yellow fish.png").convert_alpha(),
    pg.image.load("./assets/green fish.png").convert_alpha(),
    pg.image.load("./assets/food.png").convert_alpha(), pg.image.load("./assets/blue flag.png"), pg.image.load("./assets/red flag.png"), pg.image.load("./assets/yellow flag.png"), pg.image.load("./assets/green flag.png")]
    game(screen, 0, fps, textures)
