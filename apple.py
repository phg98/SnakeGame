import random, pygame


# Define colors
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
GREY = (150, 150, 150)
YELLOW = (255,255,0)


class Apple():
    def __init__(self, a_screen, a_screen_size, a_tile_size, a_tail_increase, a_apples_left, is_fake_apple=False):
        self.screen = a_screen
        self.screen_size = a_screen_size
        self.tile_size = a_tile_size
        self.board_size = (self.screen_size[0] // self.tile_size[0], self.screen_size[1] // self.tile_size[1])
        self.tail_increase = a_tail_increase
        self.apples_left = a_apples_left
        self.is_fake_apple = is_fake_apple
        if is_fake_apple:
            self.color = YELLOW
        else:
            self.color = RED

    def add_apple(self, apples, wall, snake, fake_apples):
        apple = self.get_new_apple(apples, wall, snake, fake_apples)
        apples.append(apple)
        self.draw_apple(apples)


    def get_new_apple(self, apples, wall, snake, fake_apples):
        apple = (random.randint(0, self.board_size[0] - 1), random.randint(0, self.board_size[1] - 1))
        apple = (apple[0] * self.tile_size[0], apple[1] * self.tile_size[1])
        for blocks in [apples, wall, snake, fake_apples]:
            for item in blocks:
                if item == apple:
                    apple = self.get_new_apple(apples, wall, snake, fake_apples)
        return apple


    def draw_apple(self, apples):
        for apple_pos in apples:
            pygame.draw.rect(self.screen, self.color, (apple_pos[0], apple_pos[1], self.tile_size[0], self.tile_size[1]))


    # Collision check
    def check_apple(self, wall, snake, apples, fake_apples):
        head_pos = snake.get_head_pos()
        for apple_pos in apples:
            if apple_pos == head_pos:
                del apples[apples.index(apple_pos)]
                if not self.is_fake_apple:
                    self.apples_left -= 1
                    print("apples_left : ", self.apples_left)
                    if self.apples_left <= 0:
                        return 0
                    self.add_apple(apples, wall, snake, fake_apples)
                return self.tail_increase
        return 0