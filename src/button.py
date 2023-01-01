# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
#                                                                             #
#                Invasion Engine, Land Invasion's Game Engine                 #
#                            Developer: Carbon                                #
#                                                                             #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

# Imports: #

from src.modules import *

# Button: #

class Button():
    def __init__(self, display, x, y, image):

        # Display:
        self.display = display

        # Button Properties:

        self.image = image
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.clicked = False
        self.button_cooldown = 100
        self.button_timer = pygame.time.get_ticks()

    def render(self):
        action = False
        position = pygame.mouse.get_pos()
        if self.rect.collidepoint(position):
            if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
                if(pygame.time.get_ticks() - self.button_timer >= self.button_cooldown):
                    action = True
                    self.clicked = True
                    self.button_timer = pygame.time.get_ticks()
            
        if pygame.mouse.get_pressed()[0] == 0:
            self.clicked = False

        self.display.blit(self.image, (self.rect.x, self.rect.y))
        return action

    def change_button(self, image):
        self.image = image