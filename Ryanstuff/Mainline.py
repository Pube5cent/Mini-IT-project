import pygame
import sys
from PIL import Image, ImageSequence
from Rebirth import perform_rebirth
import game_save #sva load module
import music_manager
import os

#music
pygame.init() # Initialize Pygame
music_manager.init_music()
music_manager.pause_music("Ryanstuff/Game.mp3")



# Screen settings
WIDTH, HEIGHT = 1290, 800
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("")

# Fonts
font = pygame.font.SysFont("Arial", 24)

# Global Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
LIGHT_GRAY = (230, 230, 230)
GREEN = (0, 200, 0)
DARK_GREEN = (0, 150, 0)

# Load saved game state or default values
Knowledge, player_state, items = game_save.load_game()
Knowledge_per_click = 1

# Shop Buttons
shop_buttons = {}

# Timers
clock = pygame.time.Clock()

# gif background
class GifAnimation():
    def __init__(self, gif_path):
        image = Image.open(gif_path)
        self.frames = [pygame.image.fromstring(frame.convert("RGBA").tobytes(), frame.size, "RGBA")
                       for frame in ImageSequence.Iterator(image)]
        self.frame_index = 0
        self.size = image.size

    def update(self):
        self.frame_index = (self.frame_index + 1) % len(self.frames)

    def draw(self, screen, position):
        screen.blit(self.frames[self.frame_index], position)

# Load animated gif
gif_anim = GifAnimation("Ryanstuff/main_wallpaper.gif")

# Button Settings
book_button = pygame.Rect(WIDTH // 2 - 50, HEIGHT // 2 - 50, 100, 100)

def draw_book_button():
    pygame.draw.ellipse(screen, (150, 75, 0), book_button)
    click_text = font.render("Click!", True, WHITE)
    screen.blit(click_text, (book_button.x + 15, book_button.y + 35))

def draw_shop():
    y_offset = 100
    shop_buttons.clear()
    for idx, (item_name, item) in enumerate(items.items()):
        button_rect = pygame.Rect(20, y_offset, 360, 80)
        shop_buttons[item_name] = button_rect

        mouse_pos = pygame.mouse.get_pos()
        if button_rect.collidepoint(mouse_pos):
            pygame.draw.rect(screen, LIGHT_GRAY, button_rect)
        else:
            pygame.draw.rect(screen, GRAY, button_rect)

        pygame.draw.rect(screen, BLACK, button_rect, 3)

        item_text = font.render(f"{item_name}", True, BLACK)
        cost_text = font.render(f"Cost: {int(item['cost'])}", True, BLACK)
        owned_text = font.render(f"Owned: {item['owned']}", True, BLACK)

        screen.blit(item_text, (button_rect.x + 10, button_rect.y + 5))
        screen.blit(cost_text, (button_rect.x + 10, button_rect.y + 30))
        screen.blit(owned_text, (button_rect.x + 200, button_rect.y + 30))

        bar_back = pygame.Rect(button_rect.x + 10, button_rect.y + 60, 340, 10)
        pygame.draw.rect(screen, DARK_GREEN, bar_back)

        fill_width = int(340 * item['progress'])
        bar_fill = pygame.Rect(button_rect.x + 10, button_rect.y + 60, fill_width, 10)
        pygame.draw.rect(screen, GREEN, bar_fill)

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
        if item["owned"] > 0:
            item["progress"] += dt / item["speed"]
            if item["progress"] >= 1.0:
                Knowledge += item["cps"] * item["owned"]
                item["progress"] = 0.0

def draw_knowledge_counter():
    cookie_text = font.render(f"Knowledge: {int(Knowledge)}", True, BLACK)
    screen.blit(cookie_text, (20, 20))

def draw():
    gif_anim.update()
    frame = gif_anim.frames[gif_anim.frame_index]
    scaled_frame = pygame.transform.scale(frame, (WIDTH, HEIGHT))
    screen.blit(scaled_frame, (0, 0))

    draw_book_button()
    draw_knowledge_counter()
    draw_shop()

    display_score = font.render(
        f'Knowledge: {round(player_state["score"])} | Rebirths: {player_state["rebirths"]}',
        True, WHITE, BLACK)
    screen.blit(display_score, (10, 5))

# === Main Game Loop ===
while True:
    dt = clock.tick(60) / 1000

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_save.save_game(Knowledge, player_state, items)
            pygame.quit()
            sys.exit()

        if event.type == pygame.MOUSEBUTTONDOWN:
            if book_button.collidepoint(event.pos):
                Knowledge += Knowledge_per_click
                player_state["score"] += Knowledge_per_click
            else:
                handle_shop_click(event.pos)

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:
                if perform_rebirth(player_state):
                    print("Rebirth successful!")
                    Knowledge = 0
                else:
                    print("Not enough knowledge to rebirth.")

            # === SAVE ON 'S' KEY ===
            if event.key == pygame.K_s:
                game_save.save_game(Knowledge, player_state, items)
                print("Game saved manually.")

    update_items(dt)
    draw()
    pygame.display.update()
