import pygame
<<<<<<< HEAD:MainGame.py
import math
from random import choice, randint, uniform
from particles import Particle
from particles import Ripple


=======
>>>>>>> main:Ryan stuff/gamestuff.py
pygame.init()

# Setup screen
screen = pygame.display.set_mode([800, 450])
pygame.display.set_caption('Core Game Engine')

# Color library
red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)
white = (255, 255, 255)
black = (0, 0, 0)
purple = (127, 0, 255)
orange = (255, 165, 0)

<<<<<<< HEAD:MainGame.py
# Setup screen
screen = pygame.display.set_mode([800, 450])
pygame.display.set_caption('Core Game Engine')

# Load animated gif
gif_anim = GifAnimation("your_animation.gif")

# Particle group
particle_group = pygame.sprite.Group()

# Ripple group (new group for random ripples)
ripple_group = pygame.sprite.Group()

=======
>>>>>>> main:Ryan stuff/gamestuff.py
# Global settings
background = black
framerate = 60
font = pygame.font.Font('freesansbold.ttf', 16)
timer = pygame.time.Clock()

# Game values
green_value = 1
red_value = 2
orange_value = 3
white_value = 4
purple_value = 5

green_speed = 5
red_speed = 4
orange_speed = 3
white_speed = 2
purple_speed = 1

# Game state
score = 0

# Drawing state
draw_green = False
draw_red = False
draw_orange = False
draw_white = False
draw_purple = False

green_length = 0
red_length = 0
orange_length = 0
white_length = 0
purple_length = 0

# Game state
player_state = {
    "score": 0,
    "rebirths": 0,
    "multiplier": 1.0
}

# Auto Miner (always active)
auto_miner_timer = pygame.USEREVENT + 1
pygame.time.set_timer(auto_miner_timer, 1000)  # Triggers every second

# Draw task function
def draw_task(color, y_coord, value, speed, draw, length):
    global score
    if draw and length < 200:
        length += speed
    elif draw and length >= 200:
        draw = False
        length = 0
        score += value

    task = pygame.draw.circle(screen, color, (30, y_coord), 20, 5)
    pygame.draw.rect(screen, color, [70, y_coord - 15, 200, 30])
    pygame.draw.rect(screen, black, [75, y_coord - 10, 190, 20])
    pygame.draw.rect(screen, color, [70, y_coord - 15, length, 30])
    value_text = font.render(str(value), True, white)
    screen.blit(value_text, (16, y_coord - 10))

    return task, length, draw

# Game loop
running = True
while running:
    timer.tick(framerate)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

<<<<<<< HEAD:MainGame.py
       
        if event.type == auto_miner_timer:
             player_state["score"] += 1 * player_state["multiplier"]


        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:
                if perform_rebirth(player_state):
                    print("Rebirth successful!")
                else:
                    print("Not enough knowledge to rebirth.")

=======
        # Always-running Auto Miner
        if event.type == auto_miner_timer:
            score += 1  # Passive knowledge gain
>>>>>>> main:Ryan stuff/gamestuff.py

        if event.type == pygame.MOUSEBUTTONDOWN:
            if task1.collidepoint(event.pos):
                draw_green = True
            if task2.collidepoint(event.pos):
                draw_red = True
            if task3.collidepoint(event.pos):
                draw_orange = True
            if task4.collidepoint(event.pos):
                draw_white = True
            if task5.collidepoint(event.pos):
                draw_purple = True

    # Drawing section
    screen.fill(background)

    task1, green_length, draw_green = draw_task(green, 50, green_value, green_speed, draw_green, green_length)
    task2, red_length, draw_red = draw_task(red, 110, red_value, red_speed, draw_red, red_length)
    task3, orange_length, draw_orange = draw_task(orange, 170, orange_value, orange_speed, draw_orange, orange_length)
    task4, white_length, draw_white = draw_task(white, 230, white_value, white_speed, draw_white, white_length)
    task5, purple_length, draw_purple = draw_task(purple, 290, purple_value, purple_speed, draw_purple, purple_length)

<<<<<<< HEAD:MainGame.py
    # Update and draw particles
    particle_group.update()
    particle_group.draw(screen)

    # Update and draw random ripples
    ripple_group.update()
    ripple_group.draw(screen)

    # Draw score
    f'Knowledge: {round(player_state["score"])} | Rebirths: {player_state["rebirths"]}', True, white, black)
=======
    display_score = font.render(f'Knowledge: {round(score)}', True, white, black)
>>>>>>> main:Ryan stuff/gamestuff.py
    screen.blit(display_score, (10, 5))

    #Draw the animated GIF on the screen
    gif_anim.update()
    gif_anim.draw(screen, (550, 320))  # Adjust position as needed



pygame.display.flip()

pygame.quit()
