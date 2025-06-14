import pygame
import sys
import random
import os
import json

# Initialize pygame
pygame.init()

# Load and play background music
pygame.mixer.music.load("Azim stuff/bgm_music.mp3")
pygame.mixer.music.set_volume(0.1)
pygame.mixer.music.play(-1)

# Screen settings
WIDTH, HEIGHT = 600, 400
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Catch The Right Answer")

# Load static background image 
background = pygame.image.load("Azim stuff/static_background.jpg")
background = pygame.transform.scale(background, (WIDTH, HEIGHT))

# Colors
WHITE = (255, 255, 255)
BASKET_COLOR = (100, 200, 255)
BALL_COLOR = (255, 100, 100)

# Fonts
font = pygame.font.SysFont(None, 30)
big_font = pygame.font.SysFont(None, 60)

# Load and scale basket image
basket_image = pygame.image.load("Azim stuff/basket.png")
basket_width = 100
basket_height = 60
basket_image = pygame.transform.smoothscale(basket_image, (basket_width, basket_height))

# Basket initial position and speed
basket_x = WIDTH // 2 - basket_width // 2
basket_y = HEIGHT - basket_height - 60
basket_speed = 5

# Ball settings
ball_radius = 20
ball_speed = 2
num_balls = 2

# List for sparkle particles
particles = []

# Sparkle effect when catching the correct answer
def create_sparkles(x, y):
    for _ in range(15):
        particle = {
            "x": x,
            "y": y,
            "radius": random.randint(2, 4),
            "color": (255, 255, 100),
            "speed_x": random.uniform(-1.5, 1.5),
            "speed_y": random.uniform(-1.5, 1.5),
            "life": 20
        }
        particles.append(particle)

# Ambient background particles
ambient_particles = []

# Create initial ambient particles
def init_ambient_particles(num=30):
    for _ in range(num):
        particle = {
            "x": random.uniform(0, WIDTH),
            "y": random.uniform(0, HEIGHT),
            "radius": random.uniform(2, 5),
            "color": (255, 255, 200, 100),
            "speed_x": random.uniform(-0.3, 0.3),
            "speed_y": random.uniform(-0.2, 0.2),
            "life": random.randint(100, 300),
            "max_life": 300
        }
        ambient_particles.append(particle)

init_ambient_particles()

# Generate math question based on elapsed time
def generate_question():
    seconds_passed = (pygame.time.get_ticks() - start_ticks) / 1000

    if not hasattr(generate_question, "sequence"):
        operations = ["add", "sub_add", "multiply"]
        random.shuffle(operations)
        generate_question.sequence = operations
        generate_question.index = 0

    index = int(seconds_passed)
    if index >= len(generate_question.sequence):
        index = len(generate_question.sequence) - 1
    difficulty = generate_question.sequence[index]

    if difficulty == "add":
        a = random.randint(1, 20)
        b = random.randint(1, 20)
        return f"{a} + {b}", a + b
    elif difficulty == "sub_add":
        a = random.randint(10, 30)
        b = random.randint(1, 20)
        if random.choice([True, False]):
            return f"{a} + {b}", a + b
        else:
            return f"{a} - {b}", a - b
    else:  # multiply
        a = random.randint(3, 12)
        b = random.randint(2, 10)
        return f"{a} × {b}", a * b

# Generate falling balls 
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
                wrong = random.randint(1, 100)
                if wrong != correct_answer and wrong not in used_values:
                    used_values.add(wrong)
                    value = wrong
                    break
        balls.append({"x": x, "y": y, "value": value})

# Reset game state
def reset_game():
    global score, start_ticks, game_over, question, correct_answer, lives
    score = 0
    lives = 3
    start_ticks = pygame.time.get_ticks()
    game_over = False
    question, correct_answer = generate_question()
    generate_balls()

# Generate a new question
def new_question():
    global question, correct_answer
    question, correct_answer = generate_question()
    generate_balls()

# Initial game values
score = 0
game_over = False
lives = 3
reset_game()

# Clock and game timing
clock = pygame.time.Clock()
FPS = 100
time_limit = 20

# Game loop
running = True
while running:
    now = pygame.time.get_ticks()
    screen.blit(background, (0, 0))

    # Update and draw ambient particles
    for particle in ambient_particles:
        particle["x"] += particle["speed_x"]
        particle["y"] += particle["speed_y"]
        particle["life"] -= 1

        if particle["x"] < 0:
            particle["x"] = WIDTH
        elif particle["x"] > WIDTH:
            particle["x"] = 0
        if particle["y"] < 0:
            particle["y"] = HEIGHT
        elif particle["y"] > HEIGHT:
            particle["y"] = 0

        alpha = int(255 * (particle["life"] / particle["max_life"]))
        alpha = max(50, alpha)

        surface = pygame.Surface((particle["radius"]*4, particle["radius"]*4), pygame.SRCALPHA)
        pygame.draw.circle(surface, (255, 255, 200, alpha), (particle["radius"]*2, particle["radius"]*2), particle["radius"])
        screen.blit(surface, (particle["x"] - particle["radius"]*2, particle["y"] - particle["radius"]*2))

        if particle["life"] <= 0:
            particle["x"] = random.uniform(0, WIDTH)
            particle["y"] = random.uniform(0, HEIGHT)
            particle["life"] = particle["max_life"]

    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    if not game_over:
        # Basket movement
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and basket_x > 0:
            basket_x -= basket_speed
        if keys[pygame.K_RIGHT] and basket_x < WIDTH - basket_width:
            basket_x += basket_speed

        seconds_passed = (pygame.time.get_ticks() - start_ticks) / 1000
        time_left = max(0, int(time_limit - seconds_passed))

        # Trigger upgrade if player wins
        if score >= 3:
            try:
                with open("shared_state.json", "r") as f:
                    data = json.load(f)
                data["trigger_upgrade"] = random.choice(["bonus_click", "bonus_click"])
                with open("shared_state.json", "w") as f:
                    json.dump(data, f)
                print("Upgrade triggered successfully.")
            except Exception as e:
                print("Failed to update shared state:", e)
            running = False

        # Time runs out
        if time_left == 0:
            print("You lose!")
            game_over = True

        # Update and check ball collisions
        for ball in balls:
            ball["y"] += ball_speed

            if (
                basket_x < ball["x"] < basket_x + basket_width
                and basket_y + basket_height < ball["y"] + ball_radius < basket_y + basket_height + 20
            ):
                if ball["value"] == correct_answer:
                    score += 1
                    create_sparkles(ball["x"], ball["y"])
                    new_question()
                    break
                else:
                    lives -= 1
                    if lives <= 0:
                        print("You lose!")
                        game_over = True
                    else:
                        ball["x"] = random.randint(ball_radius, WIDTH - ball_radius)
                        ball["y"] = random.randint(-HEIGHT, 0)
                        while True:
                            new_val = random.randint(1, 100)
                            if new_val != correct_answer:
                                ball["value"] = new_val
                                break

            elif ball["y"] > HEIGHT:
                ball["x"] = random.randint(ball_radius, WIDTH - ball_radius)
                ball["y"] = random.randint(-HEIGHT, 0)
                if ball["value"] != correct_answer:
                    while True:
                        new_val = random.randint(1, 100)
                        if new_val != correct_answer:
                            ball["value"] = new_val
                            break

            pygame.draw.circle(screen, BALL_COLOR, (ball["x"], ball["y"]), ball_radius)
            num_text = font.render(str(ball["value"]), True, WHITE)
            text_rect = num_text.get_rect(center=(ball["x"], ball["y"]))
            screen.blit(num_text, text_rect)

        # Draw basket
        screen.blit(basket_image, (basket_x, basket_y))

        # Draw timer
        pygame.draw.rect(screen, WHITE, (10, 10, 100, 40), 2)
        timer_text = font.render(f"Time: {time_left}", True, WHITE)
        screen.blit(timer_text, (20, 20))

        # Draw lives
        pygame.draw.rect(screen, WHITE, (120, 10, 80, 40), 2)
        lives_text = font.render(f"Lives: {lives}", True, WHITE)
        screen.blit(lives_text, (122, 20))

        # Draw question box below basket
        question_box_height = 40
        question_box_y = basket_y + basket_height + 5
        pygame.draw.rect(screen, WHITE, (0, question_box_y, WIDTH, question_box_height), 2)
        question_text = font.render(f"Q: {question}", True, WHITE)
        screen.blit(question_text, (WIDTH // 2 - question_text.get_width() // 2, question_box_y + (question_box_height - question_text.get_height()) // 2))

        # Draw score
        pygame.draw.rect(screen, WHITE, (WIDTH - 110, 10, 100, 40), 2)
        score_text = font.render(f"Score: {score}", True, WHITE)
        screen.blit(score_text, (WIDTH - 105, 20))

        # Draw sparkle particles
        for particle in particles[:]:
            particle["x"] += particle["speed_x"]
            particle["y"] += particle["speed_y"]
            particle["life"] -= 1
            particle["radius"] *= 0.95
            if particle["life"] <= 0 or particle["radius"] <= 0.5:
                particles.remove(particle)
            else:
                pygame.draw.circle(screen, particle["color"], (int(particle["x"]), int(particle["y"])), int(particle["radius"]))

    else:
        running = False

    # Instruction fade-in/fade-out
    if seconds_passed < 3:
        instruction_text = font.render(" Score 3 points to win before time runs out!", True, WHITE)
        instruction_bg = pygame.Surface((instruction_text.get_width() + 20, instruction_text.get_height() + 10), pygame.SRCALPHA)

        if seconds_passed < 1.5:
            alpha = int((seconds_passed / 1.5) * 255)
        else:
            alpha = int(((3 - seconds_passed) / 1.5) * 255)
        alpha = max(0, min(255, alpha))

        instruction_bg.fill((0, 0, 0, int(alpha * 0.8)))
        instruction_text.set_alpha(alpha)

        x = WIDTH // 2 - instruction_text.get_width() // 2
        y = HEIGHT // 2 - 55
        screen.blit(instruction_bg, (x - 10, y - 5))
        screen.blit(instruction_text, (x, y))

    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
sys.exit()
