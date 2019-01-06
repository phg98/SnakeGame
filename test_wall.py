from unittest import TestCase
from wall import Wall

import pygame
from pygame.locals import *

class TestWall(TestCase):
    def test_wall(self):
        # create test apple
        SCREEN_WIDTH = 480
        SCREEN_HEIGHT = 320
        screen_size = (SCREEN_WIDTH, SCREEN_HEIGHT)
        TILE_SIZE_X = 10
        TILE_SIZE_Y = 10
        tile_size = (TILE_SIZE_X, TILE_SIZE_Y)
        screen = pygame.display.set_mode(screen_size, DOUBLEBUF)
        wall = Wall(screen, screen_size, tile_size)

        # check apple
        self.assertEqual((480, 320), wall.screen_size)
        self.assertEqual((10, 10), wall.tile_size)
        self.assertEqual(screen, wall.screen)
