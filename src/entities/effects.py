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
    
    def __init__(self, x, y, width, height, duration=0.6):
        super().__init__(x, y, width, height)
        
        self.fire_sprite_manager = SpriteManager('src/scenes/sprite-sheet-notes/fire-note.png')
        self.setup_fire_sprites()
        
        self.duration = duration
        self.current_time = 0
        self.completed = False
        
        self.animation_stages = 2
        self.stage_duration = 0.2
        self.current_stage = 0
        
        sprite_ratio = 150 / 177
        
        if width / height > sprite_ratio:
            base_height = height
            base_width = height * sprite_ratio
        else:
            base_width = width
            base_height = width / sprite_ratio
        
        self.stage_sizes = [
            (base_width * 0.6, base_height * 0.6),
            (base_width, base_height)
        ]
        
        self.stage_positions = []
        for stage_width, stage_height in self.stage_sizes:
            stage_x = x + (width - stage_width) // 2
            stage_y = y + (height - stage_height) // 2
            self.stage_positions.append((stage_x, stage_y))
        
        self.sprite_name = 'fire_0'
        self.sprite_manager = self.fire_sprite_manager
        self.use_sprite = True
    
    def setup_fire_sprites(self):
        self.fire_sprite_manager.add_sprite('fire_0', 231, 243, 150, 177)
        self.fire_sprite_manager.add_sprite('fire_1', 224, 248, 168, 192)
    
    def update(self, dt):
        if self.completed:
            return
        
        self.current_time += dt
        
        stage_progress = self.current_time / self.stage_duration
        self.current_stage = min(int(stage_progress), self.animation_stages - 1)

        if self.current_stage < len(self.stage_sizes):
            stage_width, stage_height = self.stage_sizes[self.current_stage]
            stage_x, stage_y = self.stage_positions[self.current_stage]
            
            self.width = stage_width
            self.height = stage_height
            self.x = stage_x
            self.y = stage_y
            
            self.sprite_name = f'fire_{self.current_stage}'
        
        if self.current_time >= self.duration:
            self.completed = True
            self.mark_as_hit()
        else:
            super().update(dt) 