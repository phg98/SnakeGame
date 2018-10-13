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

# define snake direction
D_RIGHT = 1
D_LEFT = 2
D_UP = 3
D_DOWN = 4

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

