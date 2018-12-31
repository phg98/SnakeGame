import sys

import pygame


BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
GREY = (150, 150, 150)

class Wall(list):
    def __init__(self, a_screen, a_screen_size, a_tile_size):
        list.__init__([])
        self.screen = a_screen
        self.screen_size = a_screen_size
        self.tile_size = a_tile_size

    def make_horizontal_wall(self, startx, endx, y):
        for i in range(startx, endx, self.tile_size[0]):
            self.append((i, y))
        return self


    def make_vertical_wall(self, start, end, x):
        for i in range(start, end, self.tile_size[1]):
            self.append((x, i))
        return self


    def make_boundary_wall(self):
        for i in range(0, self.screen_size[0], self.tile_size[0]):
            self.append((i, 0))
            self.append((i, self.screen_size[1] - self.tile_size[1]))
        for i in range(0, self.screen_size[1], self.tile_size[1]):
            self.append((0, i))
            self.append((self.screen_size[0] - self.tile_size[0], i))
        return self


    def draw_wall(self):
        for brick in self:
            pygame.draw.rect(self.screen, GREY, (brick[0], brick[1], self.tile_size[0], self.tile_size[1]))


    def is_hit(self, snake):
        head_pos = snake.get_head_pos()
        for brick in self:
            if head_pos == brick:
                print('wall hit')
                return True
        return False