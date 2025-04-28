import pygame

class GameObject:
    
    def __init__(self, x, y, width, height, color=(255, 255, 255)):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color
        self.rect = pygame.Rect(x, y, width, height)
        self.visible = True
        self.active = True
    
    def update(self, dt):
        self.rect.x = self.x
        self.rect.y = self.y
    
    def draw(self, surface):
        if self.visible:
            pygame.draw.rect(surface, self.color, self.rect)
    
    def set_position(self, x, y):
        self.x = x
        self.y = y
        self.rect.x = x
        self.rect.y = y


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
