# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
#                                                                             #
#                Invasion Engine, Land Invasion's Game Engine                 #
#                            Developer: Carbon                                #
#                                                                             #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

# Imports: #

from src.modules import *
from src.object import *
from src.pickup import *
from src.player import *
from src.enemy import *

# World: #

class World():
    def __init__(self, game):

        # Game:

        self.game = game

        # Level Settings:

        self.level_rows = 16
        self.level_columns = 150
        self.level_complete = False

        # Tiles Settings:

        self.available_tiles = []
        self.tile_size = self.game.screen_width // 32

        # World Settings:

        self.world_data = []

        # World Objects:

        self.obstacle_list = []

    def load_tiles(self):
        for c in range(len(os.listdir('assets/Tiles'))):
            image = self.game.load_game_image(f'assets/Tiles/{c}.png', self.tile_size, self.tile_size)
            self.available_tiles.append(image)

    def set_game_level(self, game_level):
        self.game.seconds = [0, 0]
        self.game.minutes = [0, 0]
        if(game_level > 6):
            game_level = 1

        # Generate An Empty World:

        for r in range(self.level_rows):
            row = [-1] * self.level_columns
            self.world_data.append(row)

        self.game.remove_all_sprites()

        # Load a new level:

        with open(f'levels/level{game_level}.csv', newline='') as csvfile:
            reader = csv.reader(csvfile, delimiter=',')
            for x, row in enumerate(reader):
                for y, tile in enumerate(row):
                    self.world_data[x][y] = int(tile)

        # Update Level Variables:

        self.game.level = game_level

        # Handle Objects:

        self.obstacle_list = []
        self.generate_world()

    def update_game_level(self):
        if(self.level_complete):
            self.game.level += 1
            self.game.background_scroll = 0
            self.game.screen_scroll = 0
            self.set_game_level(self.game.level)

    def restart_level(self):
        self.game.background_scroll = 0
        self.set_game_level(self.game.level)

    def generate_world(self):
        self.level_length = len(self.world_data[0])
        for y, row in enumerate(self.world_data):
            for x, t in enumerate(row):
                if(t >= 0):
                    tile = self.available_tiles[t]
                    tile_rect = tile.get_rect()
                    tile_rect.x = x * self.tile_size
                    tile_rect.y = (y * self.tile_size) + (self.game.screen_width // 16)
                    tile_data = (tile, tile_rect)
                    if(t >= 0 and t <= 20):
                        self.obstacle_list.append(tile_data)

                    if(t > 20 and t <= 45):
                        object = Object(self.game, self.tile_size, tile, x * self.tile_size, (y * self.tile_size) + (self.game.screen_width // 16))
                        self.game.objects_group.add(object)

                    # Pickup (Ammo):
                    elif(t == 46):
                        ammo_pickup = Pickup(self.game, self.tile_size, 'Ammo', x * self.tile_size, (y * self.tile_size) + (self.game.screen_width // 16))
                        self.game.pickups_group.add(ammo_pickup)

                    # Pickup (Grenades):
                    elif(t == 47):
                        grenade_pickup = Pickup(self.game, self.tile_size, 'Grenade', x * self.tile_size, (y * self.tile_size) + (self.game.screen_width // 16))
                        self.game.pickups_group.add(grenade_pickup)

                    # Pickup (Health)
                    elif(t == 48):
                        health_pickup = Pickup(self.game, self.tile_size, 'Health', x * self.tile_size, (y * self.tile_size) + (self.game.screen_width // 16))
                        self.game.pickups_group.add(health_pickup)

                    # Player:
                    elif(t == 49):
                        self.game.player = Player(self.game, x * self.tile_size, (y * self.tile_size) + (self.game.screen_width // 16), self.game.screen_width // 300, 21, 3)

                    # Enemy:
                    elif(t == 50):
                        game_enemy = Enemy(self.game, x * self.tile_size, (y * self.tile_size) + (self.game.screen_width // 16), 1)
                        self.game.enemy_group.add(game_enemy)

                    # Exit: 
                    elif(t == 51):
                        exit = Object(self.game, self.tile_size, tile, x * self.tile_size, (y * self.tile_size) + (self.game.screen_width // 16))
                        self.game.exits_group.add(exit)

    def render(self):
        for tile in self.obstacle_list:
            tile[1][0] += self.game.screen_scroll
            self.game.display.blit(tile[0], tile[1])