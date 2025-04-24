import pygame
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

<<<<<<< HEAD
from scenes.guitar_hero import GuitarHeroScene
=======
from src.scenes.guitar_hero_scene import GuitarHeroScene
>>>>>>> 6409d99 (update game ideia)
from config import *

pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption(TITLE)
clock = pygame.time.Clock()

guitar_hero_scene = GuitarHeroScene(SCREEN_WIDTH, SCREEN_HEIGHT)

running = True
previous_time = pygame.time.get_ticks() / 1000 

while running:
    
    current_time = pygame.time.get_ticks() / 1000
    dt = current_time - previous_time
    previous_time = current_time
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        if event.type == pygame.KEYDOWN:
            guitar_hero_scene.handle_key_press(event.key)
            
            if event.key == pygame.K_ESCAPE:
                running = False
    
    guitar_hero_scene.update(dt)
    
    guitar_hero_scene.draw(screen)
    
    pygame.display.flip()
    
    clock.tick(FPS)

pygame.quit()
sys.exit()