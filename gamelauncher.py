import pygame
import random
from pygame.locals import *
from random import randint
import sys

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

clock = pygame.time.Clock()

class Paddle(pygame.sprite.Sprite):
    def __init__(self,x):
        super(Paddle,self).__init__()
        self.image = pygame.Surface((10,50))
        self.rect = self.image.get_rect(
            center=(x,SCREEN_HEIGHT/2)
        )
        self.image.fill((0,0,0))
    def draw(self,surface):
        surface.blit(self.image,self.rect)

    def move(self,side):
        pressed_keys = pygame.key.get_pressed()
        if(side == "Right"):
            if(pressed_keys[K_UP]):
                self.rect.move_ip(0,-5)
            if(pressed_keys[K_DOWN]):
                self.rect.move_ip(0,5)
        elif(side == "Left"):
            if(pressed_keys[K_w]):
                self.rect.move_ip(0,-5)
            if(pressed_keys[K_s]):
                self.rect.move_ip(0,5)

        if self.rect.top <= 0:
            self.rect.top = 0
        if self.rect.bottom >= SCREEN_HEIGHT:
            self.rect.bottom = SCREEN_HEIGHT


class Ball(pygame.sprite.Sprite):
    def __init__(self):
        super(Ball,self).__init__()
        self.image = pygame.Surface((20,20))
        self.rect = self.image.get_rect(
            center=((int(SCREEN_WIDTH/2),int(SCREEN_HEIGHT/2)))
        )

    def draw(self,surface):
        pygame.draw.circle(surface,(0,255,0),self.rect.center,10)

    def move(self,ball_direction_x,ball_direction_y):
        if self.rect.left <= 0:
            print("Right")
            winner = "Right"
            return winner
        if self.rect.right >= SCREEN_WIDTH:
            print("Left")
            winner = "Left"
            return winner
        if self.rect.top <= 0:
            self.rect.move_ip(ball_direction_x*3,-ball_direction_y*6) 
            ball_direction_y = -ball_direction_y
            return ball_direction_y
        if self.rect.bottom >= SCREEN_HEIGHT:
            self.rect.move_ip(ball_direction_x*3,-ball_direction_y*6)
            ball_direction_y = -ball_direction_y
            return ball_direction_y
        else:
            self.rect.move_ip(ball_direction_x*3,ball_direction_y*6)
            return ball_direction_y

    def return_ball(self,ball_direction_x,ball_direction_y):
        self.rect.move_ip(-ball_direction_x*3,ball_direction_y*6)
        ball_direction_x = -ball_direction_x
        return ball_direction_x

def draw_text(surf,text,size,x,y,font_name):
    font = pygame.font.Font(font_name,size)
    text_surface = font.render(text,True,(0,255,0))
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x,y)
    surf.blit(text_surface,text_rect)

def RunTwoPlayer(number_of_games):
    screen = pygame.display.set_mode([SCREEN_WIDTH,SCREEN_HEIGHT])
    background_surface = pygame.image.load("twoplayerbackground.jpg")
    screen.blit(background_surface,background_surface.get_rect())

    player_1 = Paddle(10)
    player_2 = Paddle(SCREEN_WIDTH - 10)
    ball = Ball()

    ##If the direction is -1 then the ball goes left and vice versa
    directions = [-1,1]
    ball_direction_x = random.choice(directions)
    ball_direction_y = random.choice(directions)

    player_sprites = pygame.sprite.Group()
    player_sprites.add([player_1,player_2])

    #player_1 = Paddle(10)
    #player_2 = Paddle(SCREEN_WIDTH - 10)
    pygame.display.update()

    for i in range(number_of_games):
        running = True
        scores = {"Right" : 0, "Left" : 0}
        while running:
            background_surface = pygame.image.load("twoplayerbackground.jpg")
            screen.blit(background_surface,background_surface.get_rect())
            for event in pygame.event.get():
                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        running = False
                if event.type == pygame.QUIT:
                    running = False

            ball_direction_y = ball.move(ball_direction_x,ball_direction_y)
            if(pygame.sprite.spritecollideany(ball,player_sprites)):
                ball_direction_x = ball.return_ball(ball_direction_x,ball_direction_y)
            if(ball_direction_y == "Left"):
                print("Left scored the point")
                scores["Left"] += 1
                break
            elif(ball_direction_y == "Right"):
                print("Right scored the point")
                scores["Right"] += 1
                break
            player_1.move("Left")
            player_2.move("Right")

            ball.draw(screen)
            player_1.draw(screen)
            player_2.draw(screen)

            pygame.display.update()

    return scores

def RunGame(click=False):
    pygame.init()
    font_name = pygame.font.match_font('helvetica')
    screen = pygame.display.set_mode([SCREEN_WIDTH,SCREEN_HEIGHT])
    background_surface = pygame.image.load("background.jpg")
    screen.blit(background_surface,background_surface.get_rect())
    clock.tick(25)
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

        screen.blit(single_player_button_image,single_player_button)
        screen.blit(two_player_button_image,two_player_button)
        screen.blit(multiplayer_button_image,multiplayer_button)
        mx,my = pygame.mouse.get_pos()

        if single_player_button.collidepoint((mx,my)):
            screen.blit(single_player_button_hover,single_player_button)
            if click:
                ##Go on to single player
                print("You selected single player")
                num_of_games = 3
                scores = RunTwoPlayer(num_of_games)
                print(scores)
                RunGame()
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

if __name__ == "__main__":
    RunGame()


