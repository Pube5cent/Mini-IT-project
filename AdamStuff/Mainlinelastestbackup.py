import pygame
import sys
import os
import time
import json
import random
import subprocess
from PIL import Image
from Ryanstuff import music_manager #from Ryanstuff import game_save
from Ryanstuff import Rebirth
from Ryanstuff import game_save
from Ryanstuff.Rebirth import RebirthSystem
from Ryanstuff.game_save import save_game, load_game
from Ryanstuff.music_manager import init_music, play_music, pause_music, unpause_music, stop_music

rebirth_system = RebirthSystem(initial_cost=2)

#Initialize Pygame
pygame.init()

# Initialize Pygame and music
pygame.init()
init_music()

# Play background music
play_music("Ryanstuff/Game.mp3")
volume_on = False

#Screen settings
WIDTH, HEIGHT = 1080, 720
FPS = 60
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Knowledge Clicker")
clock = pygame.time.Clock()
fullscreen = False

# Auto clicker Delay
auto_click_timer = 0
auto_click_delay = 0.1

# Temp upgrade timing
last_check = time.time()

#Load GIF frames
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

#Background GIF
background_gif_path = "RyanStuff/main_wallpaper.gif"
background_frames = load_gif_frames(background_gif_path, scale=(WIDTH, HEIGHT))

#Knowledge, player_state, items = game_save.load_game()
#Knowledge_per_click = 1

# Fonts
font = pygame.font.SysFont("Arial", 24)

# Pause menu state
paused = False

# Pause Button Size
button_width = 150
button_height = 40
padding = 10

pause_button_rect = pygame.Rect(
    screen.get_width() - button_width - padding,
    padding,
    button_width,
    button_height
)

pause_button_color = (70, 70, 70) 
pause_button_text_color = (255, 255, 255)  
pause_button_text = font.render("Pause", True, pause_button_text_color)

#Game Variables
Knowledge = 0
Knowledge_per_click = 1

#initialize rebirth
rebirth = RebirthSystem(initial_cost=2)
Rebirth_multiplier = 1
Rebirth_multiplier = rebirth_system.multiplier

#Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
LIGHT_GRAY = (230, 230, 230)
GREEN = (0, 200, 0)
DARK_GREEN = (0, 150, 0)
RED = (255, 100, 100)
BLUE =  (100, 100, 255)

# Pop up Menu Timing
bonus_interval = 5  # seconds
last_bonus_time = time.time()

#Items
items = {
    "Manual research": {
        "cost": 15,
        "cps": 1,
        "owned": 0,
        "elapsed": 0.0,
        "gif_path": "AdamStuff/assets/gif_0.gif"
    },
    "Turbo Learn": {
        "cost": 50,
        "cps": 1,
        "owned": 0,
        "elapsed": 0.0,
        "gif_path": "AdamStuff/assets/gif_1.gif"
    },
    "Super Click": {
        "cost": 10,
        "cps": 3,
        "owned": 0,
        "elapsed": 0.0,
        "gif_path": "AdamStuff/assets/gif_3.gif",  
        "click_bonus": 1
    }
}

for item in items.values():
    item["frames"] = load_gif_frames(item["gif_path"])


#loads the game
Knowledge, rebirth_multiplier, rebirth_count, last_saved_time = load_game(items)
rebirth_system = RebirthSystem(saved_multiplier=rebirth_multiplier, saved_count=rebirth_count)
Rebirth_multiplier = rebirth_system.multiplier

# Offline gain
offline_seconds = time.time() - last_saved_time
offline_knowledge = 0

for item in items.values():
    if item["owned"] > 0 and item["cps"] > 0:
        offline_knowledge += item["owned"] * item["cps"] * offline_seconds * Rebirth_multiplier

Knowledge += offline_knowledge

if offline_knowledge > 0:
    print(f"Gained {int(offline_knowledge)} Knowledge while offline!")


#Centre gif
center_gif_path = "AdamStuff/assets/floating_book.gif"
center_gif_frames = load_gif_frames(center_gif_path, scale=(150, 150))

#UI Elements
shop_buttons = {}
book_button = pygame.Rect(WIDTH // 2 - 50, HEIGHT // 2 - 50, 100, 100)
rebirth_button = pygame.Rect(WIDTH - 220, HEIGHT - 100, 200, 60)


# Upgrade Icons
upgrade_icons = {
    "fast_click": pygame.transform.scale(pygame.image.load("AdamStuff/assets/pill_red.png"), (40, 40)),
    "bonus_click": pygame.transform.scale(pygame.image.load("AdamStuff/assets/pill_blue.png"), (40, 40)),
}

# Active Upgrades
active_upgrades = {
    "fast_click": {
        "level": 2,                # Temp upgrade level
        "end_time": 1724341234.123
    }
}

#Toggle fullscreen
def toggle_fullscreen():
    global screen, fullscreen
    fullscreen = not fullscreen
    if fullscreen:
        screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.FULLSCREEN)
    else:
        screen = pygame.display.set_mode((WIDTH, HEIGHT))

# Temp Upgrade Duration (seconds)
UPGRADE_DURATION = 180

def activate_upgrade(upgrade_type, duration=10):
    now = time.time()
    if upgrade_type in active_upgrades:
        active_upgrades[upgrade_type]["level"] += 1
        active_upgrades[upgrade_type]["end_time"] = max(
            active_upgrades[upgrade_type]["end_time"], now + duration
        )
    else:
        active_upgrades[upgrade_type] = {
            "level": 1,
            "end_time": now + duration
        }

def update_upgrades():
    global Knowledge, Knowledge_per_click, active_upgrades, auto_click_timer, auto_click_delay
    now = time.time()
    expired = []

    for upgrade, info in active_upgrades.items():
        if info["end_time"] < now:
            expired.append(upgrade)
        elif upgrade == "fast_click":
            # Apply per-frame knowledge bonus
            if now - auto_click_timer >= auto_click_delay:
                Knowledge += 1 * Rebirth_multiplier #idk what this does yet 
                auto_click_timer = now
        elif upgrade == "bonus_click":
            Knowledge_per_click = 1 + info["level"]

    for upgrade in expired:
        del active_upgrades[upgrade]

    # Reset Knowledge_per_click if bonus_click expired
    if "bonus_click" not in active_upgrades:
        Knowledge_per_click = 1

def draw_active_upgrades():
    x = WIDTH - 50  
    y = 50
    spacing = 5

    for upgrade_type, data in active_upgrades.items():
        icon = upgrade_icons.get(upgrade_type)
        if icon:
            for i in range(data["level"]):  # draw icon per level
                screen.blit(icon, (x - (icon.get_width() + spacing) * i, y))
        y += 50  # move down for next upgrade type

def trigger_random_upgrade():
    upgrade = random.choice(["fast_click", "bonus_click"])
    activate_upgrade(upgrade)

# Drawing the Pause Menu
def draw_pause_menu():
    overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 180))
    screen.blit(overlay, (0, 0))

    text = font.render("Game Paused", True, WHITE)
    screen.blit(text, (WIDTH // 2 - text.get_width() // 2, 150))

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

        if item["owned"] > 0:
            if item["cps"] > 0:
                interval = 1.0 / item["cps"]
                progress = min(item["elapsed"] / interval, 1.0)
            else:
                progress = 1.0

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
    global Knowledge, Knowledge_per_click
    item = items[item_name]
    if Knowledge >= item["cost"]:
        Knowledge -= item["cost"]
        item["owned"] += 1
        item["cost"] *= 1.15

        if item_name == "Super Click":
            Knowledge_per_click += item["click_bonus"]

def update_items(dt):
    global Knowledge
    for item in items.values():
        if item["owned"] > 0 and item["cps"] > 0:
            interval = 1.0 / item["cps"]
            item["elapsed"] += dt
            while item["elapsed"] >= interval:
                Knowledge += item["cps"] * item["owned"] * Rebirth_multiplier #related to rebirth
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

    #draw the rebirth button
    pygame.draw.rect(screen, BLUE, rebirth_button)
    rebirth_text = font.render("Rebirth", True, WHITE)
    screen.blit(rebirth_text, (rebirth_button.centerx - rebirth_text.get_width() // 2,
                               rebirth_button.centery - rebirth_text.get_height() // 2))

    multiplier_text = font.render(f"Multiplier: x{Rebirth_multiplier}", True, WHITE)
    screen.blit(multiplier_text, (WIDTH - 150, 110))

    draw_active_upgrades()
    

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
                pygame.quit(); sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if yes_button.collidepoint(event.pos):
                    return "yes"
                elif no_button.collidepoint(event.pos):
                    return "no"
                
 # Temp upgrade handler
def check_for_triggered_upgrade():
    try:
        with open("shared_state.json", "r") as f:
            data = json.load(f)

        upgrade = data.get("trigger_upgrade")
        if upgrade:
            activate_upgrade(upgrade)
            # Reset trigger
            data["trigger_upgrade"] = None
            with open("shared_state.json", "w") as f:
                json.dump(data, f)
    except Exception as e:
        print("Error checking upgrade:", e)

# Mini Game Path
def mini_game_1():
    #subprocess.Popen(["python", "temp_mini_game.py"])
    #subprocess.Popen(["python", "Azim stuff/minigame testing 1.py"])
    subprocess.Popen(["python", "Yeap Stuff/main.py"])

def mini_game_2():
    #subprocess.Popen(["python", "temp_mini_game.py"])
    #subprocess.Popen(["python", "Azim stuff/minigame testing 1.py"])
    subprocess.Popen(["python", "Yeap Stuff/main.py"])

def draw_button(surface, rect, text, active=False):
    color = (200, 50, 50) if active else (70, 70, 70)
    pygame.draw.rect(surface, color, rect)
    pygame.draw.rect(surface, (255, 255, 255), rect, 2)
    text_surf = font.render(text, True, (255, 255, 255))
    text_rect = text_surf.get_rect(center=rect.center)
    surface.blit(text_surf, text_rect)

draw_button(screen, pause_button_rect, "Pause" if not paused else "Resume", active=paused)

def toggle_volume():
    global volume_on
    volume_on = not volume_on
    pygame.mixer.music.set_volume(1.0 if volume_on else 0.0)

def draw_pause_button():
    pygame.draw.rect(screen, pause_button_color, pause_button_rect)
    # Center text on button
    text_rect = pause_button_text.get_rect(center=pause_button_rect.center)
    screen.blit(pause_button_text, text_rect)


#Main Game Loop
while True:
    dt = clock.tick(FPS) / 1000

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            save_game(Knowledge, rebirth_system.multiplier, rebirth_system.rebirth_count, items)  # Update variables as needed
            pygame.quit()
            sys.exit()

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                paused = not paused
            elif event.key == pygame.K_f:
                toggle_fullscreen()

        elif event.type == pygame.MOUSEBUTTONDOWN:
            mx, my = event.pos
            
            # Pause button (always visible top right)
            if pause_button_rect.collidepoint(mx, my):
                paused = not paused
                
            elif paused:
                # Pause menu buttons rectangles
                menu_x = screen.get_width() - button_width - padding
                menu_y = padding
                fullscreen_button = pygame.Rect(menu_x, menu_y, button_width, button_height)
                volume_button = pygame.Rect(menu_x, menu_y + button_height + padding, button_width, button_height)
                quit_button = pygame.Rect(menu_x, menu_y + 2 * (button_height + padding), button_width, button_height)

                if fullscreen_button.collidepoint(mx, my):
                    toggle_fullscreen()
                elif volume_button.collidepoint(mx, my):
                    toggle_volume()
                elif quit_button.collidepoint(mx, my):
                    if offline_knowledge > 0:
                        print(f"Gained {int(offline_knowledge)} Knowledge while offline!")
                    pygame.quit()
                    sys.exit()

            elif book_button.collidepoint(event.pos):
                bonus = 1
                if "fast_click" in active_upgrades:
                    bonus += active_upgrades["fast_click"]["level"] * 0.5
                    Knowledge += Knowledge_per_click * bonus * Rebirth_multiplier 

            elif rebirth_button.collidepoint(mx, my):
                if rebirth_system.can_rebirth(Knowledge):
                    Knowledge = 0
                    rebirth_system.rebirth()
                    Rebirth_multiplier = rebirth_system.multiplier
                    print("Rebirth successful! Multiplier:", Rebirth_multiplier)
                else:
                    print("Not enough Knowledge to rebirth. Need:", rebirth_system.cost)

            else:
                handle_shop_click(event.pos)
                # Game clicks when not paused
                if book_button.collidepoint(event.pos):
                    bonus = 1
                    if "fast_click" in active_upgrades:
                        bonus += active_upgrades["fast_click"]["level"] * 0.5
                    Knowledge += Knowledge_per_click * bonus
                else:
                    handle_shop_click(event.pos)
                    #print("Not enough Knowledge to rebirth. Need:", rebirth_system.cost)

            
    if time.time() - last_check > 1:
        check_for_triggered_upgrade()
        last_check = time.time()

    if not paused:
        if time.time() - last_bonus_time > bonus_interval:
            if show_bonus_popup() == "yes":
                random.choice([mini_game_1, mini_game_2])()
            last_bonus_time = time.time()

        update_items(dt)
        update_upgrades()

    draw()
    draw_pause_button()

    if paused:
        # Draw transparent overlay
        overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 180))
        screen.blit(overlay, (0, 0))

        # Draw pause text
        pause_text = font.render("PAUSED - Press ESC to Resume", True, WHITE)
        screen.blit(pause_text, (WIDTH // 2 - pause_text.get_width() // 2, HEIGHT // 2 - 20))

        # Draw buttons in top-right corner
        menu_x = screen.get_width() - button_width - padding
        menu_y = padding
        fullscreen_button = pygame.Rect(menu_x, menu_y, button_width, button_height)
        volume_button = pygame.Rect(menu_x, menu_y + button_height + padding, button_width, button_height)
        quit_button = pygame.Rect(menu_x, menu_y + 2 * (button_height + padding), button_width, button_height)

        draw_button(screen, fullscreen_button, "Toggle Fullscreen")
        draw_button(screen, volume_button, f"Volume: {'On' if volume_on else 'Off'}")
        draw_button(screen, quit_button, "Quit Game")

    pygame.display.update()