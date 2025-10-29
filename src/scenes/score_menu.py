import pygame
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config import *
from score_manager import ScoreManager

class ScoreMenuScene:
    def __init__(self, screen_width, screen_height, song_name, final_score):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.song_name = song_name
        self.final_score = final_score
        
        self.title_font = pygame.font.SysFont('Arial', 36, bold=True)
        self.score_font = pygame.font.SysFont('Arial', 48, bold=True)
        self.input_font = pygame.font.SysFont('Arial', 24)
        self.button_font = pygame.font.SysFont('Arial', 20)
        
        self.score_manager = ScoreManager()
        
        self.player_name = ""
        self.input_active = True
        self.cursor_visible = True
        self.cursor_timer = 0
        
        self.save_button = self.create_button("SALVAR", GREEN, (screen_width // 2 - 100, 400))
        self.skip_button = self.create_button("PULAR", GRAY, (screen_width // 2 + 20, 400))
        
        self.score_saved = False
        self.show_message = False
        self.message_timer = 0
        self.message_text = ""
        
        self.song_text = self.title_font.render(f"Música: {song_name}", True, WHITE)
        self.score_text = self.score_font.render(f"Pontuação: {final_score:,}", True, YELLOW)
        self.name_label = self.input_font.render("Digite seu nome:", True, WHITE)
        
        self.menu_width = 500
        self.menu_height = 500
        self.menu_x = (screen_width - self.menu_width) // 2
        self.menu_y = (screen_height - self.menu_height) // 2
        
        self.input_box = pygame.Rect(self.menu_x + 50, self.menu_y + 200, 400, 40)
        
    def create_button(self, text, color, pos):
        button_rect = pygame.Rect(pos[0], pos[1], 80, 30)
        return {
            'text': text,
            'color': color,
            'rect': button_rect,
            'hover_color': tuple(min(255, c + 50) for c in color),
            'is_hovered': False
        }
    
    def handle_key_press(self, key):
        if self.input_active and not self.score_saved:
            if key == pygame.K_BACKSPACE:
                self.player_name = self.player_name[:-1]
            elif key == pygame.K_RETURN or key == pygame.K_KP_ENTER:
                self.save_score()
            elif key == pygame.K_ESCAPE:
                return "return_to_menu"
            elif key == pygame.K_TAB:
                self.skip_saving()
        elif self.score_saved:
            if key == pygame.K_SPACE or key == pygame.K_RETURN or key == pygame.K_KP_ENTER:
                return "return_to_menu"
            elif key == pygame.K_ESCAPE:
                return "return_to_menu"
        
        return None
    
    def handle_text_input(self, text):
        if self.input_active and not self.score_saved:
            if len(self.player_name) < 20:
                self.player_name += text
    
    def handle_mouse_click(self, mouse_pos):
        if self.score_saved:
            return "return_to_menu"
        
        if self.save_button['rect'].collidepoint(mouse_pos):
            self.save_score()
        elif self.skip_button['rect'].collidepoint(mouse_pos):
            self.skip_saving()
        

        if self.input_box.collidepoint(mouse_pos):
            self.input_active = True
        else:
            self.input_active = False
        
        return None
    
    def save_score(self):
        if not self.player_name.strip():
            self.player_name = "Jogador Anônimo"
        
        self.score_manager.add_score(self.player_name.strip(), self.song_name, self.final_score)
        self.score_saved = True
        self.input_active = False
        self.show_message = True
        self.message_text = f"Pontuação salva com sucesso!"
        print(f"Pontuação salva: {self.player_name} - {self.song_name} - {self.final_score}")
    
    def skip_saving(self):
        self.score_saved = True
        self.input_active = False
        self.show_message = True
        self.message_text = "Pontuação não salva"
    
    def update(self, dt):
        self.cursor_timer += dt
        if self.cursor_timer >= 0.5:
            self.cursor_visible = not self.cursor_visible
            self.cursor_timer = 0
        
        mouse_pos = pygame.mouse.get_pos()
        
        if not self.score_saved:
            self.save_button['is_hovered'] = self.save_button['rect'].collidepoint(mouse_pos)
            self.skip_button['is_hovered'] = self.skip_button['rect'].collidepoint(mouse_pos)
        
        if self.show_message:
            self.message_timer += dt
            if self.message_timer >= 2.0:
                self.show_message = False
    
    def draw(self, surface):
        overlay = pygame.Surface((self.screen_width, self.screen_height), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 200))
        surface.blit(overlay, (0, 0))
        
        menu_rect = pygame.Rect(self.menu_x, self.menu_y, self.menu_width, self.menu_height)
        pygame.draw.rect(surface, GRAY, menu_rect)
        pygame.draw.rect(surface, WHITE, menu_rect, 3)
        
        title_text = self.title_font.render("RESULTADO", True, WHITE)
        title_rect = title_text.get_rect(center=(self.screen_width // 2, self.menu_y + 50))
        surface.blit(title_text, title_rect)
        
        song_rect = self.song_text.get_rect(center=(self.screen_width // 2, self.menu_y + 100))
        surface.blit(self.song_text, song_rect)
        
        score_rect = self.score_text.get_rect(center=(self.screen_width // 2, self.menu_y + 150))
        surface.blit(self.score_text, score_rect)
        
        if not self.score_saved:
            name_label_rect = self.name_label.get_rect(center=(self.screen_width // 2, self.menu_y + 180))
            surface.blit(self.name_label, name_label_rect)
            
            pygame.draw.rect(surface, WHITE, self.input_box, 2)
            pygame.draw.rect(surface, BLACK, self.input_box)
            
            name_text = self.input_font.render(self.player_name, True, WHITE)
            surface.blit(name_text, (self.input_box.x + 5, self.input_box.y + 8))
            
            if self.input_active and self.cursor_visible:
                cursor_x = self.input_box.x + 5 + name_text.get_width()
                cursor_rect = pygame.Rect(cursor_x, self.input_box.y + 5, 2, 30)
                pygame.draw.rect(surface, WHITE, cursor_rect)
            
            self.draw_button(surface, self.save_button)
            self.draw_button(surface, self.skip_button)
            
            instruction_text = self.button_font.render("Pressione ENTER para salvar ou TAB para pular", True, WHITE)
            instruction_rect = instruction_text.get_rect(center=(self.screen_width // 2, self.menu_y + 450))
            surface.blit(instruction_text, instruction_rect)
        
        else:
            if self.show_message:
                message_surface = self.input_font.render(self.message_text, True, GREEN)
                message_rect = message_surface.get_rect(center=(self.screen_width // 2, self.menu_y + 250))
                surface.blit(message_surface, message_rect)
            
            continue_text = self.input_font.render("Pressione ESPAÇO para voltar ao menu", True, WHITE)
            continue_rect = continue_text.get_rect(center=(self.screen_width // 2, self.menu_y + 300))
            surface.blit(continue_text, continue_rect)
            
            stats = self.score_manager.get_stats()
            stats_text = f"Total de pontuações: {stats['total_scores']}"
            stats_surface = self.button_font.render(stats_text, True, YELLOW)
            stats_rect = stats_surface.get_rect(center=(self.screen_width // 2, self.menu_y + 350))
            surface.blit(stats_surface, stats_rect)
    
    def draw_button(self, surface, button):
        color = button['hover_color'] if button['is_hovered'] else button['color']
        
        shadow_rect = pygame.Rect(button['rect'].x + 2, button['rect'].y + 2, 
                                button['rect'].width, button['rect'].height)
        pygame.draw.rect(surface, BLACK, shadow_rect)
        
        pygame.draw.rect(surface, color, button['rect'])
        pygame.draw.rect(surface, WHITE, button['rect'], 2)
        
        text_surface = self.button_font.render(button['text'], True, WHITE)
        text_rect = text_surface.get_rect(center=button['rect'].center)
        surface.blit(text_surface, text_rect)
