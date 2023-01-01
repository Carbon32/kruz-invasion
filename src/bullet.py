# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
#                                                                             #
#                Invasion Engine, Land Invasion's Game Engine                 #
#                            Developer: Carbon                                #
#                                                                             #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

# Imports: #

from src.modules import *

# Bullet: #

class Bullet(pygame.sprite.Sprite):
    def __init__(self, game, x, y, direction):
        pygame.sprite.Sprite.__init__(self)

        # Game:

        self.game = game

        # Bullet Settings:

        self.speed = (self.game.screen_width // 32) // 5
        self.image = self.game.load_game_image('assets/Bullet/Bullet.png', self.game.screen_width // 200, self.game.screen_width // 400)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.direction = direction

    def render(self):
        self.game.display.blit(pygame.transform.flip(self.image, self.game.player.flip, False), self.rect)

    def update(self, world, particles):
        self.rect.x += (self.direction * self.speed) + self.game.screen_scroll
        if(self.rect.right < 0 or self.rect.left > self.game.screen_width):
            self.kill

        for tile in world.obstacle_list:
            if(tile[1].colliderect(self.rect)):
                self.kill()

        if(pygame.sprite.spritecollide(self.game.player, self.game.enemy_bullets_group, False)):
            if(self.game.player.alive):
                self.game.player.health -= 5
                particles.add_game_particle("blood", self.game.player.rect.centerx, self.game.player.rect.centery)
                random_number = random.randint(1, 4)
                self.game.sounds.play_sound(f'Hit{random_number}', 0.3)
                self.kill()

        for enemy in self.game.enemy_group:
            if(pygame.sprite.spritecollide(enemy, self.game.player_bullets_group, False)):
                if(enemy.alive):
                    enemy.health -= 25
                    particles.add_game_particle("blood", enemy.rect.centerx, enemy.rect.centery)
                    self.kill()