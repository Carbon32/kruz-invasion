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
levelSelector = True

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
again = loadGameImage('assets/Buttons/Again.png', 300, 300)

# Level Selector: 
lvl1 = loadGameImage('assets/Buttons/Lvl_1.png', 100, 100)
lvl2 = loadGameImage('assets/Buttons/Lvl_2.png', 100, 100)
lvl3 = loadGameImage('assets/Buttons/Lvl_3.png', 100, 100)
lvl4 = loadGameImage('assets/Buttons/Lvl_4.png', 100, 100)
lvl5 = loadGameImage('assets/Buttons/Lvl_5.png', 100, 100)
lvl6 = loadGameImage('assets/Buttons/Lvl_6.png', 100, 100)
lvl7 = loadGameImage('assets/Buttons/Lvl_7.png', 100, 100)
lvl8 = loadGameImage('assets/Buttons/Lvl_8.png', 100, 100)


# Music:
# playMusic("sounds/music.mp3", 0.1)

# Sounds:
gunshot = loadGameSound("sounds/shoot.mp3", 0.2)
jump = loadGameSound("sounds/jump.wav", 0.2)
explosion = loadGameSound("sounds/explosion.mp3", 0.2)
healthPick = loadGameSound("sounds/healthPickup.wav", 0.2)
grenadePick = loadGameSound("sounds/grenadePickup.wav", 0.2)
ammoPick = loadGameSound("sounds/ammoPickup.mp3", 0.2)

# Game Window: #

window = Window(1024, 768, "Land Invasion:")
window.init()

# World: #
world = World()
world.processData(worldData)

# Buttons: #
playButton = Button(window.screenWidth // 2 - 140, window.screenHeight // 2 - 300, play)
exitButton = Button(window.screenWidth // 2 - 140, window.screenHeight // 2 - 100, exit)
againButton = Button(window.screenWidth // 2 - 140, window.screenHeight // 2 - 300, again)
level1 = Button(window.screenWidth // 3, window.screenHeight // 2 - 300, lvl1)
level2 = Button(window.screenWidth // 3, window.screenHeight // 2 - 150, lvl2)
level3 = Button(window.screenWidth // 3, window.screenHeight // 2 - 0, lvl3)
level4 = Button(window.screenWidth // 3, window.screenHeight // 2 - -150, lvl4)
level5 = Button(window.screenWidth // 2 + 50, window.screenHeight // 2 - 300, lvl5)
level6 = Button(window.screenWidth // 2 + 50, window.screenHeight // 2 - 150, lvl6)
level7 = Button(window.screenWidth // 2 + 50, window.screenHeight // 2 - 0, lvl7)
level8 = Button(window.screenWidth // 2 + 50, window.screenHeight // 2 - -150, lvl8)

# Fade In:
startFade = Fade(1, ((0, 0, 0)), 5)

# Fade Out:
deathFade = Fade(2, ((0, 0, 0)), 5)

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
		if(levelSelector):
			if(level1.draw(window.engineWindow)):
				setGameLevel(1, world)
				levelSelector = False
			if(level2.draw(window.engineWindow)):
				setGameLevel(2, world)
				levelSelector = False
			if(level3.draw(window.engineWindow)):
				setGameLevel(3, world)
				levelSelector = False
			if(level4.draw(window.engineWindow)):
				setGameLevel(4, world)
				levelSelector = False
			if(level5.draw(window.engineWindow)):
				setGameLevel(5, world)
				levelSelector = False
			if(level6.draw(window.engineWindow)):
				setGameLevel(6, world)
				levelSelector = False
			if(level7.draw(window.engineWindow)):
				setGameLevel(7, world)
				levelSelector = False
			if(level8.draw(window.engineWindow)):
				setGameLevel(8, world)
				levelSelector = False
		else:
			if(playerLost()):
				deathFade.fade(window.engineWindow, window.screenWidth, window.screenHeight)
				if(againButton.draw(window.engineWindow)):
					restartLevel(world)
			else:
				updateGameLevel(world)
				updateGameMechanics(window.engineWindow, world, gunshot, explosion, jump, healthPick, grenadePick, ammoPick)
				drawGameSprites(window.engineWindow, world)
				startFade.fade(window.engineWindow, window.screenWidth, window.screenHeight)
	window.updateDisplay()
window.quit()