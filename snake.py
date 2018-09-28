#! python3
# -*- coding: utf-8 -*-

import sys, pygame
from pygame.locals import *

# frame/sec definition
TARGET_FPS = 30
clock = pygame.time.Clock()

# Define colors
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

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
tile_size = (10,10)
screen = pygame.display.set_mode(screen_size, DOUBLEBUF)
head_pos = (100, 100)
snake = [head_pos, (head_pos[0]-10, head_pos[1]), (head_pos[0]-20, head_pos[1])]

# 
direction = D_RIGHT

def erase_old_snake():
    tail_pos = snake[len(snake)-1]
    pygame.draw.rect(screen, BLACK, (tail_pos[0], tail_pos[1], tile_size[0],tile_size[1]))
    
def draw_snake():
    head_pos = snake[0]
    pygame.draw.rect(screen, GREEN, (head_pos[0], head_pos[1], tile_size[0],tile_size[1]))

# Main Loop
while True:
    for event in pygame.event.get():
        # Event handler
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        if event.type == KEYDOWN:
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

    
    erase_old_snake()

    # Update state
    head_pos = snake[0]
    if direction ==D_RIGHT:
        new_head_pos = (head_pos[0]+10, head_pos[1])
        if new_head_pos[0] >= screen_size[0]:
            new_head_pos = (0, head_pos[1])
    elif direction ==D_LEFT:
        new_head_pos = (head_pos[0]-10, head_pos[1])
        if new_head_pos[0] < 0:
            new_head_pos = (screen_size[0]-tile_size[0], head_pos[1])
    elif direction ==D_DOWN:
        new_head_pos = (head_pos[0], head_pos[1]+10)
        if new_head_pos[1] >= screen_size[1]:
            new_head_pos = (head_pos[0], 0)
    elif direction ==D_UP:
        new_head_pos = (head_pos[0], head_pos[1]-10)
        if new_head_pos[1] < 0:
            new_head_pos = (head_pos[0], screen_size[1]-tile_size[1])
    snake.insert(0, new_head_pos)
    del snake[len(snake)-1]
       
    draw_snake()

    pygame.display.flip() # Update screen
    clock.tick(TARGET_FPS) 
    
