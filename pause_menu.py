# pause_menu.py
# Gere a tela de pausa que aparece sobre a cena de gameplay.

import pygame
from PPlay.mouse import Mouse

class PauseMenu:
    def __init__(self, window, gameplay_instance):
        """Inicializa o menu de pausa."""
        self.window = window
        self.gameplay = gameplay_instance # Referência à cena de gameplay para chamar os seus métodos
        self.mouse = Mouse()
        
        try:
            self.font_title = pygame.font.Font("Assets/Fonts/pricedown bl.ttf", 80)
            self.font_button = pygame.font.Font("Assets/Fonts/pricedown bl.ttf", 40)
        except FileNotFoundError:
            self.font_title = pygame.font.Font(None, 90)
            self.font_button = pygame.font.Font(None, 50)
        
        self.color_title = (255, 215, 0)
        self.color_text = (255, 255, 255)
        self.color_hover = (255, 215, 0)

        # Overlay semi-transparente para escurecer o fundo
        self.overlay = pygame.Surface((self.window.width, self.window.height), pygame.SRCALPHA)
        self.overlay.fill((0, 0, 0, 150)) # Preto com 150 de transparência (de 255)

        self.buttons = {}
        self.button_surfaces = {}
        self._create_buttons()

    def _create_buttons(self):
        """Cria os retângulos e pré-renderiza os textos para os botões."""
        button_texts = {
            "continue": "CONTINUAR",
            "restart": "RECOMEÇAR",
            "main_menu": "VOLTAR AO MENU"
        }
        
        y_pos = self.window.height / 2 - 50
        for key, text in button_texts.items():
            rect = pygame.Rect(0, 0, 400, 50)
            rect.center = (self.window.width / 2, y_pos)
            self.buttons[key] = rect
            
            text_normal = self.font_button.render(text, True, self.color_text)
            text_hover = self.font_button.render(text, True, self.color_hover)
            self.button_surfaces[key] = {"normal": text_normal, "hover": text_hover}
            y_pos += 80

    def _check_clicks(self):
        """Verifica cliques nos botões e chama os métodos correspondentes na cena de gameplay."""
        if self.mouse.is_button_pressed(1):
            mouse_pos = self.mouse.get_position()
            
            if self.buttons["continue"].collidepoint(mouse_pos):
                self.gameplay.unpause()
            elif self.buttons["restart"].collidepoint(mouse_pos):
                self.gameplay.restart()
            elif self.buttons["main_menu"].collidepoint(mouse_pos):
                self.gameplay.go_to_main_menu()

    def _draw(self):
        """Desenha o overlay e os elementos do menu de pausa."""
        self.window.screen.blit(self.overlay, (0, 0))

        title_surf = self.font_title.render("PAUSA", True, self.color_title)
        title_rect = title_surf.get_rect(center=(self.window.width / 2, 150))
        self.window.screen.blit(title_surf, title_rect)

        mouse_pos = self.mouse.get_position()
        for key, rect in self.buttons.items():
            text_surf = self.button_surfaces[key]["hover"] if rect.collidepoint(mouse_pos) else self.button_surfaces[key]["normal"]
            text_rect = text_surf.get_rect(center=rect.center)
            self.window.screen.blit(text_surf, text_rect)

    def run(self):
        """Executa o loop do menu de pausa."""
        self._check_clicks()
        self._draw()