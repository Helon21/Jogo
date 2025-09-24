import pygame
from config import *

class ScoreMenuScene:
    def __init__(self, screen_width, screen_height, song_name, final_score):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.song_name = song_name
        self.final_score = final_score
        
        self.title_font = pygame.font.SysFont('Arial', 36, bold=True)
        self.score_font = pygame.font.SysFont('Arial', 48, bold=True)
        self.instruction_font = pygame.font.SysFont('Arial', 24)
        
        self.menu_width = 500
        self.menu_height = 300
        self.menu_x = (screen_width - self.menu_width) // 2
        self.menu_y = (screen_height - self.menu_height) // 2
        
        self.song_text = self.title_font.render(f"Música: {song_name}", True, WHITE)
        self.score_text = self.score_font.render(f"Pontuação: {final_score}", True, WHITE)
        self.instruction_text = self.instruction_font.render("Pressione ESPAÇO para voltar ao menu", True, WHITE)
    
    def handle_key_press(self, key):
        if key == pygame.K_SPACE:
            return "return_to_menu"
        return None
    
    def update(self, dt):
        pass
    
    def draw(self, surface):
        overlay = pygame.Surface((self.screen_width, self.screen_height), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 200))
        surface.blit(overlay, (0, 0))
        
        menu_rect = pygame.Rect(self.menu_x, self.menu_y, self.menu_width, self.menu_height)
        pygame.draw.rect(surface, GRAY, menu_rect)
        pygame.draw.rect(surface, WHITE, menu_rect, 3)
        
        song_rect = self.song_text.get_rect(centerx=self.screen_width // 2, 
                                          centery=self.menu_y + 80)
        score_rect = self.score_text.get_rect(centerx=self.screen_width // 2, 
                                            centery=self.menu_y + 150)
        instruction_rect = self.instruction_text.get_rect(centerx=self.screen_width // 2, 
                                                        centery=self.menu_y + 220)
        
        surface.blit(self.song_text, song_rect)
        surface.blit(self.score_text, score_rect)
        surface.blit(self.instruction_text, instruction_rect)
