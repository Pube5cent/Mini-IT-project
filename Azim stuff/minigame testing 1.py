import pygame
import sys
import random

# Initialize pygame
pygame.init()

# Screen settings
WIDTH, HEIGHT = 600, 400
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Catch The Right")

# Colors
WHITE = (255, 255, 255)
BASKET_COLOR = (100, 200, 255)
BALL_COLOR = (255, 100, 100)
TEXT_COLOR = (0, 0, 0)
TIMER_BOX_COLOR = (200, 200, 200)
SCORE_BOX_COLOR = (220, 220, 150)

# Fonts
font = pygame.font.SysFont(None, 30)
game_over_font = pygame.font.SysFont(None, 60)

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

# Timer settings
TIMER_START = 30  # seconds
start_ticks = pygame.time.get_ticks()

# Score
score = 0

# Game FPS
clock = pygame.time.Clock()
FPS = 75

# Game state
running = True
game_over = False

while running:
    screen.fill(WHITE)

    # --- Events ---
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # --- Timer ---
    seconds_passed = (pygame.time.get_ticks() - start_ticks) / 1000
    time_left = max(0, int(TIMER_START - seconds_passed))

    if time_left <= 0:
        game_over = True

    if not game_over:
        # --- Basket Movement ---
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and basket_x > 0:
            basket_x -= basket_speed
        if keys[pygame.K_RIGHT] and basket_x < WIDTH - basket_width:
            basket_x += basket_speed

        # --- Ball Movement ---
        for ball in balls:
            ball["y"] += ball_speed

            # Catch the ball with basket
            if (
                basket_x < ball["x"] < basket_x + basket_width
                and basket_y < ball["y"] + ball_radius < basket_y + basket_height
            ):
                ball["x"] = random.randint(ball_radius, WIDTH - ball_radius)
                ball["y"] = random.randint(-HEIGHT, 0)
                score += 1  # Increase score by 1 when caught

            # Ball goes off screen
            elif ball["y"] > HEIGHT:
                ball["x"] = random.randint(ball_radius, WIDTH - ball_radius)
                ball["y"] = random.randint(-HEIGHT, 0)

            # Draw ball
            pygame.draw.circle(screen, BALL_COLOR, (ball["x"], ball["y"]), ball_radius)

        # --- Draw Basket ---
        left_start = (basket_x, basket_y)
        left_end = (basket_x, basket_y + basket_height)

        right_start = (basket_x + basket_width, basket_y)
        right_end = (basket_x + basket_width, basket_y + basket_height)

        bottom_start = (basket_x, basket_y + basket_height)
        bottom_end = (basket_x + basket_width, basket_y + basket_height)

        pygame.draw.line(screen, BASKET_COLOR, left_start, left_end, basket_thickness)
        pygame.draw.line(screen, BASKET_COLOR, right_start, right_end, basket_thickness)
        pygame.draw.line(screen, BASKET_COLOR, bottom_start, bottom_end, basket_thickness)

        # --- Draw Timer Box ---
        timer_text = font.render(f"Time Left: {time_left}", True, TEXT_COLOR)
        timer_box = pygame.Rect(10, 10, 150, 40)
        pygame.draw.rect(screen, TIMER_BOX_COLOR, timer_box)
        screen.blit(timer_text, (20, 20))

        # --- Draw Score Box ---
        score_text = font.render(f"Score: {score}", True, TEXT_COLOR)
        score_box = pygame.Rect(WIDTH - 170, 10, 150, 40)
        pygame.draw.rect(screen, SCORE_BOX_COLOR, score_box)
        screen.blit(score_text, (WIDTH - 160, 20))

    else:
        # --- Game Over Screen ---
        game_over_text = game_over_font.render("Game Over Niggah", True, (255, 0, 0))
        score_end_text = font.render(f"Your Final Score Loser: {score}", True, (0, 0, 0))

        screen.blit(game_over_text, (WIDTH // 2 - game_over_text.get_width() // 2, HEIGHT // 2 - game_over_text.get_height()))
        screen.blit(score_end_text, (WIDTH // 2 - score_end_text.get_width() // 2, HEIGHT // 2 + 20))

    # --- Update Display ---
    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
sys.exit()
