# By: Tim Tarver
# Flappy Bird Game

import random
import sys
import pygame
from pygame.locals import *

# Define all Variables

feet_per_second = 32
screen_width = 289
screen_height = 511
screen = pygame.display.set_mode((screen_width, screen_height))
ground_y = screen_height*0.8
game_over = 'gameover.png'
game_images = {}
game_sounds = {}
player = 'bird.png'
background = 'background.png'
pipe = 'pipe.png'
message = 'message.png'

# Create the welcome screen function

def welcome_screen():
    
    player_x = int(screen_width/8)
    player_y = int((screen_height - game_images['player'].get_height())/2)
    message_x = int((screen_width - game_images['message'].get_width())/2)
    message_y = int(screen_height*0.2)
    title_x = int((screen_width - game_images['message'].get_width())/2)
    title_y = int(screen_height*0.04)
    base_x = 0
    
    while True:
        
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()
            elif event.type == KEYDOWN and (event.key == K_SPACE or event.key == K_UP):
                return
            else:
                screen.blit(game_images['background'],(0,0))    
                screen.blit(game_images['message'],(message_x,message_y))
                screen.blit(game_images['player'],(player_x,player_y))
                screen.blit(game_images['base'],(base_x,ground_y))
                # screen.blit(game_images['message'], (title_x,title_y))
                pygame.display.update()
                fps_clock.tick(feet_per_second)

# Create platform canvas for the game

def main_game():
    
    score = 0
    player_x = int(screen_width/8)
    player_y = int(screen_height/2)
    base_x = 0
 
    new_pipe1 = get_random_pipe()
    new_pipe2 = get_random_pipe()

    # Create the Pipes
 
    upper_pipes = [
        {'x': screen_width+200, 'y': new_pipe1[0]['y']},
        {'x': screen_width+200+(screen_width/2), 'y': new_pipe2[0]['y']}
    ]
 
    lower_pipes = [
        {'x': screen_width+200, 'y': new_pipe1[1]['y']},
        {'x': screen_width+200+(screen_width/2), 'y': new_pipe2[1]['y']}
    ]

    # Create the variables to create 
 
    pipe_velocity_x = -4
 
    player_velocity_y = -9
    player_max_velocity_y = 10
    player_min_velocity_y = -8
    player_accelerate_y = 1
 
    player_flap_velocity = -8
    player_flapped = False
 
    # Control the bird with the arrow keys

    gameover = pygame.image.load(game_over)
    
    while True:
        
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN and (event.key == K_SPACE or event.key == K_UP):
                if player_y > 0:
                    player_velocity_y = player_flap_velocity 
                    player_flapped = True
                    game_sounds['wing'].play()
 
        crash_test = is_collide(player_x, player_y, upper_pipes, lower_pipes)
        
        if crash_test:
            return gameover

        # Create positions for the pipes
         
        player_mid_position = player_x + game_images['player'].get_width()/2
        
        for pipe in upper_pipes:
            
            pipe_mid_position = pipe['x'] + game_images['pipe'][0].get_width()/2
            
            if pipe_mid_position <= player_mid_position < pipe_mid_position + 4:
                score +=1
                print(f"Your Score is {score}")
                game_sounds['point'].play()
 
        if player_velocity_y <player_max_velocity_y and not player_flapped:
            player_velocity_y += player_accelerate_y
 
        if player_flapped:
            player_flapped = False
        player_height = game_images['player'].get_height()
        player_y = player_y + min(player_velocity_y, ground_y - player_y - player_height)   
 
        for upper_pipe, lower_pipe in zip(upper_pipes, lower_pipes):
            upper_pipe['x'] += pipe_velocity_x
            lower_pipe['x']  += pipe_velocity_x
 
        if 0 < upper_pipes[0]['x']<5:
            new_pipe = get_random_pipe()
            upper_pipes.append(new_pipe[0])
            lower_pipes.append(new_pipe[1])   
 
        if upper_pipes[0]['x'] < -game_images['pipe'][0].get_width():
            upper_pipes.pop(0)
            lower_pipes.pop(0)   
 
        screen.blit(game_images['background'], (0, 0))

        # Display the Pipes to the Screen
        
        for upper_pipe, lower_pipe in zip(upper_pipes, lower_pipes):
            
            screen.blit(game_images['pipe'][0], (upper_pipe['x'], upper_pipe['y']))
            screen.blit(game_images['pipe'][1], (lower_pipe['x'], lower_pipe['y']))
        screen.blit(game_images['base'], (base_x, ground_y))    
        screen.blit(game_images['player'], (player_x, player_y))
 
        my_digits = [int(x) for x in list(str(score))]
        width = 0

        # Create digits to display on the Screen
        
        for digit in my_digits:
            width += game_images['numbers'][digit].get_width()
        x_offset = (screen_width - width)/2 
 
        for digit in my_digits:
            screen.blit(game_images['numbers'][digit], (x_offset, screen_height*0.12))
            x_offset += game_images['numbers'][digit].get_width()
        pygame.display.update()
        fps_clock.tick(feet_per_second) 

# Create the function determining if the bird has
# collided with any pipes or buildings

def is_collide(player_x, player_y, upper_pipes, lower_pipes):

    if player_y > ground_y-25 or player_y<0:        
        game_sounds['hit'].play()
        return True
 
    for pipe in upper_pipes:        
        pipe_height = game_images['pipe'][0].get_height()
        if (player_y < pipe_height + pipe['y']) and (abs(player_x - pipe['x']) < game_images['pipe'][0].get_width() - 15):
            game_sounds['hit'].play()
            return True
 
    for pipe in lower_pipes:        
        if (player_y + game_images['player'].get_height() > pipe['y']) and (abs(player_x - pipe['x']) < game_images['pipe'][0].get_width() - 15):
            game_sounds['hit'].play()
            return True
 
    return False

# Create the function to display the random
# pipes in a game.

def get_random_pipe():
    
    pipe_height = game_images['pipe'][0].get_height()    
    offset = screen_height/3
    y_2 = offset + random.randrange(0, int(screen_height - game_images['base'].get_height() - 1.2*offset))
    pipe_x = screen_width + 10
    y_1 = pipe_height - y_2 + offset
    pipe = [
        {'x': pipe_x, 'y': -y_1},
        {'x': pipe_x, 'y': y_2}
    ]
    return pipe

# Create the main Drive Code of the game

if __name__ == "__main__":
    
    pygame.init() 
    fps_clock = pygame.time.Clock()
    pygame.display.set_caption('Flappy Bird')
    game_images['numbers'] = (
        pygame.image.load('0.png').convert_alpha(),
        pygame.image.load('1.png').convert_alpha(),
        pygame.image.load('2.png').convert_alpha(),
        pygame.image.load('3.png').convert_alpha(),
        pygame.image.load('4.png').convert_alpha(),
        pygame.image.load('5.png').convert_alpha(),
        pygame.image.load('6.png').convert_alpha(),
        pygame.image.load('7.png').convert_alpha(),
        pygame.image.load('8.png').convert_alpha(),
        pygame.image.load('9.png').convert_alpha()
        )
    game_images['message'] = pygame.image.load('message.png').convert_alpha()
    game_images['base'] = pygame.image.load('base.png').convert_alpha()
    game_images['pipe'] = (
        pygame.transform.rotate(pygame.image.load(pipe).convert_alpha(), 180),
        pygame.image.load(pipe).convert_alpha()
        )
    game_images['background'] = pygame.image.load(background).convert_alpha()
    game_images['player'] = pygame.image.load(player).convert_alpha()
    game_images['message'] = pygame.image.load('message.png').convert_alpha()
    game_images['gameover'] = pygame.image.load('gameover.png').convert_alpha()
 
    #Game Sounds
    
    game_sounds['die'] = pygame.mixer.Sound('die.wav')
    game_sounds['hit'] = pygame.mixer.Sound('hit.wav')
    game_sounds['point'] = pygame.mixer.Sound('point.wav')
    game_sounds['swoosh'] = pygame.mixer.Sound('swoosh.wav')
    game_sounds['wing'] = pygame.mixer.Sound('wing.wav')
 
    while True:
        welcome_screen()
        main_game()
