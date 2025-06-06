import pygame

def init_music():
    pygame.mixer.init()

def play_music(path:str, loop: bool = True):
    pygame.mixer.music.load(path)
    pygame.mixer.music.play(-1 if loop else 0)

def pause_music():
    pygame.mixer.music.pause()

def unpause_music():
    pygame.mixer.music.unpause()

def stop_music():
    pygame.mixer.music.stop()


    