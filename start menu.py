import pygame
import sys
from PIL import Image #pip install pygame pillow

# Initialize
pygame.init()
pygame.mixer.init()
pygame.display.set_caption("Start Menu")

# Wallpaper stuff
GIF_PATH = "AdamStuff/wallpaper.gif"
WIDTH, HEIGHT = 1080, 720
screen = pygame.display.set_mode((WIDTH, HEIGHT))
FPS = 60

# Fonts
FONT = pygame.font.SysFont("Arial", 40)
TITLE_FONT = pygame.font.SysFont("Arial", 80)

# Colours
WHITE = (255, 255, 255)
GRAY = (50, 50, 50)
LIGHT_GRAY = (200, 200, 200)
HIGHLIGHT = (100, 100, 255)
BLACK = (0, 0, 0)

# States
TITLE_TEXT = "Idle Study Game"
music_on = True
fullscreen_on = False
menu_state = "main"

# Title Shadow Settings
TITLE_Y = 150
SHADOW_OFFSET = 4

# Drawing Button
class Button:
    def __init__(self, text, y_pos, callback):
        self.text = text
        self.y_pos = y_pos
        self.rect = pygame.Rect(WIDTH // 2 - 150, y_pos, 300, 60)
        self.callback = callback

    def draw(self, surface, mouse_pos):
        color = HIGHLIGHT if self.rect.collidepoint(mouse_pos) else LIGHT_GRAY
        pygame.draw.rect(surface, color, self.rect, border_radius=10)
        text_surface = FONT.render(self.text, True, GRAY)
        text_rect = text_surface.get_rect(center=self.rect.center)
        surface.blit(text_surface, text_rect)

    def click(self, mouse_pos):
        if self.rect.collidepoint(mouse_pos):
            self.callback()

# Assign Button Functions Here
def start_game():
    global menu_state
    menu_state = "main"

def open_options():
    global menu_state
    menu_state = "options"

def back_to_main():
    global menu_state
    menu_state = "main"

def toggle_music():
    global music_on
    music_on = not music_on
    if music_on:
        pygame.mixer.music.play(-1)
    else:
        pygame.mixer.music.stop()

def toggle_fullscreen():
    global fullscreen_on, screen
    fullscreen_on = not fullscreen_on
    if fullscreen_on:
        screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.FULLSCREEN)
    else:
        screen = pygame.display.set_mode((WIDTH, HEIGHT))

def quit_game():
    pygame.quit()
    sys.exit()

# Loading the GIF Frames
def load_gif_frames(path):
    gif = Image.open(path)
    frames = []
    try:
        while True:
            frame = gif.convert("RGB").resize((WIDTH, HEIGHT))
            surface = pygame.image.fromstring(frame.tobytes(), frame.size, "RGB")
            frames.append(surface)
            gif.seek(gif.tell() + 1)
    except EOFError:
        pass
    return frames

gif_frames = load_gif_frames(GIF_PATH)
current_frame = 0
frame_timer = 0
frame_delay = 100

# Button Sets
main_buttons = [
    Button("Start Game", 300, start_game),
    Button("Options", 390, open_options),
    Button("Quit", 480, quit_game),
]

options_buttons = [
    Button(lambda: f"Music: {'ON' if music_on else 'OFF'}", 300, toggle_music),
    Button(lambda: f"Fullscreen: {'ON' if fullscreen_on else 'OFF'}", 390, toggle_fullscreen),
    Button("Back", 480, back_to_main),
]

# === Render title with shadow ===
def draw_title(surface):
    shadow_surface = TITLE_FONT.render(TITLE_TEXT, True, BLACK)
    shadow_rect = shadow_surface.get_rect(center=(WIDTH // 2 + SHADOW_OFFSET, TITLE_Y + SHADOW_OFFSET))
    surface.blit(shadow_surface, shadow_rect)

    title_surface = TITLE_FONT.render(TITLE_TEXT, True, WHITE)
    title_rect = title_surface.get_rect(center=(WIDTH // 2, TITLE_Y))
    surface.blit(title_surface, title_rect)

# === Main Loop ===
def main():
    global current_frame, frame_timer
    clock = pygame.time.Clock()

    # Optional: load background music
    # pygame.mixer.music.load("background_music.mp3")
    # pygame.mixer.music.play(-1)

    while True:
        dt = clock.tick(FPS)
        mouse_pos = pygame.mouse.get_pos()
        frame_timer += dt

        # Cycle gif
        if frame_timer >= frame_delay:
            current_frame = (current_frame + 1) % len(gif_frames)
            frame_timer = 0

        screen.blit(gif_frames[current_frame], (0, 0))
        draw_title(screen)

        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit_game()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                active_buttons = main_buttons if menu_state == "main" else options_buttons
                for button in active_buttons:
                    button.click(event.pos)

        # Draw buttons
        active_buttons = main_buttons if menu_state == "main" else options_buttons
        for button in active_buttons:
            # If the button text is dynamic (a function), call it
            if callable(button.text):
                button.rect = pygame.Rect(WIDTH // 2 - 150, button.y_pos, 300, 60)
                button_draw_text = button.text()
                temp_surface = pygame.Surface((300, 60), pygame.SRCALPHA)
                pygame.draw.rect(temp_surface, (0, 0, 0, 100), temp_surface.get_rect(), border_radius=10)
                screen.blit(temp_surface, (button.rect.x, button.rect.y))
                text_surface = FONT.render(button_draw_text, True, GRAY)
                text_rect = text_surface.get_rect(center=button.rect.center)
                color = HIGHLIGHT if button.rect.collidepoint(mouse_pos) else LIGHT_GRAY
                pygame.draw.rect(screen, color, button.rect, border_radius=10)
                screen.blit(text_surface, text_rect)
            else:
                button.draw(screen, mouse_pos)

        pygame.display.flip()

if __name__ == "__main__":
    main()
