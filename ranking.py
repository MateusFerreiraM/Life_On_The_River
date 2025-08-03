# ranking.py
# Exibe a tela de ranking com um visual renovado e interativo.

import pygame
from PPlay.gameimage import GameImage
from PPlay.mouse import Mouse

class Ranking:
    def __init__(self, window, game):
        """Inicializa a cena de ranking."""
        self.window = window
        self.game = game
        self.mouse = Mouse()
        
        self.background = GameImage("Assets/Images/menu_background.png")
        
        try:
            self.font_title = pygame.font.Font("Assets/Fonts/pricedown bl.ttf", 80)
            self.font_score = pygame.font.Font("Assets/Fonts/pricedown bl.ttf", 45)
            self.font_button = pygame.font.Font("Assets/Fonts/pricedown bl.ttf", 40)
        except FileNotFoundError:
            self.font_title = pygame.font.Font(None, 90)
            self.font_score = pygame.font.Font(None, 55)
            self.font_button = pygame.font.Font(None, 50)
        
        self.color_title = (255, 215, 0)
        self.color_text = (255, 255, 255)
        self.color_hover = (255, 215, 0)
        self.color_outline = (0, 0, 0) # Cor preta para o contorno

        self.back_button_rect = pygame.Rect(0, 0, 200, 50)
        self.back_button_rect.center = (self.window.width / 2, self.window.height - 70)
        
        try:
            self.trophy_icon = pygame.image.load("Assets/Images/trophy.png")
            self.trophy_icon = pygame.transform.scale(self.trophy_icon, (40, 40))
        except FileNotFoundError:
            self.trophy_icon = None

        self.ranking_info = []

    def _render_text_with_outline(self, font, text, color, outline_color, outline_width=2):
        """
        Função auxiliar para renderizar texto com um contorno.
        Desenha o texto do contorno várias vezes, deslocado, e depois o texto principal por cima.
        """
        text_surface = font.render(text, True, color)
        outline_surface = font.render(text, True, outline_color)
        
        # Cria uma superfície final um pouco maior para acomodar o contorno
        final_surface = pygame.Surface((text_surface.get_width() + outline_width * 2, text_surface.get_height() + outline_width * 2), pygame.SRCALPHA)
        
        # Desenha o contorno em várias posições (em cima, em baixo, dos lados, etc.)
        positions = [
            (0, 0), (outline_width, 0), (outline_width * 2, 0),
            (0, outline_width), (outline_width * 2, outline_width),
            (0, outline_width * 2), (outline_width, outline_width * 2), (outline_width * 2, outline_width * 2)
        ]
        for pos in positions:
            final_surface.blit(outline_surface, pos)
            
        # Desenha o texto principal no centro
        final_surface.blit(text_surface, (outline_width, outline_width))
        
        return final_surface

    def _load_ranking(self):
        """Carrega e formata os dados do ranking a partir do ficheiro."""
        self.ranking_info = []
        scores = []
        try:
            with open("ranking.txt", 'r') as file:
                lines = file.read().splitlines()
            scores = [(line.split('#')[0], int(line.split('#')[1])) for line in lines if '#' in line]
            scores.sort(key=lambda x: x[1], reverse=True)
        except (FileNotFoundError, ValueError, IndexError):
            scores = []

        if not scores:
            self.ranking_info.append("NENHUMA PONTUAÇÃO")
            return

        top_5 = scores[:5]
        for i, (name, score) in enumerate(top_5):
            text = f"{i+1}º   {name.upper():<12}   {score} PONTOS"
            self.ranking_info.append(text)

    def _draw(self):
        """Desenha todos os elementos da tela de ranking."""
        self.background.draw()

        # Título com contorno
        title_surf = self._render_text_with_outline(self.font_title, "RANKING", self.color_title, self.color_outline)
        title_rect = title_surf.get_rect(center=(self.window.width / 2, 80))
        self.window.screen.blit(title_surf, title_rect)

        # Pontuações com contorno
        y_pos = 200
        for i, text in enumerate(self.ranking_info):
            score_surf = self._render_text_with_outline(self.font_score, text, self.color_text, self.color_outline)
            score_rect = score_surf.get_rect(center=(self.window.width / 2, y_pos))
            self.window.screen.blit(score_surf, score_rect)
            
            if self.trophy_icon and i < 3 and "NENHUMA PONTUAÇÃO" not in text:
                trophy_rect = self.trophy_icon.get_rect(centery=score_rect.centery)
                trophy_rect.right = score_rect.left - 20
                self.window.screen.blit(self.trophy_icon, trophy_rect)
                
            y_pos += 70

        # Botão de Voltar com contorno
        mouse_pos = self.mouse.get_position()
        button_color = self.color_hover if self.back_button_rect.collidepoint(mouse_pos) else self.color_text
        button_surf = self._render_text_with_outline(self.font_button, "VOLTAR", button_color, self.color_outline)
        
        button_rect = button_surf.get_rect(center=self.back_button_rect.center)
        self.window.screen.blit(button_surf, button_rect)

    def _check_clicks(self):
        """Verifica o clique no botão de voltar."""
        if self.mouse.is_button_pressed(1):
            if self.back_button_rect.collidepoint(self.mouse.get_position()):
                self.game.change_state("MENU")

    def run(self):
        """Executa a lógica da cena de ranking a cada frame."""
        self._load_ranking()
        self._check_clicks()
        self._draw()