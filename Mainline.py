import pygame
import sys
import os
from PIL import Image

# Initialize Pygame
pygame.init()

# Screen settings
WIDTH, HEIGHT = 1080, 720
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Knowledge Clicker")

# Fonts
font = pygame.font.SysFont("Arial", 24)

# Global Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
LIGHT_GRAY = (230, 230, 230)
GREEN = (0, 200, 0)
DARK_GREEN = (0, 150, 0)

# Global Variables
Knowledge = 0
Knowledge_per_click = 1

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

# Items for sale with unique GIFs for each
items = {
    "Cursor": {"cost": 15, "cps": 0.2, "owned": 0, "progress": 0.0, "speed": 2.0, "gif_path": "AdamStuff/assets/gif_0.gif"},
    "Grandma": {"cost": 100, "cps": 1, "owned": 0, "progress": 0.0, "speed": 5.0, "gif_path": "AdamStuff/assets/gif_1.gif"},
}

# Load GIF frames for each item
for item_name, item in items.items():
    item["frames"] = load_gif_frames(item["gif_path"])

# Centre GIF file location
center_gif_path = "AdamStuff/assets/floating_book.gif"
center_gif_frames = load_gif_frames(center_gif_path, scale=(150, 150)) # Book Size

# Shop Buttons
shop_buttons = {}

# Timers
clock = pygame.time.Clock()

# Button Settings (the clickable area)
book_button = pygame.Rect(WIDTH // 2 - 50, HEIGHT // 2 - 50, 100, 100)

def draw_book_button():
    pygame.draw.ellipse(screen, (WHITE), book_button)
    click_text = font.render("Click!", True, WHITE)
    screen.blit(click_text, (book_button.x + 15, book_button.y + 35))

# Drawing the book in the centre of the screen
def draw_center_gif(current_frame_index):
    if center_gif_frames:
        current_frame = center_gif_frames[current_frame_index]
        gif_pos = (WIDTH // 2 - current_frame.get_width() // 2, HEIGHT // 2 - current_frame.get_height() // 2)
        screen.blit(current_frame, gif_pos)

def draw_shop():
    y_offset = 100
    shop_buttons.clear()
    for idx, (item_name, item) in enumerate(items.items()):
        button_rect = pygame.Rect(20, y_offset, 360, 80)
        shop_buttons[item_name] = button_rect
        
        # Highlight box when hover
        mouse_pos = pygame.mouse.get_pos()
        if button_rect.collidepoint(mouse_pos):
            pygame.draw.rect(screen, LIGHT_GRAY, button_rect)
        else:
            pygame.draw.rect(screen, GRAY, button_rect)

        pygame.draw.rect(screen, BLACK, button_rect, 3)

        # Text inside
        item_text = font.render(f"{item_name}", True, BLACK)
        cost_text = font.render(f"Cost: {int(item['cost'])}", True, BLACK)
        owned_text = font.render(f"Owned: {item['owned']}", True, BLACK)

        screen.blit(item_text, (button_rect.x + 10, button_rect.y + 5))
        screen.blit(cost_text, (button_rect.x + 10, button_rect.y + 30))
        screen.blit(owned_text, (button_rect.x + 200, button_rect.y + 30))

        # Progress bar (loading bar)
        if item['owned'] > 0:
            bar_back = pygame.Rect(button_rect.x + 10, button_rect.y + 60, 340, 10)
            pygame.draw.rect(screen, DARK_GREEN, bar_back)

            # Fill based on progress
            fill_width = int(340 * (item['progress']))
            bar_fill = pygame.Rect(button_rect.x + 10, button_rect.y + 60, fill_width, 10)
            pygame.draw.rect(screen, GREEN, bar_fill)

            # Draw looping animation synced with progress
            if 'frames' in item and item['frames']:
                frame_count = len(item['frames'])
                current_frame_index = int(item['progress'] * frame_count) % frame_count
                current_frame = item['frames'][current_frame_index]
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
        item["cost"] *= 1.15  # Cost increase

def update_items(dt):
    global Knowledge
    for item in items.values():
        if item["owned"] > 0:
            item["progress"] += dt / item["speed"]
            if item["progress"] >= 1.0:
                # Add knowledge based on how many you own
                Knowledge += item["cps"] * item["owned"]
                item["progress"] = 0.0

def draw_knowledge_counter():
    cookie_text = font.render(f"Knowledge: {int(Knowledge)}", True, BLACK)
    screen.blit(cookie_text, (20, 20))

def draw():
    screen.fill(WHITE)
    draw_book_button()
    draw_knowledge_counter()
    draw_shop()

    # Drawing the centre gif
    if center_gif_frames:
        current_frame_index = pygame.time.get_ticks() // 100 % len(center_gif_frames)
        draw_center_gif(current_frame_index)

# Main Game Loop
while True:
    dt = clock.tick(60) / 1000  # Delta time in seconds

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            if book_button.collidepoint(event.pos):
                Knowledge += Knowledge_per_click
            else:
                handle_shop_click(event.pos)

    update_items(dt)
    draw()
    pygame.display.update()
