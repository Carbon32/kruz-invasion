# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
#                                                                             #
#                 Kruz Invasion, shooter video game                           #
#                                   based in World War II                     #
#                                             Developer: Carbon               #
#                                                                             #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 

# Imports: #

import pygame

# Pygame Initialization: #

pygame.init()

# Game Variables: #

gameRunning = True
moveLeft = False
moveRight = False
gameGravity = 0.75
shoot = False

# Game Window: #

screenWidth = 800
screenHeight = int(screenWidth * 0.8)

gameWindow = pygame.display.set_mode((screenWidth, screenHeight))
pygame.display.set_caption("Kruz Invasion:")

# Frame Limiter: #

handleFPS = pygame.time.Clock()
FPS = 60

# Player Class: #

class Soldier(pygame.sprite.Sprite):
	def __init__(self, type, x, y, scale, speed, ammo):
		pygame.sprite.Sprite.__init__(self)
		self.type = type
		self.health = 100
		self.maxHealth = self.health
		self.x = x
		self.y = y
		self.speed = speed
		self.ammo = ammo
		self.startAmmo = ammo
		self.shootTimer = 0
		self.alive = True
		self.direction = 1
		self.jump = False
		self.inAir = True
		self.velocityY = 0
		self.flip = False
		self.time = pygame.time.get_ticks()
		self.animationList = []
		self.index = 0
		self.action = 0

		# Loading Sprites: #
		animationTypes = ['Idle', 'Move', 'Death']
		for animation in animationTypes:
			tempList = []
			for c in range(3): # Loading all animations
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

	def updateAnimation(self):
		animTime = 100
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
			self.shootTimer = 20
			bullet = Bullet(self.rect.centerx + (0.6 * self.rect.size[0] * self.direction), self.rect.centery, self.direction)
			bulletGroup.add(bullet)
			self.ammo -= 1

	def draw(self):
		gameWindow.blit(pygame.transform.flip(self.image, self.flip, False), self.rect)

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

		if(pygame.sprite.spritecollide(gameEnemy, bulletGroup, False)):
			if(gameEnemy.alive):
				gameEnemy.health -= 25
				self.kill()

# Game Loop: #

bulletGroup = pygame.sprite.Group()

gamePlayer = Soldier('Player', 100, 0, 2, 5, 7)
gameEnemy = Soldier('Enemy', 100, 467, 2, 5, 7)

while(gameRunning):

	handleFPS.tick(FPS)
	gameWindow.fill((125, 255, 255))
	pygame.draw.line(gameWindow, (0, 0, 0), (0, 500), (screenWidth, 500))

	# Soldiers:
	gamePlayer.update()
	gameEnemy.update()

	gamePlayer.draw()
	gameEnemy.draw()

	# Bullets:
	bulletGroup.update()
	bulletGroup.draw(gameWindow)

	if(gamePlayer.alive):
		if(shoot):
			gamePlayer.shoot()

		if(moveLeft or moveRight):
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
			if(event.key == pygame.K_SPACE and firstSoldier.alive):
				firstSoldier.jump = True
			if(event.key == pygame.K_ESCAPE):
				gameRunning = False
			if(event.key == pygame.K_e):
				shoot = True

		if(event.type == pygame.KEYUP):
			if(event.key == pygame.K_d):
				moveRight = False
			if(event.key == pygame.K_q):
				moveLeft = False
			if(event.key == pygame.K_e):
				shoot = False


	pygame.display.update()


pygame.quit()

