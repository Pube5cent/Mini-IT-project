import pygame
import sys
import os
import math
import time
import json
import random
import subprocess
from PIL import Image
#from Ryanstuff import music_manager #from Ryanstuff import game_save
from Ryanstuff import Rebirth
from Ryanstuff import game_save
from Ryanstuff.Rebirth import RebirthSystem
from Ryanstuff.game_save import save_game, load_game
from Ryanstuff.music_manager import init_music, play_music, pause_music, unpause_music, stop_music


#Initialize Pygame
os.environ['SDL_VIDEO_CENTERED'] = '1'
pygame.init()

# Initialize Pygame and music
pygame.init()
init_music()
clock = pygame.time.Clock()
rebirth_system = RebirthSystem()

# Play background music
#play_music("Ryanstuff/Game.mp3")
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


#Knowledge_per_click = 1

# Fonts
font = pygame.font.SysFont("Arial", 24)
small_font = pygame.font.SysFont("Arial", 14)

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
rebirth_system = RebirthSystem()
rebirth_count = 0
rebirth_multiplier = 1
REBIRTH_BUTTON_HEIGHT = 40
rebirth_ready = False
pause_toggle_cooldown = 0.3  # seconds
last_pause_toggle = 0  # initial timestamp

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
        display_info = pygame.display.Info()
        screen = pygame.display.set_mode((display_info.current_w, display_info.current_h), pygame.NOFRAME)
    else:
        screen = pygame.display.set_mode((WIDTH, HEIGHT))

# Temp Section Upgrade Duration (seconds)
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
                Knowledge += 1 * rebirth_system.multiplier
                auto_click_timer = now
        elif upgrade == "bonus_click":
            Knowledge_per_click = 1 + info["level"]

    for upgrade in expired:
        del active_upgrades[upgrade]

    # Reset Knowledge_per_click if bonus_click expired
    if "bonus_click" not in active_upgrades:
        Knowledge_per_click = 1

# Mini-game Button
mini_game_button_rect = pygame.Rect(WIDTH - 60, 150, 40, 40)
mini_game_available = False

def draw_active_upgrades():
    global mini_game_button_rect
    x = WIDTH - 50  
    y = 50
    spacing = 5

    for upgrade_type, data in active_upgrades.items():
        icon = upgrade_icons.get(upgrade_type)
        if icon:
            for i in range(data["level"]):  # draw icon per level
                screen.blit(icon, (x - (icon.get_width() + spacing) * i, y))
        y += 50  # move down for next upgrade type

    # Draw mini-game button just below the last pill
    global mini_game_button_rect
    mini_game_button_rect = pygame.Rect(x - 40, y + 10, 40, 40)

    if mini_game_available:
        # Glow effect
        t = time.time()
        brightness = 200 + int(55 * (math.sin(t * 4) + 1) / 2)  # oscillates between 200 and 255
        glow_color = (brightness, brightness * 0.84, 0)  # Yellowish glow
        pygame.draw.rect(screen, glow_color, mini_game_button_rect, border_radius=10)
    else:
        pygame.draw.rect(screen, (120, 120, 120), mini_game_button_rect, border_radius=10)  # dimmed

    icon = font.render("!", True, BLACK)
    screen.blit(icon, (mini_game_button_rect.centerx - icon.get_width() // 2,
                       mini_game_button_rect.centery - icon.get_height() // 2))
    draw_upgrades()
    draw_tooltip()

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

    if center_gif_frames:
        center_frame_index = pygame.time.get_ticks() // 100 % len(center_gif_frames)
        draw_center_gif(center_frame_index)

    draw_active_upgrades()

    draw_pause_button()
    rebirth_btn = draw_rebirth_button()
    
    #draw rebirth button
def draw_rebirth_button():
    if rebirth_system.can_rebirth(upgrades, UPGRADE_CAP):
        rebirth_btn_rect = pygame.Rect(pause_button_rect.x, pause_button_rect.bottom + 10, 150, 40)
        pygame.draw.rect(screen, BLUE, rebirth_btn_rect, border_radius=6)
        text = font.render("Rebirth", True, WHITE)
        screen.blit(text, (rebirth_btn_rect.centerx - text.get_width() // 2,
                            rebirth_btn_rect.centery - text.get_height() // 2))
        return rebirth_btn_rect
    return None

def show_bonus_popup():
    popup_rect = pygame.Rect(WIDTH // 4, HEIGHT // 3, WIDTH // 2, HEIGHT // 3)
    yes_button = pygame.Rect(popup_rect.left + 50, popup_rect.bottom - 70, 100, 50)
    no_button = pygame.Rect(popup_rect.right - 150, popup_rect.bottom - 70, 100, 50)

    while True:
        dt = clock.tick(FPS) / 1000
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
    subprocess.Popen(["python", "temp_mini_game.py"])
    #subprocess.Popen(["python", "Azim stuff/minigame testing 1.py"])
    #subprocess.Popen(["python", "Yeap Stuff/main.py"])

def mini_game_2():
    subprocess.Popen(["python", "temp_mini_game.py"])
    #subprocess.Popen(["python", "Azim stuff/minigame testing 1.py"])
    #subprocess.Popen(["python", "Yeap Stuff/main.py"])

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

# Upgrade configuration
UPGRADE_CAP = 20

upgrade_defs = [
    {"name": "Book Stand", "base_cost": 10, "base_rate": 0.1, "base_interval": 5.0},
    {"name": "Desk Lamp", "base_cost": 50, "base_rate": 0.5, "base_interval": 4.5},
    {"name": "Whiteboard", "base_cost": 100, "base_rate": 1.0, "base_interval": 4.0},
    {"name": "Encyclopedia Set", "base_cost": 250, "base_rate": 2.0, "base_interval": 3.5},
    {"name": "Research Assistant", "base_cost": 500, "base_rate": 4.0, "base_interval": 3.0},
    {"name": "Study Timer", "base_cost": 750, "base_rate": 6.0, "base_interval": 2.5},
    {"name": "Learning App", "base_cost": 1000, "base_rate": 10.0, "base_interval": 2.0},
    {"name": "Brain Supplements", "base_cost": 1500, "base_rate": 15.0, "base_interval": 1.8},
    {"name": "VR Learning Kit", "base_cost": 2000, "base_rate": 20.0, "base_interval": 1.5},
    {"name": "AI Tutor", "base_cost": 3000, "base_rate": 30.0, "base_interval": 1.2},
]



# Upgrade runtime state
upgrades = []
for i, u in enumerate(upgrade_defs):
    upgrades.append({
        "level": 0,
        "progress": 0.0,
        "last_tick": time.time(),
        "gif": None,  # Placeholder for animation
        "frames": [],
        "frame_index": 0,
        "name": u["name"],
        "base_cost": u["base_cost"],
        "base_rate": u["base_rate"],
        "base_interval": u["base_interval"]
    })

#this loads the game 
knowledge, upgrades, multiplier, rebirth_count, last_saved_time = load_game(upgrade_defs)

rebirth_system.multiplier = multiplier
rebirth_system.rebirth_count = rebirth_count


#for the ofline progress
def get_Knowledge_per_tick(base_rate, level):
    """Calculate how much knowledge is generated per tick at a given level."""
    return base_rate * level  # Simple scaling — can customize

def get_interval(base_interval, level):
    """Calculate interval between ticks at a given level."""
    return max(0.1, base_interval * (0.98 ** (level - 1)))  # Shorter interval as level increases


# Calculate offline progress
offline_time = time.time() - last_saved_time
offline_knowledge = 0

for upg_def, upg in zip(upgrade_defs, upgrades):
    level = upg["level"]
    if level > 0:
        rate = get_Knowledge_per_tick(upg_def["base_rate"], level)
        interval = get_interval(upg_def["base_interval"], level)
        ticks = int(offline_time // interval)
        offline_knowledge += ticks * rate * rebirth_system.multiplier

Knowledge += offline_knowledge
print(f"Offline progress: +{int(offline_knowledge)} knowledge over {int(offline_time)} seconds")


# Load placeholder and gifs
placeholder_icon = pygame.Surface((40, 40))
placeholder_icon.fill((80, 80, 80))

for i in range(len(upgrades)):
    gif_path = f"assets/upgrades/upgrade_{i}.gif"
    if os.path.exists(gif_path):
        try:
            gif = pygame.image.load(gif_path)
            upgrades[i]["gif"] = gif
        except:
            upgrades[i]["gif"] = placeholder_icon
    else:
        upgrades[i]["gif"] = placeholder_icon

# Game state
scroll_y = 0
scroll_speed = 20
upgrade_rects = []
hovered_upgrade = None
UPGRADE_HEIGHT = 80
VISIBLE_HEIGHT = 700  # make sure to change decrese it when adding a new upograde
MAX_SCROLL = max(0, len(upgrades) * UPGRADE_HEIGHT - VISIBLE_HEIGHT)

# Calculate cost

def get_cost(base, level):
    return int(base * (1.15 ** level))

# Upgrade effect

def get_Knowledge_per_tick(base, level):
    return base * (1.1 ** level)

def get_interval(base, level):
    return base * (0.95 ** level)

# Draw upgrades
def draw_upgrades():
    global upgrade_rects, hovered_upgrade
    upgrade_rects = []
    start_y = 100 + scroll_y
    hovered_upgrade = None
    mouse_pos = pygame.mouse.get_pos()

    for idx, upg in enumerate(upgrades):
        y = start_y + idx * 80
        rect = pygame.Rect(20, y, 300, 65)
        upgrade_rects.append((rect, idx))

        pygame.draw.rect(screen, (50, 50, 100), rect, border_radius=8)
        screen.blit(upg["gif"], (rect.x + 10, rect.y + 10))

        level = upg["level"]
        cost = get_cost(upg["base_cost"], level)
        name = f"{upg['name']} ({level}/{UPGRADE_CAP})"
        cost_text = f"Cost: {cost}"

        screen.blit(font.render(name, True, (255, 255, 255)), (rect.x + 60, rect.y + 5))
        screen.blit(font.render(cost_text, True, (200, 200, 200)), (rect.x + 60, rect.y + 25))  # More space


        # Progress bar background
        pygame.draw.rect(screen, (80, 80, 80), (rect.x + 60, rect.y + 50, 180, 10), border_radius=5)

        # Progress bar fill
        pygame.draw.rect(screen, (0, 220, 0), (rect.x + 60, rect.y + 50, int(180 * upg["progress"]), 10), border_radius=5)


        if rect.collidepoint(mouse_pos):
            hovered_upgrade = idx

# Tooltip
def draw_tooltip():
    if hovered_upgrade is not None:
        upg = upgrades[hovered_upgrade]
        level = upg["level"]
        rate = get_Knowledge_per_tick(upg["base_rate"], level)
        interval = get_interval(upg["base_interval"], level)
        tip_lines = [
            f"{upg['name']}",
            f"Generates {rate:.2f} knowledge", 
            f"Every {interval:.2f}s"
        ]
        width = max(font.size(line)[0] for line in tip_lines) + 10
        height = len(tip_lines) * 20 + 10
        x, y = pygame.mouse.get_pos()
        pygame.draw.rect(screen, (0, 0, 0), (x, y, width, height))
        for i, line in enumerate(tip_lines):
            screen.blit(font.render(line, True, (255, 255, 255)), (x + 5, y + 5 + i * 20))

# Update upgrade timers
def update_upgrade_progress():
    global Knowledge
    now = time.time()
    for upg in upgrades:
        if upg["level"] == 0:
            continue
        interval = get_interval(upg["base_interval"], upg["level"])
        elapsed = now - upg["last_tick"]
        upg["progress"] = min(elapsed / interval, 1.0)
        if elapsed >= interval:
            gain = get_Knowledge_per_tick(upg["base_rate"], upg["level"])
            Knowledge += gain * rebirth_system.multiplier
            upg["last_tick"] = now
            upg["progress"] = 0.0

# Handle click
def handle_click(pos):
    global Knowledge
    for rect, idx in upgrade_rects:
        if rect.collidepoint(pos):
            upg = upgrades[idx]
            if upg["level"] >= UPGRADE_CAP:
                return
            cost = get_cost(upg["base_cost"], upg["level"])
            if Knowledge: #>= cost (afiq)
                #Knowledge -= cost (Afiq)
                upg["level"] += 1
                upg["last_tick"] = time.time()
                # Flash effect can be added here

def update_upgrades_logic():
    global Knowledge
    current_time = time.time()
    for upg in upgrades:
        if upg["level"] > 0:
            interval = get_interval(upg["base_interval"], upg["level"])
            elapsed = current_time - upg["last_tick"]
            upg["progress"] = min(1.0, elapsed / interval)

            if elapsed >= interval:
                gain = get_Knowledge_per_tick(upg["base_rate"], upg["level"])
                Knowledge += gain * rebirth_system.multiplier
                upg["last_tick"] = current_time
                upg["progress"] = 0.0

# Auto Saving System (requires fix)
'''SAVE_FILE = "save_data.json"
autosave_timer = 0

def save_game():
    data = {
        "knowledge": Knowledge,
        "upgrades": [u["level"] for u in upgrades]
    }
    with open(SAVE_FILE, "w") as f:
        json.dump(data, f)


def load_game():
    global knowledge
    if os.path.exists(SAVE_FILE):
        try:
            with open(SAVE_FILE, "r") as f:
                content = f.read().strip()
                if not content:
                    print("Save file empty. Starting new game.")
                    return
                data = json.loads(content)
                knowledge = data.get("knowledge", 0)
                upgrade_levels = data.get("upgrades", [])
                for i, level in enumerate(upgrade_levels):
                    if i < len(upgrades):
                        upgrades[i]["level"] = level
        except Exception as e:
            print("Failed to load save:", e)'''

#Main Game Loop
while True:
    dt = clock.tick(FPS) / 1000
    screen.blit(font.render(f"Knowledge: {int(Knowledge)}", True, (255, 255, 255)), (20, 20))
    draw_upgrades()
    draw_tooltip()
    update_upgrade_progress()
    #load_game() (Afiq)

    '''autosave_timer += dt (Afiq)
    if autosave_timer >= 10:
        save_game()
        autosave_timer = 0'''

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            
            save_game(knowledge, rebirth_system.multiplier, rebirth_system.rebirth_count, upgrades)

            pygame.quit()
            sys.exit()

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                paused = not paused
            elif event.key == pygame.K_f:
                toggle_fullscreen()
            elif event.key == pygame.K_UP:
                scroll_y = min(scroll_y + scroll_speed, 0)
            elif event.key == pygame.K_DOWN:
                scroll_y = max(-MAX_SCROLL, scroll_y - scroll_speed)

        elif event.type == pygame.MOUSEBUTTONDOWN:
            mx, my = event.pos
            current_time = time.time()

            if paused:
                # === Pause Menu Buttons ===
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
                    save_game(Knowledge, rebirth_system.multiplier, rebirth_system.rebirth_count, upgrades)
                    pygame.quit()
                    sys.exit()

            elif pause_button_rect.collidepoint(mx, my):
                if current_time - last_pause_toggle > pause_toggle_cooldown:
                    paused = not paused
                    last_pause_toggle = current_time

            elif mini_game_available and mini_game_button_rect.collidepoint(event.pos):
                mini_game_available = False
                last_bonus_time = time.time()
                random.choice([mini_game_1, mini_game_2])()

            else:
                rebirth_btn = draw_rebirth_button()
                if rebirth_btn and rebirth_btn.collidepoint(event.pos):
                    rebirth_multiplier = rebirth_system.perform_rebirth(upgrades)
                    Knowledge = 0

                elif book_button.collidepoint(event.pos):
                    bonus = 1
                    if "fast_click" in active_upgrades:
                        bonus += active_upgrades["fast_click"]["level"] * 0.5
                    Knowledge += Knowledge_per_click * bonus * rebirth_system.multiplier

                elif event.button == 1:
                    handle_click(event.pos)
                elif event.button == 4:  # Scroll up
                    scroll_y = min(scroll_y + scroll_speed, 0)
                elif event.button == 5:  # Scroll down
                    scroll_y = max(-MAX_SCROLL, scroll_y - scroll_speed)

            
    if time.time() - last_check > 1:
        check_for_triggered_upgrade()
        last_check = time.time()

    if not paused: 
        if time.time() - last_bonus_time > bonus_interval:
            mini_game_available = True

        update_upgrades_logic()
        update_upgrades()

    rebirth_ready = all(u["level"] >= UPGRADE_CAP for u in upgrades)

    draw()
    draw_pause_button()
    clock.tick(60)

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