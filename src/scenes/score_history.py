import pygame
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config import *
from score_manager import ScoreManager

class ScoreHistoryScene:
    def __init__(self, screen_width, screen_height):
        self.screen_width = screen_width
        self.screen_height = screen_height
        
        self.title_font = pygame.font.SysFont('Arial', 36, bold=True)
        self.header_font = pygame.font.SysFont('Arial', 20, bold=True)
        self.text_font = pygame.font.SysFont('Arial', 16)
        self.button_font = pygame.font.SysFont('Arial', 18)
        
        self.score_manager = ScoreManager()
        
        self.items_per_page = 15
        self.current_page = 0
        self.scroll_offset = 0
        self.max_scroll_offset = 0
        
        self.back_button = self.create_button("VOLTAR", RED, (50, screen_height - 60))
        self.clear_button = self.create_button("LIMPAR", (200, 0, 0), (screen_width - 150, screen_height - 60))
        
        self.scores = self.score_manager.get_top_scores(100)
        self.update_scroll_limits()
        
        try:
            self.background = pygame.image.load('src/scenes/spritesheet-background/albedo-shalttear-menu.png').convert_alpha()
            self.background = pygame.transform.scale(self.background, (screen_width, screen_height))
        except Exception as e:
            print(f"Erro ao carregar background: {e}")
            self.background = pygame.Surface((screen_width, screen_height))
            self.background.fill(BLACK)
    
    def create_button(self, text, color, pos):
        button_rect = pygame.Rect(pos[0], pos[1], 100, 40)
        return {
            'text': text,
            'color': color,
            'rect': button_rect,
            'hover_color': tuple(min(255, c + 50) for c in color),
            'is_hovered': False
        }
    
    def update_scroll_limits(self):
        total_items = len(self.scores)
        self.max_scroll_offset = max(0, total_items - self.items_per_page)
        self.scroll_offset = min(self.scroll_offset, self.max_scroll_offset)
    
    def handle_key_press(self, key):
        if key == pygame.K_ESCAPE or key == pygame.K_BACKSPACE:
            return "return_to_menu"
        elif key == pygame.K_UP:
            self.scroll_up()
        elif key == pygame.K_DOWN:
            self.scroll_down()
        elif key == pygame.K_PAGEUP:
            self.scroll_up_page()
        elif key == pygame.K_PAGEDOWN:
            self.scroll_down_page()
        elif key == pygame.K_HOME:
            self.scroll_to_top()
        elif key == pygame.K_END:
            self.scroll_to_bottom()
        
        return None
    
    def handle_mouse_click(self, mouse_pos):
        if self.back_button['rect'].collidepoint(mouse_pos):
            return "return_to_menu"
        elif self.clear_button['rect'].collidepoint(mouse_pos):
            self.clear_all_scores()
        
        return None
    
    def scroll_up(self):
        if self.scroll_offset > 0:
            self.scroll_offset -= 1
    
    def scroll_down(self):
        if self.scroll_offset < self.max_scroll_offset:
            self.scroll_offset += 1
    
    def scroll_up_page(self):
        self.scroll_offset = max(0, self.scroll_offset - self.items_per_page)
    
    def scroll_down_page(self):
        self.scroll_offset = min(self.max_scroll_offset, self.scroll_offset + self.items_per_page)
    
    def scroll_to_top(self):
        self.scroll_offset = 0
    
    def scroll_to_bottom(self):
        self.scroll_offset = self.max_scroll_offset
    
    def clear_all_scores(self):
        self.score_manager.clear_scores()
        self.scores = []
        self.scroll_offset = 0
        self.max_scroll_offset = 0
        print("Todas as pontuações foram limpas")
    
    def update(self, dt):
        mouse_pos = pygame.mouse.get_pos()
        
        self.back_button['is_hovered'] = self.back_button['rect'].collidepoint(mouse_pos)
        self.clear_button['is_hovered'] = self.clear_button['rect'].collidepoint(mouse_pos)
    
    def draw(self, surface):
        surface.blit(self.background, (0, 0))
        
        overlay = pygame.Surface((self.screen_width, self.screen_height), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 120))
        surface.blit(overlay, (0, 0))
        
        title_text = self.title_font.render("HISTÓRICO DE PONTUAÇÕES", True, WHITE)
        title_rect = title_text.get_rect(center=(self.screen_width // 2, 50))
        surface.blit(title_text, title_rect)
        
        stats = self.score_manager.get_stats()
        stats_text = f"Total: {stats['total_scores']} | Melhor: {stats['best_score']:,} | Média: {stats['average_score']:,}"
        stats_surface = self.text_font.render(stats_text, True, YELLOW)
        stats_rect = stats_surface.get_rect(center=(self.screen_width // 2, 90))
        surface.blit(stats_surface, stats_rect)
        
        list_x = 100
        list_y = 120
        list_width = self.screen_width - 200
        list_height = self.screen_height - 250
        
        list_rect = pygame.Rect(list_x, list_y, list_width, list_height)
        pygame.draw.rect(surface, GRAY, list_rect)
        pygame.draw.rect(surface, WHITE, list_rect, 2)
        
        header_y = list_y + 10
        headers = ["#", "JOGADOR", "MÚSICA", "PONTUAÇÃO", "DATA"]
        header_widths = [50, 200, 250, 120, 120]
        
        x_offset = list_x + 10
        for i, (header, width) in enumerate(zip(headers, header_widths)):
            header_text = self.header_font.render(header, True, WHITE)
            surface.blit(header_text, (x_offset, header_y))
            x_offset += width
        
        separator_y = header_y + 25
        pygame.draw.line(surface, WHITE, (list_x + 10, separator_y), (list_x + list_width - 10, separator_y), 2)
        
        if self.scores:
            start_idx = self.scroll_offset
            end_idx = min(start_idx + self.items_per_page, len(self.scores))
            
            for i, score in enumerate(self.scores[start_idx:end_idx]):
                row_y = separator_y + 10 + (i * 25)
                
                if i % 2 == 0:
                    row_rect = pygame.Rect(list_x + 5, row_y - 2, list_width - 10, 22)
                    pygame.draw.rect(surface, (60, 60, 60), row_rect)
                
                pos_text = self.text_font.render(f"{start_idx + i + 1}", True, WHITE)
                surface.blit(pos_text, (list_x + 15, row_y))
                
                player_name = score['player_name'][:20] + "..." if len(score['player_name']) > 20 else score['player_name']
                player_text = self.text_font.render(player_name, True, WHITE)
                surface.blit(player_text, (list_x + 70, row_y))
                
                song_name = score['song_name'][:25] + "..." if len(score['song_name']) > 25 else score['song_name']
                song_text = self.text_font.render(song_name, True, WHITE)
                surface.blit(song_text, (list_x + 280, row_y))
                
                score_text = self.text_font.render(f"{score['score']:,}", True, YELLOW)
                surface.blit(score_text, (list_x + 540, row_y))
                
                date_text = self.text_font.render(score['date'], True, WHITE)
                surface.blit(date_text, (list_x + 670, row_y))
        else:
            no_scores_text = self.text_font.render("Nenhuma pontuação encontrada", True, WHITE)
            no_scores_rect = no_scores_text.get_rect(center=(self.screen_width // 2, list_y + list_height // 2))
            surface.blit(no_scores_text, no_scores_rect)
        
        if self.max_scroll_offset > 0:
            scroll_bar_width = 15
            scroll_bar_x = list_x + list_width - scroll_bar_width - 5
            scroll_bar_height = max(20, (list_height - 40) * self.items_per_page / len(self.scores))
            scroll_ratio = self.scroll_offset / self.max_scroll_offset if self.max_scroll_offset > 0 else 0
            scroll_bar_y = list_y + 40 + scroll_ratio * (list_height - 40 - scroll_bar_height)
            
            scroll_bar_rect = pygame.Rect(scroll_bar_x, scroll_bar_y, scroll_bar_width, scroll_bar_height)
            pygame.draw.rect(surface, WHITE, scroll_bar_rect)
            pygame.draw.rect(surface, GRAY, scroll_bar_rect, 1)
        
        instructions = [
            "↑↓ - Navegar",
            "ESC - Voltar | Clique em LIMPAR para apagar todas as pontuações"
        ]
        
        instruction_y = self.screen_height - 120
        for instruction in instructions:
            instruction_text = self.text_font.render(instruction, True, WHITE)
            instruction_rect = instruction_text.get_rect(center=(self.screen_width // 2, instruction_y))
            surface.blit(instruction_text, instruction_rect)
            instruction_y += 20
        
        self.draw_button(surface, self.back_button)
        self.draw_button(surface, self.clear_button)
    
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
