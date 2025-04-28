import pygame
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from objects.game_objects import GameObject, create_hitbox, update_hitbox

class Note(GameObject):
    
    def __init__(self, x, y, width, height, color, lane, speed, duration=0):
        super().__init__(x, y, width, height, color)
        self.lane = lane
        self.speed = speed
        self.duration = duration
    
    def update(self, dt):
        if not self.hit and self.active:
            self.y += self.speed * dt
            super().update(dt)