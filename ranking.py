import pygame
from PPlay.gameimage import GameImage
from PPlay.mouse import Mouse

class Ranking:
    """
    Exibe a tela de ranking, lendo e formatando as pontuações salvas.
    """
    def __init__(self, window, game):
        self.window = window
        self.game = game
        self.mouse = Mouse()
        self.keyboard = self.window.get_keyboard()

        self.background = GameImage("Assets/Images/menu_background.png")
        
        try:
            self.font_title = pygame.font.Font("Assets/Fonts/pricedown bl.ttf", 80)
            self.font_header = pygame.font.Font("Assets/Fonts/pricedown bl.ttf", 30)
            self.font_score = pygame.font.Font("Assets/Fonts/pricedown bl.ttf", 40)
            self.font_button = pygame.font.Font("Assets/Fonts/pricedown bl.ttf", 40)
        except FileNotFoundError:
            self.font_title = pygame.font.Font(None, 90)
            self.font_header = pygame.font.Font(None, 40)
            self.font_score = pygame.font.Font(None, 50)
            self.font_button = pygame.font.Font(None, 50)
        
        self.color_title = (255, 215, 0)
        self.color_text = (255, 255, 255)
        self.color_hover = (255, 215, 0)
        self.color_outline = (0, 0, 0)

        self.back_button_rect = pygame.Rect(0, 0, 200, 50)
        self.back_button_rect.center = (self.window.width / 2, self.window.height - 70)
        
        try:
            self.trophy_icon = pygame.image.load("Assets/Images/trophy.png")
            self.trophy_icon = pygame.transform.scale(self.trophy_icon, (40, 40))
        except FileNotFoundError:
            self.trophy_icon = None

        self.ranking_info = []
        
        # Cooldown para o clique do rato
        self.click_cooldown = 0.5
        self.last_click_time = 0

    def _render_text_with_outline(self, font, text, color, outline_color, outline_width=2):
        """Função auxiliar para renderizar texto com contorno."""
        text_surface = font.render(text, True, color)
        outline_surface = font.render(text, True, outline_color)
        final_surface = pygame.Surface((text_surface.get_width() + outline_width * 2, text_surface.get_height() + outline_width * 2), pygame.SRCALPHA)
        positions = [(0, 0), (outline_width, 0), (outline_width * 2, 0), (0, outline_width), (outline_width * 2, outline_width), (0, outline_width * 2), (outline_width, outline_width * 2), (outline_width * 2, outline_width * 2)]
        for pos in positions: final_surface.blit(outline_surface, pos)
        final_surface.blit(text_surface, (outline_width, outline_width))
        return final_surface

    def _load_ranking(self):
        """Lê o ficheiro ranking.txt, ordena e formata os dados."""
        self.ranking_info = []
        scores = []
        try:
            with open("ranking.txt", 'r') as file:
                lines = file.read().splitlines()
            
            for line in lines:
                parts = line.split('#')
                if len(parts) >= 2:
                    name, score = parts[0], int(parts[1])
                    time = float(parts[2]) if len(parts) > 2 else 0.0
                    scores.append((name, score, time))
            
            scores.sort(key=lambda x: x[1], reverse=True)
            
        except (FileNotFoundError, ValueError, IndexError):
            scores = []

        if not scores:
            self.ranking_info.append(("NENHUMA PONTUAÇÃO", "", ""))
            return

        top_4 = scores[:4]
        for i, (name, score, time) in enumerate(top_4):
            pos_text = f"{i+1}º"
            name_text = f"{name.upper()}"
            score_time_text = f"{score} PTS   -   {time:.2f}s"
            self.ranking_info.append((pos_text, name_text, score_time_text))

    def _draw(self):
        """Desenha todos os elementos visuais da cena de ranking."""
        self.background.draw()

        title_surf = self._render_text_with_outline(self.font_title, "RANKING", self.color_title, self.color_outline)
        title_rect = title_surf.get_rect(center=(self.window.width / 2, 80))
        self.window.screen.blit(title_surf, title_rect)

        header_y = 180
        pos_header_surf = self._render_text_with_outline(self.font_header, "POS.", self.color_title, self.color_outline)
        nome_header_surf = self._render_text_with_outline(self.font_header, "NOME", self.color_title, self.color_outline)
        score_header_surf = self._render_text_with_outline(self.font_header, "PONTUAÇÃO E TEMPO", self.color_title, self.color_outline)

        self.window.screen.blit(pos_header_surf, (200, header_y))
        self.window.screen.blit(nome_header_surf, (300, header_y))
        self.window.screen.blit(score_header_surf, (550, header_y))

        y_pos = 240
        for i, (pos, name, score_time) in enumerate(self.ranking_info):
            pos_surf = self._render_text_with_outline(self.font_score, pos, self.color_text, self.color_outline)
            name_surf = self._render_text_with_outline(self.font_score, name, self.color_text, self.color_outline)
            score_time_surf = self._render_text_with_outline(self.font_score, score_time, self.color_text, self.color_outline)

            self.window.screen.blit(pos_surf, (200, y_pos))
            self.window.screen.blit(name_surf, (300, y_pos))
            self.window.screen.blit(score_time_surf, (550, y_pos))
            
            if self.trophy_icon and i < 3 and "NENHUMA PONTUAÇÃO" not in pos:
                trophy_rect = self.trophy_icon.get_rect(centery=y_pos + pos_surf.get_height()/2)
                trophy_rect.right = 200 - 20
                self.window.screen.blit(self.trophy_icon, trophy_rect)
                
            y_pos += 60

        mouse_pos = self.mouse.get_position()
        button_color = self.color_hover if self.back_button_rect.collidepoint(mouse_pos) else self.color_text
        button_surf = self._render_text_with_outline(self.font_button, "VOLTAR", button_color, self.color_outline)
        button_rect = button_surf.get_rect(center=self.back_button_rect.center)
        self.window.screen.blit(button_surf, button_rect)

    def _check_input(self):
        """Verifica o input do utilizador para voltar ao menu."""
        self.last_click_time += self.window.delta_time()

        if self.mouse.is_button_pressed(1) and self.last_click_time > self.click_cooldown:
            self.last_click_time = 0
            if self.back_button_rect.collidepoint(self.mouse.get_position()):
                self.game.change_state("MENU")
        
        if self.keyboard.key_pressed("ESC"):
            self.game.change_state("MENU")

    def run(self):
        """Loop principal da cena de ranking."""
        self._load_ranking()
        self._check_input()
        self._draw()
