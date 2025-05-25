import pygame
import sys
import os
import time
import random
import subprocess
from PIL import Image
from Rebirth import RebirthSystem# Import rebirth system

# Initialize Pygame
pygame.init()

# Screen settings
WIDTH, HEIGHT = 1080, 720
FPS = 60
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Knowledge Clicker")
clock = pygame.time.Clock()

# Load GIF frames
def load_gif_frames(path, scale=(64, 64)):
    frames = []
    if not os.path.exists(path):
        print(f"GIF not found at {path}")
        return frames
    gif = Image.open(path)
    try:
        while True:
            frame = gif.convert("RGBA")
            pygame_image = pygame.image.fromstring(frame.tobytes(), frame.size, frame.mode)
            if scale:
                pygame_image = pygame.transform.scale(pygame_image, scale)
            frames.append(pygame_image)
            gif.seek(gif.tell() + 1)
    except EOFError:
        pass
    return frames

# Background GIF
background_gif_path = "RyanStuff/main_wallpaper.gif"
background_frames = load_gif_frames(background_gif_path, scale=(WIDTH, HEIGHT))

# Fonts
font = pygame.font.SysFont("Arial", 24)

# Pause menu state
paused = False

# Game Variables
Knowledge = 0
Knowledge_per_click = 1

# Initialize rebirth system
rebirth = RebirthSystem(initial_cost=2)
Insight = 0
Rebirth_multiplier = 1

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
LIGHT_GRAY = (230, 230, 230)
GREEN = (0, 200, 0)
DARK_GREEN = (0, 150, 0)
RED = (255, 100, 100)
BLUE = (100, 100, 255)

# Pop up Menu Timing
bonus_interval = 10  # 10 seconds for testing; adjust as needed
last_bonus_time = time.time()

# Items
items = {
    "Manual research": {"cost": 15, "cps": 1.0, "owned": 0, "elapsed": 0.0, "gif_path": "AdamStuff/assets/gif_0.gif"},
    "Turbo Learn": {"cost": 100, "cps": 2.5, "owned": 0, "elapsed": 0.0, "gif_path": "AdamStuff/assets/gif_1.gif"},
}

for item in items.values():
    item["frames"] = load_gif_frames(item["gif_path"])

# Centre gif
center_gif_path = "AdamStuff/assets/floating_book.gif"
center_gif_frames = load_gif_frames(center_gif_path, scale=(150, 150))

# UI Elements
shop_buttons = {}
book_button = pygame.Rect(WIDTH // 2 - 50, HEIGHT // 2 - 50, 100, 100)
rebirth_button = pygame.Rect(WIDTH - 150, 20, 130, 50)

# Drawing the Pause Menu
def draw_pause_menu():
    overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 180))  # semi-transparent background
    screen.blit(overlay, (0, 0))

    # Pause text
    text = font.render("Game Paused", True, WHITE)
    screen.blit(text, (WIDTH // 2 - text.get_width() // 2, 150))

    # Buttons
    resume_button = pygame.Rect(WIDTH // 2 - 100, 250, 200, 60)
    quit_button = pygame.Rect(WIDTH // 2 - 100, 330, 200, 60)

    pygame.draw.rect(screen, GREEN, resume_button)
    pygame.draw.rect(screen, RED, quit_button)

    resume_text = font.render("Resume", True, BLACK)
    quit_text = font.render("Quit", True, BLACK)

    screen.blit(resume_text, (resume_button.centerx - resume_text.get_width() // 2,
                              resume_button.centery - resume_text.get_height() // 2))
    screen.blit(quit_text, (quit_button.centerx - quit_text.get_width() // 2,
                            quit_button.centery - quit_text.get_height() // 2))

    return resume_button, quit_button

# Draw Click Button
def draw_center_gif(current_frame_index):
    if center_gif_frames:
        current_frame = center_gif_frames[current_frame_index]
        gif_pos = (WIDTH // 2 - current_frame.get_width() // 2, HEIGHT // 2 - current_frame.get_height() // 2)
        screen.blit(current_frame, gif_pos)

def draw_shop():
    y_offset = 100
    shop_buttons.clear()
    for item_name, item in items.items():
        button_rect = pygame.Rect(20, y_offset, 360, 80)
        shop_buttons[item_name] = button_rect

        mouse_pos = pygame.mouse.get_pos()
        pygame.draw.rect(screen, LIGHT_GRAY if button_rect.collidepoint(mouse_pos) else GRAY, button_rect)
        pygame.draw.rect(screen, BLACK, button_rect, 3)

        item_text = font.render(f"{item_name}", True, BLACK)
        cost_text = font.render(f"Cost: {int(item['cost'])}", True, BLACK)
        owned_text = font.render(f"Owned: {item['owned']}", True, BLACK)
        screen.blit(item_text, (button_rect.x + 10, button_rect.y + 5))
        screen.blit(cost_text, (button_rect.x + 10, button_rect.y + 30))
        screen.blit(owned_text, (button_rect.x + 200, button_rect.y + 30))

        if item["owned"] > 0 and item["cps"] > 0:
            interval = 1.0 / item["cps"]
            progress = min(item["elapsed"] / interval, 1.0)

            bar_back = pygame.Rect(button_rect.x + 10, button_rect.y + 60, 340, 10)
            pygame.draw.rect(screen, DARK_GREEN, bar_back)
            fill_width = int(340 * progress)
            bar_fill = pygame.Rect(button_rect.x + 10, button_rect.y + 60, fill_width, 10)
            pygame.draw.rect(screen, GREEN, bar_fill)

            if item["frames"]:
                frame_count = len(item["frames"])
                current_frame_index = int(progress * frame_count) % frame_count
                current_frame = item["frames"][current_frame_index]
                gif_pos = (button_rect.right + 10, button_rect.y + 10)
                screen.blit(current_frame, gif_pos)

        y_offset += 100

def handle_shop_click(pos):
    for item_name, button_rect in shop_buttons.items():
        if button_rect.collidepoint(pos):
            buy_item(item_name)

def buy_item(item_name):
    global Knowledge
    item = items[item_name]
    if Knowledge >= item["cost"]:
        Knowledge -= item["cost"]
        item["owned"] += 1
        item["cost"] *= 1.15

def update_items(dt):
    global Knowledge
    for item in items.values():
        if item["owned"] > 0 and item["cps"] > 0:
            interval = 1.0 / item["cps"]
            item["elapsed"] += dt
            while item["elapsed"] >= interval:
                Knowledge += item["cps"] * item["owned"] * Rebirth_multiplier
                item["elapsed"] -= interval

def draw_knowledge_counter():
    text = font.render(f"Knowledge: {int(Knowledge)}", True, WHITE)
    screen.blit(text, (20, 20))

def draw():
    if background_frames:
        bg_frame_index = (pygame.time.get_ticks() // 100) % len(background_frames)
        screen.blit(background_frames[bg_frame_index], (0, 0))
    else:
        screen.fill(WHITE)

    draw_knowledge_counter()
    draw_shop()

    if center_gif_frames:
        center_frame_index = pygame.time.get_ticks() // 100 % len(center_gif_frames)
        draw_center_gif(center_frame_index)

    # Draw rebirth button and info
    pygame.draw.rect(screen, BLUE, rebirth_button)
    rebirth_text = font.render("Rebirth", True, WHITE)
    screen.blit(rebirth_text, (rebirth_button.centerx - rebirth_text.get_width() // 2,
                               rebirth_button.centery - rebirth_text.get_height() // 2))

    insight_text = font.render(f"Insight: {Insight}", True, WHITE)
    multiplier_text = font.render(f"Multiplier: x{Rebirth_multiplier}", True, WHITE)
    screen.blit(insight_text, (WIDTH - 150, 80))
    screen.blit(multiplier_text, (WIDTH - 150, 110))

def show_bonus_popup():
    popup_rect = pygame.Rect(WIDTH // 4, HEIGHT // 3, WIDTH // 2, HEIGHT // 3)
    yes_button = pygame.Rect(popup_rect.left + 50, popup_rect.bottom - 70, 100, 50)
    no_button = pygame.Rect(popup_rect.right - 150, popup_rect.bottom - 70, 100, 50)

    while True:
        dt = clock.tick(FPS) / 1000
        update_items(dt)
        draw()

        overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 128))
        screen.blit(overlay, (0, 0))

        pygame.draw.rect(screen, (255, 255, 255), popup_rect)
        pygame.draw.rect(screen, BLACK, popup_rect, 3)

        question = font.render("Play a mini-game for a bonus?", True, BLACK)
        screen.blit(question, (popup_rect.centerx - question.get_width() // 2, popup_rect.top + 40))

        pygame.draw.rect(screen, GREEN, yes_button)
        pygame.draw.rect(screen, RED, no_button)

        screen.blit(font.render("Yes", True, BLACK), (yes_button.centerx - 20, yes_button.centery - 10))
        screen.blit(font.render("No", True, BLACK), (no_button.centerx - 20, no_button.centery - 10))

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if yes_button.collidepoint(event.pos):
                    return "yes"
                elif no_button.collidepoint(event.pos):
                    return "no"

def mini_game_1():
    subprocess.run(["python", "Azimstuff/minigame_testing_1.py"])

def mini_game_2():
    subprocess.run(["python", "Yeap Stuff/main.py"])

# Game Loop
while True:
    dt = clock.tick(FPS) / 1000

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                paused = not paused

        elif event.type == pygame.MOUSEBUTTONDOWN and not paused:
            if book_button.collidepoint(event.pos):
                Knowledge += Knowledge_per_click * Rebirth_multiplier
            elif rebirth_button.collidepoint(event.pos):
                if rebirth.can_rebirth(Knowledge):
                  Knowledge, Insight, Rebirth_multiplier = rebirth.rebirth(Knowledge, Insight)



                else:
                    print("Not enough Knowledge to rebirth!")  # Could show a popup instead
            else:
                handle_shop_click(event.pos)

    # Update only if not paused
    if not paused:
        # Check for popup interval
        if time.time() - last_bonus_time > bonus_interval:
            if show_bonus_popup() == "yes":
                random.choice([mini_game_1, mini_game_2])()
            last_bonus_time = time.time()

        update_items(dt)

    draw()

    # Draw pause overlay
    if paused:
        overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 180))  # semi-transparent black
        screen.blit(overlay, (0, 0))

        pause_text = font.render("PAUSED - Press ESC to Resume", True, WHITE)
        screen.blit(pause_text, (WIDTH // 2 - pause_text.get_width() // 2, HEIGHT // 2 - 20))

    pygame.display.update()
