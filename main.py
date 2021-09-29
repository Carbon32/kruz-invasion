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
	def __init__(self, type, x, y, scale, speed):
		pygame.sprite.Sprite.__init__(self)
		self.type = type
		self.x = x
		self.y = y
		self.speed = speed
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
		animationTypes = ['Idle', 'Move']
		for animation in animationTypes:
			tempList = []
			for c in range(3): # Loading Idle animations
				gameImage = pygame.image.load(f'assets/{self.type}/{animation}/{c}.png')
				gameImage = pygame.transform.scale(gameImage, (gameImage.get_width() * scale, gameImage.get_height() * scale))
				tempList.append(gameImage)
			self.animationList.append(tempList)

		self.playerSprite = self.animationList[self.action][self.index]
		self.playerRect = self.playerSprite.get_rect()
		self.playerRect.center = (x, y)


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
		if(self.playerRect.bottom + deltaY > 500):
			deltaY = 500 - self.playerRect.bottom

		self.playerRect.x += deltaX
		self.playerRect.y += deltaY

	def updateAnimation(self):
		animTime = 100
		self.playerSprite = self.animationList[self.action][self.index]
		if(pygame.time.get_ticks() - self.time > animTime):
			self.time = pygame.time.get_ticks()
			self.index += 1
		if(self.index >= len(self.animationList[self.action])):
			self.index = 0

	def updateAction(self, newAction):
		if(newAction != self.action):
			self.action = newAction
			self.index = 0
			self.time = pygame.time.get_ticks()

	def draw(self):
		gameWindow.blit(pygame.transform.flip(self.playerSprite, self.flip, False), self.playerRect)

# Game Loop: #

firstSoldier = Soldier('Player', 200, 200, 2, 5)

while(gameRunning):

	handleFPS.tick(FPS)
	gameWindow.fill((125, 255, 255))
	pygame.draw.line(gameWindow, (0, 0, 0), (0, 500), (screenWidth, 500))
	firstSoldier.updateAnimation()
	firstSoldier.draw()
	if(firstSoldier.alive):
		if(moveLeft or moveRight):
			firstSoldier.updateAction(1)
		else:
			firstSoldier.updateAction(0)
		firstSoldier.move(moveLeft, moveRight)

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

		if(event.type == pygame.KEYUP):
			if(event.key == pygame.K_d):
				moveRight = False
			if(event.key == pygame.K_q):
				moveLeft = False


	pygame.display.update()


pygame.quit()

