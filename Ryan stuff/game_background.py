import pygame
from PIL import Image, ImageSequence

class GifAnimation():
    def __init__(self, gif_path):
        image = Image.open(gif_path)
        self.frames = [pygame.image.fromstring(frame.convert("RGBA").tobytes(), frame.size, "RGBA")
                       for frame in ImageSequence.Iterator(image)]
        self.frame_index = 0
        self.size = image.size

    def update(self):
        self.frame_index = (self.frame_index + 1) % len(self.frames)

    def draw(self, screen, position):
        screen.blit(self.frames[self.frame_index], position)