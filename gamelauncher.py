import pygame
from pygame.locals import *
from random import randint
import sys

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

clock = pygame.time.Clock()

def draw_text(surf,text,size,x,y,font_name):
    font = pygame.font.Font(font_name,size)
    text_surface = font.render(text,True,(0,255,0))
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x,y)
    surf.blit(text_surface,text_rect)

class RunGame():
    pygame.init()
    font_name = pygame.font.match_font('helvetica')
    screen = pygame.display.set_mode([SCREEN_WIDTH,SCREEN_HEIGHT])
    background_surface = pygame.image.load("background.jpg")
    screen.blit(background_surface,background_surface.get_rect())
    running = True
    while running:

        #single_player_button = pygame.Rect(SCREEN_WIDTH/6,200,200,50)
        single_player_button_image = pygame.image.load('singleplayer.png')
        single_player_button_hover = pygame.image.load('singleplayerhover.png')

        two_player_button_image = pygame.image.load('twoplayer.png')
        two_player_button_hover = pygame.image.load('twoplayerhover.png')

        multiplayer_button_image = pygame.image.load('multiplayer.png')
        multiplayer_button_hover = pygame.image.load('multiplayerhover.png')


        single_player_button = single_player_button_image.get_rect()
        single_player_button.center = (230,240)

        two_player_button = two_player_button_image.get_rect()
        two_player_button.center = (230,320)

        multiplayer_button = multiplayer_button_image.get_rect()
        multiplayer_button.center = (230,400)



        #two_player_local_button = pygame.Rect(SCREEN_WIDTH/6,285,200,50)
        #multiplayer_button = pygame.Rect(SCREEN_WIDTH/6,370,200,50)
        #pygame.draw.rect(screen,(205,117,113),single_player_button)

        screen.blit(single_player_button_image,single_player_button)
        screen.blit(two_player_button_image,two_player_button)
        screen.blit(multiplayer_button_image,multiplayer_button)

        #pygame.draw.rect(screen,(205,117,113),two_player_local_button)
        #pygame.draw.rect(screen,(205,117,113), multiplayer_button)

        mx,my = pygame.mouse.get_pos()

        if single_player_button.collidepoint((mx,my)):
            screen.blit(single_player_button_hover,single_player_button)
            if click:
                ##Go on to single player
                print("You selected single player")
                pass
        if two_player_button.collidepoint((mx,my)):
            screen.blit(two_player_button_hover,two_player_button)
            if click:
                ##Go on lan 2 player
                print("You selected lan 2 player")
                pass
        if multiplayer_button.collidepoint((mx,my)):
            screen.blit(multiplayer_button_hover,multiplayer_button)
            if click:
                ##Go on to multiplayer 
                print("You selected multiplayer")
                pass
    
        click = False

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit(0)
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    pygame.quit()
                    sys.exit(0)
            if event.type == MOUSEBUTTONDOWN:
                if event.button == 1:
                    click = True

        pygame.display.update()
        clock.tick(25)


if __name__ == '__main__':
    RunGame()



