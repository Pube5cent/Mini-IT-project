import pygame
from random import randint

class Particle(pygame.sprite.Sprite):
    def __init__(self, 
                 groups: pygame.sprite.Group, 
                 pos: list[int], 
                 color: tuple[int], 
                 direction: pygame.math.Vector2, 
                 speed: int):
        super().__init__(groups)
        self.pos = pygame.math.Vector2(pos)
        self.direction = direction
        self.speed = speed
        self.color = color

        self.create_surf()

    def create_surf(self):
        self.image = pygame.Surface((4, 4), pygame.SRCALPHA)  # Transparent background
        self.image.fill((0, 0, 0, 0))  # Set transparent background
        pygame.draw.circle(self.image, self.color, (2, 2), 2)  # Draw the circle (particle)
        self.rect = self.image.get_rect(center=(round(self.pos.x), round(self.pos.y)))

    def update(self):
        # Move the particle each frame
        self.pos += self.direction * (self.speed / 60)  # Adjust speed based on framerate 
        self.rect.center = (round(self.pos.x), round(self.pos.y))

class Ripple(pygame.sprite.Sprite):
    def __init__(self, x, color):
        super().__init__()
        self.original_size = randint(20, 60)  # Initial random width
        self.size = self.original_size
        self.image = pygame.Surface((self.size, self.size), pygame.SRCALPHA)
        
        self.alpha = randint(100, 200)  # Start with random transparency
        self.color = color
        
        # Draw a rectangle instead of a circle
        self.image.fill((self.color[0], self.color[1], self.color[2], self.alpha))
        self.rect = self.image.get_rect(center=(x, 0))
        
        self.speed = randint(1, 3)  # Fall speed
        self.fade_rate = 3  # How fast the ripple fades

    def update(self):
        # Move down
        self.rect.y += self.speed
        

        # Fade effect
        self.alpha -= self.fade_rate
        if self.alpha < 0:
            self.alpha = 0

        # Redraw with randomized alpha transparency and size
        self.image.fill((self.color[0], self.color[1], self.color[2], self.alpha))

        

        # Kill when completely transparent
        if self.alpha == 0:
            self.kill()
