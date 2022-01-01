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
tileSize = 48
engineTiles = 24
levelComplete = False

# Groups: #

healthBarGroup = []
playersGroup = pygame.sprite.Group()
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

pickups = {}

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

# Game Functions: #

def loadGamePickups(healthPickup : pygame.Surface, grenadePickup : pygame.Surface, bulletPickup : pygame.Surface):
	global pickups
	pickups = {
		'Health'	: healthPickup,
		'Grenade'	: grenadePickup,
		'Ammo'	: bulletPickup
	}

def loadGameImage(path : str, width : int, height : int):
		image = pygame.image.load(path)
		image = pygame.transform.scale(image, (width, height))
		return image

def loadStaticImage(path : str):
		image = pygame.image.load(path)
		return image

def updateGameMechanics(engineWindow : pygame.Surface, world : list):
	playersGroup.update(world)
	for enemy in enemyGroup:
		enemy.handleAI(world)
	bulletGroup.update(world)
	grenadeGroup.update(world)
	explosionGroup.update()
	gamePickups.update(engineWindow)
	gameObjects.update()
	chemicalsGroup.update()
	gameExits.update()

def drawGameSprites(engineWindow : pygame.Surface, world : list):
	world.draw(engineWindow)
	for player in playersGroup:
		player.draw(engineWindow)

	for enemy in enemyGroup:
		enemy.draw(engineWindow)

	for bullet in bulletGroup:
		bullet.draw(engineWindow)

	for grenade in grenadeGroup:
		grenade.draw(engineWindow)

	for explosion in explosionGroup:
		explosion.draw(engineWindow)
	
	for pickup in gamePickups:
		pickup.draw(engineWindow)
	
	for object in gameObjects:
		object.draw(engineWindow)

	for chemical in chemicalsGroup:
		chemical.draw(engineWindow)
	
	for exit in gameExits:
		exit.draw(engineWindow)

	for health in healthBarGroup:
		health.draw(engineWindow)

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
					elif(t == 10):
						chemicals = Object(tile, x * tileSize, y * tileSize)
						chemicalsGroup.add(chemicals)

					elif(t == 9 or t == 11):
						object = Object(tile, x * tileSize, y * tileSize)
						gameObjects.add(object)

					elif(t == 19):
						# Player:
						gamePlayer = Soldier('Player', x * tileSize, y * tileSize, 2, 4, 32, 3)
						playersGroup.add(gamePlayer)

						# Health Bar:
						healthBar = HBar(gamePlayer, 30, 70)
						healthBarGroup.append(healthBar)

					elif(t == 20):
						# Enemy:
						gameEnemy = Soldier('Enemy', x * tileSize, y * tileSize + 15, 2, 1, 24, 0)
						enemyGroup.add(gameEnemy)

					# Pickups:
					elif(t == 21):
						ammoPickup = Pickup('Ammo', x * tileSize, y * tileSize)
						gamePickups.add(ammoPickup)

					elif(t == 22):
						grenadePickup = Pickup('Grenade', x * tileSize, y * tileSize)
						gamePickups.add(grenadePickup)

					elif(t == 23):
						healthPickup = Pickup('Health', x * tileSize, y * tileSize)
						gamePickups.add(healthPickup)

					# Exit: 
					elif(t == 17):
						exit = Object(tile, x * tileSize, y * tileSize)
						gameExits.add(exit)

	def draw(self, engineWindow : pygame.Surface):
		global screenScroll
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

	def update(self, world : list):
		global shoot, throwGrenade, grenadeThrown, backgroundScroll, screenScroll, levelComplete
		self.updateAnimation()
		self.isAlive()
		screenScroll, levelComplete = self.move(world)
		backgroundScroll -= screenScroll
		if(self.shootTimer > 0):
			self.shootTimer -= 1
		if(shoot == True):
			self.shoot()
		if(throwGrenade == True):
			if(throwGrenade and grenadeThrown == False and self.grenades > 0):
				grenade = Grenade(self.rect.centerx, self.rect.top, self.direction)
				grenadeGroup.add(grenade)
				grenadeThrown = True
				self.grenades -= 1


	def move(self, world : list):
		global shoot, throwGrenade, grenadeThrown, screenScroll
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

		levelComplete = False
		if(pygame.sprite.spritecollide(self, gameExits, False)):
			levelComplete = True


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

	def handleAI(self, world : list):
			move = 0
			self.updateAnimation()
			self.isAlive()
			if(self.shootTimer > 0):
				self.shootTimer -= 1
			for player in playersGroup:
				if(self.alive and player.alive):
					if(self.idle == False and random.randint(1, 512) == 6):
						self.updateAction(0)
						self.idle = True
						self.idleCounter = 50
					if(self.enemyVision.colliderect(player.rect)):
						self.updateAction(0)
						self.shoot()
					else:
						if(self.idle == False):
							if(self.direction == 1):
								move = 1
								self.flip = False
							else:
								self.flip = True
								move = -1
							self.rect.x += move
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
			self.rect.x += screenScroll

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


	def shoot(self):
		if(self.shootTimer == 0 and self.ammo > 0):
			self.shootTimer = 10
			bullet = Bullet(self.rect.centerx + (0.6 * self.rect.size[0] * self.direction), self.rect.centery+10, self.direction)
			bulletGroup.add(bullet)
			self.ammo -= 1

	def draw(self, engineWindow : pygame.Surface):
		engineWindow.blit(pygame.transform.flip(self.image, self.flip, False), self.rect)

# Objects: #

class Object(pygame.sprite.Sprite):
	def __init__(self, image : pygame.Surface, x : int, y : int):
		pygame.sprite.Sprite.__init__(self)
		self.image = image
		self.rect = self.image.get_rect()
		self.rect.midtop = (x + tileSize // 2, y + (tileSize - self.image.get_height()))

	def draw(self, engineWindow : pygame.Surface):
		engineWindow.blit(self.image, self.rect)

	def update(self):
		global screenScroll
		self.rect.x += screenScroll

# Pickup Class: #

class Pickup(pygame.sprite.Sprite):
	def __init__(self, type : str, x : int, y : int):
		pygame.sprite.Sprite.__init__(self)
		self.type = type
		self.image = pickups[self.type]
		self.rect = self.image.get_rect()
		self.rect.midtop = (x + tileSize // 2, y + (tileSize - self.image.get_height()))

	def draw(self, engineWindow : pygame.Surface):
		engineWindow.blit(self.image, self.rect)

	def update(self, engineWindow : pygame.Surface):
		for player in playersGroup:
			if(pygame.sprite.collide_rect(self, player)):
				if(self.type == 'Ammo'):
					player.ammo += 7
				elif(self.type == 'Health'):
					player.health += 50
					if(player.health > player.maxHealth):
						player.health = player.maxHealth
				elif(self.type == 'Grenade'):
					player.grenades += 3
				self.kill()
		global screenScroll
		self.rect.x += screenScroll

# Health Bar: #

class HBar():
	def __init__(self, player : pygame.Surface, x : int, y : int):
		pygame.sprite.Sprite.__init__(self)
		self.x = x
		self.y = y
		self.health = player.health
		self.maxHealth = player.maxHealth
		self.player = player

	def draw(self, engineWindow : pygame.Surface):
		self.health = self.player.health
		pygame.draw.rect(engineWindow, (0, 0, 0), (self.x - 2, self.y - 2, 154, 24))
		pygame.draw.rect(engineWindow, (250, 0, 0), (self.x, self.y, 150, 20))
		pygame.draw.rect(engineWindow, (0, 250, 0), (self.x, self.y, 150 * (self.health / self.maxHealth), 20))


# Bullet Class: #

class Bullet(pygame.sprite.Sprite):
	def __init__(self, x : int, y : int, direction : int):
		pygame.sprite.Sprite.__init__(self)
		self.speed = 10
		self.image = pygame.image.load('assets/Bullet.png')
		self.rect = self.image.get_rect()
		self.rect.center = (x, y)
		self.direction = direction

	def draw(self, engineWindow : pygame.Surface):
		engineWindow.blit(self.image, self.rect)

	def update(self, world):
		self.rect.x += (self.direction * self.speed) + screenScroll
		if(self.rect.right < 0 or self.rect.left > windowWidth):
			self.kill
		for tile in world.obstacleList:
			if(tile[1].colliderect(self.rect)):
				self.kill()

		for player in playersGroup:
			if(pygame.sprite.spritecollide(player, bulletGroup, False)):
				if(player.alive):
					player.health -= 5
					self.kill()

		for enemy in enemyGroup:
			if(pygame.sprite.spritecollide(enemy, bulletGroup, False)):
				if(enemy.alive):
					enemy.health -= 25
					self.kill()


class Grenade(pygame.sprite.Sprite):
	def __init__(self, x, y, direction):
		pygame.sprite.Sprite.__init__(self)
		self.timer = 100
		self.velocityY = -11
		self.speed = 7
		self.image = pygame.image.load('assets/Grenade.png').convert_alpha()
		self.rect = self.image.get_rect()
		self.rect.center = (x, y)
		self.width = self.image.get_width()
		self.height = self.image.get_height()
		self.direction = direction

	def draw(self, engineWindow : pygame.Surface):
		engineWindow.blit(self.image, self.rect)

	def update(self, world):
		self.velocityY += engineGravity
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


		if(self.rect.left + deltaX < 0 or self.rect.right + deltaX > windowWidth):
			self.direction *= -1
			deltaX = self.direction * self.speed

		self.rect.x += deltaX + screenScroll
		self.rect.y += deltaY

		self.timer -= 1
		if(self.timer <= 0):
			self.kill()
			explosion = Explosion(self.rect.x, self.rect.y)
			explosionGroup.add(explosion)
			for player in playersGroup:
				if (abs(self.rect.centerx - player.rect.centerx) < tileSize * 2 and (self.rect.centery - player.rect.centery) < tileSize * 2):
					player.health -= 50
			for enemy in enemyGroup:
				if (abs(self.rect.centerx - enemy.rect.centerx) < tileSize * 2 and (self.rect.centery - enemy.rect.centery) < tileSize * 2):
					enemy.health -= 100

class Explosion(pygame.sprite.Sprite):
	def __init__(self, x, y):
		pygame.sprite.Sprite.__init__(self)
		self.explosions = []
		for c in range(19):
			image = pygame.image.load(f'assets/Explosion/{c}.png')
			image = pygame.transform.scale(image, (int(image.get_width() * 5), int(image.get_height() * 5)))
			self.explosions.append(image)
		self.index = 0
		self.image = self.explosions[self.index]
		self.rect = self.image.get_rect()
		self.rect.x = x
		self.rect.y = y
		self.rect.center = (x, y-80)
		self.timer = 0

	def draw(self, engineWindow : pygame.Surface):
		engineWindow.blit(self.image, self.rect)

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
		global screenScroll
		self.rect.x += screenScroll
