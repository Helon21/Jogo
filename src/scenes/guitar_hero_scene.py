import pygame
import sys
import os
import random
import bisect

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from objects.game_objects import GameObject, create_hitbox, update_hitbox, check_collision, SpriteManager, RandomMediaSelector
from entities.note import Note
from entities.effects import AnimatedEffect, FireEffect
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
        self.lanes_start_x = (screen_width - (self.num_lanes * self.lane_width)) // 2.3
        
        self.lane_colors = LANE_COLORS
        
        self.media_selector = RandomMediaSelector(AUDIO_FILES, BACKGROUND_IMAGES)
        self.media_selector.validate_files()
        
        self.sprite_manager = SpriteManager('src/scenes/sprite-sheet-notes/guitarhero spritesheet.png')
        self.setup_sprites()
        
        self.button_sprite_manager = SpriteManager('src/scenes/sprite-sheet-notes/spritesheet-note-buttons.png')
        self.setup_button_sprites()
        
        self.background_path = self.media_selector.select_random_background()
        if self.background_path:
            self.background = pygame.image.load(self.background_path).convert_alpha()
            self.background = pygame.transform.scale(self.background, (screen_width, screen_height))
            print(f"Background selecionado: {os.path.basename(self.background_path)}")
        else:
            self.background = pygame.Surface((screen_width, screen_height))
            self.background.fill(BLACK)
            print("Nenhum background válido encontrado, usando padrão")
        
        self.key_bindings = [
            pygame.K_a,  
            pygame.K_s,  
            pygame.K_d,
            pygame.K_f
        ]
        
        self.button_height = 30
        self.buttons = []
        
        self.button_states = [False] * NUM_LANES
        self.pressed_keys = set()
        
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
        self.music_path = self.media_selector.select_random_audio()
        self.song_playing = False
        self.music_volume = 0.4
        self.in_burst = False
        self.burst_lane = None
        self.burst_notes_left = 0
        self.burst_interval = 0.12
        self.burst_timer = 0
        
        self.multi_lane_spawn = False
        self.multi_lane_notes = []
        self.multi_lane_timer = 0
        self.multi_lane_interval = 0.2
        
        self.error_sound = None
        self.error_sound_timer = 0
        self.error_sound_duration = 0.2
        self.is_playing_error_sound = False
        self.load_error_sound()
        
        self.hit_sound = None
        self.hit_sound_timer = 0
        self.hit_sound_duration = 0.15
        self.is_playing_hit_sound = False
        self.load_hit_sound()
        
        if self.music_path:
            print(f"Música selecionada: {os.path.basename(self.music_path)}")
        else:
            print("Nenhuma música válida encontrada")
    
    def load_error_sound(self):
        try:
            self.error_sound = pygame.mixer.Sound('src/audio/missing-note-guitarhero.mp3')
            self.error_sound.set_volume(0.8)
        except Exception as e:
            print(f'Erro ao carregar som de erro: {e}')
            self.error_sound = None
    
    def load_hit_sound(self):
        try:
            self.hit_sound = pygame.mixer.Sound('src/audio/hit-note.mp3')
            self.hit_sound.set_volume(0.8)
        except Exception as e:
            print(f'Erro ao carregar som de acerto: {e}')
            self.hit_sound = None
    
    def play_error_sound(self):
        if self.error_sound and not self.is_playing_error_sound:
            try:
                self.error_sound.stop()
                self.error_sound.play()
                self.is_playing_error_sound = True
                self.error_sound_timer = 0
            except Exception as e:
                print(f'Erro ao tocar som de erro: {e}')
    
    def play_hit_sound(self):
        if self.hit_sound and not self.is_playing_hit_sound:
            try:
                self.hit_sound.stop()
                self.hit_sound.play()
                self.is_playing_hit_sound = True
                self.hit_sound_timer = 0
            except Exception as e:
                print(f'Erro ao tocar som de acerto: {e}')
    
    def setup_sprites(self):
        self.sprite_manager.add_sprite('green_note', 3, 8, 43, 21)
        self.sprite_manager.add_sprite('red_note', 47, 8, 43, 21)
        self.sprite_manager.add_sprite('yellow_note', 92, 8, 43, 21)
        self.sprite_manager.add_sprite('blue_note', 136, 8, 43, 21)
    
    def setup_button_sprites(self):
        self.button_sprite_manager.add_sprite('red_button_idle', 61, 13, 51, 49)
        self.button_sprite_manager.add_sprite('green_button_idle', 12, 14, 47, 48)
        self.button_sprite_manager.add_sprite('yellow_button_idle', 115, 13, 49, 49)
        self.button_sprite_manager.add_sprite('blue_button_idle', 167, 13, 48, 48)
        
        self.button_sprite_manager.add_sprite('red_button_pressed', 61, 67, 49, 47)
        self.button_sprite_manager.add_sprite('green_button_pressed', 13, 67, 46, 48)
        self.button_sprite_manager.add_sprite('yellow_button_pressed', 115, 68, 48, 47)
        self.button_sprite_manager.add_sprite('blue_button_pressed', 167, 68, 48, 47)
    
    def create_buttons(self):
        button_y = self.screen_height - 100
        
        sprite_names = ['red_button_idle', 'green_button_idle', 'yellow_button_idle', 'blue_button_idle']
        
        for i in range(self.num_lanes):
            x = self.lanes_start_x + (i * self.lane_width)
            
            button = GameObject(
                x + (self.lane_width - 60) // 2,
                button_y,
                60,
                40,
                self.lane_colors[i],
                sprite_name=sprite_names[i],
                sprite_manager=self.button_sprite_manager
            )
            
            button.hitbox = create_hitbox(button)
            self.buttons.append(button)
    
    def spawn_note(self, lane=None):
        if lane is None:
            lane = random.randint(0, self.num_lanes - 1)
        x = self.lanes_start_x + (lane * self.lane_width) + (self.lane_width - 50) // 2
        
        sprite_names = ['red_note', 'green_note', 'yellow_note', 'blue_note']
        
        note = Note(
            x, 0, 50, 30,
            self.lane_colors[lane],
            lane,
            self.note_speed,
            sprite_name=sprite_names[lane],
            sprite_manager=self.sprite_manager
        )
        
        self.notes.append(note)
    
    def create_hit_effect(self, x, y, color):
        lane_index = None
        for i, button in enumerate(self.buttons):
            if abs(x - (button.x + button.width/2)) < self.lane_width/2:
                lane_index = i
                break
        
        if lane_index is not None:
            button = self.buttons[lane_index]
            effect_width = 80
            effect_height = int(effect_width / 0.72)
            fire_x = button.x + (button.width - effect_width) // 2
            fire_y = button.y - effect_height // 1.3
            
            effect = FireEffect(
                fire_x, fire_y,
                effect_width, effect_height,
                0.6
            )
            self.effects.append(effect)
            
            self.play_hit_sound()
    
    def get_current_multiplier(self):
        for multiplier in range(MAX_MULTIPLIER, 0, -1):
            if self.combo >= COMBO_NEEDED[multiplier]:
                return multiplier
        return 1
    
    def set_button_state(self, lane_index, is_pressed):
        if 0 <= lane_index < len(self.buttons):
            self.button_states[lane_index] = is_pressed
            button = self.buttons[lane_index]
            
            color_names = ['red', 'green', 'yellow', 'blue']
            state_suffix = '_pressed' if is_pressed else '_idle'
            sprite_name = f'{color_names[lane_index]}_button{state_suffix}'
            
            button.sprite_name = sprite_name
    
    def update_button_states(self):
        for i, key in enumerate(self.key_bindings):
            is_pressed = key in self.pressed_keys
            self.set_button_state(i, is_pressed)

    def handle_key_press(self, key):
        if key in self.key_bindings:
            self.pressed_keys.add(key)
            
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
                self.play_error_sound()
    
    def handle_key_release(self, key):
        if key in self.key_bindings:
            self.pressed_keys.discard(key)

    def start_song(self):
        if not self.music_loaded and self.music_path:
            try:
                pygame.mixer.music.load(self.music_path)
                pygame.mixer.music.set_volume(self.music_volume)
                pygame.mixer.music.play()
                self.music_loaded = True
                self.song_playing = True
                print(f"Reproduzindo música: {os.path.basename(self.music_path)}")
            except Exception as e:
                print(f'Erro ao carregar música: {e}')
                self.music_path = self.media_selector.select_random_audio()
                if self.music_path:
                    print(f"Tentando música alternativa: {os.path.basename(self.music_path)}")
                    try:
                        pygame.mixer.music.load(self.music_path)
                        pygame.mixer.music.set_volume(self.music_volume)
                        pygame.mixer.music.play()
                        self.music_loaded = True
                        self.song_playing = True
                    except Exception as e2:
                        print(f'Erro ao carregar música alternativa: {e2}')
        self.song_start_time = pygame.time.get_ticks() / 1000.0

    def update(self, dt):
        if self.song_start_time is None:
            self.start_song()
            return
        
        self.note_spawn_timer += dt
        self.difficulty_timer += dt
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
                if random.random() < 0.15:
                    self.in_burst = True
                    self.burst_lane = random.randint(0, self.num_lanes - 1)
                    self.burst_notes_left = random.randint(2, 3)
                    self.burst_timer = 0
                    self.spawn_note(lane=self.burst_lane)
                    self.burst_notes_left -= 1
                elif random.random() < 0.3 and not self.multi_lane_spawn:
                    num_lanes = random.randint(2, 3)
                    available_lanes = list(range(self.num_lanes))
                    random.shuffle(available_lanes)
                    self.multi_lane_spawn = True
                    self.multi_lane_notes = available_lanes[:num_lanes]
                    self.multi_lane_timer = 0
                    self.spawn_note(lane=self.multi_lane_notes.pop(0))
                else:
                    self.spawn_note()
                self.note_spawn_timer = 0

        if self.multi_lane_spawn:
            self.multi_lane_timer += dt
            if self.multi_lane_timer >= self.multi_lane_interval:
                if self.multi_lane_notes:
                    self.spawn_note(lane=self.multi_lane_notes.pop(0))
                    self.multi_lane_timer = 0
                else:
                    self.multi_lane_spawn = False

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
        self.update_button_states()
        
        if self.is_playing_error_sound:
            self.error_sound_timer += dt
            if self.error_sound_timer >= self.error_sound_duration:
                if self.error_sound:
                    self.error_sound.stop()
                self.is_playing_error_sound = False
        
        if self.is_playing_hit_sound:
            self.hit_sound_timer += dt
            if self.hit_sound_timer >= self.hit_sound_duration:
                if self.hit_sound:
                    self.hit_sound.stop()
                self.is_playing_hit_sound = False
        
        for button in self.buttons:
            update_hitbox(button.hitbox)
        for note in self.notes[:]:
            note.update(dt)
            if note.y > self.screen_height:
                if not note.hit:
                    self.combo = 0
                    self.current_multiplier = 1
                    self.play_error_sound()
                self.notes.remove(note)
        for effect in self.effects[:]:
            effect.update(dt)
            if effect.completed:
                self.effects.remove(effect)
    
    def draw(self, surface):
        surface.blit(self.background, (0, 0))
        
        for i in range(self.num_lanes):
            x = self.lanes_start_x + (i * self.lane_width)
            lane_surface = pygame.Surface((self.lane_width, self.screen_height), pygame.SRCALPHA)
            lane_color = (*tuple(c // 3 for c in self.lane_colors[i]), 128)
            lane_surface.fill(lane_color)
            surface.blit(lane_surface, (x, 0))
        
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
        
        if self.music_path:
            music_name = os.path.basename(self.music_path).replace('.mp3', '')
            music_text = self.font.render(f"Música: {music_name}", True, WHITE)
            surface.blit(music_text, (20, 130))
        
        if self.background_path:
            bg_name = os.path.basename(self.background_path).replace('.png', '')
            bg_text = self.font.render(f"Background: {bg_name}", True, WHITE)
            surface.blit(bg_text, (20, 160))
        
        multiplier_color = (255, 255, 0)  
        if self.current_multiplier >= 4:
            multiplier_color = (255, 165, 0) 
        if self.current_multiplier >= 6:
            multiplier_color = (255, 0, 0)
            
        multiplier_text = self.multiplier_font.render(f"{self.current_multiplier}x", True, multiplier_color)
        surface.blit(multiplier_text, (self.screen_width - 100, 20)) 