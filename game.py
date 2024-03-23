import pygame as pg
import sys
from stuff import *
from menus import *
from more_stuff import checkCollisionRecs

def game(screen_, lvl, fps_:pg.Clock, textures:list):
    screen:pg.Surface = screen_
    pen = pg.draw
    clickCooldown = True
    won = False
    t_red_fish=textures[0]
    t_blue_fish:pg.Surface = textures[1]
    t_green_fish:pg.Surface = textures[2]
    t_yellow_fish:pg.Surface = textures[3]
    t_food:pg.Surface = textures[4]
    font = pg.font.Font("./assets/font.ttf", 20)
    fishes = []
    turns = []
    pipes = []
    winningPipes = []
    ends = []
    food = Food(100, 100)
    match (lvl):
        case 0:
            fishes = [Fish(415, 60, False, t_red_fish)]
            turns = [Turn(400, 300, Vec4Bool(True, True, False, False)), Turn(600, 300, Vec4Bool(False, False, True, True)), Turn(400, 10, Vec4Bool(False, False, True, False)), Turn(600, 530, Vec4Bool(True, False, False, False))]
            ends = [End(600, 530, False, False)]
            pipes = [LongPipe(400, 70, 400, 300), LongPipe(460, 300, 600, 300), LongPipe(600, 360, 600, 530)]
            winningPipes = [LongPipe(600, 530, 600, 800)]
            food = Food(600, 120)
        case 1:
            fishes = [Fish(715, 60, False, t_red_fish), Fish(115, 100, False, t_blue_fish)]
            turns = [Turn(300, 500, Vec4Bool(True, False, False, True)),Turn(100, 500, Vec4Bool(True, True, False, False)), Turn(700, 10, Vec4Bool(False, False, True, False)), Turn(700, 530, Vec4Bool(True, False, False, False)), Turn(100, 90, Vec4Bool(False, False, True, False)), Turn(300, 90, Vec4Bool(False, False, True, False))]
            ends = [End(700, 530, False, False), End(300, 100, False, True)]
            pipes = [LongPipe(100, 150, 100, 500), LongPipe(160, 500, 300, 500), LongPipe(300, 150, 300, 500), LongPipe(700, 70, 700, 530)]
            winningPipes = [LongPipe(700, 530, 700, 800), LongPipe(300, -70, 300, 100)]
            food = Food(600, 120)
        case 90:
            fishes = [Fish(500, 300, True, t_blue_fish), Fish(300, 400, False, t_red_fish)]
            turns = [Turn(300, 300, Vec4Bool(False, True, True, False)), Turn(300, 500, Vec4Bool(True, True, False, True)), Turn(800, 500, Vec4Bool(True, False, True, True)), Turn(800, 300, Vec4Bool(False, True, True, True)), Turn(800, 600, Vec4Bool(True, False, False, False)), Turn(200, 500, Vec4Bool(True, True, False, False))]
            #turn format is: up, right, down, left    clockwise openings
            pipes = [LongPipe(360, 300, 800, 300), LongPipe(300, 360, 300, 500)]
            winningPipes = [LongPipe(800, 600, 800, 800)]
            food = Food(200,200)
            ends = [End(800, 600, False, False), End(200, 200, False, True)]
        case 45:
            pipes = [LongPipe(300, 300, 600, 300)]
            food = Food(700,200)
            fishes = [Fish(500, 300, True, t_blue_fish), Fish(300, 400, False, t_red_fish), Fish(700, 400, False, t_green_fish), Fish(400, 500, False, t_yellow_fish)]
            ends = [End(800, 600, False, False), End(200, 200, False, True), End(200, 400, False, True), End(800, 200, False, True)]
    for pipe in pipes:
        pipe.initSurface()
    for pipe in winningPipes:
        pipe.initSurface()
        print(pipe.buffer)
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
        if not won:
            for i,fish in enumerate(fishes):
                if (fish.direction):
                    fish.foodBounds = pg.Rect(fish.position.x - 180, fish.position.y - 45, 390, 110)
                else:
                    fish.foodBounds = pg.Rect(fish.position.x - 45, fish.position.y - 180, 110, 390)
                if checkCollisionRecs(pg.Rect(food.position.x, food.position.y, 30, 30), fish.foodBounds):
                    if i == 0:
                        speed = 0.026
                    elif i == 1:
                        speed = 0.02
                    elif i == 2:
                        0.034
                    elif i == 3:
                        speed = 0.01
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
                            if fish.position.y < turn.position.y+3:
                                fish.position.y = turn.position.y+3
                        if turn.directions.x:
                            if (not fish.direction) and checkCollisionRecs(pg.Rect(fish.position.x, fish.position.y, 20, 20), pg.Rect(turn.position.x, turn.position.y, 50, 50)) and checkCollisionRecs(pg.Rect(fish.position.x, fish.position.y+30, 20, 20), pg.Rect(turn.position.x, turn.position.y, 50, 50)) and checkCollisionRecs(pg.Rect(fish.position.x - 180, fish.position.y - 20, 390, 90), pg.Rect(food.position.x, food.position.y, 30, 30))and not checkCollisionRecs(fish.foodBounds, pg.Rect(food.position.x, food.position.y, 30, 30)):
                                fish.direction = True
                                fish.position.y = turn.position.y + 20
                        elif fish.direction:
                            if fish.position.x + 50 > turn.position.x + 57:
                                fish.position.x = turn.position.x + 7
                        if turn.directions.y:
                            #print("down")
                            if (fish.direction) and checkCollisionRecs(pg.Rect(fish.position.x, fish.position.y, 20, orientation.y), pg.Rect(turn.position.x, turn.position.y, 50, 50)) and checkCollisionRecs(pg.Rect(fish.position.x + 30, fish.position.y, 20, orientation.y), pg.Rect(turn.position.x, turn.position.y, 50, 50)) and checkCollisionRecs(pg.Rect(fish.position.x - 20, fish.position.y - 180, 90, 390), pg.Rect(food.position.x, food.position.y, 30, 30)) and not checkCollisionRecs(fish.foodBounds, pg.Rect(food.position.x, food.position.y, 30, 30)):
                                fish.direction = False
                                fish.position.x = turn.position.x + 20
                                print(fish.direction)
                        elif not fish.direction:
                            if fish.position.y + 50> turn.position.y + 57:
                                print("aaaa")
                                fish.position.y = turn.position.y + 7
                        if turn.directions.z:
                            if (not fish.direction) and checkCollisionRecs(pg.Rect(fish.position.x, fish.position.y, 20, 20), pg.Rect(turn.position.x, turn.position.y, 50, 50)) and checkCollisionRecs(pg.Rect(fish.position.x, fish.position.y+30, 20, 20), pg.Rect(turn.position.x, turn.position.y, 50, 50)) and checkCollisionRecs(pg.Rect(fish.position.x - 180, fish.position.y - 20, 390, 90), pg.Rect(food.position.x, food.position.y, 30, 30))and not checkCollisionRecs(fish.foodBounds, pg.Rect(food.position.x, food.position.y, 30, 30)):
                                fish.direction = True
                                fish.position.y = turn.position.y + 20
                        elif fish.direction:
                            if fish.position.x < turn.position.x + 3:
                                fish.position.x = turn.position.x + 3
                if checkCollisionRecs(pg.Rect(fish.position.x, fish.position.y,50, 50), pg.Rect(ends[i].position.x, ends[i].position.y, 50, 50)):
                    fish.freed = True
                else:
                    fish.freed = False
                if fish.freed:
                    freedFishes += 1
            if freedFishes == len(fishes):
                print("you wonded")
                won = True
        if won:
            fullyFreedFishes = 0
            for i, fish in enumerate(fishes):
                if fish.direction:
                    if ends[i].sr:
                        fish.position.x += 4
                    else:
                        fish.position.x -= 4
                else:
                    if ends[i].su:
                        fish.position.y -= 4
                    else:
                        fish.position.y += 4
                if (fish.position.x > 1280 or fish.position.x < -60 or fish.position.y > 780 or fish.position.y < -80):
                    fullyFreedFishes += 1
            if fullyFreedFishes == len(fishes):
                break
            
        #this needs to go at the end
        if pg.mouse.get_pressed()[0]:
            clickCooldown = True
        #drawing
        screen.fill((255, 255, 255))
        for pipe in pipes:
            screen.blit(pipe.buffer, pipe.p1)
        for t in turns:
            screen.blit(t.texture, (t.position.x, t.position.y))
        if won:
            for p in winningPipes:
                screen.blit(p.buffer, p.p1)
        for i, end in enumerate(ends):
            screen.blit(textures[i+5], end.position)
        for fish in fishes:
            if fish.direction:
                if (food.position.x < fish.position.x + 25):
                    screen.blit(fish.texture, (fish.position.x, fish.position.y))
                else:
                    screen.blit(pg.transform.flip(fish.texture, True, False), (fish.position.x, fish.position.y))
            else:
                if (food.position.y > fish.position.y + 25):
                    screen.blit(fish.rot_t, (fish.position.x, fish.position.y))
                else:
                    screen.blit(pg.transform.flip(fish.rot_t, False, True), (fish.position.x, fish.position.y))
        if lvl == 0:
            screen.blit(font.render("this fish is trapped!", True, (0, 0, 0)), (600, 50))
            screen.blit(font.render("drag the food infront of the fish and guide it to the red flag", True, (0, 0, 0)), (600, 90))
            pen.rect(screen, (20, 255, 40), pg.Rect(food.position.x-5, food.position.y-5, 40, 40))
        if lvl == 1:
            screen.blit(font.render("now there are 2 fishes", True, (0, 0, 0)), (450, 50))
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
    pg.image.load("./assets/food.png").convert_alpha(), pg.image.load("./assets/red flag.png"), pg.image.load("./assets/blue flag.png"), pg.image.load("./assets/yellow flag.png"), pg.image.load("./assets/green flag.png")]
    mainMenu(screen, fps)
    game(screen, 1, fps, textures)
    endMenu(screen, fps)
