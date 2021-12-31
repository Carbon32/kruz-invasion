# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
#                                                                             #
#                Invasion Engine, Land Invasion's Game Engine                 #
#                            Developer: Carbon               				  #
#                                                                             #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

# Imports: #

import pygame
from pygame import mixer
import random
import os
import csv

# Pygame and Mixer Initializations: #

pygame.init()
mixer.init()

# Engine Variables: #

windowWidth = 0
windowHeight = 0

scrollThresh = 300
screenScroll = 0
backgroundScroll = 0
engineGravity = 0.5

level = 1
levelRows = 16
levelColumns = 150
tileSize = 50
engineTiles = 24
levelComplete = False

# Sprite Groups: 
bulletGroup = pygame.sprite.Group()
grenadeGroup = pygame.sprite.Group()
explosionGroup = pygame.sprite.Group()
enemyGroup = pygame.sprite.Group()
chemicalsGroup = pygame.sprite.Group()
gamePickups = pygame.sprite.Group()
gameObjects = pygame.sprite.Group()
gameExits = pygame.sprite.Group()

# Tiles: #

allTiles = []
for c in range(engineTiles):
	image = pygame.image.load(f'assets/Tiles/{c}.png')
	image = pygame.transform.scale(image, (tileSize, tileSize))
	allTiles.append(image)

# Levels: #

worldData = []
for r in range(levelRows):
	row = [-1] * levelColumns
	worldData.append(row)

with open(f'levels/level{level}_data.csv', newline='') as csvfile:
	reader = csv.reader(csvfile, delimiter=',')
	for x, row in enumerate(reader):
		for y, tile in enumerate(row):
			worldData[x][y] = int(tile)

# Engine Window: #

class Window():
	def __init__(self, screenWidth : int, screenHeight : int, windowTitle : str):
		global windowWidth, windowHeight
		windowWidth = screenWidth
		windowHeight = screenHeight
		self.screenWidth = screenWidth
		self.screenHeight = screenHeight
		self.engineRunning = False
		self.windowTitle = windowTitle
		self.fpsLimit = pygame.time.Clock()
	
	def init(self):
		self.engineWindow = pygame.display.set_mode((self.screenWidth, self.screenHeight))
		pygame.display.set_caption(self.windowTitle)
		self.engineRunning = True

	def quit(self):
		pygame.quit()

	def updateDisplay(self):
		for event in pygame.event.get():
			if(event.type == pygame.QUIT):
				self.engineRunning = False
		pygame.display.update()

	def limitFPS(self, fps : int):
		self.fpsLimit.tick(fps)
	
	def setBackground(self, sky : pygame.Surface, mountain : pygame.Surface, trees : pygame.Surface, x : int, y : int):
		global backgroundScroll, windowHeight
		self.engineWindow.fill((125, 255, 255))
		width = sky.get_width()
		for x in range(10):
			self.engineWindow.blit(sky, ((x * width) - backgroundScroll * 0.5, 0))
			self.engineWindow.blit(mountain, ((x * width) - backgroundScroll * 0.7, windowHeight - mountain.get_height() - 300))
			self.engineWindow.blit(trees, ((x * width) - backgroundScroll * 0.9, windowHeight - trees.get_height() - 150))
			self.engineWindow.blit(trees, ((x * width) - backgroundScroll * 1, windowHeight - trees.get_height()))

# World: #

# World Class: #

class World():
	def __init__(self):
		self.obstacleList = []

	def processData(self, data : list):
		self.levelLength = len(data[0])
		for y, row in enumerate(data):
			for x, t in enumerate(row):
				if(t >= 0):
					tile = allTiles[t]
					tileRect = tile.get_rect()
					tileRect.x = x * tileSize
					tileRect.y = y * tileSize
					tileData = (tile, tileRect)
					if(t >= 0 and t <= 8):
						self.obstacleList.append(tileData)

	def draw(self, engineWindow : pygame.Surface):
		for tile in self.obstacleList:
			tile[1][0] += screenScroll
			engineWindow.blit(tile[0], tile[1])

# Soldier: #

class Soldier(pygame.sprite.Sprite):
	def __init__(self, type : str, x : int, y : int, scale : int, speed : int, ammo : int, grenades : int):
		pygame.sprite.Sprite.__init__(self)

		# Soldier Init Variables: 
		self.type = type
		self.health = 100
		self.maxHealth = self.health
		self.x = x
		self.y = y
		self.speed = speed
		self.ammo = ammo
		self.startAmmo = ammo
		self.grenades = grenades
		self.alive = True
		self.moveRight = False
		self.moveLeft = False

		# Soldier Timers:
		self.shootTimer = 0
		self.time = pygame.time.get_ticks()

		# Soldier Movement Variables:
		self.direction = 1
		self.jump = False
		self.inAir = True
		self.velocityY = 0

		# Soldier Animation Variables:
		self.flip = False
		self.animationList = []
		self.index = 0
		self.action = 0

		# Soldier AI Variables:
		self.moveCounter = 0
		self.idle = False
		self.idleCounter = 0
		self.enemyVision = pygame.Rect(0, 0, 200, 20)

		# Loading Sprites: #
		animationTypes = ['Idle', 'Move', 'Death']
		for animation in animationTypes:
			tempList = []
			framesNumber = len(os.listdir(f'assets/{self.type}/{animation}'))
			for c in range(framesNumber): # Loading all animations
				gameImage = pygame.image.load(f'assets/{self.type}/{animation}/{c}.png')
				gameImage = pygame.transform.scale(gameImage, (gameImage.get_width() * scale, gameImage.get_height() * scale))
				tempList.append(gameImage)
			self.animationList.append(tempList)

		self.image = self.animationList[self.action][self.index]
		self.rect = self.image.get_rect()
		self.rect.center = (x, y)
		self.width = self.image.get_width()
		self.height = self.image.get_height()

	def update(self):
		self.updateAnimation()
		self.isAlive()
		'''if(self.shootTimer > 0):
			self.shootTimer -= 1'''

	def move(self, world):
		if(self.type == 'Player'):
			if(pygame.key.get_pressed()[pygame.K_d]):
				self.moveRight = True
				self.updateAction(1)
			if(pygame.key.get_pressed()[pygame.K_q]):
				self.moveLeft = True
				self.updateAction(1)
			if(pygame.key.get_pressed()[pygame.K_SPACE] and self.alive and self.inAir == False):
				self.jump = True
			if(pygame.key.get_pressed()[pygame.K_ESCAPE]):
				pygame.quit()
			if(pygame.key.get_pressed()[pygame.K_e]):
				shoot = True
			if(pygame.key.get_pressed()[pygame.K_a]):
				throwGrenade = True

			if(not pygame.key.get_pressed()[pygame.K_d]):
					self.moveRight = False
			if(not pygame.key.get_pressed()[pygame.K_q]):
					self.moveLeft = False
			if(not pygame.key.get_pressed()[pygame.K_q] and not pygame.key.get_pressed()[pygame.K_d]):
				self.updateAction(0)
			if(not pygame.key.get_pressed()[pygame.K_e]):
					shoot = False
			if(not pygame.key.get_pressed()[pygame.K_a]):
					throwGrenade = False
					grenadeThrown = False
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
			self.velocityY = -10
			self.jump = False
			self.inAir = True

		self.velocityY += engineGravity
		if(self.velocityY > 10):
			self.velocityY = 10
			self.inAir = False
		deltaY += self.velocityY

		# Improved Collision:
		for tile in world.obstacleList:
			if(tile[1].colliderect(self.rect.x + deltaX, self.rect.y, self.width - 20, self.height)):
				deltaX = 0
				if(self.type == 'Enemy'):
					self.direction *= -1
					self.moveCounter = 0

			if(tile[1].colliderect(self.rect.x, self.rect.y + deltaY, self.width - 20, self.height)):
				if(self.velocityY < 0):
					self.velocityY = 0
					deltaY = tile[1].bottom - self.rect.top

				elif(self.velocityY >= 0):
					self.velocityY = 0
					self.inAir = False
					deltaY = tile[1].top - self.rect.bottom

		if(pygame.sprite.spritecollide(self, chemicalsGroup, False)):
			self.health = 0

		if(self.rect.bottom > windowHeight):
			self.health = 0

		'''levelComplete = False
		if(pygame.sprite.spritecollide(self, gameExits, False)):
			levelComplete = True'''


		if(self.type == 'Player'):
			if(self.rect.left + deltaX < 0 or self.rect.right + deltaX > windowWidth):
				deltaX = 0

		self.rect.x += deltaX
		self.rect.y += deltaY

		if(self.type == 'Player'):
			if((self.rect.right > windowWidth - scrollThresh and backgroundScroll < (world.levelLength * tileSize) - windowWidth) or (self.rect.left < scrollThresh and backgroundScroll > abs(deltaX))):
				self.rect.x -= deltaX
				screenScroll = -deltaX

		return screenScroll, levelComplete

	'''def handleAI(self):
		if(self.alive and gamePlayer.alive):
			if(self.idle == False and random.randint(1, 512) == 6):
				self.updateAction(0)
				self.idle = True
				self.idleCounter = 50
			if(self.enemyVision.colliderect(gamePlayer.rect)):
				self.updateAction(0)
				self.shoot()
			else:
				if(self.idle == False):
					if(self.direction == 1):
						aiRight = True
					else:
						aiRight = False
					aiLeft = not aiRight
					self.move(aiLeft, aiRight)
					self.updateAction(1)
					self.moveCounter += 1
					self.enemyVision.center = (self.rect.centerx + 100 * self.direction, self.rect.centery)
					if(self.moveCounter > tileSize):
						self.direction *= -1
						self.moveCounter *= -1
				else:
					self.idleCounter -= 1
					if(self.idleCounter <= 0):
						self.idle = False
		self.rect.x += screenScroll'''

	def updateAnimation(self):
		animTime = 80
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


	'''def shoot(self):
		if(self.shootTimer == 0 and self.ammo > 0):
			self.shootTimer = 10
			bullet = Bullet(self.rect.centerx + (0.6 * self.rect.size[0] * self.direction), self.rect.centery+10, self.direction)
			bulletGroup.add(bullet)
			self.ammo -= 1
			gunshot.play()'''

	def draw(self, engineWindow):
		engineWindow.blit(pygame.transform.flip(self.image, self.flip, False), self.rect)
