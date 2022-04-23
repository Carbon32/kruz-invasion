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
	from pygame import mixer

except ImportError:
	raise ImportError("The Invasion Engine couldn't import all of the necessary packages.")

# Pygame and Mixer Initializations: #

pygame.init()
mixer.init()

# Engine Functions: #

def loadGameImage(path : str, width : int, height : int):
		image = pygame.image.load(path).convert_alpha()
		image = pygame.transform.scale(image, (width, height))
		return image

def loadStaticImage(path : str):
		image = pygame.image.load(path).convert()
		return image

def scaleImage(image : pygame.Surface, width : int, height : int):
	image = pygame.transform.scale(image, (width, height))
	return image

def drawText(display : pygame.Surface, text : str, color : tuple, x : int, y : int):
	image = pygame.font.SysFont('System', 30).render(text, True, color)
	display.blit(image, (x, y))

def destroyGame():
	pygame.quit()
	quit()

# Game: #

class Game():
	def __init__(self):

		# Display:

		self.engineRunning = True
		self.fpsHandler = pygame.time.Clock()

		# Player:

		self.movingRight = False
		self.movingLeft = False
		self.sprinting = False
		self.jumping = False
		
	def startWindow(self):
		self.display = pygame.display.set_mode((self.screenWidth, self.screenHeight), pygame.FULLSCREEN)
		pygame.display.set_caption("Land Invasion: ")

	def renderPlayer(self, world):
		try:

			self.player.render()
			self.player.update(world)

		except AttributeError:

			raise AttributeError("Couldn't load the player, check if the player exists in the level map.")

	def updateDisplay(self, fps : int):

		for event in pygame.event.get():

			if(event.type == pygame.QUIT):

				self.engineRunning = False

			if(event.type == pygame.KEYDOWN):

				if(event.key == pygame.K_ESCAPE):

					self.engineRunning = False

				if(event.key == pygame.K_d):

					self.movingRight = True

				if(event.key == pygame.K_q):

					self.movingLeft = True

				if(event.key == pygame.K_LSHIFT):

					self.sprinting = True

				if(event.key == pygame.K_SPACE):

					self.jumping = True

			if(event.type == pygame.KEYUP):

				if(event.key == pygame.K_d):

					self.movingRight = False

				if event.key == pygame.K_q:

					self.movingLeft = False

				if(event.key == pygame.K_LSHIFT):

					self.sprinting = False

		self.fpsHandler.tick(fps)
		drawText(self.display, str(round(self.fpsHandler.get_fps())), (0, 0, 0), 50, 50)
		pygame.display.update()
		self.display.fill((255, 255, 255))

# Game Resolution: #

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

		self.resolutionA = Button(self.resolutionWindow, 0, 0, loadGameImage('assets/resolution/A.png', 150, 150)) # 1920 x 1080
		self.resolutionB = Button(self.resolutionWindow, 150, 0, loadGameImage('assets/resolution/B.png', 150, 150)) # 1280 x 720

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
				destroyGame()

		pygame.display.update()

# Buttons: #

class Button():
	def __init__(self, display : pygame.Surface, x : int, y : int, image : pygame.Surface):
		self.display = display
		self.image = image
		self.rect = self.image.get_rect()
		self.rect.topleft = (x, y)
		self.clicked = False

	def render(self):
		action = False
		position = pygame.mouse.get_pos()

		if self.rect.collidepoint(position):

			if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:

				action = True
				self.clicked = True

		if pygame.mouse.get_pressed()[0] == 0:

			self.clicked = False

		self.display.blit(self.image, (self.rect.x, self.rect.y))
		return action

# Player: #

class Player():
	def __init__(self, game, x : int, y : int):

		# Game: #

		self.game = game

		# Movement Settings: 

		self.direction = 1
		self.speed = 2
		self.verticalMovement = 0
		self.inAir = False

		# Animation Settings:

		self.flip = False
		self.animationList = []
		self.index = 0
		self.action = 0
		self.animationTimer = pygame.time.get_ticks()

		# Load Animations: 

		animationTypes = ['idle', 'move', 'death']

		for animation in animationTypes:

			tempList = []
			framesNumber = len(os.listdir(f'assets/Player/{animation}'))

			for c in range(framesNumber):

				playerImage = loadGameImage(f'assets/Player/{animation}/{c}.png', self.game.screenWidth // 28, self.game.screenHeight // 14)
				tempList.append(playerImage)

			self.animationList.append(tempList)


		self.sprite = self.animationList[self.action][self.index]

		# Player Rectangle:

		self.rect = self.sprite.get_rect()
		self.rect.w = self.sprite.get_width()
		self.rect.h = self.sprite.get_height()
		self.rect.center = (x, y)

		# Scrolling:

		self.scroll = [self.rect.x - (self.game.screenWidth // 2 + self.sprite.get_width() // 2), self.rect.y]

	def render(self):
		self.game.display.blit(pygame.transform.flip(self.sprite, self.flip, False), (self.rect.x - self.scroll[0], self.rect.y - self.scroll[1]))
		pygame.draw.rect(self.game.display, (0, 0, 255), pygame.Rect(self.rect.x - self.scroll[0], self.rect.y - self.scroll[1], self.rect.w, self.rect.h), 2)

	def handleMovement(self, world):

		self.scroll[0] += (self.rect.x - self.scroll[0] - (self.game.screenWidth // 2 + self.sprite.get_width() // 2)) / 50
		self.scroll[1] += (self.rect.y - self.scroll[1] - (self.game.screenHeight // 2 + self.sprite.get_width() // 2)) / 50

		playerMovement = [0, 0]

		if(self.game.movingLeft):

			playerMovement[0] = -self.speed
			self.flip = True
			self.direction = -1
			self.updateAction(1)

		if(self.game.movingRight):

			playerMovement[0] += self.speed
			self.flip = False
			self.direction = 1
			self.updateAction(1)

		if(self.game.sprinting):

			self.speed = 4
			self.animationSpeed = 20

		if(not self.game.sprinting):

			self.speed = 2
			self.animationSpeed = 60

		if(self.game.jumping):

			if(not self.inAir):

				self.verticalMovement = -20
				self.game.jumping = False

			else:

				self.game.jumping = False

		if(not self.game.movingLeft and not self.game.movingRight):

			self.updateAction(0)

		# Gravity: #

		self.verticalMovement += 1
		playerMovement[1] += self.verticalMovement

		if(self.verticalMovement > 8):

			self.verticalMovement = 8

		# Collision:

		self.rect, collisions = world.handleMovementCollision(self.rect, playerMovement)

		# Reset Vertical Movement:

		if(collisions['bottom']):

			self.verticalMovement = 0
			self.inAir = False

		else:

			self.inAir = True

		if(collisions['top']):

			self.verticalMovement = 20

	def updateAnimation(self):
		self.sprite = self.animationList[self.action][self.index]
		
		if(pygame.time.get_ticks() - self.animationTimer > self.animationSpeed):
			
			self.animationTimer = pygame.time.get_ticks()
			self.index += 1

		if(self.index >= len(self.animationList[self.action])):
			
			if(self.action == 2):
				
				self.index = len(self.animationList[self.action]) - 1
			
			else:

				self.index = 0

	def updateAction(self, action : int):
		if(action != self.action):

			self.action = action
			self.index = 0
			self.animationTimer = pygame.time.get_ticks()

	def update(self, world):
		self.handleMovement(world)
		self.updateAnimation()


# World: #

class World():
	def __init__(self, game):

		# Game:

		self.game = game

		# Map:

		self.gameMap = []

		# Tiles:

		self.tiles = []

		# Tiles Images:
		
		self.tileImages = []

		# Tile Settings: 

		self.tileSize = self.game.screenWidth // 24

		# Rectangles: 

		self.tileRects = []

		# Tiles Loading:

		for c in range(len(os.listdir('assets/tiles/'))):

			image = loadStaticImage(f'assets/tiles/{c}.png')
			self.tileImages.append(image)

	def renderTile(self, tile : pygame.Surface, x : int, y : int):

		if(self.game.screenHeight == 720):

			scaledTile = scaleImage(tile, 60, 60)
			self.game.display.blit(scaledTile, (x * self.tileSize - self.game.player.scroll[0], y * self.tileSize + self.tileSize * 1.6 - self.game.player.scroll[1]))

		else:
						
			scaledTile = scaleImage(tile, 80, 80)
			self.game.display.blit(scaledTile, (x * self.tileSize - self.game.player.scroll[0], y * self.tileSize + self.tileSize * 1.5 - self.game.player.scroll[1]))

	def renderPlayer(self, x : int, y : int):

		if(self.game.screenHeight == 720):

			self.game.player = Player(self.game, x * self.tileSize + self.tileSize * 1.9, y * self.tileSize + self.tileSize * 1.9)

		else:

			self.game.player = Player(self.game, x * self.tileSize + self.tileSize * 1.85, y * self.tileSize + self.tileSize * -5)

	def createCollisionMap(self, x : int, y : int):

		if(self.game.screenHeight == 720):

			self.tileRects.append(pygame.Rect(x * self.tileSize, y * self.tileSize + self.tileSize * 1.6, self.tileSize + 6, self.tileSize + 6))

		else:

			self.tileRects.append(pygame.Rect(x * self.tileSize, y * self.tileSize + self.tileSize * 1.5, self.tileSize, self.tileSize))

	def detectCollision(self, playerRectangle : pygame.Rect):
		collisionList = []

		for tile in self.tileRects:

			if playerRectangle.colliderect(tile):

				collisionList.append(tile)

		return collisionList

	def handleMovementCollision(self, playerRectangle : pygame.Rect, playerMovement : list):
		collisionTypes = {'top': False, 'bottom': False, 'right': False, 'left': False}

		playerRectangle.x += playerMovement[0]
		collisionList = self.detectCollision(playerRectangle)

		for tile in collisionList:

			if(playerMovement[0] > 0):

				playerRectangle.right = tile.left
				collisionTypes['right'] = True

			elif(playerMovement[0] < 0):

				playerRectangle.left = tile.right
				collisionTypes['left'] = True

		playerRectangle.y += playerMovement[1]
		collisionList = self.detectCollision(playerRectangle)

		for tile in collisionList:

			if(playerMovement[1] > 0):

				playerRectangle.bottom = tile.top
				collisionTypes['bottom'] = True

			elif(playerMovement[1] < 0):

				playerRectangle.top = tile.bottom
				collisionTypes['top'] = True

		return playerRectangle, collisionTypes

	def renderTiles(self):

		for tile in self.tiles:
			
			try:

				self.renderTile(self.tileImages[int(tile[0])], tile[1], tile[2])

			except IndexError:

				self.renderTile(self.tileImages[0], tile[1], tile[2])

	def loadGameMap(self, path : str):

		file = open(path, 'r')
		data = file.read()
		file.close
		data = data.split('\n')

		for row in data:
			self.gameMap.append(list(row))

		y = 0

		for row in self.gameMap:

			x = 0

			for tile in row:

				if(tile == 'P'):

					self.renderPlayer(x, y)

				if(tile != '.' and tile != 'P'):
						
					self.tiles.append([tile, x, y])
					self.createCollisionMap(x, y)
					
				x += 1
			y +=  1