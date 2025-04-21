import pygame
pygame.init

WIDTH = 500
HEIGHT = 500
fps = 60
timer = pygame.time.Clock()
screen = pygame.display.set_mode([WIDTH,  HEIGHT])

run = True
while run:
    screen.fill('white')
    timer.tick(fps)
    mouse_position = pygame.mouse.get_pos()
    pygame.draw.circle(screen, 'red', mouse_position, 10)

    left_clicked = pygame.mouse.get_pressed()[0]

    for event in pygame.event.get():
        if event.type == pygame.quit:
            run = False

    pygame.display.flip()
pygame.quit()