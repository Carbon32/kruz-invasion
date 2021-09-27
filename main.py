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
		self.direction = 1
		self.flip = False
		gameImage = pygame.image.load(f'assets/{self.type}/Idle/0.png')
		self.playerSprite = pygame.transform.scale(gameImage, (gameImage.get_width() * scale, gameImage.get_height() * scale))
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

		self.playerRect.x += deltaX
		self.playerRect.y += deltaY


	def draw(self):
		gameWindow.blit(pygame.transform.flip(self.playerSprite, self.flip, False), self.playerRect)

# Game Loop: #

firstSoldier = Soldier('Player', 200, 200, 2, 5)
secondSoldier = Soldier('Enemy', 300, 300, 2, 5)

while(gameRunning):

	handleFPS.tick(FPS)
	gameWindow.fill((125, 255, 255))
	firstSoldier.draw()
	secondSoldier.draw()
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
			if(event.key == pygame.K_ESCAPE):
				gameRunning = False

		if(event.type == pygame.KEYUP):
			if(event.key == pygame.K_d):
				moveRight = False
			if(event.key == pygame.K_q):
				moveLeft = False


	pygame.display.update()


pygame.quit()

