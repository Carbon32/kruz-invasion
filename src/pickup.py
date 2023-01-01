# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
#                                                                             #
#                Invasion Engine, Land Invasion's Game Engine                 #
#                            Developer: Carbon                                #
#                                                                             #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

# Imports: #

from src.modules import *

# Pickup: #

class Pickup(pygame.sprite.Sprite):
    def __init__(self, game, tile_size, type, x, y):
        pygame.sprite.Sprite.__init__(self)

        # Game:

        self.game = game

        # Tile Size:

        self.tile_size = tile_size

        # Pickup Settings:

        self.type = type
        self.used = False
        self.image = self.game.pickups[self.type]
        self.rect = self.image.get_rect()
        self.rect.midtop = (x + self.tile_size // 2, y + (self.tile_size - self.image.get_height()))

    def render(self):
        self.game.display.blit(self.image, self.rect)

    def update(self):
        if(pygame.sprite.collide_rect(self, self.game.player) and self.used == False and self.game.player.alive):
            if(self.type == 'Ammo'):
                self.image = self.game.pickups['AmmoShine']
                pygame.draw.rect(self.game.display, (67, 131, 226), pygame.Rect(self.game.screen_width // 32, self.game.screen_height // 12, self.game.screen_width // 4, self.game.screen_width // 18))
                pygame.draw.rect(self.game.display, (0, 0, 0), pygame.Rect(self.game.screen_width // 32, self.game.screen_height // 12, self.game.screen_width // 4, self.game.screen_width // 18), self.game.screen_width // (self.game.screen_width // 12))
                self.game.draw_text("Press 'F' to open the bag (+7 Bullets).", self.game.screen_width // 64, (0, 0, 0), self.game.screen_width // 20, self.game.screen_height // 8)
                if(pygame.key.get_pressed()[pygame.K_f]):
                    self.game.ammo += 7
                    if(self.game.player.current_ammo == 0 and self.game.ammo == 7):
                        self.game.player.current_ammo = self.game.ammo
                        self.game.ammo -= self.game.ammo
                    self.used = True
                    self.game.sounds.play_sound('AmmoPickup', 1)

            elif(self.type == 'Health'):
                self.image = self.game.pickups['HealthShine']
                pygame.draw.rect(self.game.display, (67, 131, 226), pygame.Rect(self.game.screen_width // 32, self.game.screen_height // 12, self.game.screen_width // 4, self.game.screen_width // 18))
                pygame.draw.rect(self.game.display, (0, 0, 0), pygame.Rect(self.game.screen_width // 32, self.game.screen_height // 12, self.game.screen_width // 4, self.game.screen_width // 18), self.game.screen_width // (self.game.screen_width // 12))
                self.game.draw_text("Press 'F' to use the medicine (+50 Health).", self.game.screen_width // 64, (0, 0, 0), self.game.screen_width // 20, self.game.screen_height // 8)
                if(pygame.key.get_pressed()[pygame.K_f]):
                    self.game.player.health += 50
                    if(self.game.player.health > self.game.player.max_health):
                        self.game.player.health = self.game.player.max_health
                    self.used = True
                    self.game.sounds.play_sound('HealthPickup', 1)

            elif(self.type == 'Grenade'):
                self.image = self.game.pickups['GrenadeShine']
                pygame.draw.rect(self.game.display, (67, 131, 226), pygame.Rect(self.game.screen_width // 32, self.game.screen_height // 12, self.game.screen_width // 4, self.game.screen_width // 18))
                pygame.draw.rect(self.game.display, (0, 0, 0), pygame.Rect(self.game.screen_width // 32, self.game.screen_height // 12, self.game.screen_width // 4, self.game.screen_width // 18), self.game.screen_width // (self.game.screen_width // 12))
                self.game.draw_text("Press 'F' to open the chest (+3 Grenades).", self.game.screen_width // 64, (0, 0, 0), self.game.screen_width // 20, self.game.screen_height // 8)
                if(pygame.key.get_pressed()[pygame.K_f]):
                    self.game.grenades += 3
                    self.used = True
                    self.game.sounds.play_sound('GrenadePickup', 1)
        else:
            if(self.used == True):
                self.image = self.game.pickups[f'{self.type}Open']
            else:
                self.image = self.game.pickups[self.type]

        self.rect.x += self.game.screen_scroll