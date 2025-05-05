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

# Fonts
font = pygame.font.SysFont(None, 30)
big_font = pygame.font.SysFont(None, 60)

# Load basket image
basket_image = pygame.image.load("AzimStuff/basket.png")
basket_width = 100
basket_height = 60
basket_image = pygame.transform.smoothscale(basket_image, (basket_width, basket_height))

basket_x = WIDTH // 2 - basket_width // 2
basket_y = HEIGHT - basket_height - 10
basket_speed = 5

# Ball physics
ball_radius = 20
ball_speed = 3
num_balls = 3

# Function to reset the game state
def reset_game():
    global balls, score, start_ticks, game_over, basket_x
    balls = []
    for _ in range(num_balls):
        x = random.randint(ball_radius, WIDTH - ball_radius)
        y = random.randint(-HEIGHT, 0)
        value = random.randint(1, 9)  # Each ball has a fixed number between 1 and 9
        balls.append({"x": x, "y": y, "value": value})
    score = 0
    start_ticks = pygame.time.get_ticks()
    game_over = False
    basket_x = WIDTH // 2 - basket_width // 2

# Initialize game state
score = 0
game_over = False
reset_game()

# Game FPS
clock = pygame.time.Clock()
FPS = 75

# Timer duration
time_limit = 25  # 25 seconds

# Game loop
running = True
while running:
    screen.fill(WHITE)

    # --- Events ---
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    if not game_over:
        # Movement
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and basket_x > 0:
            basket_x -= basket_speed
        if keys[pygame.K_RIGHT] and basket_x < WIDTH - basket_width:
            basket_x += basket_speed

        # Ball movement
        for ball in balls:
            ball["y"] += ball_speed

            if (
                basket_x < ball["x"] < basket_x + basket_width
                and basket_y + basket_height < ball["y"] + ball_radius < basket_y + basket_height + 20
            ):
                score += 1
                ball["x"] = random.randint(ball_radius, WIDTH - ball_radius)
                ball["y"] = random.randint(-HEIGHT, 0)
                ball["value"] = random.randint(1, 9)

            elif ball["y"] > HEIGHT:
                ball["x"] = random.randint(ball_radius, WIDTH - ball_radius)
                ball["y"] = random.randint(-HEIGHT, 0)
                ball["value"] = random.randint(1, 9)

            # Draw the ball
            pygame.draw.circle(screen, BALL_COLOR, (ball["x"], ball["y"]), ball_radius)
            num_text = font.render(str(ball["value"]), True, (0, 0, 0))
            text_rect = num_text.get_rect(center=(ball["x"], ball["y"]))
            screen.blit(num_text, text_rect)

        # Timer 
        seconds_passed = (pygame.time.get_ticks() - start_ticks) / 1000
        time_left = max(0, int(time_limit - seconds_passed))

        if time_left == 0:
            game_over = True

        # basket image
        screen.blit(basket_image, (basket_x, basket_y))

        # Timer box
        pygame.draw.rect(screen, (0, 0, 0), (10, 10, 100, 40), 2)
        timer_text = font.render(f"Time: {time_left}", True, (0, 0, 0))
        screen.blit(timer_text, (20, 20))

        # Score box
        pygame.draw.rect(screen, (0, 0, 0), (WIDTH - 110, 10, 100, 40), 2)
        score_text = font.render(f"Score: {score}", True, (0, 0, 0))
        screen.blit(score_text, (WIDTH - 105, 20))

    else:
        # Game Over screen
        over_text = big_font.render("Game Over Nigger", True, (200, 0, 0))
        screen.blit(over_text, (WIDTH // 2 - over_text.get_width() // 2, HEIGHT // 2 - over_text.get_height()))

        restart_text = font.render("Press Enter to Restart (Loser)", True, (0, 0, 0))
        screen.blit(restart_text, (WIDTH // 2 - restart_text.get_width() // 2, HEIGHT // 2 + 10))

        # Press Enter to restart
        keys = pygame.key.get_pressed()
        if keys[pygame.K_RETURN]:
            reset_game()

    # Refresh
    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
sys.exit()
