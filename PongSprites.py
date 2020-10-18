import pygame
from pygame.locals import *

class Paddle(pygame.sprite.Sprite):
    """
    This is the paddle (or the player) than will be controlled by the user
    There are 2 different sides (left and right) and depending on which side is being moved the controlls will be different either up/down or w/s
    The user has the chance to enter the speed of the paddles otherwise a default value of 5 is used.
    """
    def __init__(self,x,speed,SCREEN_HEIGHT):
        super(Paddle,self).__init__()
        self.SCREEN_HEIGHT = SCREEN_HEIGHT
        self.image = pygame.Surface((10,50))
        self.rect = self.image.get_rect(
            center=(x,SCREEN_HEIGHT/2)
        )
        self.image.fill((0,0,0))
        self.speed = speed

    def draw(self,surface):
        surface.blit(self.image,self.rect)

    def move(self,side):
        pressed_keys = pygame.key.get_pressed()
        if(side == "Right"):
            if(pressed_keys[K_UP]):
                self.rect.move_ip(0,-self.speed)
            if(pressed_keys[K_DOWN]):
                self.rect.move_ip(0,self.speed)
        elif(side == "Left"):
            if(pressed_keys[K_w]):
                self.rect.move_ip(0,-self.speed)
            if(pressed_keys[K_s]):
                self.rect.move_ip(0,self.speed)

        if self.rect.top <= 0:
            self.rect.top = 0
        if self.rect.bottom >= self.SCREEN_HEIGHT:
            self.rect.bottom = self.SCREEN_HEIGHT

class Ball(pygame.sprite.Sprite):
    """ 
    This is the ball that will be 'hit' around the screen
    The ball starts moving randomly either left or right.
    The user has the chance to enter the speed of the ball otherwise a default value of 5 is used.
    """
    def __init__(self,speed,SCREEN_WIDTH,SCREEN_HEIGHT):
        super(Ball,self).__init__()
        self.SCREEN_WIDTH = SCREEN_WIDTH
        self.SCREEN_HEIGHT = SCREEN_HEIGHT
        self.image = pygame.Surface((20,20))
        self.rect = self.image.get_rect(
            center=((int(self.SCREEN_WIDTH/2),int(self.SCREEN_HEIGHT/2)))
        )
        self.speed = speed

    def draw(self,surface):
        pygame.draw.circle(surface,(0,255,0),self.rect.center,10)

    def move(self,ball_direction_x,ball_direction_y):
        if self.rect.left <= 14: ##If the ball is behind the width of the paddle, then its unreturnable and the score should be updated
            winner = "Right"
            return winner
        if self.rect.right >= self.SCREEN_WIDTH - 14 :
            winner = "Left"
            return winner
        if self.rect.top <= 0:
            ##The y speed is (speed + 1) so that the ball will move in a more diagonal line 
            self.rect.move_ip(ball_direction_x*self.speed,-ball_direction_y*(self.speed+1)) 
            ball_direction_y = -ball_direction_y
            return ball_direction_y
        if self.rect.bottom >= self.SCREEN_HEIGHT:
            self.rect.move_ip(ball_direction_x*(self.speed),-ball_direction_y*(self.speed+1))
            ball_direction_y = -ball_direction_y
            return ball_direction_y
        else:
            self.rect.move_ip(ball_direction_x*(self.speed),ball_direction_y*(self.speed+1))
            return ball_direction_y

    def return_ball(self,ball_direction_x,ball_direction_y):
        self.rect.move_ip(-ball_direction_x*(self.speed),ball_direction_y*(self.speed+1))
        ball_direction_x = -ball_direction_x
        return ball_direction_x
