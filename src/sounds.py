# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
#                                                                             #
#                Invasion Engine, Land Invasion's Game Engine                 #
#                            Developer: Carbon                                #
#                                                                             #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

# Imports: #

from src.modules import *

# Sounds: #

class Sounds():
    def __init__(self, game):

        # Game:

        self.game = game

        # Music:

        self.music_status = True

        # Sounds: 

        self.sound_status = True

        # Available Sounds: 

        self.sounds = {
            'Footsteps' : self.game.load_game_sound('sounds/footsteps/footsteps.ogg'),
            'Fall1' : self.game.load_game_sound('sounds/fall/fall_1.ogg'),
            'Fall2' : self.game.load_game_sound('sounds/fall/fall_2.ogg'),
            'Hit1' : self.game.load_game_sound('sounds/hit/hit_1.ogg'),
            'Hit2' : self.game.load_game_sound('sounds/hit/hit_2.ogg'),
            'Hit3' : self.game.load_game_sound('sounds/hit/hit_3.ogg'),
            'Hit4' : self.game.load_game_sound('sounds/hit/hit_4.ogg'),
            'Intro' : self.game.load_game_sound('sounds/intro/intro.ogg'),
            'Jump1' : self.game.load_game_sound('sounds/jump/jump_1.ogg'),
            'Jump2' : self.game.load_game_sound('sounds/jump/jump_2.ogg'),
            'HealthPickup' : self.game.load_game_sound('sounds/pickup/health_pickup.ogg'),
            'AmmoPickup' : self.game.load_game_sound('sounds/pickup/ammo_pickup.ogg'),
            'GrenadePickup' : self.game.load_game_sound('sounds//pickup/grenade_pickup.ogg'),
            'Explosion' : self.game.load_game_sound('sounds/weapons/explosion.ogg'),
            'GrenadeFall' : self.game.load_game_sound('sounds/weapons/grenade_fall.ogg'),
            'Reload' : self.game.load_game_sound('sounds/weapons/handgun_reload.ogg'),
            'Gunshot' : self.game.load_game_sound('sounds/weapons/handgun_shoot.ogg'),
            'Empty' : self.game.load_game_sound('sounds/weapons/handgun_empty.ogg')
        }

    def  play_sound(self, sound, volume):
        if(self.sound_status):
            self.sounds[sound].set_volume(volume)
            pygame.mixer.Sound.play(self.sounds[sound])

    def stop_sound(self, sound):
        pygame.mixer.Sound.stop(self.sounds[sound])

    def play_music(self, music, volume):
        if(self.music_status):
            pygame.mixer.music.load(music)
            pygame.mixer.music.set_volume(volume)
            pygame.mixer.music.play(-1, 0.0, 5000)

    def stop_music(self):
        pygame.mixer.music.stop()
