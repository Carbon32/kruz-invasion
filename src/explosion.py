# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
#                                                                             #
#                Invasion Engine, Land Invasion's Game Engine                 #
#                            Developer: Carbon                                #
#                                                                             #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

# Imports: #

from src.modules import *

# Explosion: #

class Explosion(pygame.sprite.Sprite):
	def __init__(self, game, x, y):
		pygame.sprite.Sprite.__init__(self)

		# Game:

		self.game = game

		# Explosions list:

		self.explosions = []

		# Explosion Sprite Loading:

		for c in range(19):
			image = self.game.load_game_image(f'assets/Explosion/{c}.png', self.game.screen_width // 3, self.game.screen_width // 3)
			self.explosions.append(image)

		# Explosion Settings:

		self.index = 0
		self.image = self.explosions[self.index]
		self.rect = self.image.get_rect()
		self.rect.x = x
		self.rect.y = y
		self.rect.center = (x, y)
		self.timer = 0

	def render(self):
		self.game.display.blit(self.image, self.rect)

	def update(self):
		explosion_speed = 3
		self.timer += 1
		if(self.timer >= explosion_speed):
			self.timer = 0
			self.index += 1
			if(self.index >= len(self.explosions)):
				self.kill()
			else:
				self.image = self.explosions[self.index]

		self.rect.x += self.game.screen_scroll