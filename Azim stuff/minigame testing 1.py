import pygame
import sys
import random

# Initialize pygame
pygame.init()

# Screen settings
WIDTH, HEIGHT = 600, 400
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Math Catch Game")

# Colors
WHITE = (255, 255, 255)
BASKET_COLOR = (100, 200, 255)
BALL_COLOR = (255, 100, 100)

# Fonts
font = pygame.font.SysFont(None, 40)

# Basket settings
basket_width = 100
basket_height = 20
basket_x = WIDTH // 2 - basket_width // 2
basket_y = HEIGHT - basket_height - 10
basket_speed = 5
basket_thickness = 4

# Ball settings
ball_radius = 20
ball_speed = 3
num_balls = 3

# Create multiple balls with random positions
balls = []
for _ in range(num_balls):
    x = random.randint(ball_radius, WIDTH - ball_radius)
    y = random.randint(-HEIGHT, 0)
    balls.append({"x": x, "y": y})

# Game clock
clock = pygame.time.Clock()
FPS = 75

# Game loop
running = True
while running:
    screen.fill(WHITE)

    # --- Events ---
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # --- Key Presses ---
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and basket_x > 0:
        basket_x -= basket_speed
    if keys[pygame.K_RIGHT] and basket_x < WIDTH - basket_width:
        basket_x += basket_speed

    # --- Move and Draw Balls ---
    for ball in balls:
        ball["y"] += ball_speed

        # Check collision with basket
        if (
            basket_x < ball["x"] < basket_x + basket_width
            and basket_y < ball["y"] + ball_radius < basket_y + basket_height
        ):
            # Reset ball to top at random x
            ball["x"] = random.randint(ball_radius, WIDTH - ball_radius)
            ball["y"] = random.randint(-HEIGHT, 0)

        # If ball goes off screen, reset to top
        elif ball["y"] > HEIGHT:
            ball["x"] = random.randint(ball_radius, WIDTH - ball_radius)
            ball["y"] = random.randint(-HEIGHT, 0)

        # Draw the ball
        pygame.draw.circle(screen, BALL_COLOR, (ball["x"], ball["y"]), ball_radius)

    # --- Draw Open-Top Box Basket ---
    left_start = (basket_x, basket_y)
    left_end = (basket_x, basket_y + basket_height)

    right_start = (basket_x + basket_width, basket_y)
    right_end = (basket_x + basket_width, basket_y + basket_height)

    bottom_start = (basket_x, basket_y + basket_height)
    bottom_end = (basket_x + basket_width, basket_y + basket_height)

    pygame.draw.line(screen, BASKET_COLOR, left_start, left_end, basket_thickness)
    pygame.draw.line(screen, BASKET_COLOR, right_start, right_end, basket_thickness)
    pygame.draw.line(screen, BASKET_COLOR, bottom_start, bottom_end, basket_thickness)

    # --- Update Display ---
    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
sys.exit()
