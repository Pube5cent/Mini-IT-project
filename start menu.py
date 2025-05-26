import pygame
import sys
import subprocess
from PIL import Image  # pip install pygame pillow

# Initialize
pygame.init()
pygame.mixer.init()
pygame.display.set_caption("Start Menu")

# Wallpaper stuff
GIF_PATH = "AdamStuff/assets/wallpaper.gif"
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
music_on = False # change it later for presentation
fullscreen_on = False
menu_state = "main"

# Title Shadow Settings
TITLE_Y = 150
SHADOW_OFFSET = 4

# Music Stuff
Music_Path = "AdamStuff/assets/AlanWalker.mp3"

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

# Volume Slider
class VolumeSlider:
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.rect = pygame.Rect(x, y, width, height)
        self.handle_rect = pygame.Rect(x, y, 20, height)
        self.dragging = False
        self.volume = pygame.mixer.music.get_volume()
        self.update_handle()

        # Background box like buttons
        self.background_rect = pygame.Rect(x - 10, y - 20, width + 20, height + 60)

    def update_handle(self):
        self.handle_rect.x = self.rect.x + int(self.volume * (self.rect.width - self.handle_rect.width))

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and self.handle_rect.collidepoint(event.pos):
            self.dragging = True
        elif event.type == pygame.MOUSEBUTTONUP:
            self.dragging = False
        elif event.type == pygame.MOUSEMOTION and self.dragging:
            new_x = max(self.rect.x, min(event.pos[0], self.rect.x + self.rect.width - self.handle_rect.width))
            self.handle_rect.x = new_x
            self.volume = (self.handle_rect.x - self.rect.x) / (self.rect.width - self.handle_rect.width)
            pygame.mixer.music.set_volume(self.volume)

    def draw(self, surface):
        # Drawing colour and shapes
        pygame.draw.rect(surface, LIGHT_GRAY, self.background_rect, border_radius=10)
        pygame.draw.rect(surface, GRAY, self.rect)
        pygame.draw.rect(surface, WHITE, self.handle_rect)

        # Draw label
        text = FONT.render(f"Volume: {int(self.volume * 100)}%", True, GRAY)
        text_rect = text.get_rect(center=(self.background_rect.centerx, self.background_rect.top + 25))
        surface.blit(text, text_rect)

# Assign Button Functions
def start_game():
    global menu_state
    menu_state = "game"

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
        pygame.mixer.music.load(Music_Path)
        pygame.mixer.music.play(-1)
        pygame.mixer.music.set_volume(slider.volume)
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

# Load GIF Frames
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

# Buttons
main_buttons = [
    Button("Start Game", 300, start_game),
    Button("Options", 390, open_options),
    Button("Quit", 480, quit_game),
]

options_buttons = [
    Button(lambda: f"Music: {'ON' if music_on else 'OFF'}", 300, toggle_music),
    Button(lambda: f"Fullscreen: {'ON' if fullscreen_on else 'OFF'}", 390, toggle_fullscreen),
    Button("Back", 560, back_to_main),
]

# Slider POSITION____________
slider = VolumeSlider(WIDTH // 2 - 150, 485, 300, 20)

# Title Drawing
def draw_title(surface):
    shadow_surface = TITLE_FONT.render(TITLE_TEXT, True, BLACK)
    shadow_rect = shadow_surface.get_rect(center=(WIDTH // 2 + SHADOW_OFFSET, TITLE_Y + SHADOW_OFFSET))
    surface.blit(shadow_surface, shadow_rect)

    title_surface = TITLE_FONT.render(TITLE_TEXT, True, WHITE)
    title_rect = title_surface.get_rect(center=(WIDTH // 2, TITLE_Y))
    surface.blit(title_surface, title_rect)

# Main Loop
def main():
    global current_frame, frame_timer
    clock = pygame.time.Clock()

    # Load and play music if on
    if music_on:
        pygame.mixer.music.load(Music_Path)
        pygame.mixer.music.set_volume(slider.volume)
        pygame.mixer.music.play(-1)

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

        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit_game()
            elif menu_state == "options":
                slider.handle_event(event)
            if menu_state == "game":
                __name__ = "__game__"
                subprocess.run(["python", "Mainline.py"])
            if event.type == pygame.MOUSEBUTTONDOWN:
                active_buttons = main_buttons if menu_state == "main" else options_buttons
                for button in active_buttons:
                    button.click(event.pos)

        # Draw buttons
        active_buttons = main_buttons if menu_state == "main" else options_buttons
        for button in active_buttons:
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

        # Draw slider in options
        if menu_state == "options":
            slider.draw(screen)

        pygame.display.flip()

if __name__ == "__main__":
    main()
else:
    quit()