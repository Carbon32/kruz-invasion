# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
#                                                                             #
#                   Kruz Invasion, Level Editor                               #
#                                         Developer: Carbon                   #
#                                                                             #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 

# Imports: #

import pygame
import csv

# Pygame Initialization: #

pygame.init()

handleFPS = pygame.time.Clock()
FPS = 60

# Window Creation: #

screenWidth = 800
screenHeight = 640
lowerMargin = 100
sideMargin = 300

editorWindow = pygame.display.set_mode((screenWidth + sideMargin, screenHeight + lowerMargin))
pygame.display.set_caption('Kruz Invasion: Level Editor')

# Editor Variables: #

editorRunning = True
editorRows = 16
editorColumns = 150
tileSize = screenHeight // editorRows
editorTiles = 24
level = 0
thisTile = 0
scrollLeft = False
scrollRight = False
scroll = 0
scrollSpeed = 1

# Editor Images: #

pineTrees = pygame.image.load('assets/Background/Pines.png').convert_alpha()
pineTrees_2 = pygame.image.load('assets/Background/Pines_2.png').convert_alpha()
mountain = pygame.image.load('assets/Background/Mountain.png').convert_alpha()
sky = pygame.image.load('assets/Background/Sky.png').convert_alpha()


# Button Class:

class Button():
	def __init__(self, x, y, image, scale):
		width = image.get_width()
		height = image.get_height()
		self.image = pygame.transform.scale(image, (int(width * scale), int(height * scale)))
		self.rect = self.image.get_rect()
		self.rect.topleft = (x, y)
		self.clicked = False

	def draw(self):
		action = False
		position = pygame.mouse.get_pos()
		if self.rect.collidepoint(position):
			if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
				action = True
				self.clicked = True

		if pygame.mouse.get_pressed()[0] == 0:
			self.clicked = False

		editorWindow.blit(self.image, (self.rect.x, self.rect.y))
		return action


# Tile loading: #

tilesList = []
for c in range(editorTiles):
	image = pygame.image.load(f'assets/Tiles/{c}.png').convert_alpha()
	image = pygame.transform.scale(image, (tileSize, tileSize))
	tilesList.append(image)

saveButton = pygame.image.load('assets/Save.png').convert_alpha()
loadButton = pygame.image.load('assets/Load.png').convert_alpha()
resetButton = pygame.image.load('assets/Reset.png').convert_alpha()
saveButton = pygame.transform.scale(saveButton, (saveButton.get_width() * 5, saveButton.get_height() * 5))
loadButton = pygame.transform.scale(loadButton, (loadButton.get_width() * 5, loadButton.get_height() * 5))
resetButton = pygame.transform.scale(resetButton, (resetButton.get_width() * 5, resetButton.get_height() * 5))

# Editor Font: #

font = pygame.font.SysFont('Impact', 15)

# Tile List: #

worldData = []
for row in range(editorRows):
	r = [-1] * editorColumns
	worldData.append(r)

# Ground Creation: #

for tile in range(0, editorColumns):
	worldData[editorRows - 1][tile] = 0


# Editor Text: #

def drawText(text, font, textColumn, x, y):
	image = font.render(text, True, textColumn)
	editorWindow.blit(image, (x, y))

# Load Background: #

def drawBackground():
	editorWindow.fill((144, 201, 120))
	width = sky.get_width()
	for x in range(4):
		editorWindow.blit(sky, ((x * width) - scroll * 0.5, 0))
		editorWindow.blit(mountain, ((x * width) - scroll * 0.6, screenHeight - mountain.get_height() - 300))
		editorWindow.blit(pineTrees, ((x * width) - scroll * 0.7, screenHeight - pineTrees.get_height() - 150))
		editorWindow.blit(pineTrees_2, ((x * width) - scroll * 0.8, screenHeight - pineTrees_2.get_height()))

# Draw Grid: #

def drawGrid():
	for c in range(editorColumns + 1):
		pygame.draw.line(editorWindow, ((255, 255, 255)), (c * tileSize - scroll, 0), (c * tileSize - scroll, screenHeight))

	for c in range(editorRows + 1):
		pygame.draw.line(editorWindow, ((255, 255, 255)), (0, c * tileSize), (screenWidth, c * tileSize))


# Draw World: #

def drawWorld():
	for y, row in enumerate(worldData):
		for x, tile in enumerate(row):
			if tile >= 0:
				editorWindow.blit(tilesList[tile], (x * tileSize - scroll, y * tileSize))

# Editor Buttons: #

buttonSave = Button(screenWidth // 2, screenHeight + lowerMargin - 120, saveButton, 1)
butttonLoad = Button(screenWidth // 2 + 200, screenHeight + lowerMargin - 120, loadButton, 1)
buttonReset = Button(screenWidth // 2 +  400, screenHeight + lowerMargin - 120, resetButton, 1)

buttonList = []
buttonColumn = 0
buttonRow = 0

for i in range(len(tilesList)):
	tileButton = Button(screenWidth + (75 * buttonColumn) + 50, 75 * buttonRow + 50, tilesList[i], 1)
	buttonList.append(tileButton)
	buttonColumn += 1
	if buttonColumn == 3:
		buttonRow += 1
		buttonColumn = 0


# Editor Loop: #

while editorRunning:

	handleFPS.tick(FPS)
	drawBackground()
	drawGrid()
	drawWorld()

	drawText(f'Level: {level}', font, ((255, 255, 255)), 10, screenHeight + lowerMargin - 90)
	drawText('Press UP or DOWN to change level', font, ((255, 255, 255)), 10, screenHeight + lowerMargin - 60)

	# Save & Load:
	if buttonSave.draw():
		with open(f'levels/level{level}_data.csv', 'w', newline='') as csvfile:
			writer = csv.writer(csvfile, delimiter = ',')
			for row in worldData:
				writer.writerow(row)

	if butttonLoad.draw():
		scroll = 0
		with open(f'levels/level{level}_data.csv', newline='') as csvfile:
			reader = csv.reader(csvfile, delimiter = ',')
			for x, row in enumerate(reader):
				for y, tile in enumerate(row):
					worldData[x][y] = int(tile)

	if buttonReset.draw():
		worldData = []
		for row in range(editorRows):
			r = [-1] * editorColumns
			worldData.append(r)
		for tile in range(0, editorColumns):
			worldData[editorRows - 1][tile] = 0
				
	# Draw Tiles: 
	pygame.draw.rect(editorWindow, ((123, 15, 16)), (screenWidth, 0, sideMargin, screenHeight))

	# Choose Tile:
	buttonCount = 0
	for buttonCount, c in enumerate(buttonList):
		if c.draw():
			thisTile = buttonCount

	# Highlight: 
	pygame.draw.rect(editorWindow, ((255, 0, 0)), buttonList[thisTile].rect, 3)

	# Scrolling: 
	if scrollLeft == True and scroll > 0:
		scroll -= 5 * scrollSpeed
	if scrollRight == True and scroll < (editorColumns * tileSize) - screenWidth:
		scroll += 5 * scrollSpeed

	# Adding Tiles: 
	position = pygame.mouse.get_pos()
	x = (position[0] + scroll) // tileSize
	y = position[1] // tileSize

	if position[0] < screenWidth and position[1] < screenHeight:
		if pygame.mouse.get_pressed()[0] == 1:
			if worldData[y][x] != thisTile:
				worldData[y][x] = thisTile
		if pygame.mouse.get_pressed()[2] == 1:
			worldData[y][x] = -1


	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			editorRunning = False

		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_UP:
				level += 1
			if event.key == pygame.K_DOWN and level > 0:
				level -= 1
			if event.key == pygame.K_LEFT:
				scrollLeft = True
			if event.key == pygame.K_RIGHT:
				scrollRight = True
			if event.key == pygame.K_RSHIFT:
				scrollSpeed = 5


		if event.type == pygame.KEYUP:
			if event.key == pygame.K_LEFT:
				scrollLeft = False
			if event.key == pygame.K_RIGHT:
				scrollRight = False
			if event.key == pygame.K_RSHIFT:
				scrollSpeed = 1


	pygame.display.update()
pygame.quit()