# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
#                                                                             #
#                Invasion Engine, Land Invasion's Game Engine                 #
#                            Developer: Carbon                                #
#                                                                             #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

# Imports: #

from src.modules import *

# Assets Manager: #

class AssetsManager():
    def __init__(self, game):

        # Game:

        self.game = game

        # Pickup Sprites:

        self.health_pickup = self.game.load_game_image('assets/Pickups/Health_Pickup.png', self.game.screen_width // 32, self.game.screen_width // 32)
        self.ammo_pickup = self.game.load_game_image('assets/Pickups/Bullet_Pickup.png', self.game.screen_width // 32, self.game.screen_width // 32)
        self.grenade_pickup = self.game.load_game_image('assets/Pickups/Grenade_Pickup.png', self.game.screen_width // 32, self.game.screen_width // 32)

        self.health_pickup2 = self.game.load_game_image('assets/Pickups/Health_Pickup2.png', self.game.screen_width // 32, self.game.screen_width // 32)
        self.ammo_pickup2 = self.game.load_game_image('assets/Pickups/Bullet_Pickup2.png', self.game.screen_width // 32, self.game.screen_width // 32)
        self.grenade_pickup2 =  self.game.load_game_image('assets/Pickups/Grenade_Pickup2.png', self.game.screen_width // 32, self.game.screen_width // 32)

        self.health_pickup3 = self.game.load_game_image('assets/Pickups/Health_Pickup3.png', self.game.screen_width // 32, self.game.screen_width // 32)
        self.ammo_pickup3 = self.game.load_game_image('assets/Pickups/Bullet_Pickup3.png', self.game.screen_width // 32, self.game.screen_width // 32)
        self.grenade_pickup3 =  self.game.load_game_image('assets/Pickups/Grenade_Pickup3.png', self.game.screen_width // 32, self.game.screen_width // 32)

        # Background:

        self.mountain = self.game.load_static_image('assets/Background/Mountain.png')
        self.sky = self.game.load_static_image('assets/Background/Sky.png')
        self.trees = self.game.load_static_image('assets/Background/Pines.png')
        self.menu_background = self.game.load_game_image('assets/Background/Menu.png', self.game.screen_width, self.game.screen_height)

        # Buttons:

        self.buttons = {
            "Play" : self.game.load_game_image('assets/Buttons/Play.png', self.game.screen_width // 6, self.game.screen_width // 12),
            "Editor" : self.game.load_game_image('assets/Buttons/Editor.png', self.game.screen_width // 6, self.game.screen_width // 12),
            "Exit" : self.game.load_game_image('assets/Buttons/Exit.png', self.game.screen_width // 6, self.game.screen_width // 12),
            "Again" : self.game.load_game_image('assets/Buttons/Again.png', self.game.screen_width // 6, self.game.screen_width // 12),
            "Select" : self.game.load_game_image('assets/Buttons/Select.png', self.game.screen_width // 6, self.game.screen_width // 12),
            "Save" : self.game.load_game_image('assets/Buttons/Save.png', self.game.screen_width // 12, self.game.screen_width // 24),
            "Clear" : self.game.load_game_image('assets/Buttons/Clear.png', self.game.screen_width // 12, self.game.screen_width // 24),
            "Back" : self.game.load_game_image('assets/Buttons/Back.png', self.game.screen_width // 12, self.game.screen_width // 24),
            "MusicOn" : self.game.load_game_image('assets/Buttons/MusicOn.png', self.game.screen_width // 32, self.game.screen_width // 32),
            "MusicOff" : self.game.load_game_image('assets/Buttons/MusicOff.png', self.game.screen_width // 32, self.game.screen_width // 32),
            "SoundOn" : self.game.load_game_image('assets/Buttons/SoundOn.png', self.game.screen_width // 32, self.game.screen_width // 32),
            "SoundOff" : self.game.load_game_image('assets/Buttons/SoundOff.png', self.game.screen_width // 32, self.game.screen_width // 32),
            "Lvl1" : self.game.load_game_image('assets/Buttons/Lvl_1.png', self.game.screen_width // 8, self.game.screen_width // 16),
            "Lvl2" : self.game.load_game_image('assets/Buttons/Lvl_2.png', self.game.screen_width // 8, self.game.screen_width // 16),
            "Lvl3" : self.game.load_game_image('assets/Buttons/Lvl_3.png', self.game.screen_width // 8, self.game.screen_width // 16),
            "Lvl4" : self.game.load_game_image('assets/Buttons/Lvl_4.png', self.game.screen_width // 8, self.game.screen_width // 16),
            "Lvl5" : self.game.load_game_image('assets/Buttons/Lvl_5.png', self.game.screen_width // 8, self.game.screen_width // 16),
            "Lvl6" : self.game.load_game_image('assets/Buttons/Lvl_6.png', self.game.screen_width // 8, self.game.screen_width // 16)
        }

    def load_pickups(self):
        self.game.pickups = {
            'Health'    : self.health_pickup,
            'Grenade'   : self.grenade_pickup,
            'Ammo'      : self.ammo_pickup,
            'HealthShine'   : self.health_pickup3,
            'GrenadeShine'  : self.grenade_pickup3,
            'AmmoShine'     : self.ammo_pickup3,
            'HealthOpen'        : self.health_pickup2,
            'AmmoOpen'      : self.ammo_pickup2,
            'GrenadeOpen'   : self.grenade_pickup2

        }