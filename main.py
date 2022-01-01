# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
#                                                                             #
#                        Land Invasion, shooter video game                    #
#                              Developer: Carbon               				  #
#                                                                             #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

# Imports: #

from engine import *

# Game Variables: #

mainMenu = True

# Game Assets: #

# Background:
mountain = loadStaticImage('assets/Background/Mountain.png')
trees = loadStaticImage('assets/Background/Pines.png')
sky = loadStaticImage('assets/Background/Sky.png')

# Pickups:
healthPickup = loadGameImage('assets/Pickups/Health_Pickup.png', 32, 32)
grenadePickup = loadGameImage('assets/Pickups/Grenade_Pickup.png', 32, 32)
bulletPickup = loadGameImage('assets/Pickups/Bullet_Pickup.png', 32, 32)
loadGamePickups(healthPickup, grenadePickup, bulletPickup)

# Buttons:
play = loadGameImage('assets/Buttons/Play.png', 300, 300)
exit = loadGameImage('assets/Buttons/Exit.png', 300, 300)
again = loadStaticImage('assets/Buttons/Again.png')

# Game Window: #

window = Window(1024, 768, "Land Invasion:")
window.init()

# World: #
world = World()
world.processData(worldData)

# Buttons: #
playButton = Button(window.screenWidth // 2 - 140, window.screenHeight // 2 - 300, play)
exitButton = Button(window.screenWidth // 2 - 140, window.screenHeight // 2 - 100, exit)
againButton = Button(windowWidth // 2 - 130, windowHeight // 2 - 100, again)

# Game Loop: #

while(window.engineRunning):
	window.limitFPS(60)
	window.setBackground(sky, mountain, trees, 0, 0)
	if(mainMenu == True):
		if(playButton.draw(window.engineWindow)):
			mainMenu = False

		if(exitButton.draw(window.engineWindow)):
			window.engineRunning = False
	else:
		updateGameMechanics(window.engineWindow, world)
		drawGameSprites(window.engineWindow, world)
	window.updateDisplay()
window.quit()