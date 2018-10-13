#! python3
# -*- coding: utf-8 -*-

import sys, pygame
from pygame.locals import *
import random

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
board_size = (screen_size[0] // tile_size[0], screen_size[1] // tile_size[1])
screen = pygame.display.set_mode(screen_size, DOUBLEBUF)
score = 0
TAIL_INCREASE = 3


class Snake(list):
    def __init__(self, a_screen, a_screen_size,  a_tile_size):
        list.__init__([])
        self.screen = a_screen
        self.screen_size = a_screen_size
        self.tile_size = a_tile_size
        head_pos = (100, 200)
        self.extend([head_pos, (head_pos[0] - 10, head_pos[1]), (head_pos[0] - 20, head_pos[1])])
        self.direction = D_RIGHT
        self.tail_increase_sum = 0

    def get_head_pos(self):
        return self[0]

    def erase_old_snake(self):
        tail_pos = self[len(self) - 1]
        pygame.draw.rect(self.screen, BLACK, (tail_pos[0], tail_pos[1], self.tile_size[0], self.tile_size[1]))


    def draw_snake(self):
        head_pos = self[0]
        pygame.draw.rect(self.screen, GREEN, (head_pos[0], head_pos[1], self.tile_size[0], self.tile_size[1]))


    def is_body_colision(self):
        head_pos = self.get_head_pos()
        for body in self[1:]:
            if body == head_pos:
                return True
            else:
                return False


    def move(self, direction):
        head_pos = self.get_head_pos()
        if direction == D_RIGHT:
            new_head_pos = (head_pos[0] + 10, head_pos[1])
            if new_head_pos[0] >= self.screen_size[0]:
                new_head_pos = (0, head_pos[1])
        elif direction == D_LEFT:
            new_head_pos = (head_pos[0] - 10, head_pos[1])
            if new_head_pos[0] < 0:
                new_head_pos = (self.screen_size[0] - self.tile_size[0], head_pos[1])
        elif direction == D_DOWN:
            new_head_pos = (head_pos[0], head_pos[1] + 10)
            if new_head_pos[1] >= self.screen_size[1]:
                new_head_pos = (head_pos[0], 0)
        elif direction == D_UP:
            new_head_pos = (head_pos[0], head_pos[1] - 10)
            if new_head_pos[1] < 0:
                new_head_pos = (head_pos[0], self.screen_size[1] - self.tile_size[1])
        self.insert(0, new_head_pos)
        if self.tail_increase_sum > 0:
            self.tail_increase_sum -= 1
            print("tail_increase_sum = ", self.tail_increase_sum)
        else:
            del self[len(self) - 1]

    def update_tail_increase(self, tail_increase):
        self.tail_increase_sum += tail_increase


###### Wall handling
def make_horizontal_wall(wall, startx, endx, y):
    for i in range(startx, endx, tile_size[0]):
        wall.append((i, y))
    return wall


def make_boundary_wall(wall):
    for i in range(0, screen_size[0], tile_size[0]):
        wall.append((i, 0))
        wall.append((i, screen_size[1] - tile_size[1]))
    for i in range(0, screen_size[1], tile_size[1]):
        wall.append((0, i))
        wall.append((screen_size[0] - tile_size[0], i))
    return wall


def draw_wall(wall):
    for brick in wall:
        pygame.draw.rect(screen, GREY, (brick[0], brick[1], tile_size[0], tile_size[1]))


def check_wall(snake, wall):
    head_pos = snake[0]
    for brick in wall:
        if head_pos == brick:
            # Game Over
            # Todo : display game-over message & score 
            pygame.quit()
            sys.exit()


###### Apple handling
def add_apple(apples, wall, snake):
    apple = get_new_apple(apples, wall, snake)
    apples.append(apple)
    draw_apple(apples)


def get_new_apple(apples, wall, snake):
    apple = (random.randint(0, board_size[0] - 1), random.randint(0, board_size[1] - 1))
    apple = (apple[0] * tile_size[0], apple[1] * tile_size[1])
    for blocks in [apples, wall, snake]:
        for item in blocks:
            if item == apple:
                apple = get_new_apple(apples, wall, snake)
    return apple


def draw_apple(apples):
    for apple_pos in apples:
        pygame.draw.rect(screen, RED, (apple_pos[0], apple_pos[1], tile_size[0], tile_size[1]))


def check_apple(wall, snake, apples):
    global apples_left
    head_pos = snake.get_head_pos()
    global score
    for apple_pos in apples:
        if apple_pos == head_pos:
            score += 10
            print("Score = ", score)
            del apples[apples.index(apple_pos)]
            apples_left -= 1
            print("apples_left : ", apples_left)
            if apples_left <= 0:
                return 0
            add_apple(apples, wall, snake)
            return TAIL_INCREASE
    return 0


def run_game(wall):
    global apples_left
    # frame/sec definition
    target_fps = 15
    clock = pygame.time.Clock()

    # Init snake
    direction = D_RIGHT
    snake = Snake(screen, screen_size, tile_size)
    snake.draw_snake()

    # Init wall
    draw_wall(wall)

    # Init apple
    apples = []
    add_apple(apples, wall, snake)

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

        # Collision check
        tail_increase = check_apple(wall, snake, apples)
        snake.update_tail_increase(tail_increase)

        # print(apples_left)
        if apples_left <= 0:
            print("stage cleared.")
            return True
        check_wall(snake, wall)
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
levels.append(make_boundary_wall([]))
level = make_boundary_wall([])
levels.append(make_horizontal_wall(level, 100, 400, 150))

for level in levels:
    apples_left = 5
    print(level)
    # run_game
    isClear = run_game(level)
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
