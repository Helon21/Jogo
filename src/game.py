import pygame
import sys
from scenes.guitar_hero_scene import GuitarHeroScene
from scenes.menu import MenuScene
from scenes.score_menu import ScoreMenuScene
from scenes.credits import CreditsScene
from config import *

class Game:
    def __init__(self):
        print("Iniciando o jogo...")
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption(TITLE)
        self.clock = pygame.time.Clock()
        
        self.current_scene = "menu"
        self.running = True
        
        print("Criando cena do menu...")
        self.menu_scene = MenuScene(SCREEN_WIDTH, SCREEN_HEIGHT)
        self.guitar_hero_scene = None
        self.score_menu_scene = None
        self.credits_scene = None
        
        print("Jogo inicializado com sucesso!")

    def run(self):
        print("Iniciando loop principal do jogo...")
        previous_time = pygame.time.get_ticks() / 1000
        while self.running:
            current_time = pygame.time.get_ticks() / 1000
            dt = current_time - previous_time
            previous_time = current_time

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    print("Evento QUIT detectado")
                    self.running = False
                
                elif event.type == pygame.KEYDOWN:
                    self.handle_key_press(event.key)
                
                elif event.type == pygame.KEYUP:
                    if self.current_scene == "game" and self.guitar_hero_scene:
                        self.guitar_hero_scene.handle_key_release(event.key)
                
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        self.handle_mouse_click(event.pos)

            self.update(dt)
            self.draw()
            pygame.display.flip()
            self.clock.tick(FPS)
        
        print("Encerrando o jogo...")
        pygame.quit()
        sys.exit()
    
    def handle_key_press(self, key):
        if self.current_scene == "menu":
            action = self.menu_scene.handle_key_press(key)
            if action == "start_game":
                self.start_game()
            elif action == "exit_game":
                self.running = False
        
        elif self.current_scene == "game":
            if self.guitar_hero_scene:
                self.guitar_hero_scene.handle_key_press(key)
                if key == pygame.K_ESCAPE:
                    print("Voltando ao menu...")
                    self.return_to_menu()
        
        elif self.current_scene == "score":
            if self.score_menu_scene:
                action = self.score_menu_scene.handle_key_press(key)
                if action == "return_to_menu":
                    self.return_to_menu()
        
        elif self.current_scene == "credits":
            if self.credits_scene:
                action = self.credits_scene.handle_key_press(key)
                if action == "return_to_menu":
                    self.return_to_menu()

    def handle_mouse_click(self, mouse_pos):
        if self.current_scene == "menu":
            action = self.menu_scene.handle_mouse_click(mouse_pos)
            if action == "start_game":
                self.start_game()
            elif action == "exit_game":
                self.running = False
            elif action == "show_credits":
                self.show_credits()
        
        elif self.current_scene == "credits":
            if self.credits_scene:
                action = self.credits_scene.handle_mouse_click(mouse_pos)
                if action == "return_to_menu":
                    self.return_to_menu()
    
    def start_game(self):
        print("Iniciando o jogo...")
        selected_music = self.menu_scene.get_selected_music()
        
        pygame.mixer.music.stop()
        
        self.guitar_hero_scene = GuitarHeroScene(SCREEN_WIDTH, SCREEN_HEIGHT)
        
        if selected_music:
            self.guitar_hero_scene.music_path = selected_music
            print(f"Música selecionada: {selected_music}")
        
        self.current_scene = "game"
    
    def return_to_menu(self):
        print("Retornando ao menu...")
        pygame.mixer.music.stop()
        
        self.guitar_hero_scene = None
        self.score_menu_scene = None
        self.credits_scene = None
        
        self.current_scene = "menu"
    
    def show_credits(self):
        print("Mostrando créditos...")
        self.credits_scene = CreditsScene(SCREEN_WIDTH, SCREEN_HEIGHT)
        self.current_scene = "credits"
    
    def show_score_menu(self, song_name, final_score):
        print("Mostrando menu de pontuação...")
        self.score_menu_scene = ScoreMenuScene(SCREEN_WIDTH, SCREEN_HEIGHT, song_name, final_score)
        self.current_scene = "score"
    
    def update(self, dt):
        if self.current_scene == "menu":
            self.menu_scene.update(dt)
        elif self.current_scene == "game" and self.guitar_hero_scene:
            result = self.guitar_hero_scene.update(dt)
            if result == "return_to_menu":
                print("Música finalizada, mostrando pontuação...")
                song_name = self.guitar_hero_scene.music_path.split('/')[-1].replace('.mp3', '')
                final_score = self.guitar_hero_scene.score
                self.show_score_menu(song_name, final_score)
        elif self.current_scene == "score" and self.score_menu_scene:
            self.score_menu_scene.update(dt)
        elif self.current_scene == "credits" and self.credits_scene:
            result = self.credits_scene.update(dt)
            if result == "return_to_menu":
                self.return_to_menu()
    
    def draw(self):
        if self.current_scene == "menu":
            self.menu_scene.draw(self.screen)
        elif self.current_scene == "game" and self.guitar_hero_scene:
            self.guitar_hero_scene.draw(self.screen)
        elif self.current_scene == "score" and self.score_menu_scene:
            self.score_menu_scene.draw(self.screen)
        elif self.current_scene == "credits" and self.credits_scene:
            self.credits_scene.draw(self.screen)