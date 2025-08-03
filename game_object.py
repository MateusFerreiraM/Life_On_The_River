# game_object.py
# Contém as classes para os objetos móveis do jogo.

import pygame
from PPlay.sprite import Sprite

class MovingObject(Sprite):
    """Classe para objetos que se movem da direita para a esquerda."""
    def __init__(self, image_path, object_type):
        super().__init__(image_path)
        self.type = object_type
        self.is_active = False
        self.speed = 0

    def get_hitbox(self):
        """Retorna um retângulo de colisão mais justo para o objeto."""
        hitbox_width = self.width * 0.85
        hitbox_height = self.height * 0.85
        hitbox_x = self.x + (self.width - hitbox_width) / 2
        hitbox_y = self.y + (self.height - hitbox_height) / 2
        return pygame.Rect(hitbox_x, hitbox_y, hitbox_width, hitbox_height)

    def spawn(self, window, speed, y_pos):
        self.is_active = True
        self.speed = speed
        self.x = window.width
        self.y = y_pos - self.height

    def update(self, game_speed, delta_time):
        """Move o objeto para a esquerda com base na velocidade do jogo."""
        if self.is_active:
            self.speed = game_speed
            self.x -= self.speed * delta_time
            if self.x < -self.width:
                self.is_active = False
    
    def draw(self):
        if self.is_active:
            super().draw()