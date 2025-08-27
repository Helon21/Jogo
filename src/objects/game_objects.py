import pygame
import random
import os

class RandomMediaSelector:
    def __init__(self, audio_files, background_images):
        self.audio_files = audio_files
        self.background_images = background_images
        self.current_audio = None
        self.current_background = None
        
    def select_random_audio(self):
        if self.audio_files:
            self.current_audio = random.choice(self.audio_files)
            return self.current_audio
        return None
    
    def select_random_background(self):
        if self.background_images:
            self.current_background = random.choice(self.background_images)
            return self.current_background
        return None
    
    def get_current_audio(self):
        """Retorna a música atualmente selecionada"""
        return self.current_audio
    
    def get_current_background(self):
        """Retorna o background atualmente selecionado"""
        return self.current_background
    
    def validate_files(self):
        """Valida se os arquivos existem e retorna apenas os válidos"""
        valid_audio = []
        valid_backgrounds = []
        
        for audio_file in self.audio_files:
            if os.path.exists(audio_file):
                valid_audio.append(audio_file)
            else:
                print(f"Arquivo de áudio não encontrado: {audio_file}")
        
        for bg_file in self.background_images:
            if os.path.exists(bg_file):
                valid_backgrounds.append(bg_file)
            else:
                print(f"Arquivo de background não encontrado: {bg_file}")
        
        self.audio_files = valid_audio
        self.background_images = valid_backgrounds
        
        return len(valid_audio) > 0, len(valid_backgrounds) > 0

class SpriteManager:
    def __init__(self, spritesheet_path):
        self.spritesheet = pygame.image.load(spritesheet_path).convert_alpha()
        self.sprites = {}
    
    def add_sprite(self, name, x, y, width, height):
        sprite_surface = pygame.Surface((width, height), pygame.SRCALPHA)
        sprite_surface.blit(self.spritesheet, (0, 0), (x, y, width, height))
        self.sprites[name] = sprite_surface
    
    def get_sprite(self, name):
        return self.sprites.get(name)

class GameObject:
    
    def __init__(self, x, y, width, height, color=(255, 255, 255), sprite_name=None, sprite_manager=None):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color
        self.rect = pygame.Rect(x, y, width, height)
        self.visible = True
        self.active = True
        self.hitbox = self.create_hitbox()
        self.hit = False
        
        self.sprite_name = sprite_name
        self.sprite_manager = sprite_manager
        self.use_sprite = sprite_name is not None and sprite_manager is not None
    
    def update(self, dt):
        self.rect.x = self.x
        self.rect.y = self.y
        self.update_hitbox()
    
    def draw(self, surface):
        if self.visible:
            if self.use_sprite and self.sprite_name:
                sprite = self.sprite_manager.get_sprite(self.sprite_name)
                if sprite:
                    scaled_sprite = pygame.transform.scale(sprite, (self.width, self.height))
                    surface.blit(scaled_sprite, (self.x, self.y))
                else:
                    pygame.draw.rect(surface, self.color, self.rect)
            else:
                pygame.draw.rect(surface, self.color, self.rect)
    
    def set_position(self, x, y):
        self.x = x
        self.y = y
        self.rect.x = x
        self.rect.y = y
        self.update_hitbox()

    def mark_as_hit(self):
        self.hit = True
        self.active = False
        self.visible = False

    def create_hitbox(self, width=None, height=None, offset_x=0, offset_y=0):
        width = width if width is not None else self.width
        height = height if height is not None else self.height
        hitbox = {
            'parent': self,
            'width': width,
            'height': height,
            'offset_x': offset_x,
            'offset_y': offset_y,
            'rect': pygame.Rect(
                self.x + offset_x,
                self.y + offset_y,
                width,
                height
            )
        }
        return hitbox

    def update_hitbox(self):
        self.hitbox['rect'].x = self.x + self.hitbox['offset_x']
        self.hitbox['rect'].y = self.y + self.hitbox['offset_y']

    def check_collision(self, other_hitbox):
        return self.hitbox['rect'].colliderect(other_hitbox['rect'])

    def draw_hitbox(self, surface, color=(255, 0, 0)):
        pygame.draw.rect(surface, color, self.hitbox['rect'], 1)


def create_hitbox(parent, width=None, height=None, offset_x=0, offset_y=0):
    
    width = width if width is not None else parent.width
    height = height if height is not None else parent.height

    hitbox = {
        'parent': parent,
        'width': width,
        'height': height,
        'offset_x': offset_x,
        'offset_y': offset_y,
        'rect': pygame.Rect(
            parent.x + offset_x,
            parent.y + offset_y,
            width,
            height
        )
    }
    
    return hitbox


def update_hitbox(hitbox):
    hitbox['rect'].x = hitbox['parent'].x + hitbox['offset_x']
    hitbox['rect'].y = hitbox['parent'].y + hitbox['offset_y']


def check_collision(hitbox1, hitbox2):
    return hitbox1['rect'].colliderect(hitbox2['rect'])


def draw_hitbox(hitbox, surface, color=(255, 0, 0)):
    pygame.draw.rect(surface, color, hitbox['rect'], 1)
