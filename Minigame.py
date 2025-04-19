#to import pygame into codes, along with some other modules
import pygame
import sys
import os

#pygame initialisation
pygame.init()

#set fps to 60

fps=60

#window building, 800x600
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("IDLEStudy: Beat rhythm")
screen.fill((255,0,0))

#set colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
PURPLE = (70, 50, 200)
BUTTON_COLOR = (100, 200, 100)
TEXT_COLOR = (255, 255, 255)
BG_COLOR = (30, 30, 30)
    
#set fonts
title_font = pygame.font.Font(None,100)
font = pygame.font.Font(None,36)

#set bg if it works
background_image = pygame.image.load("wallpep.jpg")
background_image = pygame.transform.scale(background_image, (screen_width, screen_height))
screen.blit(background_image,(0,0))
#update as of 19/4,it works now

#mainmenu setup
def main_menu():
    menu_text = pygame.font.SysFont("Roboto", 100).render("Beat Rhythm", True, GRAY)
    menu_rect = menu_text.get_rect(center=(400, 100))

    while True:
        

        pos = pygame.mouse.get_pos()

        screen.blit(menu_text, menu_rect)

  
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
           
                    
                    
#this to make sure the game proceeds and do not crash on startup
#not sure how to not have it respond atm
#DONT REMOVE IT
while True:
    pygame.display.update()