#! python3
# -*- coding: utf-8 -*-

import sys, pygame
from pygame.locals import *

from apple import Apple
from screen import Screens
from snake import Snake
from level import Level

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
SCREEN_WIDTH = 480
SCREEN_HEIGHT = 320
screen_size = (SCREEN_WIDTH, SCREEN_HEIGHT)
TILE_SIZE_X = 10
TILE_SIZE_Y = 10
tile_size = (TILE_SIZE_X, TILE_SIZE_Y)
screen = pygame.display.set_mode(screen_size, pygame.DOUBLEBUF | pygame.FULLSCREEN)
screen_maker = Screens(screen, screen_size, tile_size)
score = 0
TAIL_INCREASE = 3
START_LIVES = 3
APPLES_LEFT = 5

if "-d" in sys.argv:  # Debug Mode
    START_LIVES = 2
    APPLES_LEFT = 2

def run_game(wall, apples_left):
    global score
    # frame/sec definition
    target_fps = 10
    clock = pygame.time.Clock()

    # Init snake
    direction = D_RIGHT
    snake = Snake(screen, screen_size, tile_size)
    snake.draw_snake()

    # Init wall
    wall.draw_wall()

    # Init fake apples
    num_fake_apples = 20
    fake_apples = []
    for i in range(0, num_fake_apples):
        fake_apple = Apple(screen, screen_size, tile_size, TAIL_INCREASE, apples_left, True)
        fake_apple.add_apple(fake_apples, wall, snake, fake_apples)

    # Init apple
    apples = []
    apple = Apple(screen, screen_size, tile_size, TAIL_INCREASE, apples_left)
    apple.add_apple(apples, wall, snake, fake_apples)

    # Main Loop
    while True:
        event = pygame.event.poll()
        # Event handler
        if event.type == QUIT:
            return False

        if event.type == KEYDOWN:  # Press 'Q' to quit the game
            if event.key == K_q:
                pygame.quit()
                sys.exit()

            if event.key == K_SPACE:    # Press space-bar will pause the game
                is_paused = True
                # display_pause_message()
                while is_paused:
                    for event in pygame.event.get():
                        if event.type == KEYDOWN:
                            is_paused = False
                # clear_pause_message(apples, wall, snake))

        if event.type == MOUSEBUTTONDOWN and event.button == LEFT:
            print("left mouse up at (%d, %d)" % event.pos)

        if event.type == KEYDOWN:
            if event.key == K_RIGHT:
                if direction != D_LEFT:
                    direction = D_RIGHT
            elif event.key == K_LEFT:
                if direction != D_RIGHT:
                    direction = D_LEFT
            elif event.key == K_UP:
                if direction != D_DOWN:
                    direction = D_UP
            elif event.key == K_DOWN:
                if direction != D_UP:
                    direction = D_DOWN

        if event.type == pygame.USEREVENT:
            print("target_pfs : ", target_fps)
            target_fps += 2
            if target_fps > 70: target_fps = 70

        snake.erase_old_snake()

        # Update state
        snake.move(direction)

        tail_increase = apple.check_apple(wall, snake, apples, fake_apples)
        if tail_increase > 0 :
            snake.update_tail_increase(tail_increase)
            score += 10
            print("Score = ", score)

        tail_increase = fake_apple.check_apple(wall, snake, fake_apples, apples)
        if tail_increase > 0 :
            snake.update_tail_increase(tail_increase)
            score += 2
            print("Score = ", score)

        # print(apples_left)
        if apple.apples_left <= 0:
            print("stage cleared.")
            return True
        if wall.is_hit(snake):
            return False

        if snake.is_body_colision():
            return False

        snake.draw_snake()

        pygame.display.flip()  # Update screen
        clock.tick(target_fps)


# Speed handling
pygame.time.set_timer(pygame.USEREVENT, 10000)


# Levels
level_manager = Level(screen, screen_size, tile_size)
levels = level_manager.create_levels()

is_game_continue = True

while is_game_continue:
    screen_maker.start_screen()
    screen.fill(BLACK)
    lives = START_LIVES

    for level in levels:
        isClear = False
        is_game_over = False
        while not isClear:
            print(level)
            screen_maker.ready_screen(levels.index(level) + 1, lives)
            screen.fill(BLACK)
            # run_game
            isClear = run_game(level, APPLES_LEFT)
            if isClear is True:
                screen_maker.result_screen("Level Cleared!", GREEN)
                print("Level Cleared!")
                print("Score = ", score)
            else:
                screen_maker.result_screen("Snake DEAD !!!", RED)
                print("Level Failed!")
                print("Score = ", score)
                lives -= 1
                if lives == 0:
                    is_game_over = True
                    break

            screen.fill(BLACK)
        if is_game_over:
            break

    screen.fill(BLACK)
    print(len(levels), " levels ")
    print("Game End")
    is_game_continue = screen_maker.gameover_screen()
    screen.fill(BLACK)

pygame.quit()
sys.exit()

