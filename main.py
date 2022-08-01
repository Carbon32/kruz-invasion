# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
#                                                                             #
#                        Land Invasion, shooter video game                    #
#                              Developer: Carbon               				  #
#                                                                             #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

# Imports: #

from engine import *

# Game: #

game = Game()

# Sounds: #

sounds = Sounds()

# Resolution: #

resolution = Resolution(game)

# Resoltuion Selection: #

while(resolution.resolutionStatus):

    resolution.updateBackground()

    if(resolution.resolutionA.render()):

        resolution.setResolution(1280, 720)
        break

    if(resolution.resolutionB.render()):

        resolution.setResolution(1920, 1080)

        break

    resolution.updateWindow()

# Graphics: #

graphics = Graphics(game)

# Graphics Selection: #

while(graphics.graphicsStatus):

    graphics.updateBackground()

    if(graphics.effects.render()):

        graphics.setEffects()

    if(graphics.start.render()):

        break

    graphics.updateWindow()

# Start Window:

game.startWindow(sounds)

# World:

world = World(game)

# Assets Manager:

assetsManager = AssetsManager(game)

# Menu: #

menu = Menu(game, assetsManager)

# Editor:

editor = Editor(game, world, assetsManager, menu)

# User Interface:

ui = UserInterface(game)

# Particles:

particles = Particles(game)

# Game Icon: 

game.setGameIcon('assets/Player/Idle/0.png')

# Tiles:

assetsManager.loadPickups()
world.loadTiles()

# World: #

world.setGameLevel(1)

# Fade In:

gameFade = Fade(game, 1, ((0, 0, 0)))

# Game Loop: #

while(game.engineRunning):

	game.setBackground(assetsManager)

	if(game.menuOn):

		menu.handleMenu(world)
		gameFade.reset()

	else:

		if(game.editorStatus):

			editor.generateEditorWorld()
			editor.drawWorld()
			editor.drawGrid()
			editor.drawUserInterface()
			editor.drawInformation()
			editor.handleButtons()
			if(gameFade.fade()):

				editor.handleEditor()

		else:

			game.updateGameMechanics(game, world, particles)
			game.drawGameSprites(game, world, ui)
			particles.drawParticles(game)
			menu.checkDeath(world)
			if(gameFade.fade()):

				game.startGame()
				game.startLevel()

	game.updateDisplay(60)