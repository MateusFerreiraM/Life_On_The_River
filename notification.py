# Ficheiro: notification.py (COMPLETO E ATUALIZADO)
import pygame
import constants as C

class Notification:
    """
    Exibe uma notificação na tela por um tempo limitado.
    """
    def __init__(self, text, asset_manager, duration=4.0):
        self.text = text
        self.duration = duration
        self.timer = 0
        self.is_active = True
        
        self.font = asset_manager.get_font("pricedown_header")
        self.color_bg = (*C.COLOR_BLACK, 200)
        self.color_title = C.COLOR_GOLD
        self.color_text = C.COLOR_WHITE
        
        # ALTERADO: Posição inicial no centro para animação de subida
        self.start_y = C.SCREEN_HEIGHT / 2
        self.end_y = 50
        self.y_pos = self.start_y
        
        self.alpha = 0

    def update(self, delta_time):
        if not self.is_active:
            return
            
        self.timer += delta_time
        
        # Animação de entrada (fade in e subida)
        if self.timer < 0.5:
            progress = self.timer / 0.5
            self.alpha = 255 * progress
            self.y_pos = self.start_y - (self.start_y - self.end_y) * progress
        else:
            self.alpha = 255
            self.y_pos = self.end_y

        # Animação de saída (fade out)
        if self.timer > self.duration - 1:
            self.alpha = max(0, 255 * (self.duration - self.timer))
        
        if self.timer >= self.duration:
            self.is_active = False

    def draw(self, window):
        if not self.is_active:
            return

        title_surf = self.font.render("CONQUISTA DESBLOQUEADA!", True, self.color_title)
        text_surf = self.font.render(self.text, True, self.color_text)
        
        panel_width = max(title_surf.get_width(), text_surf.get_width()) + 40
        panel_height = title_surf.get_height() + text_surf.get_height() + 20
        panel_x = (window.width - panel_width) / 2
        
        panel_surface = pygame.Surface((panel_width, panel_height), pygame.SRCALPHA)
        panel_surface.fill(self.color_bg)
        
        panel_surface.blit(title_surf, ((panel_width - title_surf.get_width()) / 2, 10))
        panel_surface.blit(text_surf, ((panel_width - text_surf.get_width()) / 2, 15 + title_surf.get_height()))
        
        panel_surface.set_alpha(self.alpha)
        
        window.screen.blit(panel_surface, (panel_x, self.y_pos))