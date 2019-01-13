
import pygame, time
from pygame.locals import *

# Define colors
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
GREY = (150, 150, 150)


class Screens():
    def __init__(self, a_screen, a_screen_size, a_tile_size):
        self.screen = a_screen
        self.screen_size = a_screen_size
        self.tile_size = a_tile_size
        self.screen_width  = a_screen_size[0]
        self.screen_height = a_screen_size[1]

    def wait_for_space_input(self):
        while True:
            for event in pygame.event.get():
                # Event handler
                if event.type == KEYDOWN:  # Press 'space' to continue
                    if event.key == K_SPACE:
                        return 'continue'


    def render_multi_line(self, text, x, y, fsize, center=False, color=GREEN):
        font_obj = pygame.font.Font('C:\\freesansbold.ttf', fsize)  # 현재 디렉토리로부터 myfont.ttf 폰트 파일을 로딩한다. 텍스트 크기를 32로 한다
        lines = text.splitlines()
        for i, l in enumerate(lines):
            if center:
                lineObj = font_obj.render(l, True, color)
                text_rect = lineObj.get_rect(center=(self.screen_width/2, y + fsize * i + (fsize//2)))
                self.screen.blit(lineObj, text_rect)
            else:
                self.screen.blit(font_obj.render(l, 0, color), (x, y + fsize * i))


    def start_screen(self):
        howTo = '''
        Use arrow key to change direction of snake.
        Eat apples to finish the stage.
        
        Press 'q' to quit.
        Press space-bar to pause.[not yet implemented]
        
        Press SPACE to start the game!
        '''
        self.render_multi_line(howTo, 0, 0, 16)

        pygame.display.update()

        self.wait_for_space_input()


    def ready_screen(self, level, lives):
        message = '''
        
        Press SPACE to start the game!
        '''
        message = "    Level "+str(level) + "\n    Life remain " + str(lives) + message
        self.render_multi_line(message, 5, 100, 16, center=True)
        pygame.display.update()
        self.wait_for_space_input()


    def result_screen(self, message, color):
        margin_x = 100
        margin_y = 50
        pygame.draw.rect(self.screen, BLACK, (margin_x, margin_y, self.screen_width - margin_x*2, self.screen_height - margin_y*2))
        self.render_multi_line(message, 10, margin_y+50, 30, center=True, color=color)
        pygame.display.update()
        time.sleep(2)


    def gameover_screen(self):
        end_message = '''
        Game Over
        
        Press q to quit the game.
        Press any key to restart the game.
        '''
        self.render_multi_line(end_message, 0, 10, 16)

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