import pygame
import sys

pygame.init()

# Screen setup
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)
pygame.display.set_caption("Pause Menu Example")
clock = pygame.time.Clock()

# Font and colors
font = pygame.font.SysFont(None, 36)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
TRANSPARENT_BLACK = (0, 0, 0, 180)
GRAY = (100, 100, 100)

# Game state
paused = False
fullscreen = False
volume_on = True

# Button setup
button_width, button_height = 200, 50
padding = 10

# Helper to draw a button
def draw_button(surface, rect, text):
    pygame.draw.rect(surface, GRAY, rect)
    pygame.draw.rect(surface, WHITE, rect, 2)
    label = font.render(text, True, WHITE)
    label_rect = label.get_rect(center=rect.center)
    surface.blit(label, label_rect)

def toggle_fullscreen():
    global fullscreen, screen
    fullscreen = not fullscreen
    if fullscreen:
        screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
    else:
        screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)

def toggle_volume():
    global volume_on
    volume_on = not volume_on
    pygame.mixer.music.set_volume(1.0 if volume_on else 0.0)

# Create a surface for transparent overlay
overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)

# Dummy background movement (to show paused effect)
rect_x = 0

# Main loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            paused = not paused

        if event.type == pygame.MOUSEBUTTONDOWN and paused:
            mx, my = pygame.mouse.get_pos()

            # Check button clicks
            if fullscreen_button.collidepoint(mx, my):
                toggle_fullscreen()
            elif volume_button.collidepoint(mx, my):
                toggle_volume()
            elif quit_button.collidepoint(mx, my):
                pygame.quit()
                sys.exit()

    # Update game only if not paused
    if not paused:
        rect_x = (rect_x + 2) % WIDTH

    # Draw game
    screen.fill((30, 30, 60))
    pygame.draw.rect(screen, (255, 100, 100), (rect_x, HEIGHT // 2, 50, 50))  # Demo moving object

    # If paused, draw overlay and menu
    if paused:
        overlay.fill(TRANSPARENT_BLACK)
        screen.blit(overlay, (0, 0))

        # Top-right corner positioning
        menu_x = screen.get_width() - button_width - padding
        menu_y = padding

        fullscreen_button = pygame.Rect(menu_x, menu_y, button_width, button_height)
        volume_button = pygame.Rect(menu_x, menu_y + button_height + padding, button_width, button_height)
        quit_button = pygame.Rect(menu_x, menu_y + 2 * (button_height + padding), button_width, button_height)

        draw_button(screen, fullscreen_button, "Toggle Fullscreen")
        draw_button(screen, volume_button, f"Volume: {'On' if volume_on else 'Off'}")
        draw_button(screen, quit_button, "Quit Game")

    pygame.display.flip()
    clock.tick(60)
