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

level = 1
levelRows = 16
levelColumns = 150
tileSize = 50
engineTiles = 24

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

	def draw(self, engineWindow):
		for tile in self.obstacleList:
			tile[1][0] += screenScroll
			engineWindow.blit(tile[0], tile[1])