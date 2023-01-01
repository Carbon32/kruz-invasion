# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
#                                                                             #
#                Invasion Engine, Land Invasion's Game Engine                 #
#                            Developer: Carbon                                #
#                                                                             #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

# Imports: #

from src.modules import *

# Game: #

class Game():
    def __init__(self):

        # Display:

        self.screen_width = 1920
        self.screen_height = 1080
        self.engine_running = False
        self.fps_handler = pygame.time.Clock()
        self.game_ready = False
        self.level_started = False

        # Menu Status:

        self.menu_on = True

        # Editor Status:

        self.editor_status = False

        # Ambience:

        self.music_started = False

        # Game Time:

        self.change_time = False
        self.time_update = pygame.time.get_ticks()
        self.seconds = [0, 0]
        self.minutes = [0, 0]

        # Scroll:

        self.scroll_thresh = 300
        self.screen_scroll = 0
        self.background_scroll = 0

        # Graphics:

        self.effects = True

        # Pickups:

        self.pickups = {}

        # Level:

        self.level = 1

        # Player Settings:

        self.ammo = 0
        self.grenades = 0

        # Sprite Groups:

        self.player_bullets_group = pygame.sprite.Group()
        self.enemy_bullets_group = pygame.sprite.Group()
        self.grenades_group = pygame.sprite.Group()
        self.explosion_group = pygame.sprite.Group()
        self.enemy_group = pygame.sprite.Group()
        self.objects_group = pygame.sprite.Group()
        self.pickups_group = pygame.sprite.Group()
        self.exits_group = pygame.sprite.Group()

    def start_game(self):
        self.game_ready = True

    def start_level(self):
        self.level_started = True
        if(self.player.alive):
            self.change_time = True
        else:
            self.change_time = False

        if(not self.music_started):
            self.sounds.play_music('sounds/background/wild_ambience.ogg', 0.1)
            self.music_started = True

    def set_game_icon(self, path):
        icon = pygame.image.load(path)
        pygame.display.set_icon(icon)

    def start_window(self, sounds):
        self.display = pygame.display.set_mode((self.screen_width, self.screen_height), pygame.FULLSCREEN | pygame.DOUBLEBUF)
        pygame.display.set_caption("Land Invasion: ")
        self.engine_running = True
        self.engine_gravity = (self.screen_width // 300) * 0.1
        self.sounds = sounds

    def remove_all_sprites(self):
        self.enemy_group.empty()
        self.player_bullets_group.empty()
        self.enemy_bullets_group.empty()
        self.grenades_group.empty()
        self.explosion_group.empty()
        self.pickups_group.empty()
        self.objects_group.empty()
        self.exits_group.empty()

    def set_background(self, sprite_manager):
        self.display.fill((130, 181, 210))
        for x in range(10):
            self.display.blit(sprite_manager.sky, ((x * sprite_manager.sky.get_width()) - self.background_scroll * 0.5, 0))
            self.display.blit(sprite_manager.mountain, ((x * sprite_manager.sky.get_width()) - self.background_scroll * 0.7, self.screen_height - sprite_manager.mountain.get_height() - 300))
            self.display.blit(sprite_manager.trees, ((x * sprite_manager.sky.get_width()) - self.background_scroll * 0.9, self.screen_height - sprite_manager.trees.get_height() - 150))
            self.display.blit(sprite_manager.trees, ((x * sprite_manager.sky.get_width()) - self.background_scroll * 1, self.screen_height - sprite_manager.trees.get_height()))

    def update_display(self, fps):
        self.fps_handler.tick(fps)
        if(self.change_time):
            if(pygame.time.get_ticks() - self.time_update > 1):
                self.seconds[1] += 1
                if(self.seconds[1] == 9 and self.seconds[0] != 5):
                    self.seconds[0] += 1
                    self.seconds[1] = 0

                if(self.seconds[0] == 5 and self.seconds[1] == 9):
                    self.minutes[1] += 1
                    self.seconds[0] = 0
                    self.seconds[1] = 0

                if(self.minutes[1] == 9):
                    self.minutes[0] += 1
                    self.minutes[1] = 0

            self.time_update = pygame.time.get_ticks()

        for event in pygame.event.get():
            if(event.type == pygame.QUIT):
                self.engine_running = False

        pygame.display.update()

    def load_game_sound(self, path):
        sound = pygame.mixer.Sound(path)
        return sound

    def load_game_image(self, path, width, height):
        image = pygame.image.load(path).convert_alpha()
        image = pygame.transform.scale(image, (width, height))
        return image

    def load_static_image(self, path):
        image = pygame.image.load(path).convert_alpha()
        return image

    def draw_text(self, text, size, color, x, y):
        image = pygame.font.SysFont('System', size).render(text, True, color)
        self.display.blit(image, (x, y))
        
    def update_game_mechanics(self, world, particles):
        self.player.update(world, particles)
        for enemy in self.enemy_group:
            enemy.handle_ai(world, particles)

        for bullet in self.player_bullets_group:
            bullet.update(world, particles)

        for bullet in self.enemy_bullets_group:
            bullet.update(world, particles)

        for grenade in self.grenades_group:
            grenade.update(world, particles)

        for explosion in self.explosion_group:
            explosion.update()

        for pickup in self.pickups_group:
            pickup.update()

        for object in self.objects_group:
            object.update()

        for exit in self.exits_group:
            exit.update()

    def draw_game_sprites(self, world, ui):
            world.render()
            for object in self.objects_group:
                object.render()

            for pickup in self.pickups_group:
                pickup.render()

            for exit in self.exits_group:
                exit.render()

            for enemy in self.enemy_group:
                enemy.render()

            for bullet in self.player_bullets_group:
                bullet.render()

            for bullet in self.enemy_bullets_group:
                bullet.render()

            for grenade in self.grenades_group:
                grenade.render()

            for explosion in self.explosion_group:
                explosion.render()

            self.player.render()
            ui.draw_stats()
