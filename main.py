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
testPlayer = pygame.image.load('assets/Player/Idle/0.png')

# Game Window: #

screenWidth = 800
screenHeight = int(screenWidth * 0.8)

gameWindow = pygame.display.set_mode((screenWidth, screenHeight))
pygame.display.set_caption("Kruz Invasion:")


# Player Class: #

class Soldier(pygame.sprite.Sprite):
	def __init__(self, x, y):
		pygame.sprite.Sprite.__init__(self)
		self.x = x
		self.y = y
		self.playerSprite = pygame.transform.scale(testPlayer, (testPlayer.get_width() * 2, testPlayer.get_height() * 2))
		self.playerRect = self.playerSprite.get_rect()
		self.playerRect.center = (x, y)

	def draw(self):
		gameWindow.blit(self.playerSprite, self.playerRect)

# Game Loop: #

firstSoldier = Soldier(200, 200)
secondSoldier = Soldier(300, 300)

while(gameRunning):

	
	firstSoldier.draw()
	secondSoldier.draw()

	# Event Handler:
	for event in pygame.event.get():
		if(event.type == pygame.QUIT):
			gameRunning = False

	pygame.display.update()


pygame.quit()

