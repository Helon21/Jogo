import pygame
import sys
import os
import random

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from objects.game_objects import GameObject, create_hitbox, update_hitbox
from config import *

class MenuButton(GameObject):
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

class MusicSelector:
    def __init__(self, x, y, width, height, audio_files, font):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.audio_files = audio_files
        self.font = font
        self.current_index = 0
        self.visible_files = []
        self.max_visible = 6
        self.scroll_offset = 0
        
        self.valid_files = []
        for audio_file in audio_files:
            if os.path.exists(audio_file):
                self.valid_files.append(audio_file)
        
        self.update_visible_files()
    
    def update_visible_files(self):
        start_idx = self.scroll_offset
        end_idx = min(start_idx + self.max_visible, len(self.valid_files))
        self.visible_files = self.valid_files[start_idx:end_idx]
    
    def scroll_up(self):
        if self.current_index > 0:
            self.current_index -= 1
        elif self.scroll_offset > 0:
            self.scroll_offset -= 1
            self.update_visible_files()
    
    def scroll_down(self):
        if self.current_index < len(self.visible_files) - 1:
            self.current_index += 1
        elif self.scroll_offset + self.max_visible < len(self.valid_files):
            self.scroll_offset += 1
            self.update_visible_files()
            if self.current_index >= len(self.visible_files):
                self.current_index = len(self.visible_files) - 1
    
    def get_selected_music(self):
        if self.valid_files and self.visible_files:
            actual_index = self.scroll_offset + self.current_index
            if actual_index < len(self.valid_files):
                return self.valid_files[actual_index]
        return None
    
    def draw(self, surface):
        shadow_rect = pygame.Rect(self.x + 2, self.y + 2, self.width, self.height)
        pygame.draw.rect(surface, BLACK, shadow_rect)
        
        selector_rect = pygame.Rect(self.x, self.y, self.width, self.height)
        pygame.draw.rect(surface, GRAY, selector_rect)
        pygame.draw.rect(surface, WHITE, selector_rect, 3)
        
        title_shadow = self.font.render("Escolha uma Música:", True, BLACK)
        surface.blit(title_shadow, (self.x + 11, self.y + 11))
        
        title_text = self.font.render("Escolha uma Música:", True, WHITE)
        surface.blit(title_text, (self.x + 10, self.y + 10))
        
        y_offset = 40
        item_height = 25
        
        for i, music_file in enumerate(self.visible_files):
            music_name = os.path.basename(music_file).replace('.mp3', '')
            if len(music_name) > 35:
                music_name = music_name[:32] + "..."
            
            if i == self.current_index:
                highlight_rect = pygame.Rect(self.x + 5, self.y + y_offset - 2, self.width - 10, item_height)
                pygame.draw.rect(surface, BLUE, highlight_rect)
            
            music_number = f"{self.scroll_offset + i + 1:2d}."
            number_shadow = self.font.render(music_number, True, BLACK)
            surface.blit(number_shadow, (self.x + 11, self.y + y_offset + 1))
            
            number_text = self.font.render(music_number, True, WHITE)
            surface.blit(number_text, (self.x + 10, self.y + y_offset))
            
            music_shadow = self.font.render(music_name, True, BLACK)
            surface.blit(music_shadow, (self.x + 51, self.y + y_offset + 1))
            
            music_text = self.font.render(music_name, True, WHITE)
            surface.blit(music_text, (self.x + 50, self.y + y_offset))
            
            y_offset += item_height
        
        scroll_bar_width = 15
        scroll_bar_x = self.x + self.width - scroll_bar_width - 5
        
        if len(self.valid_files) > self.max_visible:
            scroll_ratio = self.scroll_offset / (len(self.valid_files) - self.max_visible)
            scroll_bar_height = max(20, (self.height - 40) * self.max_visible / len(self.valid_files))
            scroll_bar_y = self.y + 40 + scroll_ratio * (self.height - 40 - scroll_bar_height)
            
            scroll_bar_rect = pygame.Rect(scroll_bar_x, scroll_bar_y, scroll_bar_width, scroll_bar_height)
            pygame.draw.rect(surface, WHITE, scroll_bar_rect)
            pygame.draw.rect(surface, GRAY, scroll_bar_rect, 1)
        
        if self.scroll_offset > 0:
            up_arrow = self.font.render("▲", True, WHITE)
            surface.blit(up_arrow, (scroll_bar_x + 2, self.y + 15))
        
        if self.scroll_offset + self.max_visible < len(self.valid_files):
            down_arrow = self.font.render("▼", True, WHITE)
            surface.blit(down_arrow, (scroll_bar_x + 2, self.y + self.height - 20))

class MenuScene:
    def __init__(self, screen_width, screen_height):
        self.screen_width = screen_width
        self.screen_height = screen_height
        
        self.title_font = pygame.font.SysFont('Arial', MENU_TITLE_SIZE, bold=True)
        self.button_font = pygame.font.SysFont('Arial', MENU_BUTTON_FONT_SIZE)
        self.music_font = pygame.font.SysFont('Arial', MENU_MUSIC_FONT_SIZE)
        
        try:
            self.background = pygame.image.load('src/scenes/spritesheet-background/albedo-shalttear-menu.png').convert_alpha()
            self.background = pygame.transform.scale(self.background, (screen_width, screen_height))
            print("Background do menu carregado: albedo-shalttear-menu.png")
        except Exception as e:
            print(f"Erro ao carregar background do menu: {e}")
            self.background = pygame.Surface((screen_width, screen_height))
            self.background.fill(BLACK)
        
        self.title_text = self.title_font.render("GUITAR HERO - Anime Edition", True, WHITE)
        self.title_rect = self.title_text.get_rect(center=(screen_width // 2, 120))
        
        button_width = 250
        button_height = 50
        button_spacing = 60
        start_y = 200
        
        self.start_button = MenuButton(
            screen_width // 2 - button_width // 2,
            start_y,
            button_width,
            button_height,
            "INICIAR JOGO",
            GREEN,
            MENU_BUTTON_HOVER_GREEN,
            self.button_font
        )
        
        self.credits_button = MenuButton(
            screen_width // 2 - button_width // 2,
            start_y + button_spacing,
            button_width,
            button_height,
            "CRÉDITOS",
            BLUE,
            (0, 150, 255),
            self.button_font
        )
        
        self.exit_button = MenuButton(
            screen_width // 2 - button_width // 2,
            start_y + button_spacing * 2,
            button_width,
            button_height,
            "SAIR",
            RED,
            MENU_BUTTON_HOVER_RED,
            self.button_font
        )
        
        selector_width = 450
        selector_height = 220
        self.music_selector = MusicSelector(
            screen_width // 2 - selector_width // 2,
            start_y + button_spacing * 3 + 20,
            selector_width,
            selector_height,
            AUDIO_FILES,
            self.music_font
        )
        
        self.instructions = [
            "Use as setas ↑↓ para navegar pelas músicas",
            "Pressione ENTER para iniciar o jogo",
            "Pressione C para ver os créditos",
            "Pressione ESC para sair"
        ]
        
        self.instruction_font = pygame.font.SysFont('Arial', MENU_INSTRUCTION_FONT_SIZE)
        
        self.selected_music = None
        self.show_music_selector = True
        
    def handle_key_press(self, key):
        if key == pygame.K_RETURN or key == pygame.K_KP_ENTER:
            self.selected_music = self.music_selector.get_selected_music()
            return "start_game"
        
        elif key == pygame.K_ESCAPE:
            return "exit_game"
        
        elif key == pygame.K_c:
            return "show_credits"
        
        elif key == pygame.K_UP:
            self.music_selector.scroll_up()
        
        elif key == pygame.K_DOWN:
            self.music_selector.scroll_down()
        
        return None
    
    def handle_mouse_click(self, mouse_pos):
        if self.start_button.rect.collidepoint(mouse_pos):
            self.selected_music = self.music_selector.get_selected_music()
            return "start_game"
        
        elif self.credits_button.rect.collidepoint(mouse_pos):
            return "show_credits"
        
        elif self.exit_button.rect.collidepoint(mouse_pos):
            return "exit_game"
        
        return None
    
    def update(self, dt):
        self.start_button.update(dt)
        self.credits_button.update(dt)
        self.exit_button.update(dt)
        
        mouse_pos = pygame.mouse.get_pos()
        self.start_button.check_hover(mouse_pos)
        self.credits_button.check_hover(mouse_pos)
        self.exit_button.check_hover(mouse_pos)
    
    def draw(self, surface):
        surface.blit(self.background, (0, 0))
        
        overlay = pygame.Surface((self.screen_width, self.screen_height), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 80))
        surface.blit(overlay, (0, 0))
        
        title_shadow = self.title_font.render("GUITAR HERO - Anime Edition", True, BLACK)
        shadow_rect = title_shadow.get_rect(center=(self.screen_width // 2 + 2, 120))
        surface.blit(title_shadow, shadow_rect)
        surface.blit(self.title_text, self.title_rect)
        
        self.start_button.draw(surface)
        self.credits_button.draw(surface)
        self.exit_button.draw(surface)
        
        if self.show_music_selector:
            self.music_selector.draw(surface)
        
        instruction_start_y = self.music_selector.y + self.music_selector.height + 20
        for instruction in self.instructions:
            instruction_shadow = self.instruction_font.render(instruction, True, BLACK)
            shadow_rect = instruction_shadow.get_rect(center=(self.screen_width // 2 + 1, instruction_start_y + 1))
            surface.blit(instruction_shadow, shadow_rect)
            
            instruction_text = self.instruction_font.render(instruction, True, WHITE)
            instruction_rect = instruction_text.get_rect(center=(self.screen_width // 2, instruction_start_y))
            surface.blit(instruction_text, instruction_rect)
            instruction_start_y += 20
    
    def get_selected_music(self):
        return self.selected_music
