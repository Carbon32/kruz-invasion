# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
#                                                                             #
#                 Kruz Invasion, shooter video game                           #
#                                   based in World War II                     #
#                                             Developer: Carbon               #
#                                                                             #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 

# Imports: #

import pygame
import random
import os

# Pygame Initialization: #

pygame.init()

# Game Variables: #

gameRunning = True
moveLeft = False
moveRight = False
gameGravity = 0.75
shoot = False
throwGrenade = False
grenadeThrown = False
tileSize = 50

# Game Window: #

screenWidth = 1024
screenHeight = int(screenWidth * 0.8)

gameWindow = pygame.display.set_mode((screenWidth, screenHeight))
pygame.display.set_caption("Kruz Invasion:")

# Frame Limiter: #

handleFPS = pygame.time.Clock()
FPS = 60

# Pickups: #

healthPickup = pygame.image.load('assets/Pickups/Health_Pickup.png').convert_alpha()
grenadePickup = pygame.image.load('assets/Pickups/Grenade_Pickup.png').convert_alpha()
bulletPickup = pygame.image.load('assets/Pickups/Bullet_Pickup.png').convert_alpha()

pickups = {
	'Health'	: healthPickup,
	'Grenade'	: grenadePickup,
	'Bullets'	: bulletPickup
}

# Text: #

font = pygame.font.SysFont('System', 30)

def drawText(text, color, x, y):
	image = font.render(text, True, color)
	gameWindow.blit(image, (x, y))

# Player Class: #

class Soldier(pygame.sprite.Sprite):
	def __init__(self, type, x, y, scale, speed, ammo, grenades):
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
				gameImage = pygame.image.load(f'assets/{self.type}/{animation}/{c}.png').convert_alpha()
				gameImage = pygame.transform.scale(gameImage, (gameImage.get_width() * scale, gameImage.get_height() * scale))
				tempList.append(gameImage)
			self.animationList.append(tempList)

		self.image = self.animationList[self.action][self.index]
		self.rect = self.image.get_rect()
		self.rect.center = (x, y)

	def update(self):
		self.updateAnimation()
		self.isAlive()
		if(self.shootTimer > 0):
			self.shootTimer -= 1

	def move(self, movingLeft, movingRight):
		deltaX = 0
		deltaY = 0
		if(movingLeft):
			deltaX = -self.speed
			self.flip = True
			self.direction = -1

		if(movingRight):
			deltaX = self.speed
			self.flip = False
			self.direction = 1

		if(self.jump == True and self.inAir == False):
			self.velocityY = -10
			self.jump = False
			self.inAir = True

		self.velocityY += gameGravity
		if(self.velocityY > 10):
			self.velocityY = 10
			self.inAir = False
		deltaY += self.velocityY

		# Collision:
		if(self.rect.bottom + deltaY > 500):
			deltaY = 500 - self.rect.bottom

		self.rect.x += deltaX
		self.rect.y += deltaY

	def handleAI(self):
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

	def updateAnimation(self):
		animTime = 130
		self.image = self.animationList[self.action][self.index]
		if(pygame.time.get_ticks() - self.time > animTime):
			self.time = pygame.time.get_ticks()
			self.index += 1
		if(self.index >= len(self.animationList[self.action])):
			if(self.action == 2):
				self.index = len(self.animationList[self.action]) - 1
			else:
				self.index = 0

	def updateAction(self, newAction):
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
			self.shootTimer = 40
			bullet = Bullet(self.rect.centerx + (0.6 * self.rect.size[0] * self.direction), self.rect.centery+10, self.direction)
			bulletGroup.add(bullet)
			self.ammo -= 1

	def draw(self):
		gameWindow.blit(pygame.transform.flip(self.image, self.flip, False), self.rect)


# Pickup Class: #

class Pickup(pygame.sprite.Sprite):
	def __init__(self, type, x, y):
		pygame.sprite.Sprite.__init__(self)
		self.type = type
		self.image = pickups[self.type]
		self.rect = self.image.get_rect()
		self.rect.midtop = (x + tileSize // 2, y + (tileSize - self.image.get_height()))

	def update(self):
		if(pygame.sprite.collide_rect(self, gamePlayer)):
			if(self.type == 'Bullets'):
				gamePlayer.ammo += 7
			elif(self.type == 'Health'):
				gamePlayer.health += 50
				if(gamePlayer.health > gamePlayer.maxHealth):
					gamePlayer.health = maxHealth
			elif(self.type == 'Grenade'):
				gamePlayer.grenades += 3
			self.kill()

# Health Bar: #

class HBar():
	def __init__(self, x, y):
		self.x = x
		self.y = y
		self.health = gamePlayer.health
		self.maxHealth = gamePlayer.maxHealth

	def draw(self, health):
		self.health = health
		pygame.draw.rect(gameWindow, (0, 0, 0), (self.x - 2, self.y - 2, 154, 24))
		pygame.draw.rect(gameWindow, (250, 0, 0), (self.x, self.y, 150, 20))
		pygame.draw.rect(gameWindow, (0, 250, 0), (self.x, self.y, 150 * (self.health / self.maxHealth), 20))

# Bullet Class: #

class Bullet(pygame.sprite.Sprite):
	def __init__(self, x, y, direction):
		pygame.sprite.Sprite.__init__(self)
		self.speed = 10
		self.image = pygame.image.load('assets/Bullet.png').convert_alpha()
		self.rect = self.image.get_rect()
		self.rect.center = (x, y)
		self.direction = direction

	def update(self):
		self.rect.x += (self.direction * self.speed)
		if(self.rect.right < 0 or self.rect.left > screenWidth):
			self.kill

		if(pygame.sprite.spritecollide(gamePlayer, bulletGroup, False)):
			if(gamePlayer.alive):
				gamePlayer.health -= 5
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
		self.image = pygame.transform.scale(self.image, (10, 10))
		self.rect = self.image.get_rect()
		self.rect.center = (x, y)
		self.direction = direction

	def update(self):
		self.velocityY += gameGravity
		deltaX = self.direction * self.speed 
		deltaY = self.velocityY
		if(self.rect.bottom + deltaY > 500):
			deltaY = 500 - self.rect.bottom
			self.speed = 0

		if(self.rect.left + deltaX < 0 or self.rect.right + deltaX > screenWidth):
			self.direction *= -1
			deltaX = self.direction * self.speed

		self.rect.x += deltaX
		self.rect.y += deltaY

		self.timer -= 1
		if(self.timer <= 0):
			self.kill()
			explosion = Explosion(self.rect.x, self.rect.y)
			explosionGroup.add(explosion)
			if abs((self.rect.centerx - gamePlayer.rect.centerx) < tileSize * 2 and (self.rect.centery - gamePlayer.rect.centery) < tileSize * 2):
				gamePlayer.health -= 50
			for enemy in enemyGroup:
				if abs((self.rect.centerx - enemy.rect.centerx) < tileSize * 2 and (self.rect.centery - enemy.rect.centery) < tileSize * 2):
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
		self.rect.x = x-250
		self.rect.y = 150 # Pff quick fix
		self.timer = 0

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


# Game Creations: #

# Groups: 
bulletGroup = pygame.sprite.Group()
grenadeGroup = pygame.sprite.Group()
explosionGroup = pygame.sprite.Group()
enemyGroup = pygame.sprite.Group()
gamePickups = pygame.sprite.Group()

# Pickups:
grenadePickup = Pickup('Grenade', 300, 450)
gamePickups.add(grenadePickup)

# Player:
gamePlayer = Soldier('Player', 100, 0, 3, 4, 7, 3)

# Enemy:
gameEnemy = Soldier('Enemy', 400, 450, 3, 1, 24, 0)
enemyGroup.add(gameEnemy)

# User Interface:
healthBar = HBar(30, 70)

# Game Loop: #

while(gameRunning):
	handleFPS.tick(FPS)
	gameWindow.fill((125, 255, 255))
	pygame.draw.line(gameWindow, (0, 0, 0), (0, 500), (screenWidth, 500))

	# User Interface:
	drawText(f'Ammo: {gamePlayer.ammo}', (0, 0, 0), 30, 20)
	drawText(f'Grenades: {gamePlayer.grenades}', (0, 0, 0), 150, 20)
	healthBar.draw(gamePlayer.health)

	# Player:
	gamePlayer.update()
	gamePlayer.draw()

	# Enemies:
	for enemy in enemyGroup:
		enemy.handleAI()
		enemy.update()
		enemy.draw()

	# Bullets & Grenades:
	bulletGroup.update()
	grenadeGroup.update()
	bulletGroup.draw(gameWindow)
	grenadeGroup.draw(gameWindow)

	# Game Explosions: 
	explosionGroup.update()
	explosionGroup.draw(gameWindow)

	# Game Pickups: 
	gamePickups.update()
	gamePickups.draw(gameWindow)

	if(gamePlayer.alive):
		if(shoot):
			gamePlayer.shoot()
		elif(throwGrenade and grenadeThrown == False and gamePlayer.grenades > 0):
			grenade = Grenade(gamePlayer.rect.centerx, gamePlayer.rect.top, gamePlayer.direction)
			grenadeGroup.add(grenade)
			grenadeThrown = True
			gamePlayer.grenades -= 1
		elif(moveLeft or moveRight):
			gamePlayer.updateAction(1)
		else:
			gamePlayer.updateAction(0)
		gamePlayer.move(moveLeft, moveRight)

	# Event Handler:
	for event in pygame.event.get():
		if(event.type == pygame.QUIT):
			gameRunning = False

		# Movement:
		if(event.type == pygame.KEYDOWN):
			if(event.key == pygame.K_d):
				moveRight = True
			if(event.key == pygame.K_q):
				moveLeft = True
			if(event.key == pygame.K_SPACE and gamePlayer.alive):
				gamePlayer.jump = True
			if(event.key == pygame.K_ESCAPE):
				gameRunning = False
			if(event.key == pygame.K_e):
				shoot = True
			if(event.key == pygame.K_a):
				throwGrenade = True

		if(event.type == pygame.KEYUP):
			if(event.key == pygame.K_d):
				moveRight = False
			if(event.key == pygame.K_q):
				moveLeft = False
			if(event.key == pygame.K_e):
				shoot = False
			if(event.key == pygame.K_a):
				throwGrenade = False
				grenadeThrown = False


	pygame.display.update()


pygame.quit()

