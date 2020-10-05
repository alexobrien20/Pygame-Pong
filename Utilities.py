import pygame
from pygame.locals import *

def draw_text(surf,text,size,x,y):
    font_name = pygame.font.Font("Molot.ttf",size)
    text_surface = font_name.render(text,True,(255,0,0))
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x,y)
    surf.blit(text_surface,text_rect)

class text_input_box:
    def __init__(self,x,y,width,height,text,SCREEN_WIDTH,SCREEN_HEIGHT):
        self.SCREEN_WIDTH = SCREEN_WIDTH
        self.SCREEN_HEIGHT = SCREEN_HEIGHT
        self.x = x
        self.y = y
        self.width = width
        self.height = height 
        self.text = text
        self.button = pygame.Rect((self.x,self.y,self.width,self.height))
        self.active = False
        self.user_input = ''
        self.colour_passive = ((255,255,255))
        self.colour_active = ((255,110,0))
        self.colour = self.colour_passive
        self.error_message = ''

    def check_user_input(self,user_input):
        if len(user_input) > 2 or user_input.isdigit() != True:
            self.error_message = "Input must be an integer between 1-99!"
        else:
            self.error_message = ''
    
    def draw(self,screen):
        if self.active == True:
            self.colour = self.colour_active
        else:
            self.colour = self.colour_passive
        self.check_user_input(self.user_input)
        draw_text(screen,self.error_message,35,self.SCREEN_WIDTH/2,self.SCREEN_HEIGHT-75)
        draw_text(screen,self.text,40,self.x + 80, self.y - 75)
        base_font = pygame.font.Font("Molot.ttf",75)
        button_text_surface = base_font.render(self.user_input,True,(255,255,255))
        screen.blit(button_text_surface,(self.button.x + 20, self.button.y - 5))
        pygame.draw.rect(screen,self.colour,self.button,2)
        
    def handle_event(self,event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.button.collidepoint(event.pos):
                self.active = True
            else:
                self.active = False
        if event.type == pygame.KEYDOWN:
            if self.active == True:
                if event.key == K_BACKSPACE:
                    self.user_input = self.user_input[:-1]
                elif event.key == K_RETURN:
                    self.active = False
                else:
                    self.user_input += event.unicode


