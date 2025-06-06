import pygame
import time

pygame.init()

# Screen settings
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Knowledge Clicker")

font = pygame.font.SysFont(None, 30)
clock = pygame.time.Clock()

# Game values
score = 0
click_value = 1
auto_click_rate = 1
last_auto_click_time = time.time()

# Upgrade system
active_upgrade = None
upgrade_end_time = 0

# Upgrade mapping per mini-game
MINIGAME_UPGRADES = {
    1: "Click Bonus",
    2: "Auto Click"
}

def apply_upgrade(upgrade_type):
    global active_upgrade, upgrade_end_time, click_value, auto_click_rate
    active_upgrade = upgrade_type
    upgrade_end_time = time.time() + 30  # Upgrade lasts 30 seconds

    if upgrade_type == "Click Bonus":
        click_value += 2
    elif upgrade_type == "Auto Click":
        auto_click_rate += 3

def remove_upgrade():
    global active_upgrade, click_value, auto_click_rate
    if active_upgrade == "Click Bonus":
        click_value -= 2
    elif active_upgrade == "Auto Click":
        auto_click_rate -= 3
    active_upgrade = None

def reward_upgrade(minigame_id):
    if minigame_id in MINIGAME_UPGRADES:
        upgrade_type = MINIGAME_UPGRADES[minigame_id]
        apply_upgrade(upgrade_type)

def draw_upgrade_status():
    if active_upgrade:
        remaining = int(upgrade_end_time - time.time())
        upgrade_text = f"{active_upgrade} ({remaining}s)"
        text_surf = font.render(upgrade_text, True, (255, 215, 0))
        screen.blit(text_surf, (WIDTH - text_surf.get_width() - 80, 10))  # leave space for pause

def auto_click():
    global score
    now = time.time()
    if now - last_auto_click_time >= 1:
        score += auto_click_rate
        return now
    return last_auto_click_time

def draw_pause_button():
    pygame.draw.rect(screen, (200, 200, 200), (WIDTH - 70, 10, 60, 30))
    pause_text = font.render("Pause", True, (0, 0, 0))
    screen.blit(pause_text, (WIDTH - 60, 15))

def draw_score():
    score_text = font.render(f"Score: {score}", True, (255, 255, 255))
    screen.blit(score_text, (10, 10))

# TEMP: Simulate minigame completion for testing
def simulate_minigame_completion():
    reward_upgrade(minigame_id=1)  # Change to 2 for minigame 2

simulate_minigame_completion()  # Trigger upgrade manually for testing

# Game loop
running = True
while running:
    screen.fill((30, 30, 30))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            # Click to add points
            score += click_value

    draw_score()
    draw_upgrade_status()
    draw_pause_button()

    # Handle upgrade expiration
    if active_upgrade and time.time() >= upgrade_end_time:
        remove_upgrade()

    # Handle auto click
    last_auto_click_time = auto_click()

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
