#! python3
# -*- coding: utf-8 -*-

import sys, pygame, time
from pygame.locals import *

from apple import Apple
from snake import Snake
from wall import Wall
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
screen = pygame.display.set_mode(screen_size, DOUBLEBUF)
score = 0
TAIL_INCREASE = 3
START_LIVES = 3


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

def wait_for_space_input():
    while True:
        for event in pygame.event.get():
            # Event handler
            if event.type == KEYDOWN:  # Press 'space' to continue
                if event.key == K_SPACE:
                    return 'continue'

def render_multi_line(text, x, y, fsize, center=False):
    fontObj = pygame.font.Font('C:\\freesansbold.ttf', fsize)  # 현재 디렉토리로부터 myfont.ttf 폰트 파일을 로딩한다. 텍스트 크기를 32로 한다
    lines = text.splitlines()
    for i, l in enumerate(lines):
        if center:
            lineObj = fontObj.render(l, True, GREEN)
            text_rect = lineObj.get_rect(center=(SCREEN_WIDTH/2, y + fsize * i + (fsize//2)))
            screen.blit(lineObj, text_rect)
        else:
            screen.blit(fontObj.render(l, 0, GREEN), (x, y + fsize * i))

def start_screen():
    howTo = '''
    Use arrow key to change direction of snake.
    Eat apples to finish the stage.
    
    Press 'q' to quit.
    Press space-bar to pause.[not yet implemented]
    
    Press SPACE to start the game!
    '''
    render_multi_line(howTo, 0, 0, 16)

    pygame.display.update()

    wait_for_space_input()


def ready_screen(level, lives):
    message = '''
    
    Press SPACE to start the game!
    '''
    message = "    Level "+str(level) + "\n    Life remain " + str(lives) + message
    render_multi_line(message, 5, 100, 16, center=True)
    pygame.display.update()
    wait_for_space_input()


def gameover_screen():
    end_message = '''
    Game Over
    
    Press q to quit the game.
    Press any key to restart the game.
    '''
    render_multi_line(end_message, 0, 10, 16)

    pygame.display.update()

    time.sleep(1) # player's last input should be discarded.
    pygame.event.clear()

    while True:
        for event in pygame.event.get():
            # Event handler
            if event.type == KEYDOWN:  # Press 'space' to continue
                if event.key == K_q:
                    return False
                else:
                    return True

# Speed handling
pygame.time.set_timer(pygame.USEREVENT, 10000)


###### Levels
level_manager = Level(screen, screen_size, tile_size)
levels = level_manager.create_levels()

is_game_continue = True

while (is_game_continue):
    start_screen()
    screen.fill(BLACK)
    lives = START_LIVES

    for level in levels:
        isClear = False
        is_game_over = False
        while (not isClear):
            apples_left = 5
            print(level)
            ready_screen(levels.index(level)+1, lives)
            screen.fill(BLACK)
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
                lives -= 1
                if lives == 0:
                    is_game_over = True
                    break
        if is_game_over:
            break

    print(len(levels), " levels ")
    print("Game End")
    is_game_continue = gameover_screen()
    screen.fill(BLACK)

pygame.quit()
sys.exit()

