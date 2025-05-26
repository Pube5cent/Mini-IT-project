import pygame
import sys
import random
import Shared_state

pygame.init()

WIDTH, HEIGHT = 400, 300
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Test Mini-Game")

font = pygame.font.SysFont(None, 36)
button_rect = pygame.Rect(150, 120, 100, 50)
clock = pygame.time.Clock()

def draw_button():
    pygame.draw.rect(screen, (0, 200, 0), button_rect)
    text = font.render("Win!", True, (255, 255, 255))
    text_rect = text.get_rect(center=button_rect.center)
    screen.blit(text, text_rect)

def run_mini_game():
    running = True
    while running:
        screen.fill((30, 30, 30))
        draw_button()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                if button_rect.collidepoint(event.pos):
                    print("Mini-game won! Activating upgrade...")
                    Shared_state.upgrade_triggered = True
                    Shared_state.upgrade_type = random.choice(["fast_click", "bonus_click"])            

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    run_mini_game()
