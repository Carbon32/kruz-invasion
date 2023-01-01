# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
#                                                                             #
#                Invasion Engine, Land Invasion's Game Engine                 #
#                            Developer: Carbon                                #
#                                                                             #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

# Imports: #

from src.modules import *
from src.bullet import *
from src.explosion import *

# Enemy: #

class Enemy(pygame.sprite.Sprite):
    def __init__(self, game, x : int, y : int, speed):
        pygame.sprite.Sprite.__init__(self)

        # Game:

        self.game = game

        # Enemy Settings: 

        self.health = 100
        self.max_health = self.health
        self.x = x
        self.y = y
        self.speed = speed

        # Enemy Status:

        self.alive = True
        self.shoot = False

        # Enemy Timers:

        self.shoot_timer = 0
        self.time = pygame.time.get_ticks()

        # Enemy Movement Variables:

        self.direction = 1
        self.velocity_y = 0

        # Enemy Animation Variables:

        self.flip = False
        self.animation_list = []
        self.index = 0
        self.action = 0

        # Enemy AI Variables:

        self.move_counter = 0
        self.idle = False
        self.idle_counter = 0
        self.enemy_vision_front = pygame.Rect(0, 0, self.game.screen_width // 4, self.game.screen_height * 0.01)

        # Collision Patches:

        if(self.game.screen_width == 1920):
            self.x_collision = 30
            self.width_collision = 60
        else:
            self.x_collision = 20
            self.width_collision = 40

        # Loading Sprites: #

        animation_types = ['Idle', 'Move', 'Death']
        for animation in animation_types:
            temp_list = []
            frames_number = len(os.listdir(f'assets/Enemy/{animation}'))
            for c in range(frames_number): # Loading all animations
                game_image = self.game.load_game_image(f'assets/Enemy/{animation}/{c}.png', self.game.screen_width // 16, self.game.screen_height // 10)
                temp_list.append(game_image)

            self.animation_list.append(temp_list)

        self.image = self.animation_list[self.action][self.index]
        self.rect = pygame.Rect(x, y, self.image.get_width() - self.width_collision, self.image.get_height())
        self.rect.center = (x, y)

    def handle_ai(self, world, particles):
            move = 0
            self.update_animation()
            self.is_alive()
            if(self.shoot_timer > 0):
                self.shoot_timer -= 1

            if(self.alive and self.game.player.alive):
                if(self.idle == False and random.randint(1, 512) == 6):
                    self.update_action(0)
                    self.idle = True
                    self.idle_counter = 50

                if(self.enemy_vision_front.colliderect(self.game.player.rect)):
                    self.update_action(0)
                    self.fire(particles)
                else:
                    if(self.idle == False):
                        if(self.direction == 1):
                            move = 1
                            self.flip = False
                        else:
                            move = -1
                            self.flip = True

                        self.rect.x += move
                        self.update_action(1)
                        self.move_counter += 1
                        self.enemy_vision_front.center = (self.rect.centerx + (self.rect.w * 4.5) * self.direction, self.rect.centery)
                        if(self.move_counter > world.tile_size):
                            self.direction *= -1
                            self.move_counter *= -1
                    else:
                        self.idle_counter -= 1
                        if(self.idle_counter <= 0):
                            self.idle = False

            self.velocity_y += self.game.engine_gravity
            for tile in world.obstacle_list:
                if(tile[1].colliderect(self.rect.x, self.rect.y, self.rect.w, self.rect.h)):
                    self.velocity_y = 0

            self.enemy_vision_front.x += self.game.screen_scroll
            self.rect.x += self.game.screen_scroll
            self.rect.y += self.velocity_y

    def update_animation(self):
        animation_time = 90
        self.image = self.animation_list[self.action][self.index]
        if(pygame.time.get_ticks() - self.time > animation_time):
            self.time = pygame.time.get_ticks()
            self.index += 1

        if(self.index >= len(self.animation_list[self.action])):
            if(self.action == 2):
                self.index = len(self.animation_list[self.action]) - 1
            else:
                self.index = 0

    def update_action(self, new_action):
        if(new_action != self.action):
            self.action = new_action
            self.index = 0
            self.time = pygame.time.get_ticks()

    def is_alive(self):
        if(self.health <= 0):
            self.health = 0
            self.speed = 0
            self.alive = False
            self.update_action(2)

    def fire(self, particles):
        if(self.shoot_timer == 0):
            self.shoot_timer = 15
            bullet = Bullet(self.game, self.rect.centerx + (0.6 * self.rect.size[0] * self.direction), self.rect.centery - self.rect.h // 4, self.direction)
            self.game.enemy_bullets_group.add(bullet)
            particles.add_game_particle("gun", self.rect.centerx + (0.6 * self.rect.size[0]  * self.direction), self.rect.centery - self.rect.h // 4)
            self.game.sounds.play_sound('Gunshot', 0.5)

    def render(self):
        self.game.display.blit(pygame.transform.flip(self.image, self.flip, False), (self.rect.x - self.x_collision, self.rect.y))