import pygame
import random
import time
from pygame.locals import *
from random import randint
from PongSprites import Paddle, Ball
from Utilities import text_input_box,draw_text
import sys

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

number_of_games = 5 #The default number of games if non is picked

clock = pygame.time.Clock()

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
    start_game_text = "Start"

    ball_speed_button = text_input_box(150,175,150,75,ball_speed_text,SCREEN_WIDTH,SCREEN_HEIGHT)
    paddle_speed_button = text_input_box(500,175,150,75,paddle_speed_text,SCREEN_WIDTH,SCREEN_HEIGHT)
    number_of_games_button = text_input_box(150,400,150,75,number_of_games_text,SCREEN_WIDTH,SCREEN_HEIGHT)

    all_buttons = [ball_speed_button,paddle_speed_button,number_of_games_button]

    start_game_font = pygame.font.Font("Molot.ttf",75)
    start_game_surface = start_game_font.render(start_game_text,True,(255,255,255))

    start_game_button = start_game_surface.get_rect()
    start_game_button.center = (550,400)
    screen.blit(start_game_surface,start_game_button)

    pygame.display.update()

    running = True

    while running:
        background_surface = pygame.image.load("twoplayerbackground.jpg")
        screen.blit(background_surface,background_surface.get_rect())

        mx,my = pygame.mouse.get_pos()

        for event in pygame.event.get():
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    running = False
                    RunGame()
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                sys.exit()
            for button in all_buttons:
                button.handle_event(event)
            if start_game_button.collidepoint((mx,my)):
                start_game_surface = start_game_font.render(start_game_text,True,(255,110,0))
            else:
                start_game_surface = start_game_font.render(start_game_text,True,(255,255,255))
            if event.type == pygame.MOUSEBUTTONDOWN:
                if start_game_button.collidepoint(event.pos):
                    errors = [button.error_message for button in all_buttons]
                    if errors[0] == '' and errors[1] == '' and errors[2] == '':
                        return ball_speed_button.user_input,paddle_speed_button.user_input,number_of_games_button.user_input
                    else:
                        return 5,5,10 ##Returns the default speeds if the user hasn't entered the settings correctly.
        screen.blit(start_game_surface,start_game_button)


        for button in all_buttons:
            button.draw(screen)

        pygame.display.update()
    
def RunTwoPlayer(ball_speed_input=5,paddle_speed_input=5,number_of_games_input=5): ##These are the default values if the user dosn't enter the settings correctly
    screen = pygame.display.set_mode([SCREEN_WIDTH,SCREEN_HEIGHT])
    background_surface = pygame.image.load("twoplayerbackground.jpg")
    screen.blit(background_surface,background_surface.get_rect())

    player_1 = Paddle(10,paddle_speed_input,SCREEN_HEIGHT)
    player_2 = Paddle(SCREEN_WIDTH - 10,paddle_speed_input,SCREEN_HEIGHT)
    ball = Ball(ball_speed_input,SCREEN_WIDTH,SCREEN_HEIGHT)

    ##If the direction is -1 then the ball goes left and vice versa
    directions = [-1,1]
    ball_direction_x = random.choice(directions)
    ball_direction_y = random.choice(directions)

    player_sprites = pygame.sprite.Group()
    player_sprites.add([player_1,player_2])

    ball.draw(screen)
    player_1.draw(screen)
    player_2.draw(screen)

    pygame.display.update()
    pygame.time.wait(2000)

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
                ball_speed,paddle_speed,number_of_games = map(int,RunTwoPlayerSettings())
                total_scores = {"Right" : 0, "Left" : 0}
                for i in range(number_of_games):
                    scores = RunTwoPlayer(ball_speed,paddle_speed,number_of_games)
                    total_scores["Right"] += scores["Right"]
                    total_scores["Left"] += scores["Left"]
                    if(i == number_of_games - 1):
                        DisplayScores(total_scores,number_of_games,final_score=True)
                    else:
                        DisplayScores(total_scores,number_of_games)
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
            if event.type == MOUSEBUTTONDOWN:
                if event.button == 1:
                    click = True

        pygame.display.update()

if __name__ == "__main__":
    RunGame()


