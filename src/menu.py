# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
#                                                                             #
#                Invasion Engine, Land Invasion's Game Engine                 #
#                            Developer: Carbon                                #
#                                                                             #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

# Imports: #

from src.modules import *
from src.button import *

# Menu: #

class Menu():
    def __init__(self, game, assets_manager):

        # Game:

        self.game = game

        # Assets Manager:

        self.assets_manager = assets_manager

        # Menu:

        self.main_menu = True

        # Level Designs:

        self.level_designs = []
        for i in range(len(os.listdir('assets/Levels/'))):
            self.level_designs.append(self.game.load_game_image(f'assets/Levels/Level{i}.png', self.game.screen_width // 2, self.game.screen_height // 2))

        # Level Selector:

        self.level_selector = True
        self.selected_level = 0
        self.border = pygame.Rect(0, 0, 0, 0)

        # Buttons: #

        self.play_button = Button(self.game.display, self.game.screen_width // 2 - (self.game.screen_width // 14), self.game.screen_height // 2 - (self.game.screen_height // 3), self.assets_manager.buttons["Play"])
        self.editor_button = Button(self.game.display, self.game.screen_width // 2 - (self.game.screen_width // 14), self.game.screen_height // 2 - (self.game.screen_height // 6), self.assets_manager.buttons["Editor"])
        self.exit_button = Button(self.game.display, self.game.screen_width // 2 - (self.game.screen_width // 14), self.game.screen_height // 6 + (self.game.screen_height // 3), self.assets_manager.buttons["Exit"])
        self.again_button = Button(self.game.display, self.game.screen_width // 2 - (self.game.screen_width // 14), self.game.screen_height // 2 - (self.game.screen_height // 4), self.assets_manager.buttons["Again"])
        self.select_button = Button(self.game.display, self.game.screen_width // 4 + (self.game.screen_width // 4), self.game.screen_height // 2 + (self.game.screen_height // 4), self.assets_manager.buttons["Select"])
        self.back_button = Button(self.game.display, self.game.screen_width // 2 - (self.game.screen_width // 14), self.game.screen_height // 6 + (self.game.screen_height // 2), self.assets_manager.buttons["Back"])
        self.music_button = Button(self.game.display, self.game.screen_width // 2 + (self.game.screen_width // 2.3), self.game.screen_height // 2 - (self.game.screen_height // 2.1), self.assets_manager.buttons["MusicOn"])
        self.sound_button = Button(self.game.display, self.game.screen_width // 2 + (self.game.screen_width // 2.8), self.game.screen_height // 2 - (self.game.screen_height // 2.1), self.assets_manager.buttons["SoundOn"])
        self.level1 = Button(self.game.display, self.game.screen_width // 10, self.game.screen_height // 2 - (self.game.screen_width // 4), self.assets_manager.buttons["Lvl1"])
        self.level2 = Button(self.game.display, self.game.screen_width // 10, self.game.screen_height // 2 - (self.game.screen_width // 6), self.assets_manager.buttons["Lvl2"])
        self.level3 = Button(self.game.display, self.game.screen_width // 10, self.game.screen_height // 2 - (self.game.screen_width // 12), self.assets_manager.buttons["Lvl3"])
        self.level4 = Button(self.game.display, self.game.screen_width // 10, self.game.screen_height // 2, self.assets_manager.buttons["Lvl4"])
        self.level5 = Button(self.game.display, self.game.screen_width // 10, self.game.screen_height // 2 + (self.game.screen_width // 12), self.assets_manager.buttons["Lvl5"])
        self.level6 = Button(self.game.display, self.game.screen_width // 10, self.game.screen_height // 2 + (self.game.screen_width // 6), self.assets_manager.buttons["Lvl6"])
    
    def handle_menu(self, world):
        self.update_background()
        if(self.game.game_ready):
            self.main_menu = True
            self.level_selector = True
            self.game.game_ready = False

        if(self.main_menu):
            if(self.game.level_started):
                if(self.back_button.render()):
                    self.level_selector = False
                    self.main_menu = False
                    self.game.menu_on = False

            if(self.play_button.render()):
                self.main_menu = False
                self.game.level_started = False
                self.game.sounds.music_started = False
                self.game.sounds.stop_music()

            if(self.editor_button.render()):
                self.game.editor_status = True
                self.level_selector = False
                self.game.menu_on = False
                self.main_menu = False
                self.game.level_started = False
                self.game.sounds.music_started = False
                self.game.sounds.stop_music()

            if(self.music_button.render()):
                if(self.game.sounds.music_status):
                    self.music_button.change_button(self.assets_manager.buttons["MusicOff"])
                    self.game.sounds.music_status = False
                    self.game.sounds.stop_music()
                else:
                    self.music_button.change_button(self.assets_manager.buttons["MusicOn"])
                    self.game.sounds.music_status = True
                    self.game.music_started = False

            if(self.sound_button.render()):
                if(self.game.sounds.sound_status):
                    self.sound_button.change_button(self.assets_manager.buttons["SoundOff"])
                    self.game.sounds.sound_status = False
                else:
                    self.sound_button.change_button(self.assets_manager.buttons["SoundOn"])
                    self.game.sounds.sound_status = True

            if(self.exit_button.render()):
                self.game.engine_running = False
        else:
            if(self.level_selector):
                if(self.level1.render()):
                    self.selected_level = 1
                    self.border = pygame.Rect(self.game.screen_width // 10, self.game.screen_height // 2 - (self.game.screen_width // 4), self.game.screen_width // 8, self.game.screen_width // 16)

                if(self.level2.render()):
                    self.selected_level = 2
                    self.border = pygame.Rect(self.game.screen_width // 10, self.game.screen_height // 2 - (self.game.screen_width // 6), self.game.screen_width // 8, self.game.screen_width // 16)

                if(self.level3.render()):
                    self.selected_level = 3
                    self.border = pygame.Rect(self.game.screen_width // 10, self.game.screen_height // 2 - (self.game.screen_width // 12), self.game.screen_width // 8, self.game.screen_width // 16)

                if(self.level4.render()):
                    self.selected_level = 4
                    self.border = pygame.Rect(self.game.screen_width // 10, self.game.screen_height // 2, self.game.screen_width // 8, self.game.screen_width // 16)
                    
                if(self.level5.render()):
                    self.selected_level = 5
                    self.border = pygame.Rect(self.game.screen_width // 10, self.game.screen_height // 2 + (self.game.screen_width // 12), self.game.screen_width // 8, self.game.screen_width // 16)

                if(self.level6.render()):
                    self.selected_level = 6
                    self.border = pygame.Rect(self.game.screen_width // 10, self.game.screen_height // 2 + (self.game.screen_width // 6), self.game.screen_width // 8, self.game.screen_width // 16)

                if(self.select_button.render() and self.selected_level != 0):
                    world.set_game_level(self.selected_level)
                    self.level_selector = False
                    self.game.menu_on = False
                    self.game.music_started = False

                if(self.selected_level > len(self.level_designs) - 1):
                    self.game.display.blit(self.level_designs[0], (self.game.screen_width // 3, self.game.screen_height // 6))

                else:
                    self.game.display.blit(self.level_designs[self.selected_level], (self.game.screen_width // 3, self.game.screen_height // 6))

                pygame.draw.rect(self.game.display, (0, 0, 0), pygame.Rect(self.game.screen_width // 3, self.game.screen_height // 6, self.game.screen_width // 2, self.game.screen_height // 2), self.game.screen_width // 128)
                pygame.draw.rect(self.game.display, (150, 255, 0), self.border, self.game.screen_width // 128)

    def check_death(self, world):
        if(self.game.player.health <= 0 and self.game.level_started):
            self.game.change_time = False
            if(self.again_button.render()):
                world.restart_level()

    def update_background(self):
        self.game.display.blit(self.assets_manager.menu_background, (0, 0))
