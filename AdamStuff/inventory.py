import pygame
import sys
import time
import random

pygame.init()

# Screen setup
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Main Game")
clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 36)

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
GREEN = (100, 255, 100)
RED = (255, 100, 100)

# Timing
BONUS_INTERVAL = 600  # 10 minutes
last_bonus_time = time.time()

# Button helper
def draw_button(rect, text, color):
    pygame.draw.rect(screen, color, rect)
    label = font.render(text, True, BLACK)
    label_rect = label.get_rect(center=rect.center)
    screen.blit(label, label_rect)

def show_bonus_popup():
    popup_rect = pygame.Rect(WIDTH // 4, HEIGHT // 3, WIDTH // 2, HEIGHT // 3)
    yes_button = pygame.Rect(popup_rect.left + 50, popup_rect.bottom - 70, 100, 50)
    no_button = pygame.Rect(popup_rect.right - 150, popup_rect.bottom - 70, 100, 50)

    while True:
        screen.fill(GRAY)
        pygame.draw.rect(screen, WHITE, popup_rect)

        # Prompt
        text = font.render("Play a mini-game for a bonus?", True, BLACK)
        screen.blit(text, (popup_rect.centerx - text.get_width() // 2, popup_rect.top + 40))

        # Buttons
        draw_button(yes_button, "Yes", GREEN)
        draw_button(no_button, "No", RED)

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if yes_button.collidepoint(event.pos):
                    return "yes"
                elif no_button.collidepoint(event.pos):
                    return "no"

        clock.tick(30)

# Placeholder mini-games
def mini_game_1():
    print("Mini-game 1 started")
    running = True
    while running:
        screen.fill((0, 100, 200))
        text = font.render("Mini-Game 1: Press ESC to exit", True, WHITE)
        screen.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT // 2))
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                running = False

        clock.tick(60)

def mini_game_2():
    print("Mini-game 2 started")
    running = True
    while running:
        screen.fill((200, 100, 0))
        text = font.render("Mini-Game 2: Press ESC to exit", True, WHITE)
        screen.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT // 2))
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                running = False

        clock.tick(60)

def play_random_mini_game():
    mini_game = random.choice([mini_game_1, mini_game_2])
    mini_game()  # Call the selected mini-game

# Main game loop
def main():
    global last_bonus_time

    running = True
    while running:
        screen.fill((30, 30, 60))

        # Display timer
        time_elapsed = time.time() - last_bonus_time
        time_remaining = max(0, BONUS_INTERVAL - int(time_elapsed))
        timer_text = font.render(f"Next bonus in: {time_remaining}s", True, WHITE)
        screen.blit(timer_text, (20, 20))

        # Trigger bonus popup
        if time_elapsed >= BONUS_INTERVAL:
            result = show_bonus_popup()
            last_bonus_time = time.time()
            if result == "yes":
                play_random_mini_game()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
