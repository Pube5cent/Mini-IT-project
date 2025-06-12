import pygame
import os
import math
import time

pygame.init()
screen = pygame.display.set_mode((800, 600))
clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 24)

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
for i, ud in enumerate(upgrade_defs):
    upgrades.append({
        "level": 0,
        "progress": 0.0,
        "last_tick": time.time(),
        "gif": None,  # Placeholder for animation
        "frames": [],
        "frame_index": 0,
        "name": ud["name"],
        "base_cost": ud["base_cost"],
        "base_rate": ud["base_rate"],
        "base_interval": ud["base_interval"]
    })

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
knowledge = 1000
scroll_y = 0
scroll_speed = 20
upgrade_rects = []
hovered_upgrade = None

# Calculate cost

def get_cost(base, level):
    return int(base * (1.15 ** level))

# Upgrade effect

def get_knowledge_per_tick(base, level):
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
        y = start_y + idx * 70
        rect = pygame.Rect(20, y, 270, 60)
        upgrade_rects.append((rect, idx))

        pygame.draw.rect(screen, (50, 50, 100), rect, border_radius=8)
        screen.blit(upg["gif"], (rect.x + 10, rect.y + 10))

        level = upg["level"]
        cost = get_cost(upg["base_cost"], level)
        name = f"{upg['name']} ({level}/{UPGRADE_CAP})"
        cost_text = f"Cost: {cost}"

        screen.blit(font.render(name, True, (255, 255, 255)), (rect.x + 60, rect.y + 5))
        screen.blit(font.render(cost_text, True, (200, 200, 200)), (rect.x + 60, rect.y + 25))

        # Progress bar background
        pygame.draw.rect(screen, (80, 80, 80), (rect.x + 60, rect.y + 45, 180, 10), border_radius=5)

        # Progress bar fill
        pygame.draw.rect(screen, (0, 220, 0), (rect.x + 60, rect.y + 45, int(180 * upg["progress"]), 10), border_radius=5)


        if rect.collidepoint(mouse_pos):
            hovered_upgrade = idx

# Tooltip

def draw_tooltip():
    if hovered_upgrade is not None:
        upg = upgrades[hovered_upgrade]
        level = upg["level"]
        rate = get_knowledge_per_tick(upg["base_rate"], level)
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
    global knowledge
    now = time.time()
    for upg in upgrades:
        if upg["level"] == 0:
            continue
        interval = get_interval(upg["base_interval"], upg["level"])
        elapsed = now - upg["last_tick"]
        upg["progress"] = min(elapsed / interval, 1.0)
        if elapsed >= interval:
            gain = get_knowledge_per_tick(upg["base_rate"], upg["level"])
            knowledge += gain
            upg["last_tick"] = now
            upg["progress"] = 0.0

# Handle click

def handle_click(pos):
    global knowledge
    for rect, idx in upgrade_rects:
        if rect.collidepoint(pos):
            upg = upgrades[idx]
            if upg["level"] >= UPGRADE_CAP:
                return
            cost = get_cost(upg["base_cost"], upg["level"])
            if knowledge >= cost:
                knowledge -= cost
                upg["level"] += 1
                upg["last_tick"] = time.time()
                # Flash effect can be added here

# Main loop
running = True
while running:
    screen.fill((30, 30, 30))
    screen.blit(font.render(f"Knowledge: {int(knowledge)}", True, (255, 255, 255)), (20, 20))
    draw_upgrades()
    draw_tooltip()
    update_upgrade_progress()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                handle_click(event.pos)
            elif event.button == 4:
                scroll_y = min(scroll_y + scroll_speed, 0)
            elif event.button == 5:
                max_scroll = max(0, len(upgrades) * 70 - 400)
                scroll_y = max(scroll_y - scroll_speed, -max_scroll)
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                scroll_y = min(scroll_y + scroll_speed, 0)
            elif event.key == pygame.K_DOWN:
                max_scroll = max(0, len(upgrades) * 70 - 400)
                scroll_y = max(scroll_y - scroll_speed, -max_scroll)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
