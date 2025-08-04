# Ficheiro: achievements_scene.py (COMPLETO E COM AJUSTES DE POSIÇÃO)

import pygame
from PPlay.gameimage import GameImage
from PPlay.mouse import Mouse
import constants as C

class AchievementsScene:
    """
    Exibe a tela com a lista de todas as conquistas e o seu estado.
    """
    def __init__(self, window, game, asset_manager, achievement_manager):
        self.window = window
        self.game = game
        self.mouse = Mouse()
        self.keyboard = self.window.get_keyboard()
        self.achievement_manager = achievement_manager

        self.background = GameImage(C.IMG_MENU_BACKGROUND)
        
        self.font_title = asset_manager.get_font("pricedown_title")
        self.font_ach_title = asset_manager.get_font("pricedown_ach_title_small")
        self.font_ach_desc = asset_manager.get_font("pricedown_ach_desc_small")
        self.font_button = asset_manager.get_font("pricedown_button")
        
        self.color_title = C.COLOR_GOLD
        self.color_text = C.COLOR_WHITE
        self.color_hover = C.COLOR_GOLD
        self.color_outline = C.COLOR_BLACK
        self.color_unlocked = C.COLOR_ACH_UNLOCKED
        self.color_locked = C.COLOR_ACH_LOCKED

        self.back_button_rect = pygame.Rect(0, 0, 200, 50)
        # --- 3. BOTÃO "VOLTAR" MAIS PARA BAIXO ---
        self.back_button_rect.center = (self.window.width / 2, self.window.height - 40) # ALTERADO de 70 para 40
        
        self.click_cooldown = C.CLICK_COOLDOWN
        self.last_click_time = 0

    def _render_text_with_outline(self, font, text, color, outline_color, outline_width=2):
        text_surface = font.render(text, True, color)
        outline_surface = font.render(text, True, outline_color)
        final_surface = pygame.Surface((text_surface.get_width() + outline_width * 2, text_surface.get_height() + outline_width * 2), pygame.SRCALPHA)
        positions = [(0, 0), (outline_width, 0), (outline_width * 2, 0), (0, outline_width), (outline_width * 2, outline_width), (0, outline_width * 2), (outline_width, outline_width * 2), (outline_width * 2, outline_width * 2)]
        for pos in positions: final_surface.blit(outline_surface, pos)
        final_surface.blit(text_surface, (outline_width, outline_width))
        return final_surface

    def _draw(self):
        self.background.draw()

        # Painel de Fundo
        largura_painel = self.window.width * 0.85
        altura_painel = self.window.height * 0.7
        pos_x_painel = (self.window.width - largura_painel) / 2
        # --- 2. PAINEL E TEXTOS MAIS PARA CIMA ---
        pos_y_painel = 100 # ALTERADO de 120 para 100
        painel_rect = pygame.Rect(pos_x_painel, pos_y_painel, largura_painel, altura_painel)

        painel_surface = pygame.Surface((largura_painel, altura_painel), pygame.SRCALPHA)
        painel_surface.fill((0, 0, 0, 180))
        self.window.screen.blit(painel_surface, painel_rect.topleft)

        # Título Principal
        # --- 1. TÍTULO "CONQUISTAS" MAIS PARA CIMA ---
        title_surf = self._render_text_with_outline(self.font_title, "CONQUISTAS", self.color_title, self.color_outline)
        title_rect = title_surf.get_rect(center=(self.window.width / 2, 60)) # ALTERADO de 80 para 60
        self.window.screen.blit(title_surf, title_rect)

        # Lista de Conquistas
        y_pos = painel_rect.y + 40
        x_pos_texto = painel_rect.x + 50

        for ach_key, ach_data in self.achievement_manager.achievements.items():
            is_unlocked = ach_data["unlocked"]
            cor_titulo_ach = self.color_unlocked if is_unlocked else self.color_locked
            cor_desc = self.color_text if is_unlocked else C.COLOR_GRAY_DARK
            
            progress_text = ""
            stats = self.achievement_manager.stats
            if not is_unlocked:
                if ach_key == "collect_100_bags":
                    progress_text = f" ({stats['total_money_bags']}/100)"
                elif ach_key == "dodge_500_cars":
                    progress_text = f" ({stats['total_cars_dodged']}/500)"
                elif ach_key == "dodge_500_bullets":
                     progress_text = f" ({stats['total_bullets_dodged']}/500)"

            title_surf = self._render_text_with_outline(self.font_ach_title, ach_data["title"].upper(), cor_titulo_ach, self.color_outline)
            desc_surf = self.font_ach_desc.render(ach_data["desc"] + progress_text, True, cor_desc)
            
            self.window.screen.blit(title_surf, (x_pos_texto, y_pos))
            self.window.screen.blit(desc_surf, (x_pos_texto, y_pos + 30))
            
            y_pos += 80

        # Botão "VOLTAR"
        mouse_pos = self.mouse.get_position()
        button_color = self.color_hover if self.back_button_rect.collidepoint(mouse_pos) else self.color_text
        button_surf = self._render_text_with_outline(self.font_button, "VOLTAR", button_color, self.color_outline)
        button_rect = button_surf.get_rect(center=self.back_button_rect.center)
        self.window.screen.blit(button_surf, button_rect)

    def _check_input(self):
        self.last_click_time += self.window.delta_time()

        if self.mouse.is_button_pressed(1) and self.last_click_time > self.click_cooldown:
            self.last_click_time = 0
            if self.back_button_rect.collidepoint(self.mouse.get_position()):
                self.game.change_state("MENU")
        
        if self.keyboard.key_pressed("ESC"):
            self.game.change_state("MENU")

    def run(self):
        self._check_input()
        self._draw()