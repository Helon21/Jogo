import pygame
import sys
import os
import random
from PIL import Image, ImageSequence

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from objects.game_objects import GameObject, create_hitbox, update_hitbox
from config import *

class GIFPlayer:
    def __init__(self, gif_path, max_width=300, max_height=300):
        self.gif_path = gif_path
        self.max_width = max_width
        self.max_height = max_height
        self.frames = []
        self.current_frame = 0
        self.frame_timer = 0
        self.frame_durations = []
        self.loaded = False
        
        try:
            self.load_gif()
        except Exception as e:
            print(f"Erro ao carregar GIF: {e}")
            self.loaded = False
    
    def load_gif(self):
        try:
            pil_image = Image.open(self.gif_path)
            
            frames = []
            durations = []
            
            for frame in ImageSequence.Iterator(pil_image):
                frame_rgba = frame.convert('RGBA')
                frame_data = frame_rgba.tobytes()
                frame_size = frame_rgba.size
                
                pygame_frame = pygame.image.fromstring(frame_data, frame_size, 'RGBA')
                
                original_width, original_height = pygame_frame.get_size()
                scale_factor = min(self.max_width / original_width, self.max_height / original_height)
                new_width = int(original_width * scale_factor)
                new_height = int(original_height * scale_factor)
                
                resized_frame = pygame.transform.scale(pygame_frame, (new_width, new_height))
                frames.append(resized_frame)
                
                duration = frame.info.get('duration', 100)
                durations.append(duration / 1000.0)
            
            self.frames = frames
            self.frame_durations = durations
            
            if self.frames:
                self.loaded = True
                print(f"GIF carregado com sucesso: {self.gif_path}")
                print(f"Total de frames: {len(self.frames)}")
            else:
                print(f"Nenhum frame encontrado no GIF: {self.gif_path}")
                self.loaded = False
            
        except Exception as e:
            print(f"Erro ao carregar GIF {self.gif_path}: {e}")
            self.loaded = False
    
    def update(self, dt):
        if not self.loaded or not self.frames:
            return
        
        current_duration = self.frame_durations[self.current_frame] if self.current_frame < len(self.frame_durations) else 0.1
        
        self.frame_timer += dt
        if self.frame_timer >= current_duration:
            self.frame_timer = 0
            self.current_frame = (self.current_frame + 1) % len(self.frames)
    
    def draw(self, surface, x, y):
        if not self.loaded or not self.frames:
            return
        
        frame = self.frames[self.current_frame]
        surface.blit(frame, (x, y))

class CreditsButton(GameObject):
    def __init__(self, x, y, width, height, text, color, hover_color, font):
        super().__init__(x, y, width, height, color)
        self.text = text
        self.hover_color = hover_color
        self.original_color = color
        self.font = font
        self.is_hovered = False
        self.hitbox = create_hitbox(self)
        
    def update(self, dt):
        super().update(dt)
        
    def draw(self, surface):
        current_color = self.hover_color if self.is_hovered else self.original_color
        
        shadow_rect = pygame.Rect(self.rect.x + 2, self.rect.y + 2, self.rect.width, self.rect.height)
        pygame.draw.rect(surface, BLACK, shadow_rect)
        
        pygame.draw.rect(surface, current_color, self.rect)
        pygame.draw.rect(surface, WHITE, self.rect, 3)
        
        text_shadow = self.font.render(self.text, True, BLACK)
        shadow_rect = text_shadow.get_rect(center=(self.rect.centerx + 1, self.rect.centery + 1))
        surface.blit(text_shadow, shadow_rect)
        
        text_surface = self.font.render(self.text, True, WHITE)
        text_rect = text_surface.get_rect(center=self.rect.center)
        surface.blit(text_surface, text_rect)
    
    def check_hover(self, mouse_pos):
        self.is_hovered = self.rect.collidepoint(mouse_pos)
        return self.is_hovered

class CreditsScene:
    def __init__(self, screen_width, screen_height):
        self.screen_width = screen_width
        self.screen_height = screen_height
        
        self.title_font = pygame.font.SysFont('Arial', 48, bold=True)
        self.subtitle_font = pygame.font.SysFont('Arial', 32, bold=True)
        self.text_font = pygame.font.SysFont('Arial', 24)
        self.button_font = pygame.font.SysFont('Arial', 28)
        
        try:
            self.background = pygame.image.load('src/scenes/spritesheet-background/albedo-shalttear-menu.png').convert_alpha()
            self.background = pygame.transform.scale(self.background, (screen_width, screen_height))
            print("Background dos créditos carregado: albedo-shalttear-menu.png")
        except Exception as e:
            print(f"Erro ao carregar background dos créditos: {e}")
            self.background = pygame.Surface((screen_width, screen_height))
            self.background.fill(BLACK)
        
        self.credits_texts = [
            ("GUITAR HERO", self.title_font, WHITE),
            ("ANIME EDITION", self.title_font, WHITE),
            ("", self.text_font, WHITE),
            ("Criado utilizando Python e Pygame", self.text_font, WHITE),
            ("", self.text_font, WHITE),
            ("Orientado pelo Professor Eduardo", self.subtitle_font, YELLOW),
            ("", self.text_font, WHITE),
            ("Criado por Helon Xavier", self.subtitle_font, YELLOW),
            ("", self.text_font, WHITE),
            ("", self.text_font, WHITE),
            ("Obrigado por jogar!", self.subtitle_font, GREEN),
            ("", self.text_font, WHITE),
            ("", self.text_font, WHITE)
        ]
        
        gif_path = 'src/scenes/gifs/chika-chika-dance.gif'
        self.chika_gif = GIFPlayer(gif_path, max_width=250, max_height=250)
        
        button_width = 200
        button_height = 50
        self.back_button = CreditsButton(
            screen_width // 2 - button_width // 2,
            screen_height - 100,
            button_width,
            button_height,
            "VOLTAR",
            BLUE,
            (0, 150, 255),
            self.button_font
        )
        
        self.scroll_speed = 50
        self.start_y = screen_height + 50
        self.current_y = self.start_y
        self.final_y = -len(self.credits_texts) * 50 - 100
        
        self.is_scrolling = True
        self.scroll_pause_time = 0
        self.scroll_pause_duration = 2.0
        
        self.auto_return_timer = 0
        self.auto_return_duration = 0.1
        self.has_finished_scrolling = False
        
    def handle_key_press(self, key):
        if key == pygame.K_RETURN or key == pygame.K_KP_ENTER or key == pygame.K_SPACE:
            return "return_to_menu"
        elif key == pygame.K_ESCAPE:
            return "return_to_menu"
        return None
    
    def handle_mouse_click(self, mouse_pos):
        if self.back_button.rect.collidepoint(mouse_pos):
            return "return_to_menu"
        return None
    
    def update(self, dt):
        self.back_button.update(dt)
        
        self.chika_gif.update(dt)
        
        mouse_pos = pygame.mouse.get_pos()
        self.back_button.check_hover(mouse_pos)
        
        if self.is_scrolling:
            self.current_y -= self.scroll_speed * dt
            
            if self.current_y <= self.final_y:
                self.current_y = self.final_y
                self.is_scrolling = False
                self.scroll_pause_time = 0
                self.has_finished_scrolling = True
        else:
            self.scroll_pause_time += dt
            if self.scroll_pause_time >= self.scroll_pause_duration:
                self.is_scrolling = True
                self.current_y = self.start_y
        
        if self.has_finished_scrolling and not self.is_scrolling:
            self.auto_return_timer += dt
            if self.auto_return_timer >= self.auto_return_duration:
                return "return_to_menu"
        
        return None
    
    def draw(self, surface):
        surface.blit(self.background, (0, 0))
        
        overlay = pygame.Surface((self.screen_width, self.screen_height), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 120))
        surface.blit(overlay, (0, 0))
        
        y_offset = self.current_y
        for i, (text, font, color) in enumerate(self.credits_texts):
            if text: 

                text_shadow = font.render(text, True, BLACK)
                shadow_rect = text_shadow.get_rect(center=(self.screen_width // 2 + 2, y_offset + 2))
                surface.blit(text_shadow, shadow_rect)
                
                text_surface = font.render(text, True, color)
                text_rect = text_surface.get_rect(center=(self.screen_width // 2, y_offset))
                surface.blit(text_surface, text_rect)
            
            if i == len(self.credits_texts) - 1 and self.chika_gif.loaded:
                gif_y = y_offset + 30
                gif_x = self.screen_width // 2 - 125
                self.chika_gif.draw(surface, gif_x, gif_y)
            
            y_offset += 50

        if not self.is_scrolling and self.scroll_pause_time >= self.scroll_pause_duration:
            self.back_button.draw(surface)
            
            instruction_text = self.text_font.render("Pressione ESPAÇO ou clique em VOLTAR", True, WHITE)
            instruction_shadow = self.text_font.render("Pressione ESPAÇO ou clique em VOLTAR", True, BLACK)
            
            instruction_rect = instruction_text.get_rect(center=(self.screen_width // 2, self.back_button.rect.y - 30))
            shadow_rect = instruction_shadow.get_rect(center=(self.screen_width // 2 + 1, self.back_button.rect.y - 29))
            
            surface.blit(instruction_shadow, shadow_rect)
            surface.blit(instruction_text, instruction_rect)
            
            if self.has_finished_scrolling:
                remaining_time = max(0, self.auto_return_duration - self.auto_return_timer)
                countdown_text = f"Voltando ao menu em {remaining_time:.1f}s"
                countdown_surface = self.text_font.render(countdown_text, True, YELLOW)
                countdown_shadow = self.text_font.render(countdown_text, True, BLACK)
                
                countdown_rect = countdown_surface.get_rect(center=(self.screen_width // 2, self.back_button.rect.y + 70))
                countdown_shadow_rect = countdown_shadow.get_rect(center=(self.screen_width // 2 + 1, self.back_button.rect.y + 71))
                
                surface.blit(countdown_shadow_rect, countdown_shadow_rect)
                surface.blit(countdown_surface, countdown_rect)
