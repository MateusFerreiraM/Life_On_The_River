import pygame
from PPlay.gameimage import GameImage
from PPlay.mouse import Mouse

class Menu:
    """
    Gere a cena do menu principal, incluindo o título e os botões.
    """
    def __init__(self, window, game):
        self.window = window
        self.game = game
        self.mouse = Mouse()

        self.background = GameImage("Assets/Images/menu_background.png")
        try:
            self.font_gametitle = pygame.font.Font("Assets/Fonts/pricedown bl.ttf", 100)
            self.font_button = pygame.font.Font("Assets/Fonts/pricedown bl.ttf", 50)
        except FileNotFoundError:
            self.font_gametitle = pygame.font.Font(None, 120)
            self.font_button = pygame.font.Font(None, 60)
        
        self.color_title = (255, 215, 0)
        self.color_text = (255, 255, 255)
        self.color_hover = (255, 215, 0)
        self.color_outline = (0, 0, 0)

        self.opcoes_menu = ["Jogar", "Ranking", "Sair"]
        self.buttons = {}
        self._create_buttons()
        
        self.click_cooldown = 0.5
        self.last_click_time = 0

    def _render_text_with_outline(self, font, text, color, outline_color, outline_width=2):
        """Função auxiliar para renderizar texto com um contorno para legibilidade."""
        text_surface = font.render(text, True, color)
        outline_surface = font.render(text, True, outline_color)
        final_surface = pygame.Surface((text_surface.get_width() + outline_width * 2, text_surface.get_height() + outline_width * 2), pygame.SRCALPHA)
        positions = [(0, 0), (outline_width, 0), (outline_width * 2, 0), (0, outline_width), (outline_width * 2, outline_width), (0, outline_width * 2), (outline_width, outline_width * 2), (outline_width * 2, outline_width * 2)]
        for pos in positions: final_surface.blit(outline_surface, pos)
        final_surface.blit(text_surface, (outline_width, outline_width))
        return final_surface

    def _create_buttons(self):
        """Cria as áreas retangulares para os botões do menu."""
        y_pos = self.window.height / 2
        for texto in self.opcoes_menu:
            rect = pygame.Rect(0, 0, 300, 60)
            rect.center = (self.window.width / 2, y_pos)
            self.buttons[texto] = rect
            y_pos += 80

    def _desenhar(self):
        """Desenha todos os elementos visuais do menu."""
        self.background.draw()

        title_surf = self._render_text_with_outline(self.font_gametitle, "Life On The River", self.color_title, self.color_outline, 3)
        title_rect = title_surf.get_rect(center=(self.window.width / 2, 130))
        self.window.screen.blit(title_surf, title_rect)

        mouse_pos = self.mouse.get_position()
        for texto, rect in self.buttons.items():
            button_color = self.color_hover if rect.collidepoint(mouse_pos) else self.color_text
            button_surf = self._render_text_with_outline(self.font_button, texto.upper(), button_color, self.color_outline)
            button_rect = button_surf.get_rect(center=rect.center)
            self.window.screen.blit(button_surf, button_rect)

    def _verificar_cliques(self):
        """Verifica cliques do rato nos botões e muda o estado do jogo."""
        self.last_click_time += self.window.delta_time()

        if self.mouse.is_button_pressed(1) and self.last_click_time > self.click_cooldown:
            self.last_click_time = 0
            mouse_pos = self.mouse.get_position()
            
            if self.buttons["Jogar"].collidepoint(mouse_pos):
                self.game.change_state("PLAYING")
            elif self.buttons["Ranking"].collidepoint(mouse_pos):
                self.game.change_state("RANKING")
            elif self.buttons["Sair"].collidepoint(mouse_pos):
                self.game.change_state("EXIT")

    def run(self):
        """Loop principal da cena do menu."""
        self._desenhar()
        self._verificar_cliques()