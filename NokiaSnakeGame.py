#import all the required libraries 
import pygame
import random
import sys

from pygame.constants import QUIT
from pygame.display import update
from pygame.sprite import Sprite
from os import path
#initialize pygames 
pygame.init()

#colors 
red = pygame.Color(255, 0, 0)
green = pygame.Color(0, 255, 0)
black = pygame.Color(0, 0, 0)
white = pygame.Color(255, 255, 255)
brown = pygame.Color(165, 42, 42)
orange = pygame.Color(255,165,0)

#Window 
Width = 1600
Height = 900
screen = pygame.display.set_mode((Width,Height))
pygame.display.set_caption("Nokia Snake Gamer")
clock = pygame.time.Clock()
FPS = 60
#Importing sprites
game_folder = path.dirname(__file__)
imgfolder = path.join(game_folder, "img")
snake_img = pygame.image.load(path.join(imgfolder, "snake_head.png"))
snake_img = pygame.transform.scale(snake_img, (40,40))
apple_img = pygame.image.load(path.join(imgfolder,"rabbit.png"))
apple_img = pygame.transform.scale(apple_img, (40,40))
#Importing sounds
sound_folder = path.join(game_folder, "sound")
eat_sound = pygame.mixer.Sound(path.join(sound_folder, "eat.wav"))
eat_sound.set_volume(0.5)
music = pygame.mixer.music.load(path.join(sound_folder, "music.wav"))
music = pygame.mixer.music.set_volume(0.2)
pygame.mixer.music.play(-1)
#Snake class
class snake(pygame.sprite.Sprite):
    #Init method, to create templates for all needed variables
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = snake_img
        self.rect = self.image.get_rect()
        self.rect.x = Width/2
        self.rect.y = Height/2
        self.snake_speed_x = 0
        self.snake_speed_y = 0
        self.gameOn = True
        self.gameOpen = True
        self.snake_list = []
        self.snake_length = 1
        self.score = 0
    #snake movement 
    def slither(self):
        #Key event pygame function
        key = pygame.key.get_pressed()
        #Make the snake go on a positive x movement when the right key is pressed 
        if key[pygame.K_RIGHT]:
            self.snake_speed_x = 5
            self.snake_speed_y = 0 
            self.image = pygame.transform.rotate(snake_img, 90)
        #Make the snake go on a negative x movement when the left key is pressed 
        elif key[pygame.K_LEFT]:
            self.snake_speed_x = -5
            self.snake_speed_y = 0
            self.image = pygame.transform.rotate(snake_img, -90)
        #Make the snake go on a negative y movement when the up key is pressed 
        elif key[pygame.K_UP]:
            self.snake_speed_y = -5
            self.snake_speed_x = 0
            self.image = pygame.transform.rotate(snake_img, 180)
        #make the snake go on a positive movement when the up key is pressed 
        elif key[pygame.K_DOWN]:
            self.snake_speed_y = 5
            self.snake_speed_x = 0
            self.image = pygame.transform.rotate(snake_img, 0)
        #Make em move it move it
        self.rect.x += self.snake_speed_x
        self.rect.y += self.snake_speed_y
    #Bounds
    def game_boundaries(self):
        #Make the game ened when the snake goes out of bounds 
        if self.rect.right > Width + 5 or self.rect.left < -5 or self.rect.top < -5 or self.rect.bottom > Height + 5:
            self.gameOpen = False
            pygame.mixer.music.stop()
            replay_game("Out of bounds man",self.score,self.gameOn,self.gameOpen)
            
    def snake_pos(self): 
        snake_cord = []
        snake_cord.append(self.rect.x)
        snake_cord.append(self.rect.y)
        self.snake_list.append(snake_cord)
        if len(self.snake_list) > self.snake_length:
            del self.snake_list[0]
        for each_seg in self.snake_list[:-1]:
            if each_seg == snake_cord:
                self.gameOpen = False
                pygame.mixer.music.stop()
                replay_game("Looks like you bit your self",self.score,self.gameOn,self.gameOpen)

    def draw_snake(self):
        for i in self.snake_list[:-1]:
            snake_body = pygame.Surface((40,40))
            snake_body.fill(green)
            snake_rect = (i[0], i[1])
            screen.blit(snake_body, snake_rect)

    def update(self):
        self.slither()
        self.game_boundaries()
        self.snake_pos()
        self.draw_snake()
class food(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = apple_img
        self.rect = self.image.get_rect()
        self.food_size = 40
        self.rect.x = round(random.randrange(0, Width-self.food_size)/10)*10.0
        self.rect.y = round(random.randrange(0, Height-self.food_size)/10)*10.0
    def draw_food(self):
        self.rect.x = round(random.randrange(0, Width-self.food_size)/10)*10.0
        self.rect.y = round(random.randrange(0, Height-self.food_size)/10)*10.0
    def update(self):
        pass

#game functions 
def message_to_screen(text,color,font_size, ypos):
    font = pygame.font.SysFont("comicsansms", font_size)
    message = font.render(text, True, color)
    message_rect = message.get_rect()
    message_rect.center = (Width/2, ypos)
    screen.blit(message, message_rect)
def replay_game(message,score,gameOn,gameOpen):
    while gameOpen == False:
            screen.fill(orange)
            message_to_screen(message, black,30, Height/2 + 40)
            message_to_screen("Score: " +str(score) , black, 30 , 10)
            message_to_screen("YOU DIED", red, 50 , Height/2)
            message_to_screen("PRESS (SPACE) TO PLAY AGAIN" , black, 30 , Height/2 + 80)
            message_to_screen("PRESS (ESC) TO PLAY EXIT" , black, 30 , Height/2 + 120)
            pygame.display.update()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    gameOn = True
                    gameOpen = False
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        gameOn = True
                        gameOpen = False
                        pygame.quit()
                        sys.exit()
                    elif event.key == pygame.K_SPACE:
                        pygame.mixer.music.play(-1)
                        game()
#main game 
def game():
    gameOn = True 
    gameOpen = True
#sprites 
    Player = snake()
    Apple = food()
    all_sprites = pygame.sprite.Group()
    all_sprites.add(Player)
    all_sprites.add(Apple)
    while gameOn:
        
        clock.tick(FPS)
        
        for event in pygame.event.get(): 
            if event.type == pygame.QUIT:
                gameOn = False
        if pygame.sprite.collide_rect(Player, Apple):
           Apple.draw_food()
           Player.score += 1
           Player.snake_length += 1
           eat_sound.play()
        screen.fill(orange)
        all_sprites.update()
        all_sprites.draw(screen)
        message_to_screen("Score: " +str(Player.score) , black, 30 , 10)
        pygame.display.update()
    pygame.quit()
game()
