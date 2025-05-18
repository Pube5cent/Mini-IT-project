import pygame
import sys
import random
import os
import re

# Initialize pygame
pygame.init()

# Load and play background music
pygame.mixer.music.load("Azimstuff/bgm_music.mp3")
pygame.mixer.music.set_volume(0.1)
pygame.mixer.music.play(-1)

# Screen settings
WIDTH, HEIGHT = 600, 400
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Catch The Right")

# Load and sort background frames
frame_files = sorted(os.listdir('Azimstuff/gif_frames'), key=lambda f: int(re.search(r'frame_(\d+)', f).group(1)))
background_frames = [pygame.transform.scale(pygame.image.load(os.path.join('Azimstuff/gif_frames', f)).convert(), (WIDTH, HEIGHT)) for f in frame_files]

current_frame = 0
frame_interval = 100
last_update = pygame.time.get_ticks()

# Colors
WHITE = (255, 255, 255)
BASKET_COLOR = (100, 200, 255)
BALL_COLOR = (255, 100, 100)

# Fonts
font = pygame.font.SysFont(None, 30)
big_font = pygame.font.SysFont(None, 60)

# Load basket image
basket_image = pygame.image.load("Azimstuff/basket.png")
basket_width = 100
basket_height = 60
basket_image = pygame.transform.smoothscale(basket_image, (basket_width, basket_height))

basket_x = WIDTH // 2 - basket_width // 2
basket_y = HEIGHT - basket_height - 60
basket_speed = 5

# Ball physics
ball_radius = 20
ball_speed = 2
num_balls = 2

def generate_question():
    a = random.randint(1, 9)
    b = random.randint(1, 9)
    return f"{a} + {b}", a + b

def generate_balls():
    global balls
    balls = []
    used_values = {correct_answer}
    correct_ball_placed = False

    for i in range(num_balls):
        x = random.randint(ball_radius, WIDTH - ball_radius)
        y = random.randint(-HEIGHT, -20)
        if not correct_ball_placed:
            value = correct_answer
            correct_ball_placed = True
        else:
            while True:
                wrong = random.randint(1, 18)
                if wrong != correct_answer and wrong not in used_values:
                    used_values.add(wrong)
                    value = wrong
                    break
        balls.append({"x": x, "y": y, "value": value})

def reset_game():
    global score, start_ticks, game_over, question, correct_answer
    question, correct_answer = generate_question()
    generate_balls()
    score = 0
    start_ticks = pygame.time.get_ticks()
    game_over = False

def new_question():
    global question, correct_answer
    question, correct_answer = generate_question()
    generate_balls()

score = 0
game_over = False
reset_game()

clock = pygame.time.Clock()
FPS = 100
time_limit = 60

running = True
while running:
    now = pygame.time.get_ticks()
    if now - last_update >= frame_interval:
        current_frame = (current_frame + 1) % len(background_frames)
        last_update = now
    screen.blit(background_frames[current_frame], (0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    if not game_over:
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and basket_x > 0:
            basket_x -= basket_speed
        if keys[pygame.K_RIGHT] and basket_x < WIDTH - basket_width:
            basket_x += basket_speed

        seconds_passed = (pygame.time.get_ticks() - start_ticks) / 1000
        time_left = max(0, int(time_limit - seconds_passed))

        if time_left == 0:
            game_over = True

        for ball in balls:
            ball["y"] += ball_speed

            if (
                basket_x < ball["x"] < basket_x + basket_width
                and basket_y + basket_height < ball["y"] + ball_radius < basket_y + basket_height + 20
            ):
                if ball["value"] == correct_answer:
                    score += 1
                    new_question()
                    break  # Skip further checks after correct answer is caught
                else:
                    # Reposition wrong answer
                    ball["x"] = random.randint(ball_radius, WIDTH - ball_radius)
                    ball["y"] = random.randint(-HEIGHT, 0)
                    while True:
                        new_val = random.randint(1, 18)
                        if new_val != correct_answer:
                            ball["value"] = new_val
                            break

            elif ball["y"] > HEIGHT:
                ball["x"] = random.randint(ball_radius, WIDTH - ball_radius)
                ball["y"] = random.randint(-HEIGHT, 0)
                if ball["value"] != correct_answer:
                    while True:
                        new_val = random.randint(1, 18)
                        if new_val != correct_answer:
                            ball["value"] = new_val
                            break

            pygame.draw.circle(screen, BALL_COLOR, (ball["x"], ball["y"]), ball_radius)
            num_text = font.render(str(ball["value"]), True, (0, 0, 0))
            text_rect = num_text.get_rect(center=(ball["x"], ball["y"]))
            screen.blit(num_text, text_rect)

        screen.blit(basket_image, (basket_x, basket_y))

        pygame.draw.rect(screen, (0, 0, 0), (10, 10, 100, 40), 2)
        timer_text = font.render(f"Time: {time_left}", True, (0, 0, 0))
        screen.blit(timer_text, (20, 20))

        question_box_height = 40
        question_box_y = basket_y + basket_height + 5
        pygame.draw.rect(screen, (0, 0, 0), (0, question_box_y, WIDTH, question_box_height), 2)
        question_text = font.render(f"Q: {question}", True, (0, 0, 0))
        screen.blit(question_text, (WIDTH // 2 - question_text.get_width() // 2, question_box_y + (question_box_height - question_text.get_height()) // 2))

        pygame.draw.rect(screen, (0, 0, 0), (WIDTH - 110, 10, 100, 40), 2)
        score_text = font.render(f"Score: {score}", True, (0, 0, 0))
        screen.blit(score_text, (WIDTH - 105, 20))

    else:
        over_text = big_font.render("Game Over", True, (200, 0, 0))
        screen.blit(over_text, (WIDTH // 2 - over_text.get_width() // 2, HEIGHT // 2 - over_text.get_height()))

        restart_text = font.render("Press Enter to Restart", True, (0, 0, 0))
        screen.blit(restart_text, (WIDTH // 2 - restart_text.get_width() // 2, HEIGHT // 2 + 10))

        keys = pygame.key.get_pressed()
        if keys[pygame.K_RETURN]:
            reset_game()

    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
sys.exit()
