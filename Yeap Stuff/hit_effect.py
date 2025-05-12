import pygame
import random
from variables import *

class Particle():
    def __init__(self, start_loc,start_size):
        self.x, self.y = start_loc
        self.size = start_size
        self.remove_flag = False
        self.xdirection = (random.randint(0,1)*2 - 1) *random.randint(1,4)
        self.ydirection = random.randint(-2,2)

    def move(self):
        self.x += self.xdirection
        self.y += self.ydirection

    def draw(self,screen):
        pygame.draw.rect(screen, node_color[change_background_color[0]],
                         [ self.x, self.y, self.size,self.size], border_radius = 2)

    def update(self):
        self.size -= 1
        self.check()

    def check(self):
        if self.size <= 4:
            self.remove_flag = True



def hit_effect(screen,effect_queue):
    #print(effect_queue)
    for effect in effect_queue:
        # draw effects
        effect.move()
        effect.draw(screen)
        effect.update()

        if effect.remove_flag == True:
            effect_queue.remove(effect)

def append_effect(effect_queue, lane):
    for i in range(5):
        effect_queue.append( Particle((line_width * (lane) + line_width // 2, judgement_line - 10), 20) )

