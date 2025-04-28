import pygame
import sys
from scenes.guitar_hero_scene import GuitarHeroScene
from config import *

class Game:
    def __init__(self):
        print("Iniciando o jogo...")
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption(TITLE)
        self.clock = pygame.time.Clock()
        print("Criando cena Guitar Hero...")
        self.guitar_hero_scene = GuitarHeroScene(SCREEN_WIDTH, SCREEN_HEIGHT)
        self.running = True
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
                if event.type == pygame.KEYDOWN:
                    self.guitar_hero_scene.handle_key_press(event.key)
                    if event.key == pygame.K_ESCAPE:
                        print("Tecla ESC pressionada")
                        self.running = False

            self.guitar_hero_scene.update(dt)
            self.guitar_hero_scene.draw(self.screen)
            pygame.display.flip()
            self.clock.tick(FPS)
        print("Encerrando o jogo...")
        pygame.quit()
        sys.exit() 