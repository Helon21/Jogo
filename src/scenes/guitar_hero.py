import pygame
import sys
import os
import random


sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from Objects.game_objects import GameObject, create_hitbox, update_hitbox, check_collision
from entities.note import Note
from entities.effects import AnimatedEffect
from config import *

class GuitarHeroScene:
    
    def __init__(self, screen_width, screen_height):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.score = 0
        self.combo = 0
        self.max_combo = 0
        self.current_multiplier = 1
        
        
        self.num_lanes = NUM_LANES
        self.lane_width = LANE_WIDTH
        self.lanes_start_x = (screen_width - (self.num_lanes * self.lane_width)) // 2
        
        
        self.lane_colors = LANE_COLORS
        
        
        self.key_bindings = [
            pygame.K_a,  
            pygame.K_s,  
            pygame.K_d,
            pygame.K_f
        ]
        
        
        self.button_height = 30
        self.buttons = []
        self.create_buttons()
        
        
        self.notes = []
        self.note_speed = NOTE_SPEED  
        self.note_spawn_timer = 0
        self.note_spawn_interval = INITIAL_SPAWN_INTERVAL  
        
        self.effects = []
        
        self.font = pygame.font.SysFont('Arial', 24)
        self.score_font = pygame.font.SysFont('Arial', 36)
        self.multiplier_font = pygame.font.SysFont('Arial', 48)
    
    def create_buttons(self):
        button_y = self.screen_height - 100
        
        for i in range(self.num_lanes):
            x = self.lanes_start_x + (i * self.lane_width)
            button = GameObject(
                x + (self.lane_width - 80) // 2, 
                button_y,
                80,
                self.button_height,
                self.lane_colors[i]
            )
            button.hitbox = create_hitbox(button)
            self.buttons.append(button)
    
    def spawn_note(self):
        lane = random.randint(0, self.num_lanes - 1)
        
        x = self.lanes_start_x + (lane * self.lane_width) + (self.lane_width - 60) // 2
        
        note = Note(
            x, 0, 60, 20, 
            self.lane_colors[lane],
            lane,
            self.note_speed
        )
        
        self.notes.append(note)
    
    def create_hit_effect(self, x, y, color):
        effect = AnimatedEffect(
            x - 40, y - 40,
            80, 80,
            0.3,
            color
        )
        self.effects.append(effect)
    
    def get_current_multiplier(self):
        for multiplier in range(MAX_MULTIPLIER, 0, -1):
            if self.combo >= COMBO_NEEDED[multiplier]:
                return multiplier
        return 1

    def handle_key_press(self, key):
        if key in self.key_bindings:
            lane_index = self.key_bindings.index(key)
            button = self.buttons[lane_index]
            hit = False
            
            for note in self.notes:
                if note.lane == lane_index and not note.hit:
                    if abs(note.y + note.height - button.y) < 30:
                        note.mark_as_hit()
                        hit = True
                        
                        self.combo += 1
                        if self.combo > self.max_combo:
                            self.max_combo = self.combo
                        
                        self.current_multiplier = self.get_current_multiplier()
                        
                        self.score += BASE_SCORE * self.current_multiplier
                        
                        self.create_hit_effect(button.x + button.width/2, button.y, note.color)
                        break
            
            if not hit:
                self.combo = 0
                self.current_multiplier = 1
    
    def update(self, dt):
        self.note_spawn_timer += dt
        if self.note_spawn_timer >= self.note_spawn_interval:
            self.spawn_note()
            self.note_spawn_timer = 0
        
        for button in self.buttons:
            update_hitbox(button.hitbox)
        
        for note in self.notes[:]:
            note.update(dt)
            
            if note.y > self.screen_height:
                if not note.hit:
                    self.combo = 0
                    self.current_multiplier = 1
                self.notes.remove(note)
        
        for effect in self.effects[:]:
            effect.update(dt)
            if effect.completed:
                self.effects.remove(effect)
    
    def draw(self, surface):
        surface.fill(GRAY)
        
        for i in range(self.num_lanes):
            x = self.lanes_start_x + (i * self.lane_width)
            pygame.draw.rect(
                surface,
                tuple(c // 3 for c in self.lane_colors[i]),
                (x, 0, self.lane_width, self.screen_height)
            )
        
        for button in self.buttons:
            button.draw(surface)
        
        for note in self.notes:
            note.draw(surface)

        for effect in self.effects:
            effect.draw(surface)
        
        score_text = self.score_font.render(f"Pontuação: {self.score}", True, WHITE)
        surface.blit(score_text, (20, 20))
        
        combo_text = self.font.render(f"Combo: {self.combo}", True, WHITE)
        surface.blit(combo_text, (20, 70))
        
        max_combo_text = self.font.render(f"Combo Max: {self.max_combo}", True, WHITE)
        surface.blit(max_combo_text, (20, 100))
        
        multiplier_color = (255, 255, 0)  
        if self.current_multiplier >= 4:
            multiplier_color = (255, 165, 0) 
        if self.current_multiplier >= 6:
            multiplier_color = (255, 0, 0)
            
        multiplier_text = self.multiplier_font.render(f"{self.current_multiplier}x", True, multiplier_color)
        surface.blit(multiplier_text, (self.screen_width - 100, 20)) 