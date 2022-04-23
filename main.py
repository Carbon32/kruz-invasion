# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
#                                                                             #
#                        Land Invasion, shooter video game                    #
#                              Developer: Carbon                              #
#                                                                             #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

# Imports: #

from engine import *

# Game: #

game = Game()

# Resolution: #

resolution = Resolution(game)

# Resoltuion Selection: #

while(resolution.resolutionStatus):

	resolution.updateBackground()

	if(resolution.resolutionA.render()):

		resolution.setResolution(1920, 1080)
		break

	if(resolution.resolutionB.render()):

		resolution.setResolution(1280, 720)
		break

	resolution.updateWindow()

# Create Window: #

game.startWindow()

# World: #

world = World(game)

# Map: #

world.loadGameMap('levels/level1.txt')

# Game Loop: #

def main():

	while(game.engineRunning):

		# Player: 

		game.renderPlayer(world)

		# Map:

		world.renderTiles()

		# Update Display:

		game.updateDisplay(60)

	# Quit: #

	destroyGame()

main()