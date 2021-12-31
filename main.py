# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
#                                                                             #
#                        Land Invasion, shooter video game                    #
#                              Developer: Carbon               				  #
#                                                                             #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

# Imports: #

from engine import *

# Game Assets: #

mountain = pygame.image.load('assets/Background/Mountain.png')
trees = pygame.image.load('assets/Background/Pines.png')
sky = pygame.image.load('assets/Background/Sky.png')

# Game Window: #

window = Window(1024, 768, "Land Invasion:")
window.init()

# World: #
world = World()
world.processData(worldData)

# Game Loop: #

while(window.engineRunning):
	window.limitFPS(60)
	window.setBackground(sky, mountain, trees, 0, 0)
	world.draw(window.engineWindow)
	window.updateDisplay()
window.quit()