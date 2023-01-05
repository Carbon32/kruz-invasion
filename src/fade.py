# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
#                                                                             #
#                Invasion Engine, Land Invasion's Game Engine                 #
#                            Developer: Carbon                                #
#                                                                             #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

# Imports: #

from src.modules import *

# Fade: #

class Fade():
    def __init__(self, game, direction, color):

        # Display: 

        self.game = game

        # Fade Settings: 

        self.direction = direction
        self.color = color
        self.speed = self.game.screen_width // 128
        self.fade_counter = 0
        self.fade_completed = False

    def reset(self):
        self.fade_counter = 0
        self.fade_completed = False

    def fade(self):
        self.fade_counter += self.speed
        if(self.direction == 1):
            pygame.draw.rect(self.game.display, self.color, (0 - self.fade_counter, 0, self.game.screen_width // 2, self.game.screen_height))
            pygame.draw.rect(self.game.display, self.color, (self.game.screen_width // 2 + self.fade_counter, 0, self.game.screen_width, self.game.screen_height))
            pygame.draw.rect(self.game.display, self.color, (0, 0 - self.fade_counter, self.game.screen_width, self.game.screen_height // 2))
            pygame.draw.rect(self.game.display, self.color, (0, self.game.screen_height // 2 + self.fade_counter, self.game.screen_width, self.game.screen_height))

        if(self.direction == 2):
            pygame.draw.rect(self.game.display, self.color, (0, 0, self.game.screen_width, 0 + self.fade_counter))
        
        if(self.fade_counter >= self.game.screen_width // 2):
            self.fade_completed = True

        return self.fade_completed