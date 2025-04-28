import pygame
import sys
import os
import random
import bisect

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from objects.game_objects import GameObject, create_hitbox, update_hitbox, check_collision
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
        self.difficulty_timer = 0
        self.difficulty_interval = DIFFICULTY_INTERVAL
        self.effects = []
        
        self.font = pygame.font.SysFont('Arial', 24)
        self.score_font = pygame.font.SysFont('Arial', 36)
        self.multiplier_font = pygame.font.SysFont('Arial', 48)
        
        self.song_start_time = None
        self.music_loaded = False
        self.music_path = 'src/audio/03_Sonne.mp3'
        self.song_playing = False
        self.in_burst = False
        self.burst_lane = None
        self.burst_notes_left = 0
        self.burst_interval = 0.12
        self.burst_timer = 0
    
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
    
    def spawn_note(self, lane=None):
        if lane is None:
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

    def start_song(self):
        if not self.music_loaded:
            try:
                pygame.mixer.music.load(self.music_path)
                pygame.mixer.music.play()
                self.music_loaded = True
                self.song_playing = True
            except Exception as e:
                print(f'Erro ao carregar música: {e}')
        self.song_start_time = pygame.time.get_ticks() / 1000.0

    def update(self, dt):
        if self.song_start_time is None:
            self.start_song()
            return
        
        self.note_spawn_timer += dt
        self.difficulty_timer += dt
        # Lógica de bursts/sequências
        if self.in_burst:
            self.burst_timer += dt
            if self.burst_timer >= self.burst_interval:
                self.spawn_note(lane=self.burst_lane)
                self.burst_notes_left -= 1
                self.burst_timer = 0
                if self.burst_notes_left <= 0:
                    self.in_burst = False
        else:
            if self.note_spawn_timer >= self.note_spawn_interval:
                # 15% de chance de iniciar um burst
                if random.random() < 0.15:
                    self.in_burst = True
                    self.burst_lane = random.randint(0, self.num_lanes - 1)
                    self.burst_notes_left = random.randint(2, 5)
                    self.burst_timer = 0
                    self.spawn_note(lane=self.burst_lane)  # Primeira nota do burst
                    self.burst_notes_left -= 1
                else:
                    self.spawn_note()
                self.note_spawn_timer = 0
        if self.difficulty_timer >= DIFFICULTY_INTERVAL:
            self.note_spawn_interval = max(
                MIN_SPAWN_INTERVAL,
                self.note_spawn_interval - SPAWN_INTERVAL_INCREASE
            )
            self.note_speed = min(
                MAX_NOTE_SPEED,
                self.note_speed + NOTE_SPEED_INCREASE
            )
            self.difficulty_timer = 0
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