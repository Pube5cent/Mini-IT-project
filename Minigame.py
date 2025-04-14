#to import pygame into codes, along with some other modules
import pygame
import sys
import tkinter as tk 
from pygame import mixer

#pygame initialisation
pygame.init()
mixer.init()

#window building, 800x600
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("IDLEStudy: Beat rhythm")


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

#set bg
background_image = pygame.image.load("assets/lofi.jpg")
background_image = pygame.transform.scale(background_image, (screen_width, screen_height))

#button config
button_width = 220
button_height = 40
dropdown_button_width = 400
dropdown_button_height = 40
selectsong_button_width = 400
selectsong_button_height = 40

#dropdown button positions
title_y = 20
button_x = (screen_width - button_width) // 2
button_y = 350
selectsong_button_x = (screen_width - dropdown_button_width) // 2
selectsong_button_y = 270
dropdown_button_x = (screen_width - dropdown_button_width) // 2
dropdown_button_y = 430

#confirmation button
button_box = pygame.Rect(button_x, button_y, button_width, button_height)
button_text = "Confirm and Play"