# gameplay.py
# Contém a lógica da partida, agora com um estado de pausa.

import pygame
from PPlay.sprite import Sprite
from PPlay.collision import Collision
from player import Player
from scenery import Scenery
from spawner import Spawner
from pause_menu import PauseMenu # Importa o novo menu de pausa

class Gameplay:
    def __init__(self, window, game):
        """Inicializa a cena de gameplay."""
        self.window = window
        self.game = game
        self.keyboard = self.window.get_keyboard()

        self.scenery = Scenery(self.window, "Assets/Images/fundo_jogo.png", "Assets/Images/fundo_jogo1.png")
        self.player = Player(self.window)
        self.spawner = Spawner(self.window)
        self.pause_menu = PauseMenu(self.window, self) # Cria a instância do menu de pausa
        
        self.is_paused = False
        self.esc_was_pressed = False
        
        try:
            self.hud_font = pygame.font.Font("Assets/Fonts/pricedown bl.ttf", 40)
        except FileNotFoundError:
            self.hud_font = pygame.font.Font(None, 50)
            
        self.color_text = (255, 255, 255)
        self.color_outline = (0, 0, 0)

        self.game_speed = 0
        self.score = 0
        self.time_survived = 0
        self.reset()

    # --- MÉTODOS DE CONTROLO CHAMADOS PELO MENU DE PAUSA ---
    def unpause(self):
        self.is_paused = False

    def restart(self):
        self.unpause()
        self.reset()

    def go_to_main_menu(self):
        self.unpause()
        self.game.change_state("MENU")
    
    def reset(self):
        """Reseta o estado da partida."""
        self.score = 0
        self.time_survived = 0
        self.game_speed = 300
        self.player.reset()
        self.spawner.reset()

    def _render_text_with_outline(self, font, text, color, outline_color, outline_width=2):
        """Função auxiliar para renderizar texto com um contorno."""
        text_surface = font.render(text, True, color)
        outline_surface = font.render(text, True, outline_color)
        final_surface = pygame.Surface((text_surface.get_width() + outline_width * 2, text_surface.get_height() + outline_width * 2), pygame.SRCALPHA)
        positions = [(0, 0), (outline_width, 0), (outline_width * 2, 0), (0, outline_width), (outline_width * 2, outline_width), (0, outline_width * 2), (outline_width, outline_width * 2), (outline_width * 2, outline_width * 2)]
        for pos in positions: final_surface.blit(outline_surface, pos)
        final_surface.blit(text_surface, (outline_width, outline_width))
        return final_surface

    def _check_collisions(self):
        """Verifica e trata as colisões."""
        player_hitbox = self.player.get_hitbox()
        all_objects = []
        for pool in self.spawner.object_pool.values(): all_objects.extend(pool)
        for obj in all_objects:
            if obj.is_active:
                obj_hitbox = obj.get_hitbox()
                if player_hitbox.colliderect(obj_hitbox):
                    if obj.type == "score_boost":
                        self.player.activate_score_boost()
                        obj.is_active = False
                    elif obj.type == "obstacle":
                        self.game.change_state("GAME_OVER", score=int(self.score), time=self.time_survived)
                        return

    def run(self):
        """Executa um único frame da lógica da partida."""
        # Lógica para pausar o jogo com a tecla ESC
        esc_is_pressed = self.keyboard.key_pressed("ESC")
        if esc_is_pressed and not self.esc_was_pressed:
            self.is_paused = not self.is_paused
        self.esc_was_pressed = esc_is_pressed

        # Se o jogo não estiver pausado, toda a lógica de gameplay é executada
        if not self.is_paused:
            delta_time = self.window.delta_time()
            self.game_speed = 300 + (self.score // 30) * 20
            self.time_survived += delta_time
            
            scenery_move_delta = (self.game_speed * 0.5) * delta_time
            self.scenery.update(scenery_move_delta)
            
            self.player.update(self.keyboard, delta_time)
            self.spawner.update(self.game_speed, self.score, delta_time)

            self._check_collisions()

            score_multiplier = 2 if self.player.is_score_boosted else 1
            self.score += (1 * score_multiplier) * delta_time * 20
        
        # --- LÓGICA DE DESENHO ---
        # Os elementos do jogo são sempre desenhados, mesmo quando pausados
        self.scenery.draw()
        self.player.draw()
        self.spawner.draw()
        
        score_text = f"PONTOS: {int(self.score)}"
        score_surf = self._render_text_with_outline(self.hud_font, score_text, self.color_text, self.color_outline)
        self.window.screen.blit(score_surf, (10, 10))

        # Se o jogo estiver pausado, desenha o menu de pausa por cima de tudo
        if self.is_paused:
            self.pause_menu.run()