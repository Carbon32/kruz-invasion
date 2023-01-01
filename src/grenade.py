# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
#                                                                             #
#                Invasion Engine, Land Invasion's Game Engine                 #
#                            Developer: Carbon                                #
#                                                                             #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

# Imports: #

from src.modules import *
from src.explosion import *

# Grenades: #

class Grenade(pygame.sprite.Sprite):
    def __init__(self, game, x, y, direction):
        pygame.sprite.Sprite.__init__(self)

        # Game:

        self.game = game

        # Timers:

        self.timer = 100

        # Grenade Settings:

        self.velocity_y = -(self.game.screen_width // 128)
        self.speed = self.game.screen_width // 256
        self.image = self.game.load_game_image("assets/Grenade/Grenade.png", self.game.screen_width // 128, self.game.screen_width // 128)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        self.direction = direction

    def render(self):
        self.game.display.blit(self.image, self.rect)

    def update(self, world, particles):
        self.velocity_y += self.game.engine_gravity
        delta_x = self.direction * self.speed 
        delta_y = self.velocity_y
        for tile in world.obstacle_list:
            if(tile[1].colliderect(self.rect.x + delta_x, self.rect.y, self.width, self.height)):
                self.direction *= -1
                delta_x = self.direction * self.speed

            if(tile[1].colliderect(self.rect.x, self.rect.y + delta_y, self.width, self.height)):
                self.speed = 0
                if(self.velocity_y < 0):
                    self.velocity_y = 0
                    delta_y = tile[1].bottom - self.rect.top
                elif(self.velocity_y >= 0):
                    self.velocity_y = 0
                    delta_y = tile[1].top - self.rect.bottom

        if(self.rect.left + delta_x < 0 or self.rect.right + delta_x > self.game.screen_width):
            self.direction *= -1
            delta_x = self.direction * self.speed

        self.rect.x += delta_x + self.game.screen_scroll
        self.rect.y += delta_y
        self.timer -= 1
        if(self.timer <= 0):
            self.kill()
            explosion_effect = Explosion(self.game, self.rect.x, self.rect.y - (world.tile_size * 2))
            self.game.explosion_group.add(explosion_effect)
            self.game.sounds.play_sound('Explosion', 1)
            for i in range(5):
                particles.add_game_particle("explosion", self.rect.x, self.rect.y)

            if (abs(self.rect.centerx - self.game.player.rect.centerx) < world.tile_size * 2 and (self.rect.centery - self.game.player.rect.centery) < world.tile_size * 2):
                self.game.player.health -= 50
            for enemy in self.game.enemy_group:
                if (abs(self.rect.centerx - enemy.rect.centerx) < world.tile_size * 2 and (self.rect.centery - enemy.rect.centery) < world.tile_size * 2):
                    enemy.health -= 100