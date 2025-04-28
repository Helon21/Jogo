import pygame
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from objects.game_objects import GameObject

class AnimatedEffect(GameObject):
    
    def __init__(self, x, y, width, height, duration=0.5, color=(255, 255, 255)):
        super().__init__(x, y, width, height, color)
        self.duration = duration
        self.current_time = 0
        self.completed = False
    
    def update(self, dt):
        if self.completed:
            return
            
        self.current_time += dt
        if self.current_time >= self.duration:
            self.completed = True
            self.mark_as_hit()
        else:
            progress = self.current_time / self.duration
            self.width = self.width * (1 - progress)
            self.height = self.height * (1 - progress)
            self.x = self.x + (progress * self.width / 2)
            self.y = self.y + (progress * self.height / 2)
            super().update(dt) 