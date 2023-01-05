# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
#                                                                             #
#                Invasion Engine, Land Invasion's Game Engine                 #
#                            Developer: Carbon                                #
#                                                                             #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

# Imports: #

from src.modules import *

# Buttons: #

class ButtonImage():
    def __init__(self, display, image, x, y, width, height, elevation, border_radius):

        # Game:

        self.display = display

        # Top Rectangle:

        self.top_rect = pygame.Rect((x, y), (width, height))
        self.original_top_rect_y = y
        self.top_color = (204,57,52)

        # Bottom Rectangle:

        self.bottom_rect = pygame.Rect((x, y), (width, height))
        self.bottom_color = (183,51,46)

        # Border Radius:

        self.border_radius = border_radius

        # Image:

        self.image = image
        self.image_rect = self.image.get_rect(center = self.top_rect.center)

        # Properties:

        self.elevation = elevation
        self.dynamic_elevation = elevation
        self.clicked = False
        self.action = False
        self.button_cooldown = 100
        self.button_timer = pygame.time.get_ticks()
        self.click_time = pygame.time.get_ticks()

    def render(self):
        self.top_rect.y = self.original_top_rect_y - self.dynamic_elevation
        self.image_rect.center = self.top_rect.center
        self.bottom_rect.midtop = self.top_rect.midtop
        self.bottom_rect.height = self.top_rect.height + self.dynamic_elevation
        pygame.draw.rect(self.display, self.bottom_color, self.bottom_rect, border_radius = self.border_radius)
        pygame.draw.rect(self.display, (122,34,31), self.bottom_rect, 2, border_radius = self.border_radius)
        pygame.draw.rect(self.display, self.top_color, self.top_rect, border_radius = self.border_radius)
        pygame.draw.rect(self.display, (122,34,31), self.top_rect, 2, border_radius = self.border_radius)
        self.display.blit(self.image, self.image_rect)
        position = pygame.mouse.get_pos()
        if(not self.action):
            if self.top_rect.collidepoint(position):
                self.top_color = (215, 75, 75)
                if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
                    if(pygame.time.get_ticks() - self.button_timer >= self.button_cooldown):
                        self.dynamic_elevation = 0
                        self.action = True
                        self.clicked = True
                        self.button_timer = pygame.time.get_ticks()
            else:
                self.top_color = (204,57,52)

        if pygame.mouse.get_pressed()[0] == 0:
            self.dynamic_elevation = self.elevation
            if(self.clicked):
                self.click_time = pygame.time.get_ticks()

            self.clicked = False
            if(self.action):
                if(pygame.time.get_ticks() - self.click_time > 100):
                    self.action = False
                    return True

    def change_button(self, image):
        self.image = image

class ButtonText():
    def __init__(self, game, text, x, y, width, height, elevation, font_type):

        # Game:

        self.game = game

        # Top Rectangle:

        self.top_rect = pygame.Rect((x, y), (width, height))
        self.original_top_rect_y = y
        self.top_color = (203, 92, 100)

        # Bottom Rectangle:

        self.bottom_rect = pygame.Rect((x, y), (width, height))
        self.bottom_color = (160, 68, 93)

        # Properties:

        self.elevation = elevation
        self.dynamic_elevation = elevation
        self.clicked = False
        self.action = False
        self.button_cooldown = 100
        self.button_timer = pygame.time.get_ticks()
        self.click_time = pygame.time.get_ticks()

        # Text:

        self.text_surface = self.game.fonts[font_type].render(text, True, (255, 255, 255))
        self.text_rect = self.text_surface.get_rect(center = self.top_rect.center)

    def render(self):
        self.top_rect.y = self.original_top_rect_y - self.dynamic_elevation
        self.text_rect.center = self.top_rect.center
        self.bottom_rect.midtop = self.top_rect.midtop
        self.bottom_rect.height = self.top_rect.height + self.dynamic_elevation
        pygame.draw.rect(self.game.display, self.bottom_color, self.bottom_rect, border_radius = 50)
        pygame.draw.rect(self.game.display, self.top_color, self.top_rect, border_radius = 50)
        self.game.display.blit(self.text_surface, self.text_rect)
        position = pygame.mouse.get_pos()
        if(not self.action):
            if self.top_rect.collidepoint(position):
                self.top_color = (215, 75, 75)
                if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
                    if(pygame.time.get_ticks() - self.button_timer >= self.button_cooldown):
                        self.dynamic_elevation = 0
                        self.action = True
                        self.clicked = True
                        self.button_timer = pygame.time.get_ticks()
            else:
                self.top_color = (203, 92, 100)
                self.bottom_color = (160, 68, 93)

        if pygame.mouse.get_pressed()[0] == 0:
            self.dynamic_elevation = self.elevation
            if(self.clicked):
                self.click_time = pygame.time.get_ticks()

            self.clicked = False
            if(self.action):
                if(pygame.time.get_ticks() - self.click_time > 100):
                    self.action = False
                    return True
    def change_color(self, first_color, second_color):
        self.top_color = first_color
        self.bottom_color = second_color

    def change_text(self, text):
        self.text_surface = self.game.game_font.render(text, True, (255, 255, 255))
        self.text_rect = self.text_surface.get_rect(center = self.top_rect.center)
        
class ButtonTile():
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