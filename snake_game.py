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
                return False

            if event.type == KEYDOWN:  # Press 'Q' to quit the game
                if event.key == K_q:
                    return False

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
            if event.type == KEYDOWN:  # Press 'q' to quit
                if event.key == K_q:
                    return 'quit'

def render_multi_line(text, x, y, fsize):
    fontObj = pygame.font.Font('C:\\freesansbold.ttf', fsize)  # 현재 디렉토리로부터 myfont.ttf 폰트 파일을 로딩한다. 텍스트 크기를 32로 한다
    lines = text.splitlines()
    for i, l in enumerate(lines):
        screen.blit(fontObj.render(l, 0, GREEN), (x, y + fsize * i))

def start_screen():
    # howTo = "Use arrow key to change direction of snake.\nPress 'q' to quit.\nPress space-bar to pause.[not yet implemented]\nEat apples to finish the stage.\nEat apple will makes snake grow, which makes the game more difficult.\nSnake speed will get faster as time passed.\n\nPress SPACE to start the game!"
    howTo = '''
    Use arrow key to change direction of snake.
    Eat apples to finish the stage.
    
    Press 'q' to quit.
    Press space-bar to pause.[not yet implemented]
    
    Press SPACE to start the game!
    '''
    render_multi_line(howTo, 0, 0, 16)
    '''
    textSurfaceObj = fontObj.render(howTo, True, GREEN)  # 텍스트 객체를 생성한다. 첫번째 파라미터는 텍스트 내용, 두번째는 Anti-aliasing 사용 여부, 세번째는 텍스트 컬러를 나타낸다
    textRectObj = textSurfaceObj.get_rect();  # 텍스트 객체의 출력 위치를 가져온다
    textRectObj.center = (150, 150)  # 텍스트 객체의 출력 중심 좌표를 설정한다
    screen.fill(BLACK)
    screen.blit(textSurfaceObj, textRectObj)  # 설정한 위치에 텍스트 객체를 출력한다
    '''
    pygame.display.update()

    # Font 객체 생성의 다른 예
    #fontObj = pygame.font.Font(None, 32)  # 폰트 파일에 None을 지정할 경우 기본 폰트가 사용된다
    #fontObj = pygame.font.Font('C:\\Windows\\Fonts\\tahoma.ttf', 32)  # 윈도우 경로에 있는 폰트를 사용할 경우

    # render 함수 사용의 다른 예
    #textSurfaceObj = fontObj.render('Hello font!', True, GREEN, BLUE)  # 텍스트 색을 녹색, 배경색을 파란색으로 설정한다

    wait_for_space_input()


def gameover_screen():
    end_message = '''
    Game Over
    
    Press R to restart the game.
    Press any key to quit the game.
    '''
    render_multi_line(end_message, 0, 10, 16)

    pygame.display.update()

    while True:
        for event in pygame.event.get():
            # Event handler
            if event.type == KEYDOWN:  # Press 'space' to continue
                if event.key == K_r:
                    return True
                else:
                    return False

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

is_game_continue = True

while (is_game_continue):
    start_screen()
    screen.fill(BLACK)

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
    is_game_continue = gameover_screen()
    screen.fill(BLACK)

pygame.quit()
sys.exit()

