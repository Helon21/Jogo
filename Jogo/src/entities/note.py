import pygame
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

<<<<<<< HEAD
from world.objects import GameObject, create_hitbox, update_hitbox
=======
from src.world.game_object import GameObject, create_hitbox, update_hitbox
>>>>>>> 6409d99 (update game ideia)

class Note(GameObject):
    
    def __init__(self, x, y, width, height, color, lane, speed):
        super().__init__(x, y, width, height, color)
        self.lane = lane
        self.speed = speed
        self.hitbox = create_hitbox(self)
        self.hit = False
    
    def update(self, dt):
        if not self.hit and self.active:
            self.y += self.speed * dt
            super().update(dt)
            update_hitbox(self.hitbox)
    
    def mark_as_hit(self):
        self.hit = True
        self.active = False
        self.visible = False 