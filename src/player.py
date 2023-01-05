# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
#                                                                             #
#                Invasion Engine, Land Invasion's Game Engine                 #
#                            Developer: Carbon                                #
#                                                                             #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

# Imports: #

from src.modules import *
from src.bullet import *
from src.grenade import *
from src.explosion import *

# Player: #

class Player(pygame.sprite.Sprite):
    def __init__(self, game, x, y, speed, ammo, grenades):
        pygame.sprite.Sprite.__init__(self)

        # Game:

        self.game = game

        # Player Settings: 

        self.health = 100
        self.max_health = self.health
        self.x = x
        self.y = y
        self.speed = speed

        # Player Inventory: 
        
        self.current_ammo = 7
        self.game.ammo = ammo
        self.game.grenades = grenades

        # Player Status:

        self.alive = True
        self.shoot = False
        self.throw_grenade = False
        self.grenade_thrown = False

        # Re-loading:

        self.start_reload = False
        self.timer_reload = 0
        self.reload_time = 1000

        # Player Timers:

        self.shoot_timer = 0
        self.time = pygame.time.get_ticks()

        # Player Movement Variables:

        self.direction = 1
        self.jump = False
        self.in_air = False
        self.move_right = False
        self.move_left = False
        self.moving = False
        self.footsteps_playing = False
        self.velocity_y = 0

        # Player Sound:

        self.sound_length = 0
        self.sound_time = pygame.time.get_ticks()

        # Player Animation Variables:

        self.flip = False
        self.animation_list = []
        self.index = 0
        self.action = 0

        # Collision Patches:

        if(self.game.screen_width == 1920):
            self.x_collision = 30
            self.width_collision = 60
        else:
            self.x_collision = 20
            self.width_collision = 40

        # Loading Sprites: #

        animation_types = ['Idle', 'Move', 'Death', 'Jump']
        for animation in animation_types:
            temp_list = []
            frames_number = len(os.listdir(f'assets/Player/{animation}'))
            for c in range(frames_number): # Loading all animations
                game_image = self.game.load_game_image(f'assets/Player/{animation}/{c}.png', self.game.screen_width // 16, self.game.screen_height // 10)
                temp_list.append(game_image)

            self.animation_list.append(temp_list)

        self.image = self.animation_list[self.action][self.index]
        self.rect = pygame.Rect(x, y, self.image.get_width() - self.width_collision, self.image.get_height())
        self.rect.center = (x, y)

    def update(self, world, particles):
        self.update_animation()
        self.is_alive()
        if(self.alive):
            self.game.screen_scroll, world.level_complete = self.move(world, particles)
            self.game.background_scroll -= self.game.screen_scroll
            if(self.shoot_timer > 0):
                self.shoot_timer -= 1

            if(self.shoot == True):
                if(self.game.game_ready):
                    self.fire(particles)

            if(self.throw_grenade == True):
                if(self.throw_grenade and self.grenade_thrown == False and self.game.grenades > 0):
                    grenade = Grenade(self.game, self.rect.centerx, self.rect.top, self.direction)
                    self.game.grenades_group.add(grenade)
                    self.grenade_thrown = True
                    self.game.grenades -= 1
        else:
            self.game.screen_scroll = 0

        if(self.start_reload == False and self.current_ammo == 0 and self.shoot):
            self.timer_reload = pygame.time.get_ticks()
            self.start_reload = True
            if(self.game.ammo == 0):
                self.game.sounds.play_sound('Empty', 0.5)
            else:
                self.game.sounds.play_sound('Reload', 0.5)

        if(self.current_ammo == 0 and self.game.ammo >= 7):
            if(pygame.time.get_ticks() - self.timer_reload > self.reload_time):
                self.current_ammo = 7
                self.game.ammo -= 7
                self.start_reload = False

        if(self.current_ammo == 0 and self.game.ammo <= 7):
                if(pygame.time.get_ticks() - self.timer_reload > self.reload_time):
                    self.current_ammo = self.game.ammo
                    self.game.ammo -= self.game.ammo
                    self.start_reload = False

    def move(self, world, particles):
        if(pygame.key.get_pressed()[pygame.K_ESCAPE] and self.game.game_ready):
            self.game.menu_on = True

        if(pygame.key.get_pressed()[pygame.K_d]):
            self.move_right = True
            self.moving = True
            self.update_action(1)

        if(pygame.key.get_pressed()[pygame.K_q]):
            self.move_left = True
            self.moving = True
            self.update_action(1)

        if(pygame.key.get_pressed()[pygame.K_SPACE] and self.alive and self.in_air == False):
            self.jump = True

        if(pygame.mouse.get_pressed()[0]):
            self.shoot = True

        if(pygame.mouse.get_pressed()[2]):
            self.throw_grenade = True

        if(not pygame.key.get_pressed()[pygame.K_d]):
                self.move_right = False

        if(not pygame.key.get_pressed()[pygame.K_q]):
                self.move_left = False

        if(not pygame.key.get_pressed()[pygame.K_q] and not pygame.key.get_pressed()[pygame.K_d]):
            self.moving = False
            self.update_action(0)

        if(not pygame.mouse.get_pressed()[0]):
            self.shoot = False

        if(not pygame.mouse.get_pressed()[2]):
            self.throw_grenade = False
            self.grenade_thrown = False

        if(self.sound_length == round(pygame.mixer.Sound.get_length(self.game.sounds.sounds['Footsteps']))):
            self.game.sounds.play_sound('Footsteps', 0.2)
            self.sound_length = 0

        if(pygame.time.get_ticks() - self.sound_time > 1000):
            self.sound_length += 1
            self.sound_time = pygame.time.get_ticks()

        if(self.moving):
            if(not self.footsteps_playing):
                self.game.sounds.play_sound('Footsteps', 0.2)
                self.footsteps_playing = True

        if(not self.moving):
            self.footsteps_playing = False
            self.game.sounds.stop_sound('Footsteps')

        delta_x = 0
        delta_y = 0
        screen_scroll = 0
        if(self.move_left):
            delta_x = -self.speed
            self.flip = True
            self.direction = -1

        if(self.move_right):
            delta_x = self.speed
            self.flip = False
            self.direction = 1

        if(self.jump == True and self.in_air == False):
            if(self.game.screen_width == 1920):
                self.velocity_y = -(world.tile_size // 3.6)
            else:
                self.velocity_y = -(world.tile_size // 3.4)

            self.jump = False
            self.in_air = True
            particles.add_game_particle("jump", self.rect.centerx, self.rect.bottom)
            random_number = random.randint(1, 2)
            self.game.sounds.play_sound(f'Jump{random_number}', 0.2)

        if(self.in_air):
            self.footsteps_playing = False
            self.game.sounds.stop_sound('Footsteps')
            self.update_action(3)

        self.velocity_y += self.game.engine_gravity
        delta_y += self.velocity_y
        for tile in world.obstacle_list:
            if(tile[1].colliderect(self.rect.x + delta_x, self.rect.y, self.rect.w, self.rect.h)):
                delta_x = 0

            if(tile[1].colliderect(self.rect.x, self.rect.y + delta_y, self.rect.w, self.rect.h)):
                if(self.velocity_y < 0):
                    self.velocity_y = 0
                    delta_y = tile[1].bottom - self.rect.top

                elif(self.velocity_y >= 0):
                    self.velocity_y = 0

                    if(self.in_air):
                        random_number = random.randint(1, 2)
                        self.game.sounds.play_sound(f'Fall{random_number}', 0.2)
                        self.in_air = False
                    delta_y = tile[1].top - self.rect.bottom

        if(self.rect.bottom > self.game.screen_width):
            self.health = 0

        level_complete = False
        if(pygame.sprite.spritecollide(self, self.game.exits_group, False)):
            level_complete = True
            world.update_game_level()

        if(self.rect.left + delta_x < 0 or self.rect.right + delta_x > self.game.screen_width):
            delta_x = 0

        self.rect.x += delta_x
        self.rect.y += delta_y
        if((self.rect.right > self.game.screen_width - self.game.scroll_thresh and self.game.background_scroll < (world.level_length * world.tile_size) - self.game.screen_width) or (self.rect.left < self.game.scroll_thresh and self.game.background_scroll > abs(delta_x))):
            self.rect.x -= delta_x
            screen_scroll = -delta_x

        return screen_scroll, level_complete

    def update_animation(self):
        if(self.move_left or self.move_right):
            animation_time = 80
        else:
            animation_time = 140

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
        if(not self.move_right and not self.move_left and not self.in_air):
            if(self.shoot_timer == 0 and self.current_ammo > 0):
                self.shoot_timer = 15
                bullet = Bullet(self.game, self.rect.centerx + (0.6 * self.rect.size[0] * self.direction), self.rect.centery - self.rect.h // 4, self.direction)
                self.game.player_bullets_group.add(bullet)
                self.current_ammo -= 1
                particles.add_game_particle("gun", self.rect.centerx + (0.6 * self.rect.size[0]  * self.direction), self.rect.centery - self.rect.h // 4)
                self.game.sounds.play_sound('Gunshot', 0.5)

    def render(self):
        self.game.display.blit(pygame.transform.flip(self.image, self.flip, False), (self.rect.x - self.x_collision, self.rect.y))
        pygame.draw.rect(self.game.display, (250, 0, 0), (self.game.screen_width // 3, self.game.screen_height // 18, (self.rect.w * 3), self.game.screen_width // 80), border_radius = self.game.screen_width // 128)
        pygame.draw.rect(self.game.display, (0, 250, 0), (self.game.screen_width // 3, self.game.screen_height // 18, (self.rect.w * 3) * (self.health / self.max_health), self.game.screen_width // 80), border_radius = self.game.screen_width // 128)
        pygame.draw.rect(self.game.display, (0, 0, 0), (self.game.screen_width // 3, self.game.screen_height // 18, (self.rect.w * 3), self.game.screen_width // 80), self.game.screen_width // (self.game.screen_width // 4), border_radius = self.game.screen_width // 128)
