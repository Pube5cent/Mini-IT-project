#to import pygame into codes
import pygame

#this will be where to put pygame.init if needed so leave it blank first 
pygame.init()

running=True
while running:
    #user input
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

#set width and height of window
    WIDTH = 800
    HEIGHT = 600
    WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))
    DRAW_SCREEN = pygame.Surface((WIDTH,HEIGHT))
#set bg
    BACKGROUND_COLOR=(255,255,0)
    DRAW_SCREEN.fill(BACKGROUND_COLOR)
    
    
    
    
    
