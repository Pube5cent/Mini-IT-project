import pygame
import math
from random import choice, randint, uniform
from particles import Particle
from particles import Ripple

pygame.init()

# Color library
red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)
white = (255, 255, 255)
black = (0, 0, 0)
purple = (127, 0, 255)
orange = (255, 165, 0)

# Setup screen
screen = pygame.display.set_mode([800, 450])
pygame.display.set_caption('Core Game Engine')

# Particle group
particle_group = pygame.sprite.Group()

# Ripple group (new group for random ripples)
ripple_group = pygame.sprite.Group()

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

# Auto Miner (always active)
auto_miner_timer = pygame.USEREVENT + 1
pygame.time.set_timer(auto_miner_timer, 1000)

# New function: draw ripple bar with sideways wave
def draw_rippled_bar(x, y, width, height, color, progress):
    # Draw outer border
    pygame.draw.rect(screen, color, (x, y, width, height))
    pygame.draw.rect(screen, black, (x+5, y+5, width-10, height-10))

    # Draw ripple inside
    fill_width = (width - 10) * (progress / 200)
    ripple_surface = pygame.Surface((fill_width, height-10), pygame.SRCALPHA)

    for i in range(0, height-10, 3):  # Loop across HEIGHT
        wave_offset = 10 * math.sin(pygame.time.get_ticks() * 0.005 + i * 0.5)  # Bigger sideways ripples
        pygame.draw.line(ripple_surface, color, ((fill_width//2) + wave_offset, i), (fill_width, i))

    screen.blit(ripple_surface, (x+5, y+5))

# Draw task function
def draw_task(color, y_coord, value, speed, draw, length):
    global score
    if draw and length < 200:
        length += speed
    elif draw and length >= 200:
        draw = False
        length = 0
        score += value
        # Full screen explosion when full
        for _ in range(500):  # Big particle explosion
            pos = (randint(0, 800), randint(0, 450))
            direction = pygame.math.Vector2(uniform(-1, 1), uniform(-1, 1))
            if direction.length() == 0:
                direction = pygame.math.Vector2(1, 0)
            direction = direction.normalize()
            speed_particle = randint(100, 600)
            color_particle = choice([red, green, blue, purple, orange, white])
            Particle(particle_group, pos, color_particle, direction, speed_particle)

    # Draw circle and new rippled bar
    task = pygame.draw.circle(screen, color, (30, y_coord), 20, 5)
    draw_rippled_bar(70, y_coord - 15, 200, 30, color, length)

    value_text = font.render(str(value), True, white)
    screen.blit(value_text, (16, y_coord - 10))

    return task, length, draw

# Game loop test
running = True
while running:
    timer.tick(framerate)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == auto_miner_timer:
            score += 1

        if event.type == pygame.MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()  # Get mouse position
            num_particles = 100
            speed = randint(50, 400)
            color = choice([red, green, blue, purple, orange])

            # Handle particle explosions based on which task was clicked
            if task1.collidepoint(event.pos):
                draw_green = True
                for _ in range(num_particles):
                    direction = pygame.math.Vector2(uniform(-1, 1), uniform(-1, 1))
                    if direction.length() == 0:
                        direction = pygame.math.Vector2(1, 0)
                    direction = direction.normalize()
                    Particle(particle_group, pos, color, direction, speed)

            if task2.collidepoint(event.pos):
                draw_red = True
                for _ in range(num_particles):
                    direction = pygame.math.Vector2(uniform(-1, 1), uniform(-1, 1))
                    if direction.length() == 0:
                        direction = pygame.math.Vector2(1, 0)
                    direction = direction.normalize()
                    Particle(particle_group, pos, color, direction, speed)

            if task3.collidepoint(event.pos):
                draw_orange = True
                for _ in range(num_particles):
                    direction = pygame.math.Vector2(uniform(-1, 1), uniform(-1, 1))
                    if direction.length() == 0:
                        direction = pygame.math.Vector2(1, 0)
                    direction = direction.normalize()
                    Particle(particle_group, pos, color, direction, speed)

            if task4.collidepoint(event.pos):
                draw_white = True
                for _ in range(num_particles):
                    direction = pygame.math.Vector2(uniform(-1, 1), uniform(-1, 1))
                    if direction.length() == 0:
                        direction = pygame.math.Vector2(1, 0)
                    direction = direction.normalize()
                    Particle(particle_group, pos, color, direction, speed)

            if task5.collidepoint(event.pos):
                draw_purple = True
                for _ in range(num_particles):
                    direction = pygame.math.Vector2(uniform(-1, 1), uniform(-1, 1))
                    if direction.length() == 0:
                        direction = pygame.math.Vector2(1, 0)
                    direction = direction.normalize()
                    Particle(particle_group, pos, color, direction, speed)

    # Spawn ripples randomly
    if randint(0, 10) == 0:  # 10% chance to spawn a ripple
        random_x = randint(0, 800)
        random_color = choice([red, green, blue, purple, orange, white])
        ripple = Ripple(random_x, random_color)
        ripple_group.add(ripple)

    # Drawing section
    screen.fill(background)

    # Update and draw tasks
    task1, green_length, draw_green = draw_task(green, 50, green_value, green_speed, draw_green, green_length)
    task2, red_length, draw_red = draw_task(red, 110, red_value, red_speed, draw_red, red_length)
    task3, orange_length, draw_orange = draw_task(orange, 170, orange_value, orange_speed, draw_orange, orange_length)
    task4, white_length, draw_white = draw_task(white, 230, white_value, white_speed, draw_white, white_length)
    task5, purple_length, draw_purple = draw_task(purple, 290, purple_value, purple_speed, draw_purple, purple_length)

    # Update and draw particles
    particle_group.update()
    particle_group.draw(screen)

    # Update and draw random ripples
    ripple_group.update()
    ripple_group.draw(screen)

    # Draw score
    display_score = font.render(f'Knowledge: {round(score)}', True, white, black)
    screen.blit(display_score, (10, 5))

    pygame.display.flip()

pygame.quit()
