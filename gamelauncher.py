import pygame
import random
import time
from pygame.locals import *
from random import randint
import sys

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

NUMBER_OF_GAMES = 2

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
        if self.rect.left <= 14: ##If the ball is behind the width of the paddle, then its unreturnable and the score should be updated
            winner = "Right"
            return winner
        if self.rect.right >= SCREEN_WIDTH - 14 :
            winner = "Left"
            return winner
        if self.rect.top <= 0:
            self.rect.move_ip(ball_direction_x*3,-ball_direction_y*4) 
            ball_direction_y = -ball_direction_y
            return ball_direction_y
        if self.rect.bottom >= SCREEN_HEIGHT:
            self.rect.move_ip(ball_direction_x*3,-ball_direction_y*4)
            ball_direction_y = -ball_direction_y
            return ball_direction_y
        else:
            self.rect.move_ip(ball_direction_x*3,ball_direction_y*4)
            return ball_direction_y

    def return_ball(self,ball_direction_x,ball_direction_y):
        try:
            self.rect.move_ip(-ball_direction_x*3,ball_direction_y*6)
            ball_direction_x = -ball_direction_x
        except TypeError as message:
            print(message)
            print(ball_direction_x)
            print(ball_direction_y)
        return ball_direction_x

def draw_text(surf,text,size,x,y):
    font_name = pygame.font.Font("Molot.ttf",size)
    text_surface = font_name.render(text,True,(255,0,0))
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x,y)
    surf.blit(text_surface,text_rect)

def DisplayScores(scores,number_of_games,final_score=False):
    clock.tick(25)
    number_of_games_text = f'Best of {number_of_games}'
    screen = pygame.display.set_mode([SCREEN_WIDTH,SCREEN_HEIGHT])
    background_surface = pygame.image.load("twoplayerbackground.jpg")
    screen.blit(background_surface,background_surface.get_rect())
    start_time = time.time()
    end_time = start_time + 5 ##Want the scores to be shown for 10 seconds
    dt = 0

    player_1_score = scores["Left"]
    player_2_score = scores["Right"]


    draw_text(screen,number_of_games_text,110,SCREEN_WIDTH/2,-20)   

    pygame.display.update()  

    pygame.time.Clock()
    running = True
    if(final_score == False):
        while running:
            while(start_time < end_time):
                for event in pygame.event.get():
                    if event.type == KEYDOWN:
                        if event.key == K_ESCAPE:
                            running = False
                            RunGame()
                    if event.type == pygame.QUIT:
                        running = False
                        pygame.quit()
                        sys.exit()

                draw_text(screen,str(player_1_score),170,SCREEN_WIDTH*0.25,SCREEN_HEIGHT/3)       
                draw_text(screen,str(player_2_score),170,SCREEN_WIDTH*0.75,SCREEN_HEIGHT/3)    
                pygame.display.update()   
                dt = clock.tick(25) / 1000
                start_time += dt
            running = False
        return 0
    else:
        while running:
            for event in pygame.event.get():
                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        running = False
                if event.type == pygame.QUIT:
                    running = False
                    pygame.quit()
                    sys.exit()

            if(player_1_score > player_2_score):
                winner_text = 'The Winner is Left!'
                draw_text(screen,winner_text,70,SCREEN_WIDTH*0.5,SCREEN_HEIGHT*0.85)
            elif(player_1_score < player_2_score):
                winner_text = 'The Winner is Right!'
                draw_text(screen,winner_text,70,SCREEN_WIDTH*0.5,SCREEN_HEIGHT*0.85) 
            else:
                winner_text = "Its a Draw!"
                draw_text(screen,winner_text,70,SCREEN_WIDTH*0.5,SCREEN_HEIGHT*0.85) 


            draw_text(screen,str(player_1_score),170,SCREEN_WIDTH*0.25,SCREEN_HEIGHT/3)       
            draw_text(screen,str(player_2_score),170,SCREEN_WIDTH*0.75,SCREEN_HEIGHT/3)    
            pygame.display.update()   

def RunTwoPlayerSettings():
    screen = pygame.display.set_mode([SCREEN_WIDTH,SCREEN_HEIGHT])

    paddle_speed_text = "Paddle Speed"
    ball_speed_text = "Ball Speed"
    number_of_games_text = "Num. of Games"

    user_paddle_speed_input = ''
    user_ball_speed_input = ''
    user_number_of_games_input = ''

    paddle_speed_button = pygame.Rect((150,175,150,75))
    ball_speed_button = pygame.Rect((500,175,150,75))
    number_of_games_button = pygame.Rect((150,400,150,75))

    colour = ((255,255,255))

    paddle_speed_active = False
    ball_speed_active = False
    number_of_games_active = False

    running = True

    while running:
        background_surface = pygame.image.load("twoplayerbackground.jpg")
        screen.blit(background_surface,background_surface.get_rect())

        draw_text(screen,paddle_speed_text,40,230,100)
        draw_text(screen,ball_speed_text,40,545,100)
        draw_text(screen,number_of_games_text,40,230,325)

        pygame.draw.rect(screen,colour,paddle_speed_button,2)
        pygame.draw.rect(screen,colour,ball_speed_button,2)
        pygame.draw.rect(screen,colour,number_of_games_button,2)

        for event in pygame.event.get():
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    running = False
                    RunGame()
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if paddle_speed_button.collidepoint(event.pos):
                    paddle_speed_active = True
                else:
                    paddle_speed_active = False
            if(event.type == pygame.KEYDOWN):
                if paddle_speed_active == True:
                    if event.key == K_BACKSPACE:
                        user_paddle_speed_input = user_paddle_speed_input[:-1]
                    elif event.key == K_RETURN:
                        paddle_speed_active = False
                    else:
                        user_paddle_speed_input += event.unicode     
        base_font = pygame.font.Font("Molot.ttf",75)
        text_surface = base_font.render(user_paddle_speed_input,True,(255,255,255))
        screen.blit(text_surface,(paddle_speed_button.x + 35,paddle_speed_button.y -5 ))

        pygame.display.update()


def RunTwoPlayer():
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

    running = True
    scores = {"Right" : 0, "Left" : 0}
    while running:
        background_surface = pygame.image.load("twoplayerbackground.jpg")
        screen.blit(background_surface,background_surface.get_rect())
        for event in pygame.event.get():
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    running = False
                    RunGame()
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                sys.exit()

        ball_direction_y = ball.move(ball_direction_x,ball_direction_y)
        if(pygame.sprite.spritecollideany(ball,player_sprites)):
            ball_direction_x = ball.return_ball(ball_direction_x,ball_direction_y)
        if(ball_direction_y == "Left"):
            scores["Left"] += 1
            running = False
        elif(ball_direction_y == "Right"):
            scores["Right"] += 1
            running = False
        player_1.move("Left")
        player_2.move("Right")

        ball.draw(screen)
        player_1.draw(screen)
        player_2.draw(screen)

        pygame.display.update()

    return scores

def RunGame(click=False):
    pygame.init()
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
                pass
        if two_player_button.collidepoint((mx,my)):
            screen.blit(two_player_button_hover,two_player_button)
            if click:
                RunTwoPlayerSettings()
                total_scores = {"Right" : 0, "Left" : 0}
                for i in range(NUMBER_OF_GAMES):
                    scores = RunTwoPlayer()
                    total_scores["Right"] += scores["Right"]
                    total_scores["Left"] += scores["Left"]
                    if(i == NUMBER_OF_GAMES - 1):
                        DisplayScores(total_scores,NUMBER_OF_GAMES,final_score=True)
                    else:
                        DisplayScores(total_scores,NUMBER_OF_GAMES)
                RunGame()
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


