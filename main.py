# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
#                                                                             #
#                        Land Invasion, shooter video game                    #
#                              Developer: Carbon               				  #
#                                                                             #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

# Imports: #

from engine import *

# Game Assets: #

mountain = loadStaticImage('assets/Background/Mountain.png')
trees = loadStaticImage('assets/Background/Pines.png')
sky = loadStaticImage('assets/Background/Sky.png')
healthPickup = loadGameImage('assets/Pickups/Health_Pickup.png', 32, 32)
grenadePickup = loadGameImage('assets/Pickups/Grenade_Pickup.png', 32, 32)
bulletPickup = loadGameImage('assets/Pickups/Bullet_Pickup.png', 32, 32)
loadGamePickups(healthPickup, grenadePickup, bulletPickup)

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
	updateGameMechanics(window.engineWindow, world)
	drawGameSprites(window.engineWindow, world)
	window.updateDisplay()
window.quit()