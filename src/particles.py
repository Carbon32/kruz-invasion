# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
#                                                                             #
#                Invasion Engine, Land Invasion's Game Engine                 #
#                            Developer: Carbon                                #
#                                                                             #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

# Imports: #

from src.modules import *

# Particles: #

class Particles():
    def __init__(self, game):

        # Display:

        self.game = game

        # Particles List:

        self.particles = {
            'run_particles' : [],
            'blood_particles' : [],
            'gun_particles' : [],
            'jump_particles' : [],
            'explosion_particles' : []
        }

    def add_game_particle(self, particle_type : str, x : int, y : int):
        particle_type.lower()
        if(particle_type == "gun"):
            self.particles['gun_particles'].append([[x, y], [random.randint(-4, 4), -0.8], random.randint(4, 6)])

        elif(particle_type == "blood"):
            self.particles['blood_particles'].append([[x, y], [random.randint(-3, 3), -1], random.randint(6, 8)])

        elif(particle_type == "jump"):
            self.particles['jump_particles'].append([[x, y], [0, -2], random.randint(6, 8)])

        elif(particle_type == "explosion"):
            self.particles['explosion_particles'].append([[x, y], [random.randint(-4, 4), -10], 40])

        else:
            print(f"Cannot find {particle_type} in the game particles list. The particle won't be displayed.")

    def draw_particles(self, particle_type, color):
        try:
            if(self.game.effects):
                for particle in self.particles[particle_type]:
                    particle[0][0] += particle[1][0] + self.game.screen_scroll
                    particle[0][1] += particle[1][1]
                    particle[2] -= 0.1
                    pygame.draw.circle(self.game.display, color, [int(particle[0][0]), int(particle[0][1])], int(particle[2]))
                    if(particle[2] <= 0):
                        self.particles[particle_type].remove(particle)
        except KeyError:
            print(f"Cannot find {particle_type} in the game particles list. The particle won't be displayed.")

    def draw_game_particles(self):
        self.draw_particles("gun_particles", (128, 128, 128))
        self.draw_particles("explosion_particles", (128, 128, 128))
        self.draw_particles("blood_particles", (255, 0, 0))
        self.draw_particles("jump_particles", (160, 82, 45))