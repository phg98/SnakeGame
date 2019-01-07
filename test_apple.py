from unittest import TestCase
from apple import Apple

import pygame
from pygame.locals import *


class TestApple(TestCase):
    def test_apple(self):
        # create test apple
        SCREEN_WIDTH = 480
        SCREEN_HEIGHT = 320
        screen_size = (SCREEN_WIDTH, SCREEN_HEIGHT)
        TILE_SIZE_X = 10
        TILE_SIZE_Y = 10
        tile_size = (TILE_SIZE_X, TILE_SIZE_Y)
        screen = pygame.display.set_mode(screen_size, DOUBLEBUF)
        TAIL_INCREASE = 3
        apples_left = 3
        apple = Apple(screen, screen_size, tile_size, TAIL_INCREASE, apples_left)

        self.assertEqual(apple.screen, screen)
        self.assertEqual(apple.screen_size, screen_size)
        self.assertEqual(apple.tile_size, tile_size)
        self.assertEqual(apple.board_size, (48, 32))
        self.assertEqual(apple.tail_increase, TAIL_INCREASE)
        self.assertEqual(apple.apples_left, apples_left)

'''
    def test_add_apple(self):
        apple = Apple()
        #apple.add_apple(apples, wall, snake):
        self.fail()

    def test_get_new_apple(self):
        self.fail()

    def test_draw_apple(self):
        self.fail()

    def test_check_apple(self):
        self.fail()
'''