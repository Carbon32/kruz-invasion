# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
#                                                                             #
#                Invasion Engine, Land Invasion's Game Engine                 #
#                            Developer: Carbon               				  #
#                                                                             #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

# Imports: #

try:
	import pygame 
	import math
	import random
	import os
	import csv
	from pygame import mixer

except ImportError:
	raise ImportError("The Invasion Engine couldn't import all of the necessary packages.")

# Pygame Initialization: #

pygame.init()

# Mixer Initialization: #

pygame.mixer.pre_init(44100, 16, 2, 4096)
mixer.init()

# Engine Functions: #

def loadGameSound(path : str):
	sound = pygame.mixer.Sound(path)
	return sound

def loadGameImage(path : str, width : int, height : int):
	image = pygame.image.load(path).convert_alpha()
	image = pygame.transform.scale(image, (width, height))
	return image

def loadStaticImage(path : str):
	image = pygame.image.load(path).convert_alpha()
	return image

def drawText(display : pygame.Surface, text : str, size : int, color : tuple, x : int, y : int):
	image = pygame.font.SysFont('System', size).render(text, True, color)
	display.blit(image, (x, y))

def playerLost(game):
	if(game.player.health <= 0):
		return True

# Game: #

class Game():
	def __init__(self):

		# Display:

		self.screenWidth = 1920
		self.screenHeight = 1080
		self.engineRunning = False
		self.fpsHandler = pygame.time.Clock()
		self.gameReady = False
		self.levelStarted = False

		# Menu Status:

		self.menuOn = True

		# Editor Status:

		self.editorStatus = False

		# Ambience:

		self.musicStarted = False

		# Game Time:

		self.changeTime = False
		self.timeUpdate = pygame.time.get_ticks()
		self.seconds = [0, 0]
		self.minutes = [0, 0]

		# Scroll:

		self.scrollThresh = 300
		self.screenScroll = 0
		self.backgroundScroll = 0

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

		self.playerBulletGroup = pygame.sprite.Group()
		self.enemyBulletGroup = pygame.sprite.Group()
		self.grenadeGroup = pygame.sprite.Group()
		self.explosionGroup = pygame.sprite.Group()
		self.enemyGroup = pygame.sprite.Group()
		self.objectsGroup = pygame.sprite.Group()
		self.pickupsGroup = pygame.sprite.Group()
		self.exitsGroup = pygame.sprite.Group()

	def startGame(self):

		self.gameReady = True

	def startLevel(self):

		self.levelStarted = True
		if(self.player.alive):
			self.changeTime = True
		else:
			self.changeTime = False

		if(not self.musicStarted):
			self.sounds.playMusic('sounds/background/wild_ambience.ogg', 0.1)
			self.musicStarted = True

	def setGameIcon(self, path : str):
		icon = pygame.image.load(path)
		pygame.display.set_icon(icon)

	def startWindow(self, sounds):
		self.display = pygame.display.set_mode((self.screenWidth, self.screenHeight), pygame.FULLSCREEN | pygame.DOUBLEBUF)
		pygame.display.set_caption("Land Invasion: ")
		self.engineRunning = True
		self.engineGravity = (self.screenWidth // 300) * 0.1
		self.sounds = sounds

	def removeAllSprites(self):
		self.enemyGroup.empty()
		self.playerBulletGroup.empty()
		self.enemyBulletGroup.empty()
		self.grenadeGroup.empty()
		self.pickupsGroup.empty()
		self.objectsGroup.empty()
		self.exitsGroup.empty()

	def setBackground(self, spriteManager):
		self.display.fill((130, 181, 210))

		for x in range(10):
			self.display.blit(spriteManager.sky, ((x * spriteManager.sky.get_width()) - self.backgroundScroll * 0.5, 0))
			self.display.blit(spriteManager.mountain, ((x * spriteManager.sky.get_width()) - self.backgroundScroll * 0.7, self.screenHeight - spriteManager.mountain.get_height() - 300))
			self.display.blit(spriteManager.trees, ((x * spriteManager.sky.get_width()) - self.backgroundScroll * 0.9, self.screenHeight - spriteManager.trees.get_height() - 150))
			self.display.blit(spriteManager.trees, ((x * spriteManager.sky.get_width()) - self.backgroundScroll * 1, self.screenHeight - spriteManager.trees.get_height()))

	def updateDisplay(self, fps : int):
		self.fpsHandler.tick(fps)

		if(self.changeTime):
			if(pygame.time.get_ticks() - self.timeUpdate > 1):
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

				

			self.timeUpdate = pygame.time.get_ticks()

		for event in pygame.event.get():

			if(event.type == pygame.QUIT):

				self.engineRunning = False

		pygame.display.update()

	def updateGameMechanics(self, game, world, particles):

		game.player.update(world, particles)

		for enemy in self.enemyGroup:
				
			enemy.handleAI(world, particles)

		for bullet in self.playerBulletGroup:

			bullet.update(world, particles)

		for bullet in self.enemyBulletGroup:

			bullet.update(world, particles)

		for grenade in self.grenadeGroup:

			grenade.update(world, particles)

		for explosion in self.explosionGroup:

			explosion.update()

		for pickup in self.pickupsGroup:

			pickup.update()

		for object in self.objectsGroup:

			object.update()

		for exit in self.exitsGroup:

			exit.update()

	def drawGameSprites(self, game, world, ui):

			world.render()

			for object in self.objectsGroup:

				object.draw(self.display)

			for pickup in self.pickupsGroup:

				pickup.draw(self.display)

			for exit in self.exitsGroup:

				exit.draw(self.display)

			for enemy in self.enemyGroup:

				enemy.draw(self.display)

			for bullet in self.playerBulletGroup:

				bullet.draw(self.display)

			for bullet in self.enemyBulletGroup:

				bullet.draw(self.display)

			for grenade in self.grenadeGroup:

				grenade.draw(self.display)

			for explosion in self.explosionGroup:

				explosion.draw(self.display)

			game.player.draw(self.display)


			ui.drawStats()

# Menu: #

class Menu():
	def __init__(self, game, assetsManager):

		# Game:

		self.game = game

		# Assets Manager:

		self.assetsManager = assetsManager

		# Menu:

		self.mainMenu = True

		# Level Designs:

		self.levelDesigns = []
		for i in range(len(os.listdir('assets/levels/'))):
			self.levelDesigns.append(loadGameImage(f'assets/levels/level{i}.png', self.game.screenWidth // 2, self.game.screenHeight // 2))

		# Level Selector:

		self.levelSelector = True
		self.selectedLevel = 0
		self.border = pygame.Rect(0, 0, 0, 0)

		# Buttons: #

		self.playButton = Button(self.game.display, self.game.screenWidth // 2 - (self.game.screenWidth // 14), self.game.screenHeight // 2 - (self.game.screenHeight // 3), self.assetsManager.buttons["Play"])
		self.editorButton = Button(self.game.display, self.game.screenWidth // 2 - (self.game.screenWidth // 14), self.game.screenHeight // 2 - (self.game.screenHeight // 6), self.assetsManager.buttons["Editor"])
		self.exitButton = Button(self.game.display, self.game.screenWidth // 2 - (self.game.screenWidth // 14), self.game.screenHeight // 6 + (self.game.screenHeight // 3), self.assetsManager.buttons["Exit"])
		self.againButton = Button(self.game.display, self.game.screenWidth // 2 - (self.game.screenWidth // 14), self.game.screenHeight // 2 - (self.game.screenHeight // 4), self.assetsManager.buttons["Again"])
		self.selectButton = Button(self.game.display, self.game.screenWidth // 4 + (self.game.screenWidth // 4), self.game.screenHeight // 2 + (self.game.screenHeight // 4), self.assetsManager.buttons["Select"])
		self.backButton = Button(self.game.display, self.game.screenWidth // 2 - (self.game.screenWidth // 14), self.game.screenHeight // 6 + (self.game.screenHeight // 2), self.assetsManager.buttons["Back"])
		self.musicButton = Button(self.game.display, self.game.screenWidth // 2 + (self.game.screenWidth // 2.3), self.game.screenHeight // 2 - (self.game.screenHeight // 2.1), self.assetsManager.buttons["MusicOn"])
		self.soundButton = Button(self.game.display, self.game.screenWidth // 2 + (self.game.screenWidth // 2.8), self.game.screenHeight // 2 - (self.game.screenHeight // 2.1), self.assetsManager.buttons["SoundOn"])
		self.level1 = Button(self.game.display, self.game.screenWidth // 10, self.game.screenHeight // 2 - (self.game.screenWidth // 4), self.assetsManager.buttons["Lvl1"])
		self.level2 = Button(self.game.display, self.game.screenWidth // 10, self.game.screenHeight // 2 - (self.game.screenWidth // 6), self.assetsManager.buttons["Lvl2"])
		self.level3 = Button(self.game.display, self.game.screenWidth // 10, self.game.screenHeight // 2 - (self.game.screenWidth // 12), self.assetsManager.buttons["Lvl3"])
		self.level4 = Button(self.game.display, self.game.screenWidth // 10, self.game.screenHeight // 2, self.assetsManager.buttons["Lvl4"])
		self.level5 = Button(self.game.display, self.game.screenWidth // 10, self.game.screenHeight // 2 + (self.game.screenWidth // 12), self.assetsManager.buttons["Lvl5"])
		self.level6 = Button(self.game.display, self.game.screenWidth // 10, self.game.screenHeight // 2 + (self.game.screenWidth // 6), self.assetsManager.buttons["Lvl6"])
	
	def handleMenu(self, world):

		self.updateBackground()

		if(self.game.gameReady):

			self.mainMenu = True
			self.levelSelector = True
			self.game.gameReady = False

		if(self.mainMenu):

			if(self.game.levelStarted):

				if(self.backButton.render()):

					self.levelSelector = False
					self.mainMenu = False
					self.game.menuOn = False

			if(self.playButton.render()):

				self.mainMenu = False
				self.game.levelStarted = False
				self.game.sounds.musicStarted = False
				self.game.sounds.stopMusic()

			if(self.editorButton.render()):

				self.game.editorStatus = True
				self.levelSelector = False
				self.game.menuOn = False
				self.mainMenu = False
				self.game.levelStarted = False
				self.game.sounds.musicStarted = False
				self.game.sounds.stopMusic()

			if(self.musicButton.render()):

				if(self.game.sounds.musicStatus):

					self.musicButton.changeButton(self.assetsManager.buttons["MusicOff"])
					self.game.sounds.musicStatus = False
					self.game.sounds.stopMusic()

				else:

					self.musicButton.changeButton(self.assetsManager.buttons["MusicOn"])
					self.game.sounds.musicStatus = True
					self.game.musicStarted = False

			if(self.soundButton.render()):

				if(self.game.sounds.soundStatus):

					self.soundButton.changeButton(self.assetsManager.buttons["SoundOff"])
					self.game.sounds.soundStatus = False

				else:

					self.soundButton.changeButton(self.assetsManager.buttons["SoundOn"])
					self.game.sounds.soundStatus = True

			if(self.exitButton.render()):

				self.game.engineRunning = False
		else:

			if(self.levelSelector):

				if(self.level1.render()):
					self.selectedLevel = 1
					self.border = pygame.Rect(self.game.screenWidth // 10, self.game.screenHeight // 2 - (self.game.screenWidth // 4), self.game.screenWidth // 8, self.game.screenWidth // 16)

				if(self.level2.render()):
					self.selectedLevel = 2
					self.border = pygame.Rect(self.game.screenWidth // 10, self.game.screenHeight // 2 - (self.game.screenWidth // 6), self.game.screenWidth // 8, self.game.screenWidth // 16)

				if(self.level3.render()):
					self.selectedLevel = 3
					self.border = pygame.Rect(self.game.screenWidth // 10, self.game.screenHeight // 2 - (self.game.screenWidth // 12), self.game.screenWidth // 8, self.game.screenWidth // 16)

				if(self.level4.render()):
					self.selectedLevel = 4
					self.border = pygame.Rect(self.game.screenWidth // 10, self.game.screenHeight // 2, self.game.screenWidth // 8, self.game.screenWidth // 16)
					
				if(self.level5.render()):
					self.selectedLevel = 5
					self.border = pygame.Rect(self.game.screenWidth // 10, self.game.screenHeight // 2 + (self.game.screenWidth // 12), self.game.screenWidth // 8, self.game.screenWidth // 16)

				if(self.level6.render()):
					self.selectedLevel = 6
					self.border = pygame.Rect(self.game.screenWidth // 10, self.game.screenHeight // 2 + (self.game.screenWidth // 6), self.game.screenWidth // 8, self.game.screenWidth // 16)


				if(self.selectButton.render() and self.selectedLevel != 0):
					world.setGameLevel(self.selectedLevel)
					self.levelSelector = False
					self.game.menuOn = False
					self.game.musicStarted = False

				if(self.selectedLevel > len(self.levelDesigns) - 1):

					self.game.display.blit(self.levelDesigns[0], (self.game.screenWidth // 3, self.game.screenHeight // 6))

				else:

					self.game.display.blit(self.levelDesigns[self.selectedLevel], (self.game.screenWidth // 3, self.game.screenHeight // 6))

				pygame.draw.rect(self.game.display, (0, 0, 0), pygame.Rect(self.game.screenWidth // 3, self.game.screenHeight // 6, self.game.screenWidth // 2, self.game.screenHeight // 2), self.game.screenWidth // 128)
				pygame.draw.rect(self.game.display, (150, 255, 0), self.border, self.game.screenWidth // 128)

	def checkDeath(self, world):

		if(playerLost(self.game)):

			self.game.changeTime = False

			if(self.againButton.render()):

				world.restartLevel()

	def updateBackground(self):

		self.game.display.blit(self.assetsManager.menuBackground, (0, 0))

# World: #

class World():
	def __init__(self, game):

		# Game:

		self.game = game

		# Level Settings:

		self.levelRows = 16
		self.levelColumns = 150
		self.levelComplete = False

		# Tiles Settings:

		self.availableTiles = []
		self.tileSize = self.game.screenWidth // 32

		# World Settings:

		self.worldData = []

		# World Objects:

		self.obstacleList = []

	def loadTiles(self):
		for c in range(len(os.listdir('assets/Tiles'))):

			image = loadGameImage(f'assets/Tiles/{c}.png', self.tileSize, self.tileSize)
			self.availableTiles.append(image)

	def setGameLevel(self, gameLevel : int):
		self.game.seconds = [0, 0]
		self.game.minutes = [0, 0]
		if(gameLevel > 6):

			gameLevel = 1

			# Generate An Empty World:

		for r in range(self.levelRows):

			row = [-1] * self.levelColumns
			self.worldData.append(row)

		self.game.removeAllSprites()

		# Load a new level:

		with open(f'levels/level{gameLevel}.csv', newline='') as csvfile:

			reader = csv.reader(csvfile, delimiter=',')

			for x, row in enumerate(reader):

				for y, tile in enumerate(row):

					self.worldData[x][y] = int(tile)

		# Update Level Variables:

		self.game.level = gameLevel

		# Handle Objects:

		self.obstacleList = []
		self.generateWorld()

	def updateGameLevel(self):
		if(self.levelComplete):

			self.game.level += 1
			self.game.backgroundScroll = 0
			self.game.screenScroll = 0
			self.setGameLevel(self.game.level)

	def restartLevel(self):
		self.game.backgroundScroll = 0
		self.setGameLevel(self.game.level)

	def generateWorld(self):
		self.levelLength = len(self.worldData[0])

		for y, row in enumerate(self.worldData):

			for x, t in enumerate(row):

				if(t >= 0):

					tile = self.availableTiles[t]
					tileRect = tile.get_rect()
					tileRect.x = x * self.tileSize
					tileRect.y = (y * self.tileSize) + (self.game.screenWidth // 16)
					tileData = (tile, tileRect)

					if(t >= 0 and t <= 20):

						self.obstacleList.append(tileData)

					if(t > 20 and t <= 45):

						object = Object(self.game, self.tileSize, tile, x * self.tileSize, (y * self.tileSize) + (self.game.screenWidth // 16))
						self.game.objectsGroup.add(object)


					# Pickup (Ammo):
					elif(t == 46):

						ammoPickup = Pickup(self.game, self.tileSize, 'Ammo', x * self.tileSize, (y * self.tileSize) + (self.game.screenWidth // 16))
						self.game.pickupsGroup.add(ammoPickup)

					# Pickup (Grenades):
					elif(t == 47):

						grenadePickup = Pickup(self.game, self.tileSize, 'Grenade', x * self.tileSize, (y * self.tileSize) + (self.game.screenWidth // 16))
						self.game.pickupsGroup.add(grenadePickup)

					# Pickup (Health)
					elif(t == 48):

						healthPickup = Pickup(self.game, self.tileSize, 'Health', x * self.tileSize, (y * self.tileSize) + (self.game.screenWidth // 16))
						self.game.pickupsGroup.add(healthPickup)

					# Player:
					elif(t == 49):

						self.game.player = Player(self.game, x * self.tileSize, (y * self.tileSize) + (self.game.screenWidth // 16), self.game.screenWidth // 300, 21, 3)

					# Enemy:
					elif(t == 50):

						gameEnemy = Enemy(self.game, x * self.tileSize, (y * self.tileSize) + (self.game.screenWidth // 16), 1)
						self.game.enemyGroup.add(gameEnemy)

					# Exit: 
					elif(t == 51):

						exit = Object(self.game, self.tileSize, tile, x * self.tileSize, (y * self.tileSize) + (self.game.screenWidth // 16))
						self.game.exitsGroup.add(exit)

	def render(self):
		for tile in self.obstacleList:

			tile[1][0] += self.game.screenScroll
			self.game.display.blit(tile[0], tile[1])

# Sounds: #

class Sounds():
	def __init__(self):

		# Music:

		self.musicStatus = True

		# Sounds: 

		self.soundStatus = True

		# Available Sounds: 

		self.sounds = {
			'Footsteps' : loadGameSound('sounds/footsteps/footsteps.ogg'), # Added
			'Fall1' : loadGameSound('sounds/fall/fall_1.ogg'), # Added
			'Fall2' : loadGameSound('sounds/fall/fall_2.ogg'), # Added
			'Hit1' : loadGameSound('sounds/hit/hit_1.ogg'), # Added
			'Hit2' : loadGameSound('sounds/hit/hit_2.ogg'), # Added
			'Hit3' : loadGameSound('sounds/hit/hit_3.ogg'), # Added
			'Hit4' : loadGameSound('sounds/hit/hit_4.ogg'), # Added
			'Intro' : loadGameSound('sounds/intro/intro.ogg'),
			'Jump1' : loadGameSound('sounds/jump/jump_1.ogg'), # Added
			'Jump2' : loadGameSound('sounds/jump/jump_2.ogg'), # Added
			'HealthPickup' : loadGameSound('sounds/pickup/health_pickup.ogg'), # Added
			'AmmoPickup' : loadGameSound('sounds/pickup/ammo_pickup.ogg'), # Added
			'GrenadePickup' : loadGameSound('sounds//pickup/grenade_pickup.ogg'), # Added
			'Explosion' : loadGameSound('sounds/weapons/explosion.ogg'), # Added
			'GrenadeFall' : loadGameSound('sounds/weapons/grenade_fall.ogg'), # Added
			'Reload' : loadGameSound('sounds/weapons/handgun_reload.ogg'), # Added
			'Gunshot' : loadGameSound('sounds/weapons/handgun_shoot.ogg'), # Added
			'Empty' : loadGameSound('sounds/weapons/handgun_empty.ogg') # Added
		}

	def playSound(self, sound : str, volume : float):

		if(self.soundStatus):
			self.sounds[sound].set_volume(volume)
			pygame.mixer.Sound.play(self.sounds[sound])

	def stopSound(self, sound : str):

		pygame.mixer.Sound.stop(self.sounds[sound])

	def playMusic(self, music : str, volume : float):
		if(self.musicStatus):
			pygame.mixer.music.load(music)
			pygame.mixer.music.set_volume(volume)
			pygame.mixer.music.play(-1, 0.0, 5000)

	def stopMusic(self):
		pygame.mixer.music.stop()



# Particles: #

class Particles():
	def __init__(self, game : pygame.Surface):

		# Display:

		self.game = game

		# Particles List:

		self.runParticles = []
		self.bloodParticles = []
		self.gunParticles = []
		self.jumpParticles = []
		self.explosionParticles = []

	def addGameParticle(self, particleType : str, x : int, y : int):
		particleType.lower()
		if(particleType == "gun"):
			self.gunParticles.append([[x, y], [random.randint(-4, 4), -0.8], random.randint(4, 6)])

		elif(particleType == "blood"):
			self.bloodParticles.append([[x, y], [random.randint(-3, 3), -1], random.randint(6, 8)])

		elif(particleType == "jump"):
			self.jumpParticles.append([[x, y], [0, -2], random.randint(6, 8)])

		elif(particleType == "explosion"):
			self.explosionParticles.append([[x, y], [random.randint(-4, 4), -10], 40])

		else:
			print(f"Cannot find {particleType} in the game particles list. The particle won't be displayed.")

	def drawGameParticles(self, particleType : str):
		if(self.game.effects):
			if(particleType == "gun"):
				for particle in self.gunParticles:
					particle[0][0] += particle[1][0] + self.game.screenScroll
					particle[0][1] += particle[1][1]
					particle[2] -= 0.1
					pygame.draw.circle(self.game.display, (128, 128, 128), [int(particle[0][0]), int(particle[0][1])], int(particle[2]))
					if(particle[2] <= 0):
						self.gunParticles.remove(particle)

			elif(particleType == "blood"):
				for particle in self.bloodParticles:
					particle[0][0] += particle[1][0] + self.game.screenScroll
					particle[0][1] += particle[1][1]
					particle[2] -= 0.1
					pygame.draw.circle(self.game.display, (255, 0, 0), [int(particle[0][0]), int(particle[0][1])], int(particle[2]))
					if(particle[2] <= 0):
						self.bloodParticles.remove(particle)

			elif(particleType == "jump"):
				for particle in self.jumpParticles:
					particle[0][0] += particle[1][0] + self.game.screenScroll
					particle[0][1] += particle[1][1]
					particle[2] -= 0.1
					pygame.draw.circle(self.game.display, (160, 82, 45), [int(particle[0][0]), int(particle[0][1])], int(particle[2]))
					if(particle[2] <= 0):
						self.jumpParticles.remove(particle)

			elif(particleType == "explosion"):
				for particle in self.explosionParticles:
					particle[0][0] += particle[1][0] + self.game.screenScroll
					particle[0][1] += particle[1][1]
					particle[2] -= 0.1
					pygame.draw.circle(self.game.display, (128, 128, 128), [int(particle[0][0]), int(particle[0][1])], int(particle[2]))
					if(particle[2] <= 0):
						self.explosionParticles.remove(particle)

			else:
				print(f"Cannot find {particleType} in the game particles list. The particle won't be displayed.")

	def drawParticles(self, game):

		self.drawGameParticles("gun")
		self.drawGameParticles("explosion")
		self.drawGameParticles("blood")
		self.drawGameParticles("jump")

# User Interface: #

class UserInterface():
	def __init__(self, game):
		
		# Game:

		self.game = game

	def drawStats(self):
		drawText(self.game.display, f'Ammo: {self.game.player.currentAmmo}/{self.game.ammo}', self.game.screenWidth // 64, (48, 45, 45), self.game.screenWidth // 32, (self.game.screenHeight // 4 - self.game.screenHeight // 5))
		drawText(self.game.display, f'Grenades: {self.game.grenades}', self.game.screenWidth // 64, (48, 45, 45), self.game.screenWidth // 8, (self.game.screenHeight // 4 - self.game.screenHeight // 5))
		drawText(self.game.display, f'Level: {self.game.level}', self.game.screenWidth // 64, (48, 45, 45), self.game.screenWidth // 4, (self.game.screenHeight // 4 - self.game.screenHeight // 5))
		drawText(self.game.display, f'FPS: {int(self.game.fpsHandler.get_fps())}', self.game.screenWidth // 64, (48, 45, 45), self.game.screenWidth // 2, (self.game.screenHeight // 4 - self.game.screenHeight // 5))
		drawText(self.game.display, f'Time: {self.game.minutes[0]}{self.game.minutes[1]}:{self.game.seconds[0]}{self.game.seconds[1]}', self.game.screenWidth // 64, (48, 45, 45), self.game.screenWidth - (self.game.screenWidth // 3), (self.game.screenHeight // 4 - self.game.screenHeight // 5))

# Assets Manager: #

class AssetsManager():
	def __init__(self, game):

		# Game:

		self.game = game

		# Pickup Sprites:

		self.healthPickup = loadGameImage('assets/Pickups/Health_Pickup.png', self.game.screenWidth // 32, self.game.screenWidth // 32)
		self.ammoPickup = loadGameImage('assets/Pickups/Bullet_Pickup.png', self.game.screenWidth // 32, self.game.screenWidth // 32)
		self.grenadePickup = loadGameImage('assets/Pickups/Grenade_Pickup.png', self.game.screenWidth // 32, self.game.screenWidth // 32)

		self.healthPickup2 = loadGameImage('assets/Pickups/Health_Pickup2.png', self.game.screenWidth // 32, self.game.screenWidth // 32)
		self.ammoPickup2 = loadGameImage('assets/Pickups/Bullet_Pickup2.png', self.game.screenWidth // 32, self.game.screenWidth // 32)
		self.grenadePickup2 =  loadGameImage('assets/Pickups/Grenade_Pickup2.png', self.game.screenWidth // 32, self.game.screenWidth // 32)

		self.healthPickup3 = loadGameImage('assets/Pickups/Health_Pickup3.png', self.game.screenWidth // 32, self.game.screenWidth // 32)
		self.ammoPickup3 = loadGameImage('assets/Pickups/Bullet_Pickup3.png', self.game.screenWidth // 32, self.game.screenWidth // 32)
		self.grenadePickup3 =  loadGameImage('assets/Pickups/Grenade_Pickup3.png', self.game.screenWidth // 32, self.game.screenWidth // 32)

		# Background:

		self.mountain = loadStaticImage('assets/Background/Mountain.png')
		self.sky = loadStaticImage('assets/Background/Sky.png')
		self.trees = loadStaticImage('assets/Background/Pines.png')
		self.menuBackground = loadGameImage('assets/Background/Menu.png', self.game.screenWidth, self.game.screenHeight)

		# Buttons:

		self.buttons = {
			"Play" : loadGameImage('assets/Buttons/Play.png', self.game.screenWidth // 6, self.game.screenWidth // 12),
			"Editor" : loadGameImage('assets/Buttons/Editor.png', self.game.screenWidth // 6, self.game.screenWidth // 12),
			"Exit" : loadGameImage('assets/Buttons/Exit.png', self.game.screenWidth // 6, self.game.screenWidth // 12),
			"Again" : loadGameImage('assets/Buttons/Again.png', self.game.screenWidth // 6, self.game.screenWidth // 12),
			"Select" : loadGameImage('assets/Buttons/select.png', self.game.screenWidth // 6, self.game.screenWidth // 12),
			"Save" : loadGameImage('assets/Buttons/Save.png', self.game.screenWidth // 12, self.game.screenWidth // 24),
			"Clear" : loadGameImage('assets/Buttons/Clear.png', self.game.screenWidth // 12, self.game.screenWidth // 24),
			"Back" : loadGameImage('assets/Buttons/Back.png', self.game.screenWidth // 12, self.game.screenWidth // 24),
			"MusicOn" : loadGameImage('assets/Buttons/musicOn.png', self.game.screenWidth // 32, self.game.screenWidth // 32),
			"MusicOff" : loadGameImage('assets/Buttons/musicOff.png', self.game.screenWidth // 32, self.game.screenWidth // 32),
			"SoundOn" : loadGameImage('assets/Buttons/soundOn.png', self.game.screenWidth // 32, self.game.screenWidth // 32),
			"SoundOff" : loadGameImage('assets/Buttons/soundOff.png', self.game.screenWidth // 32, self.game.screenWidth // 32),
			"Lvl1" : loadGameImage('assets/Buttons/Lvl_1.png', self.game.screenWidth // 8, self.game.screenWidth // 16),
			"Lvl2" : loadGameImage('assets/Buttons/Lvl_2.png', self.game.screenWidth // 8, self.game.screenWidth // 16),
			"Lvl3" : loadGameImage('assets/Buttons/Lvl_3.png', self.game.screenWidth // 8, self.game.screenWidth // 16),
			"Lvl4" : loadGameImage('assets/Buttons/Lvl_4.png', self.game.screenWidth // 8, self.game.screenWidth // 16),
			"Lvl5" : loadGameImage('assets/Buttons/Lvl_5.png', self.game.screenWidth // 8, self.game.screenWidth // 16),
			"Lvl6" : loadGameImage('assets/Buttons/Lvl_6.png', self.game.screenWidth // 8, self.game.screenWidth // 16)
		}

	def loadPickups(self):
		self.game.pickups = {
			'Health'	: self.healthPickup,
			'Grenade'	: self.grenadePickup,
			'Ammo'		: self.ammoPickup,
			'HealthShine'	: self.healthPickup3,
			'GrenadeShine'	: self.grenadePickup3,
			'AmmoShine'		: self.ammoPickup3,
			'HealthOpen'		: self.healthPickup2,
			'AmmoOpen'		: self.ammoPickup2,
			'GrenadeOpen'	: self.grenadePickup2

		}

# Player: #

class Player(pygame.sprite.Sprite):
	def __init__(self, game, x : int, y : int, speed : int, ammo : int, grenades : int):
		pygame.sprite.Sprite.__init__(self)

		# Game:

		self.game = game

		# Player Settings: 

		self.health = 100
		self.maxHealth = self.health
		self.x = x
		self.y = y
		self.speed = speed

		# Player Inventory: 
		
		self.currentAmmo = 7
		self.game.ammo = ammo
		self.game.grenades = grenades

		# Player Status:

		self.alive = True
		self.shoot = False
		self.throwGrenade = False
		self.grenadeThrown = False

		# Re-loading:

		self.startReload = False
		self.timerReload = 0
		self.reloadTime = 1000

		# Player Timers:

		self.shootTimer = 0
		self.time = pygame.time.get_ticks()

		# Player Movement Variables:

		self.direction = 1
		self.jump = False
		self.inAir = False
		self.moveRight = False
		self.moveLeft = False
		self.moving = False
		self.footstepsPlaying = False
		self.velocityY = 0

		# Player Animation Variables:

		self.flip = False
		self.animationList = []
		self.index = 0
		self.action = 0

		# Collision Patches:

		if(self.game.screenWidth == 1920):

			self.xcollision = 30
			self.widthCollision = 60

		else:

			self.xcollision = 20
			self.widthCollision = 40

		# Loading Sprites: #

		animationTypes = ['Idle', 'Move', 'Death', 'Jump']
		for animation in animationTypes:

			tempList = []
			framesNumber = len(os.listdir(f'assets/Player/{animation}'))

			for c in range(framesNumber): # Loading all animations

				gameImage = pygame.image.load(f'assets/Player/{animation}/{c}.png').convert_alpha()
				gameImage = pygame.transform.scale(gameImage, (self.game.screenWidth // 16, self.game.screenHeight // 10))
				tempList.append(gameImage)

			self.animationList.append(tempList)

		self.image = self.animationList[self.action][self.index]
		self.rect = pygame.Rect(x, y, self.image.get_width() - self.widthCollision, self.image.get_height())
		self.rect.center = (x, y)

	def update(self, world, particles):
		self.updateAnimation()
		self.isAlive()

		if(self.alive):

			self.game.screenScroll, world.levelComplete = self.move(world, particles)
			self.game.backgroundScroll -= self.game.screenScroll

			if(self.shootTimer > 0):

				self.shootTimer -= 1

			if(self.shoot == True):

				if(self.game.gameReady):

					self.fire(particles)

			if(self.throwGrenade == True):

				if(self.throwGrenade and self.grenadeThrown == False and self.game.grenades > 0):

					grenade = Grenade(self.game, self.rect.centerx, self.rect.top, self.direction)
					self.game.grenadeGroup.add(grenade)
					self.grenadeThrown = True
					self.game.grenades -= 1
		else:

			self.game.screenScroll = 0

		if(self.startReload == False and self.currentAmmo == 0 and self.shoot):

				self.timerReload = pygame.time.get_ticks()
				self.startReload = True
				if(self.game.ammo == 0):

					self.game.sounds.playSound('Empty', 0.5)

				else:

					self.game.sounds.playSound('Reload', 0.5)

		if(self.currentAmmo == 0 and self.game.ammo >= 7):

				if(pygame.time.get_ticks() - self.timerReload > self.reloadTime):

					self.currentAmmo = 7
					self.game.ammo -= 7
					self.startReload = False

		if(self.currentAmmo == 0 and self.game.ammo <= 7):

				if(pygame.time.get_ticks() - self.timerReload > self.reloadTime):

					self.currentAmmo = self.game.ammo
					self.game.ammo -= self.game.ammo
					self.startReload = False

	def move(self, world, particles):

		if(pygame.key.get_pressed()[pygame.K_ESCAPE] and self.game.gameReady):

			self.game.menuOn = True

		if(pygame.key.get_pressed()[pygame.K_d]):

			self.moveRight = True
			self.moving = True
			self.updateAction(1)

		if(pygame.key.get_pressed()[pygame.K_q]):

			self.moveLeft = True
			self.moving = True
			self.updateAction(1)

		if(pygame.key.get_pressed()[pygame.K_SPACE] and self.alive and self.inAir == False):

			self.jump = True

		if(pygame.mouse.get_pressed()[0]):

			self.shoot = True

		if(pygame.mouse.get_pressed()[2]):

			self.throwGrenade = True

		if(not pygame.key.get_pressed()[pygame.K_d]):

				self.moveRight = False

		if(not pygame.key.get_pressed()[pygame.K_q]):

				self.moveLeft = False

		if(not pygame.key.get_pressed()[pygame.K_q] and not pygame.key.get_pressed()[pygame.K_d]):

			self.moving = False
			self.updateAction(0)

		if(not pygame.mouse.get_pressed()[0]):

			self.shoot = False

		if(not pygame.mouse.get_pressed()[2]):

			self.throwGrenade = False
			self.grenadeThrown = False

		if(self.moving):

			if(not self.footstepsPlaying):
				self.game.sounds.playSound('Footsteps', 0.2)
				self.footstepsPlaying = True

		if(not self.moving):

			self.footstepsPlaying = False
			self.game.sounds.stopSound('Footsteps')

		deltaX = 0
		deltaY = 0
		screenScroll = 0

		if(self.moveLeft):

			deltaX = -self.speed
			self.flip = True
			self.direction = -1

		if(self.moveRight):

			deltaX = self.speed
			self.flip = False
			self.direction = 1

		if(self.jump == True and self.inAir == False):

			if(self.game.screenWidth == 1920):

				self.velocityY = -(world.tileSize // 3.6)

			else:

				self.velocityY = -(world.tileSize // 3.4)

			self.jump = False
			self.inAir = True
			particles.addGameParticle("jump", self.rect.centerx, self.rect.bottom)

			randomNumber = random.randint(1, 2)
			self.game.sounds.playSound(f'Jump{randomNumber}', 0.2)

		if(self.inAir):

			self.footstepsPlaying = False
			self.game.sounds.stopSound('Footsteps')
			self.updateAction(3)


		self.velocityY += self.game.engineGravity

		deltaY += self.velocityY

		for tile in world.obstacleList:

			if(tile[1].colliderect(self.rect.x + deltaX, self.rect.y, self.rect.w, self.rect.h)):

				deltaX = 0

			if(tile[1].colliderect(self.rect.x, self.rect.y + deltaY, self.rect.w, self.rect.h)):

				if(self.velocityY < 0):

					self.velocityY = 0
					deltaY = tile[1].bottom - self.rect.top

				elif(self.velocityY >= 0):

					self.velocityY = 0

					if(self.inAir):
						randomNumber = random.randint(1, 2)
						self.game.sounds.playSound(f'Fall{randomNumber}', 0.2)
						self.inAir = False
					deltaY = tile[1].top - self.rect.bottom

		if(self.rect.bottom > self.game.screenWidth):

			self.health = 0

		levelComplete = False
		if(pygame.sprite.spritecollide(self, self.game.exitsGroup, False)):

			levelComplete = True
			world.updateGameLevel()


		if(self.rect.left + deltaX < 0 or self.rect.right + deltaX > self.game.screenWidth):
				
			deltaX = 0

		self.rect.x += deltaX
		self.rect.y += deltaY

		if((self.rect.right > self.game.screenWidth - self.game.scrollThresh and self.game.backgroundScroll < (world.levelLength * world.tileSize) - self.game.screenWidth) or (self.rect.left < self.game.scrollThresh and self.game.backgroundScroll > abs(deltaX))):
				
			self.rect.x -= deltaX
			screenScroll = -deltaX

		return screenScroll, levelComplete

	def updateAnimation(self):
		if(self.moveLeft or self.moveRight):
				animTime = 80

		else:

			animTime = 140

		self.image = self.animationList[self.action][self.index]

		if(pygame.time.get_ticks() - self.time > animTime):

			self.time = pygame.time.get_ticks()
			self.index += 1

		if(self.index >= len(self.animationList[self.action])):

			if(self.action == 2):

				self.index = len(self.animationList[self.action]) - 1

			else:

				self.index = 0

	def updateAction(self, newAction : int):
		if(newAction != self.action):

			self.action = newAction
			self.index = 0
			self.time = pygame.time.get_ticks()

	def isAlive(self):
		if(self.health <= 0):

			self.health = 0
			self.speed = 0
			self.alive = False
			self.updateAction(2)


	def fire(self, particles):
		if(not self.moveRight and not self.moveLeft and not self.inAir):

			if(self.shootTimer == 0 and self.currentAmmo > 0):

				self.shootTimer = 15
				bullet = Bullet(self.game, self.rect.centerx + (0.6 * self.rect.size[0] * self.direction), self.rect.centery - self.rect.h // 4, self.direction)
				self.game.playerBulletGroup.add(bullet)
				self.currentAmmo -= 1
				particles.addGameParticle("gun", self.rect.centerx + (0.6 * self.rect.size[0]  * self.direction), self.rect.centery - self.rect.h // 4)
				self.game.sounds.playSound('Gunshot', 0.5)

	def draw(self, display : pygame.Surface):
		display.blit(pygame.transform.flip(self.image, self.flip, False), (self.rect.x - self.xcollision, self.rect.y))
		pygame.draw.rect(self.game.display, (250, 0, 0), (self.game.screenWidth // 3, (self.game.screenHeight // 4 - self.game.screenHeight // 5), (self.rect.w * 3), self.game.screenWidth // 80))
		pygame.draw.rect(self.game.display, (0, 250, 0), (self.game.screenWidth // 3, (self.game.screenHeight // 4 - self.game.screenHeight // 5), (self.rect.w * 3) * (self.health / self.maxHealth), self.game.screenWidth // 80))
		pygame.draw.rect(self.game.display, (0, 0, 0), (self.game.screenWidth // 3, (self.game.screenHeight // 4 - self.game.screenHeight // 5),(self.rect.w * 3), self.game.screenWidth // 80), 2)


# Enemy: #

class Enemy(pygame.sprite.Sprite):
	def __init__(self, game, x : int, y : int, speed):
		pygame.sprite.Sprite.__init__(self)

		# Game:

		self.game = game

		# Enemy Settings: 

		self.health = 100
		self.maxHealth = self.health
		self.x = x
		self.y = y
		self.speed = speed

		# Enemy Status:

		self.alive = True
		self.shoot = False

		# Enemy Timers:

		self.shootTimer = 0
		self.time = pygame.time.get_ticks()

		# Enemy Movement Variables:

		self.direction = 1
		self.velocityY = 0

		# Enemy Animation Variables:

		self.flip = False
		self.animationList = []
		self.index = 0
		self.action = 0

		# Enemy AI Variables:

		self.moveCounter = 0
		self.idle = False
		self.idleCounter = 0
		self.enemyVisionFront = pygame.Rect(0, 0, self.game.screenWidth // 4, self.game.screenHeight * 0.01)

		# Collision Patches:

		if(self.game.screenWidth == 1920):

			self.xcollision = 30
			self.widthCollision = 60

		else:

			self.xcollision = 20
			self.widthCollision = 40

		# Loading Sprites: #

		animationTypes = ['Idle', 'Move', 'Death']
		for animation in animationTypes:

			tempList = []
			framesNumber = len(os.listdir(f'assets/Enemy2/{animation}'))

			for c in range(framesNumber): # Loading all animations

				gameImage = pygame.image.load(f'assets/Enemy2/{animation}/{c}.png').convert_alpha()
				gameImage = pygame.transform.scale(gameImage, (self.game.screenWidth // 16, self.game.screenHeight // 10))
				tempList.append(gameImage)

			self.animationList.append(tempList)

		self.image = self.animationList[self.action][self.index]
		self.rect = pygame.Rect(x, y, self.image.get_width() - self.widthCollision, self.image.get_height())
		self.rect.center = (x, y)

	def handleAI(self, world, particles):
			move = 0
			self.updateAnimation()
			self.isAlive()

			if(self.shootTimer > 0):

				self.shootTimer -= 1

			if(self.alive and self.game.player.alive):

				if(self.idle == False and random.randint(1, 512) == 6):

					self.updateAction(0)
					self.idle = True
					self.idleCounter = 50

				if(self.enemyVisionFront.colliderect(self.game.player.rect)):

					self.updateAction(0)
					self.fire(particles)

				else:

					if(self.idle == False):

						if(self.direction == 1):

							move = 1
							self.flip = False

						else:

							move = -1
							self.flip = True

						self.rect.x += move
						self.updateAction(1)
						self.moveCounter += 1
						self.enemyVisionFront.center = (self.rect.centerx + (self.rect.w * 4.5) * self.direction, self.rect.centery)

						if(self.moveCounter > world.tileSize):

							self.direction *= -1
							self.moveCounter *= -1
					else:

						self.idleCounter -= 1

						if(self.idleCounter <= 0):

							self.idle = False

			self.velocityY += self.game.engineGravity

			for tile in world.obstacleList:

				if(tile[1].colliderect(self.rect.x, self.rect.y, self.rect.w, self.rect.h)):

					self.velocityY = 0

			self.enemyVisionFront.x += self.game.screenScroll
			self.rect.x += self.game.screenScroll
			self.rect.y += self.velocityY


	def updateAnimation(self):
		animTime = 90
		self.image = self.animationList[self.action][self.index]

		if(pygame.time.get_ticks() - self.time > animTime):

			self.time = pygame.time.get_ticks()
			self.index += 1

		if(self.index >= len(self.animationList[self.action])):

			if(self.action == 2):

				self.index = len(self.animationList[self.action]) - 1

			else:

				self.index = 0

	def updateAction(self, newAction : int):
		if(newAction != self.action):

			self.action = newAction
			self.index = 0
			self.time = pygame.time.get_ticks()

	def isAlive(self):
		if(self.health <= 0):

			self.health = 0
			self.speed = 0
			self.alive = False
			self.updateAction(2)


	def fire(self, particles):
		if(self.shootTimer == 0):

			self.shootTimer = 15
			bullet = Bullet(self.game, self.rect.centerx + (0.6 * self.rect.size[0] * self.direction), self.rect.centery - self.rect.h // 4, self.direction)
			self.game.enemyBulletGroup.add(bullet)
			particles.addGameParticle("gun", self.rect.centerx + (0.6 * self.rect.size[0]  * self.direction), self.rect.centery - self.rect.h // 4)
			self.game.sounds.playSound('Gunshot', 0.5)

	def draw(self, display : pygame.Surface):
		display.blit(pygame.transform.flip(self.image, self.flip, False), (self.rect.x - self.xcollision, self.rect.y))

# Object: #

class Object(pygame.sprite.Sprite):
	def __init__(self, game, tileSize, image : pygame.Surface, x : int, y : int):
		pygame.sprite.Sprite.__init__(self)

		# Game: 

		self.game = game

		# World: 

		self.tileSize = tileSize

		# Object Settings: 

		self.image = image
		self.rect = self.image.get_rect()
		self.rect.midtop = (x + self.tileSize // 2, y + (self.tileSize - self.image.get_height()))
		self.rect.h = 1

	def draw(self, display : pygame.Surface):
		display.blit(self.image, self.rect)

	def update(self):
		self.rect.x += self.game.screenScroll

# Pickup: #

class Pickup(pygame.sprite.Sprite):
	def __init__(self, game, tileSize, type : str, x : int, y : int):
		pygame.sprite.Sprite.__init__(self)

		# Game:

		self.game = game

		# Tile Size:

		self.tileSize = tileSize

		# Pickup Settings:

		self.type = type
		self.used = False
		self.image = self.game.pickups[self.type]
		self.rect = self.image.get_rect()
		self.rect.midtop = (x + self.tileSize // 2, y + (self.tileSize - self.image.get_height()))

	def draw(self, display : pygame.Surface):
		display.blit(self.image, self.rect)

	def update(self):

		if(pygame.sprite.collide_rect(self, self.game.player) and self.used == False and self.game.player.alive):

			if(self.type == 'Ammo'):

				self.image = self.game.pickups['AmmoShine']
				pygame.draw.rect(self.game.display, (67, 131, 226), pygame.Rect(self.game.screenWidth // 32, self.game.screenHeight // 12, self.game.screenWidth // 4, self.game.screenWidth // 18))
				pygame.draw.rect(self.game.display, (0, 0, 0), pygame.Rect(self.game.screenWidth // 32, self.game.screenHeight // 12, self.game.screenWidth // 4, self.game.screenWidth // 18), self.game.screenWidth // (self.game.screenWidth // 12))
				drawText(self.game.display, "Press 'F' to open the bag (+7 Bullets).", self.game.screenWidth // 64, (0, 0, 0), self.game.screenWidth // 20, self.game.screenHeight // 8)

				if(pygame.key.get_pressed()[pygame.K_f]):

					self.game.ammo += 7

					if(self.game.player.currentAmmo == 0 and self.game.ammo == 7):

						self.game.player.currentAmmo = self.game.ammo
						self.game.ammo -= self.game.ammo

					self.used = True
					self.game.sounds.playSound('AmmoPickup', 1)


			elif(self.type == 'Health'):

				self.image = self.game.pickups['HealthShine']
				pygame.draw.rect(self.game.display, (67, 131, 226), pygame.Rect(self.game.screenWidth // 32, self.game.screenHeight // 12, self.game.screenWidth // 4, self.game.screenWidth // 18))
				pygame.draw.rect(self.game.display, (0, 0, 0), pygame.Rect(self.game.screenWidth // 32, self.game.screenHeight // 12, self.game.screenWidth // 4, self.game.screenWidth // 18), self.game.screenWidth // (self.game.screenWidth // 12))
				drawText(self.game.display, "Press 'F' to use the medicine (+50 Health).", self.game.screenWidth // 64, (0, 0, 0), self.game.screenWidth // 20, self.game.screenHeight // 8)

				if(pygame.key.get_pressed()[pygame.K_f]):

					self.game.player.health += 50
					if(self.game.player.health > self.game.player.maxHealth):

						self.game.player.health = self.game.player.maxHealth

					self.used = True
					self.game.sounds.playSound('HealthPickup', 1)


			elif(self.type == 'Grenade'):

				self.image = self.game.pickups['GrenadeShine']
				pygame.draw.rect(self.game.display, (67, 131, 226), pygame.Rect(self.game.screenWidth // 32, self.game.screenHeight // 12, self.game.screenWidth // 4, self.game.screenWidth // 18))
				pygame.draw.rect(self.game.display, (0, 0, 0), pygame.Rect(self.game.screenWidth // 32, self.game.screenHeight // 12, self.game.screenWidth // 4, self.game.screenWidth // 18), self.game.screenWidth // (self.game.screenWidth // 12))
				drawText(self.game.display, "Press 'F' to open the chest (+3 Grenades).", self.game.screenWidth // 64, (0, 0, 0), self.game.screenWidth // 20, self.game.screenHeight // 8)
				if(pygame.key.get_pressed()[pygame.K_f]):

					self.game.grenades += 3
					self.used = True
					self.game.sounds.playSound('GrenadePickup', 1)
		else:

			if(self.used == True):

				self.image = self.game.pickups[f'{self.type}Open']

			else:

				self.image = self.game.pickups[self.type]


		self.rect.x += self.game.screenScroll

# Bullet: #

class Bullet(pygame.sprite.Sprite):
	def __init__(self, game, x : int, y : int, direction : int):
		pygame.sprite.Sprite.__init__(self)

		# Game:

		self.game = game

		# Bullet Settings:

		self.speed = (self.game.screenWidth // 32) // 5
		self.image = loadGameImage('assets/Bullet/bullet.png', self.game.screenWidth // 200, self.game.screenWidth // 400)
		self.rect = self.image.get_rect()
		self.rect.center = (x, y)
		self.direction = direction


	def draw(self, display : pygame.Surface):
		display.blit(pygame.transform.flip(self.image, self.game.player.flip, False), self.rect)

	def update(self, world, particles):
		self.rect.x += (self.direction * self.speed) + self.game.screenScroll

		if(self.rect.right < 0 or self.rect.left > self.game.screenWidth):

			self.kill

		for tile in world.obstacleList:

			if(tile[1].colliderect(self.rect)):

				self.kill()


		if(pygame.sprite.spritecollide(self.game.player, self.game.enemyBulletGroup, False)):

			if(self.game.player.alive):

				self.game.player.health -= 5
				particles.addGameParticle("blood", self.game.player.rect.centerx, self.game.player.rect.centery)
				randomNumber = random.randint(1, 4)
				self.game.sounds.playSound(f'Hit{randomNumber}', 0.3)
				self.kill()

		for enemy in self.game.enemyGroup:

			if(pygame.sprite.spritecollide(enemy, self.game.playerBulletGroup, False)):

				if(enemy.alive):

					enemy.health -= 25
					particles.addGameParticle("blood", enemy.rect.centerx, enemy.rect.centery)
					self.kill()

# Grenades: #

class Grenade(pygame.sprite.Sprite):
	def __init__(self, game, x : int, y : int, direction : int):
		pygame.sprite.Sprite.__init__(self)

		# Game:

		self.game = game

		# Timers:

		self.timer = 100

		# Grenade Settings:

		self.velocityY = -(self.game.screenWidth // 128)
		self.speed = self.game.screenWidth // 256
		self.image = loadGameImage("assets/Grenade/Grenade.png", self.game.screenWidth // 128, self.game.screenWidth // 128)
		self.rect = self.image.get_rect()
		self.rect.center = (x, y)
		self.width = self.image.get_width()
		self.height = self.image.get_height()
		self.direction = direction

	def draw(self, display : pygame.Surface):
		display.blit(self.image, self.rect)

	def update(self, world, particles):
		self.velocityY += self.game.engineGravity
		deltaX = self.direction * self.speed 
		deltaY = self.velocityY

		for tile in world.obstacleList:

			if(tile[1].colliderect(self.rect.x + deltaX, self.rect.y, self.width, self.height)):

				self.direction *= -1
				deltaX = self.direction * self.speed

			if(tile[1].colliderect(self.rect.x, self.rect.y + deltaY, self.width, self.height)):

				self.speed = 0

				if(self.velocityY < 0):

					self.velocityY = 0
					deltaY = tile[1].bottom - self.rect.top

				elif(self.velocityY >= 0):

					self.velocityY = 0
					deltaY = tile[1].top - self.rect.bottom


		if(self.rect.left + deltaX < 0 or self.rect.right + deltaX > self.game.screenWidth):
			self.direction *= -1
			deltaX = self.direction * self.speed

		self.rect.x += deltaX + self.game.screenScroll
		self.rect.y += deltaY

		self.timer -= 1

		if(self.timer <= 0):

			self.kill()
			explosionEffect = Explosion(self.game, self.rect.x, self.rect.y - (world.tileSize * 2))
			self.game.explosionGroup.add(explosionEffect)
			self.game.sounds.playSound('Explosion', 1)

			for i in range(5):

				particles.addGameParticle("explosion", self.rect.x, self.rect.y)

			if (abs(self.rect.centerx - self.game.player.rect.centerx) < world.tileSize * 2 and (self.rect.centery - self.game.player.rect.centery) < world.tileSize * 2):
				self.game.player.health -= 50

			for enemy in self.game.enemyGroup:

				if (abs(self.rect.centerx - enemy.rect.centerx) < world.tileSize * 2 and (self.rect.centery - enemy.rect.centery) < world.tileSize * 2):
					enemy.health -= 100


# Explosion: #

class Explosion(pygame.sprite.Sprite):
	def __init__(self, game, x : int, y : int):
		pygame.sprite.Sprite.__init__(self)

		# Game:

		self.game = game

		# Explosions list:

		self.explosions = []

		# Explosion Sprite Loading:

		for c in range(19):
			image = loadGameImage(f'assets/Explosion/{c}.png', self.game.screenWidth // 3, self.game.screenWidth // 3)
			self.explosions.append(image)

		# Explosion Settings:

		self.index = 0
		self.image = self.explosions[self.index]
		self.rect = self.image.get_rect()
		self.rect.x = x
		self.rect.y = y
		self.rect.center = (x, y)
		self.timer = 0

	def draw(self, display : pygame.Surface):
		display.blit(self.image, self.rect)

	def update(self):
		explosionSpeed = 3
		self.timer += 1

		if(self.timer >= explosionSpeed):

			self.timer = 0
			self.index += 1

			if(self.index >= len(self.explosions)):

				self.kill()

			else:

				self.image = self.explosions[self.index]

		self.rect.x += self.game.screenScroll

# Button: #

class Button():
	def __init__(self, display : pygame.Surface, x : int, y : int, image : pygame.Surface):
		self.display = display
		self.image = image
		self.rect = self.image.get_rect()
		self.rect.topleft = (x, y)
		self.clicked = False
		self.buttonCooldown = 100
		self.buttonTimer = pygame.time.get_ticks()

	def render(self):
		action = False
		position = pygame.mouse.get_pos()
		if self.rect.collidepoint(position):

			if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:

				if(pygame.time.get_ticks() - self.buttonTimer >= self.buttonCooldown):

					action = True
					self.clicked = True
					self.buttonTimer = pygame.time.get_ticks()
			
		if pygame.mouse.get_pressed()[0] == 0:

			self.clicked = False

		self.display.blit(self.image, (self.rect.x, self.rect.y))
		return action

	def changeButton(self, image : pygame.Surface):

		self.image = image

# Fade: #

class Fade():
	def __init__(self, game, direction : int, color : tuple):

		# Display: 

		self.game = game

		# Fade Settings: 

		self.direction = direction
		self.color = color
		self.speed = self.game.screenWidth // 128
		self.fadeCounter = 0
		self.fadeCompleted = False

	def reset(self):

		self.fadeCounter = 0
		self.fadeCompleted = False

	def fade(self):

		self.fadeCounter += self.speed

		if(self.direction == 1):

			pygame.draw.rect(self.game.display, self.color, (0 - self.fadeCounter, 0, self.game.screenWidth // 2, self.game.screenHeight))
			pygame.draw.rect(self.game.display, self.color, (self.game.screenWidth // 2 + self.fadeCounter, 0, self.game.screenWidth, self.game.screenHeight))
			pygame.draw.rect(self.game.display, self.color, (0, 0 - self.fadeCounter, self.game.screenWidth, self.game.screenHeight // 2))
			pygame.draw.rect(self.game.display, self.color, (0, self.game.screenHeight // 2 + self.fadeCounter, self.game.screenWidth, self.game.screenHeight))

		if(self.direction == 2):

			pygame.draw.rect(self.game.display, self.color, (0, 0, screenWidth, 0 + self.fadeCounter))
		
		if(self.fadeCounter >= self.game.screenWidth // 2):
			self.fadeCompleted = True

		return self.fadeCompleted


# Resolution: #

class Resolution():
	def __init__(self, game):
		
		# Game: 

		self.game = game

		# Display:

		self.resolutionWindow = pygame.display.set_mode((300, 400))
		pygame.display.set_caption("Land Invasion: ")
		pygame.display.set_icon(loadGameImage('assets/icon.png', 32, 32))
		self.resolutionStatus = True

		# Background:

		self.background = loadGameImage('assets/menu.png', 300, 400)

		# Buttons: 

		self.resolutionA = Button(self.resolutionWindow, 80, 200, loadGameImage('assets/resolution/B.png', 150, 100)) # 1280 x 720
		self.resolutionB = Button(self.resolutionWindow, 80, 50, loadGameImage('assets/resolution/A.png', 150, 100)) # 1920 x 1080

	def updateBackground(self):
		self.resolutionWindow.fill((255, 255, 255))
		self.resolutionWindow.blit(self.background, (0, 0))

	def setResolution(self, screenWidth : int, screenHeight : int):
		self.game.screenWidth = screenWidth
		self.game.screenHeight = screenHeight
		self.resolutionStatus = False


	def updateWindow(self):
		for event in pygame.event.get():

			if(event.type == pygame.QUIT):

				self.resolutionStatus = False
				exit()

		pygame.display.update()

# Graphics: #

class Graphics():
	def __init__(self, game):

		# Game: 

		self.game = game

		# Display:

		self.graphicsWindows = pygame.display.set_mode((300, 400))
		pygame.display.set_caption("Land Invasion: ")
		pygame.display.set_icon(loadGameImage('assets/icon.png', 32, 32))
		self.graphicsStatus = True

		# Background:

		self.background = loadGameImage('assets/menu.png', 300, 400)

		# Buttons: 

		self.effects = Button(self.graphicsWindows, 80, 50, loadGameImage('assets/graphics/AOn.png', 150, 100)) 
		self.start = Button(self.graphicsWindows, 75, 250, loadGameImage('assets/graphics/start.png', 150, 100)) 

	def updateBackground(self):
		self.graphicsWindows.fill((255, 255, 255))
		self.graphicsWindows.blit(self.background, (0, 0))

	def setEffects(self):
		if(self.game.effects):

			self.game.effects = False

		else:

			self.game.effects = True

	def updateWindow(self):

		if(self.game.effects):

			self.effects.changeButton(loadGameImage('assets/graphics/AOn.png', 150, 100))

		else:

			self.effects.changeButton(loadGameImage('assets/graphics/AOff.png', 150, 100)) 


		for event in pygame.event.get():

			if(event.type == pygame.QUIT):

				self.resolutionStatus = False
				exit()
		pygame.display.update()

# Editor: #

class Editor():
	def __init__(self, game, world, assetsManager, menu):

		# Game:

		self.game = game

		# World:

		self.world = world
		self.worldGenerated = False

		# Assets Manager:

		self.assetsManager = assetsManager

		# Menu:

		self.menu = menu

		# Editor Settings:

		self.unsaved = False
		self.thisTile = 0

		# Camera Movement:

		self.scrollLeft = False
		self.scrollRight = False
		self.scroll = 0
		self.scrollSpeed = 1
		self.move = 0

		# Tile Selection:

		self.tileButtons = []
		self.tileColumn = 0
		self.tileRow = 0
		self.thisTile = 0

		# User Interface:

		self.interfaceReady = False
		self.buttonCount = 0
		self.sideMargin = pygame.Rect(self.game.screenWidth - self.game.screenWidth // 4, 0, self.game.screenWidth // 4, self.game.screenHeight)
		self.lowerMargin = pygame.Rect(0, self.game.screenHeight - self.game.screenHeight // 9, self.game.screenWidth, self.game.screenHeight // 8)
		
		# Buttons:

		self.saveButton = Button(self.game.display, self.game.screenWidth // 2 - (self.game.screenWidth // 18), self.game.screenHeight - (self.game.screenHeight // 12), self.assetsManager.buttons["Save"])
		self.clearButton = Button(self.game.display, self.game.screenWidth // 2 - (self.game.screenWidth // 3), self.game.screenHeight - (self.game.screenHeight // 12), self.assetsManager.buttons["Clear"])
		self.backButton = Button(self.game.display, self.game.screenWidth // 2 - (self.game.screenWidth // 5), self.game.screenHeight - (self.game.screenHeight // 12), self.assetsManager.buttons["Back"])

		# Timers:

		self.changeTimer = pygame.time.get_ticks()
		self.speedTimer = pygame.time.get_ticks()

	def loadNewLevel(self):

		with open(f'levels/level{self.game.level}.csv', newline='') as csvfile:
			reader = csv.reader(csvfile, delimiter = ',')
			for x, row in enumerate(reader):
				for y, tile in enumerate(row):
					self.world.worldData[x][y] = int(tile)

	def generateEditorWorld(self):

		if(not self.worldGenerated):

			for row in range(self.world.levelColumns):
				r = [-1] * self.world.levelColumns
				self.world.worldData.append(r)

			self.worldGenerated = True

	def drawGrid(self):

		for c in range(self.world.levelColumns + 1):
			pygame.draw.line(self.game.display, ((255, 255, 255)), (c * self.world.tileSize - self.scroll, 0), (c * self.world.tileSize - self.scroll, self.game.screenHeight))

		for c in range(self.world.levelRows + 1):
			pygame.draw.line(self.game.display, ((255, 255, 255)), (0, c * self.world.tileSize), (self.game.screenWidth, c * self.world.tileSize))

	def drawWorld(self):
		for y, row in enumerate(self.world.worldData):
			for x, tile in enumerate(row):
				if tile >= 0:
					self.game.display.blit(self.world.availableTiles[tile], (x * self.world.tileSize - self.scroll, y * self.world.tileSize))

	def drawUserInterface(self):

		pygame.draw.rect(self.game.display, ((140, 146, 172)), self.sideMargin)
		pygame.draw.rect(self.game.display, ((140, 146, 172)), self.lowerMargin)
		if(self.interfaceReady == False):

			for i in range(len(self.world.availableTiles)):
				tileButton = Button(self.game.display, self.game.screenWidth - ((self.game.screenWidth // 20) * self.tileColumn) - (self.game.screenWidth // 16), ((self.game.screenWidth // 25) * self.tileRow) + (self.game.screenHeight // 20), self.world.availableTiles[i])

				self.tileButtons.append(tileButton)
				self.tileColumn += 1
				if self.tileColumn == 4:
					self.tileRow += 1
					self.tileColumn = 0

			self.interfaceReady = True

		self.buttonCount = 0
		for self.buttonCount, button in enumerate(self.tileButtons):
			if button.render():
				self.thisTile = self.buttonCount

		for tile in range (len(self.tileButtons)):
			pygame.draw.rect(self.game.display, ((0, 0, 0)), self.tileButtons[tile].rect, self.game.screenWidth // 512)

		pygame.draw.rect(self.game.display, ((255, 0, 0)), self.tileButtons[self.thisTile].rect, self.game.screenWidth // 256)

	def drawInformation(self):

		if(self.unsaved):

			drawText(self.game.display, "Unsaved", self.game.screenWidth // 64, (255, 20, 10), self.game.screenWidth // 20, self.game.screenHeight - (self.game.screenHeight // 18))

		drawText(self.game.display, f"Level: {self.game.level}", self.game.screenWidth // 64, (0, 0, 0), self.game.screenWidth // 20, self.game.screenHeight - (self.game.screenHeight // 12))
		drawText(self.game.display, f"Speed: {self.scrollSpeed}", self.game.screenWidth // 64, (0, 0, 0), self.game.screenWidth // 20, self.game.screenHeight - (self.game.screenHeight // 32))

	def handleButtons(self):
		i = 0
		if(self.saveButton.render() and self.unsaved):
			with open(f'levels/level{self.game.level}.csv', 'w', newline='') as csvfile:
				writer = csv.writer(csvfile, delimiter = ',')
				for row in self.world.worldData:
					if(i >= self.world.levelRows):
						break
					writer.writerow(row)
					i += 1

			self.unsaved = False

		if(self.clearButton.render()):
			self.world.worldData = []

			for row in range(self.world.levelRows):

				r = [-1] * self.world.levelColumns
				self.world.worldData.append(r)

			for tile in range(0, self.world.levelColumns):

				self.world.worldData[self.world.levelRows - 1][tile] = 0

			self.unsaved = True

		if(self.backButton.render()):
			self.game.menuOn = True
			self.menu.mainMenu = True
			self.menu.levelSelector = True
			self.game.editorStatus = False

	def handleEditor(self):

		position = pygame.mouse.get_pos()
		x = (position[0] + self.scroll) // self.world.tileSize
		y = position[1] // self.world.tileSize

		if(pygame.key.get_pressed()[pygame.K_z]):

			if(pygame.time.get_ticks() - self.changeTimer > 200 and self.game.level < 6):

				self.game.level += 1
				self.unsaved = False
				self.loadNewLevel()
				self.changeTimer = pygame.time.get_ticks()

		if(pygame.key.get_pressed()[pygame.K_s]):

			if(pygame.time.get_ticks() - self.changeTimer > 200 and self.game.level != 1):

				self.game.level -= 1
				self.unsaved = False
				self.loadNewLevel()
				self.changeTimer = pygame.time.get_ticks()

		if(pygame.key.get_pressed()[pygame.K_d]):

			self.scrollRight = True

		if(pygame.key.get_pressed()[pygame.K_q]):

			self.scrollLeft = True

		if(pygame.key.get_pressed()[pygame.K_SPACE]):

			if(pygame.time.get_ticks() - self.speedTimer > 200 and self.scrollSpeed < 7):
				self.scrollSpeed += 1
				self.speedTimer = pygame.time.get_ticks()

		if(pygame.key.get_pressed()[pygame.K_LSHIFT]):

			if(pygame.time.get_ticks() - self.speedTimer > 200 and self.scrollSpeed != 1):
				self.scrollSpeed -= 1
				self.speedTimer = pygame.time.get_ticks()

		if(not pygame.key.get_pressed()[pygame.K_d]):

			self.scrollRight = False

		if(not pygame.key.get_pressed()[pygame.K_q]):

			self.scrollLeft = False

		if(position[0] < self.game.screenWidth and position[1] < self.game.screenHeight):

			if(not self.sideMargin.collidepoint(position) and not self.lowerMargin.collidepoint(position)):

				if (pygame.mouse.get_pressed()[0] == 1):

					if (self.world.worldData[y][x] != self.thisTile):

						self.world.worldData[y][x] = self.thisTile
						self.unsaved = True

				if (pygame.mouse.get_pressed()[2] == 1):

					if(not self.world.worldData[y][x] == -1):

						self.world.worldData[y][x] = -1
						self.unsaved = True

		if self.scrollLeft == True and self.scroll > 0:
			self.scroll -= 5 * self.scrollSpeed
		if self.scrollRight == True and self.scroll < (self.world.levelColumns * self.world.tileSize) - (self.game.screenWidth - (self.game.screenWidth // 4)):
			self.scroll += 5 * self.scrollSpeed
