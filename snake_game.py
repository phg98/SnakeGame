#! python3
# -*- coding: utf-8 -*-

import sys, pygame
from pygame.locals import *

from apple import Apple
from snake import Snake
from wall import Wall

# Define colors
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
GREY = (150, 150, 150)

# mouse button define
LEFT = 1
RIGHT = 3

# define snake direction
D_RIGHT = 1
D_LEFT = 2
D_UP = 3
D_DOWN = 4

# Initialize
pygame.init()
screen_size = (480, 320)
tile_size = (10, 10)
screen = pygame.display.set_mode(screen_size, DOUBLEBUF)
score = 0
TAIL_INCREASE = 3


def run_game(wall, apples_left):
    global score
    # frame/sec definition
    target_fps = 15
    clock = pygame.time.Clock()

    # Init snake
    direction = D_RIGHT
    snake = Snake(screen, screen_size, tile_size)
    snake.draw_snake()

    # Init wall
    wall.draw_wall()

    # Init apple
    apples = []
    apple = Apple(screen, screen_size, tile_size, TAIL_INCREASE, apples_left)
    apple.add_apple(apples, wall, snake)

    # Main Loop
    while True:
        for event in pygame.event.get():
            # Event handler
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

            if event.type == KEYDOWN:  # Press 'Q' to quit the game
                if event.key == K_q:
                    pygame.quit()
                    sys.exit()

            if event.type == MOUSEBUTTONDOWN and event.button == LEFT:
                print("left mouse up at (%d, %d)" % event.pos)

            if event.type == KEYDOWN:
                if event.key == K_RIGHT:
                    if direction != D_LEFT:
                        direction = D_RIGHT
            if event.type == KEYDOWN:
                if event.key == K_LEFT:
                    if direction != D_RIGHT:
                        direction = D_LEFT
            if event.type == KEYDOWN:
                if event.key == K_UP:
                    if direction != D_DOWN:
                        direction = D_UP
            if event.type == KEYDOWN:
                if event.key == K_DOWN:
                    if direction != D_UP:
                        direction = D_DOWN

            if event.type == pygame.USEREVENT:
                print("target_pfs : ", target_fps)
                target_fps += 2
                if target_fps > 70: target_fps = 70

        snake.erase_old_snake()

        # Update state
        snake.move(direction)


        tail_increase = apple.check_apple(wall, snake, apples)
        if tail_increase > 0 :
            snake.update_tail_increase(tail_increase)
            score += 10
            print("Score = ", score)

        # print(apples_left)
        if apple.apples_left <= 0:
            print("stage cleared.")
            return True
        if wall.is_hit(snake):
            # Game Over
            # Todo : display game-over message & score
            pygame.quit()
            sys.exit()

        if snake.is_body_colision():
            # Game Over
            # Todo : display game-over message & score
            pygame.quit()
            sys.exit()

        snake.draw_snake()

        pygame.display.flip()  # Update screen
        clock.tick(target_fps)


# Speed handling
pygame.time.set_timer(pygame.USEREVENT, 10000)


###### Levels
levels = []

level1 = Wall(screen, screen_size, tile_size)
levels.append(level1.make_boundary_wall())

level2 = Wall(screen, screen_size, tile_size)
level2 = level2.make_boundary_wall()
levels.append(level2.make_horizontal_wall(100, 400, 150))

level3 = Wall(screen, screen_size, tile_size)
level3 = level3.make_boundary_wall()
levels.append(level3.make_vertical_wall(100, 300, 200))

level4 = Wall(screen, screen_size, tile_size)
level4 = level4.make_boundary_wall()
level4 = level4.make_horizontal_wall(100, 400, 150)
level4.append(level4.make_vertical_wall(100, 300, 200))

for level in levels:
    apples_left = 5
    print(level)
    # run_game
    isClear = run_game(level, apples_left)
    screen.fill(BLACK)
    if isClear is True:
        # display end screen       
        print("Level Cleared!")
        print("Score = ", score)
    else:
        # display failed screen
        print("Level Failed!")
        print("Score = ", score)
        break
print(len(levels), " levels ")
print("Game End")
pygame.quit()
sys.exit()
