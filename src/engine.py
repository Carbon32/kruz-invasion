# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
#                                                                             #
#                Invasion Engine, Land Invasion's Game Engine                 #
#                            Developer: Carbon                                #
#                                                                             #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

# Imports: #

from src.modules import *
from src.world import *
from src.button import *
from src.assets_manager import *
from src.editor import *
from src.fade import *
from src.game import *
from src.menu import *
from src.particles import *
from src.sounds import *
from src.ui import *

# Resolution: #

class Resolution():
    def __init__(self, game):
        
        # Game: 

        self.game = game

        # Display:

        self.resolution_window = pygame.display.set_mode((300, 400))
        pygame.display.set_caption("Land Invasion: ")
        pygame.display.set_icon(self.game.load_game_image('assets/Icon.png', 32, 32))
        self.resolution_status = True

        # Background:

        self.background = self.game.load_game_image('assets/Menu.png', 300, 400)

        # Buttons: 

        self.resolution_a = ButtonImage(self.resolution_window, self.game.load_game_image('assets/Resolution/B.png', 150, 100), 55, 200, 200, 100, 10, 50) # 1280 x 720
        self.resolution_b = ButtonImage(self.resolution_window, self.game.load_game_image('assets/Resolution/A.png', 150, 100), 55, 50, 200, 100, 10, 50) # 1920 x 1080

    def update_background(self):
        self.resolution_window.fill((255, 255, 255))
        self.resolution_window.blit(self.background, (0, 0))

    def set_resolution(self, screen_width, screen_height):
        self.game.screen_width = screen_width
        self.game.screen_height = screen_height
        self.resolution_status = False


    def update_window(self):
        for event in pygame.event.get():
            if(event.type == pygame.QUIT):
                self.resolution_status = False
                exit()

        pygame.display.update()

# Graphics: #

class Graphics():
    def __init__(self, game):

        # Game: 

        self.game = game

        # Display:

        self.graphics_window = pygame.display.set_mode((300, 400))
        self.graphics_status = True
        pygame.display.set_icon(self.game.load_game_image('assets/Icon.png', 32, 32))

        # Background:

        self.background = self.game.load_game_image('assets/Menu.png', 300, 400)

        # Buttons: 

        self.effects = ButtonImage(self.graphics_window, self.game.load_game_image('assets/Graphics/AOn.png', 150, 100), 55, 50, 200, 100, 10, 50) 
        self.start = ButtonImage(self.graphics_window, self.game.load_game_image('assets/Graphics/Start.png', 150, 100), 55, 250, 200, 100, 10, 50) 

    def update_background(self):
        self.graphics_window.fill((255, 255, 255))
        self.graphics_window.blit(self.background, (0, 0))

    def set_effects(self):
        if(self.game.effects):
            self.game.effects = False
        else:
            self.game.effects = True

    def update_window(self):
        if(self.game.effects):
            self.effects.change_button(self.game.load_game_image('assets/Graphics/AOn.png', 150, 100))
        else:
            self.effects.change_button(self.game.load_game_image('assets/Graphics/AOff.png', 150, 100)) 

        for event in pygame.event.get():
            if(event.type == pygame.QUIT):
                self.resolution_status = False
                exit()
        pygame.display.update()