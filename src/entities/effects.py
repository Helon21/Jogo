import pygame
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from objects.game_objects import GameObject, SpriteManager

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


class FireEffect(GameObject):
    
    def __init__(self, x, y, width, height, duration=0.8):
        super().__init__(x, y, width, height)
        
        self.fire_sprite_manager = SpriteManager('src/scenes/sprite-sheet-notes/fire-note.png')
        self.setup_fire_sprites()
        
        self.duration = duration
        self.current_time = 0
        self.completed = False
        
        self.frame_duration = 0.2
        self.current_frame = 0
        self.total_frames = 9
        
        self.sprite_name = 'fire_0'
        self.sprite_manager = self.fire_sprite_manager
        self.use_sprite = True
    
    def setup_fire_sprites(self):
        self.fire_sprite_manager.add_sprite('fire_0', 224, 248, 168, 192)
    
    def update(self, dt):
        if self.completed:
            return
        
        self.current_time += dt
        
        self.sprite_name = 'fire_0'
        
        if self.current_time >= self.duration:
            self.completed = True
            self.mark_as_hit()
        else:
            super().update(dt) 