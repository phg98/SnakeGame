#! python3
# -*- coding: utf-8 -*-

import sys, pygame

from wall import Wall


class Level():
    def __init__(self, a_screen, a_screen_size, a_tile_size):
        self.screen = a_screen
        self.screen_size = a_screen_size
        self.tile_size = a_tile_size
        self.screen_width  = a_screen_size[0]
        self.screen_height = a_screen_size[1]

    def create_levels(self):
        levels = []

        level1 = Wall(self.screen, self.screen_size, self.tile_size)
        levels.append(level1.make_boundary_wall())

        levels = self.create_basic_levels(levels, 10)
        levels = self.create_basic_levels(levels, 5)
        levels = self.create_basic_levels(levels, 3)

        return levels

    def create_basic_levels(self, levels, margin):
        level2 = Wall(self.screen, self.screen_size, self.tile_size)
        level2 = level2.make_boundary_wall()
        margin_pix = margin * self.tile_size[0]
        levels.append(level2.make_horizontal_wall(margin_pix, self.screen_width - margin_pix, self.screen_height // 2))
        level3 = Wall(self.screen, self.screen_size, self.tile_size)
        level3 = level3.make_boundary_wall()
        levels.append(level3.make_vertical_wall(margin_pix, self.screen_height - margin_pix, self.screen_width // 2))
        level4 = Wall(self.screen, self.screen_size, self.tile_size)
        level4 = level4.make_boundary_wall()
        level4 = level4.make_horizontal_wall(margin_pix, self.screen_width - margin_pix, self.screen_height // 2)
        levels.append(level4.make_vertical_wall(margin_pix, self.screen_height - margin_pix, self.screen_width // 2))
        return levels