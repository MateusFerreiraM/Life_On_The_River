# player.py
# Controla o estado, as ações e a aparência do jogador.

import pygame
from PPlay.sprite import Sprite

class Player:
    def __init__(self, window):
        """Inicializa o jogador."""
        self.window = window
        
        # Apenas os sprites de correr e agachar são necessários agora
        self.run_sprite = Sprite("Assets/Images/burglar.png", 9)
        self.duck_sprite = Sprite("Assets/Images/burglar_state2.png")
        
        self.run_sprite.set_sequence(0, 4, True)
        self.run_sprite.set_total_duration(800)
        
        self.gravity = 2400
        self.jump_velocity = -1100
        
        self.velocity_y = 0
        
        self.ground_y = self.window.height - self.run_sprite.height
        self.duck_y = self.window.height - self.duck_sprite.height

        # Estado de bónus de pontos (o único power-up que resta)
        self.is_score_boosted = False
        self.score_boost_timer = 0
        self.score_boost_duration = 10
        
        self.up_key_was_pressed = False
        self.reset()

    def reset(self):
        """Reseta o jogador para o estado inicial."""
        self.sprite = self.run_sprite
        self.sprite.set_position(100, self.ground_y)
        self.is_ducking = False
        self.velocity_y = 0
        self.is_score_boosted = False
        self.score_boost_timer = 0
        self.up_key_was_pressed = False

    def get_hitbox(self):
        """Retorna um retângulo de colisão mais justo para o jogador."""
        hitbox_width = self.sprite.width * 0.85
        hitbox_height = self.sprite.height * 0.90
        hitbox_x = self.sprite.x + (self.sprite.width - hitbox_width) / 2
        hitbox_y = self.sprite.y + (self.sprite.height - hitbox_height) / 2
        return pygame.Rect(hitbox_x, hitbox_y, hitbox_width, hitbox_height)

    def _handle_powerups(self, delta_time):
        """Gerencia os timers dos power-ups."""
        if self.is_score_boosted:
            self.score_boost_timer += delta_time
            if self.score_boost_timer >= self.score_boost_duration:
                self.is_score_boosted = False
                self.score_boost_timer = 0

    def update(self, keyboard, delta_time):
        """Atualiza a lógica do jogador a cada frame."""
        self._handle_powerups(delta_time)

        self.velocity_y += self.gravity * delta_time
        self.sprite.y += self.velocity_y * delta_time

        current_ground_level = self.duck_y if self.is_ducking else self.ground_y
        
        if self.sprite.y >= current_ground_level:
            self.sprite.y = current_ground_level
            self.velocity_y = 0

        up_key_is_pressed = keyboard.key_pressed("UP")
        if self.velocity_y == 0:
            if keyboard.key_pressed("DOWN"):
                if not self.is_ducking:
                    current_x = self.sprite.x
                    self.is_ducking = True
                    self.sprite = self.duck_sprite
                    self.sprite.set_position(current_x, self.duck_y)
            else:
                if self.is_ducking:
                    current_x = self.sprite.x
                    self.is_ducking = False
                    self.sprite = self.run_sprite
                    self.sprite.set_position(current_x, self.ground_y)
            
            if not self.is_ducking and up_key_is_pressed and not self.up_key_was_pressed:
                self.velocity_y = self.jump_velocity

        self.up_key_was_pressed = up_key_is_pressed

        if not self.is_ducking and self.velocity_y == 0:
            self.sprite.update()

    def activate_score_boost(self):
        self.is_score_boosted = True
        self.score_boost_timer = 0

    def draw(self):
        """Desenha o jogador na tela."""
        self.sprite.draw()