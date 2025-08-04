import pygame
from PPlay.gameimage import GameImage
from PPlay.mouse import Mouse
import constants as C

class InstructionsScene:
    """
    Exibe a tela com as instruções de como jogar.
    """
    def __init__(self, window, game, asset_manager):
        self.window = window
        self.game = game
        self.mouse = Mouse()
        self.keyboard = self.window.get_keyboard()

        self.background = GameImage(C.IMG_MENU_BACKGROUND)
        
        self.font_title = asset_manager.get_font("pricedown_title")
        self.font_header = asset_manager.get_font("pricedown_header")
        self.font_text = asset_manager.get_font("pricedown_instructions_text")
        self.font_button = asset_manager.get_font("pricedown_button")
        
        self.color_title = C.COLOR_GOLD
        self.color_text = C.COLOR_WHITE
        self.color_hover = C.COLOR_GOLD
        self.color_outline = C.COLOR_BLACK

        self.back_button_rect = pygame.Rect(0, 0, 200, 50)
        self.back_button_rect.center = (self.window.width / 2, self.window.height - 70)
        
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

    # --- NOVA FUNÇÃO PARA QUEBRAR O TEXTO ---
    def _wrap_text(self, text, font, max_width):
        """Quebra o texto em múltiplas linhas se ele for maior que a largura máxima."""
        words = text.split(' ')
        lines = []
        current_line = ""
        for word in words:
            test_line = current_line + word + " "
            if font.size(test_line)[0] < max_width:
                current_line = test_line
            else:
                lines.append(current_line)
                current_line = word + " "
        lines.append(current_line)
        return lines

    def _draw(self):
        self.background.draw()

        # Painel de Fundo
        largura_painel = self.window.width * 0.8
        altura_painel = self.window.height * 0.6
        pos_x_painel = (self.window.width - largura_painel) / 2
        pos_y_painel = 120
        painel_rect = pygame.Rect(pos_x_painel, pos_y_painel, largura_painel, altura_painel)

        painel_surface = pygame.Surface((largura_painel, altura_painel), pygame.SRCALPHA)
        painel_surface.fill((0, 0, 0, 180))
        self.window.screen.blit(painel_surface, painel_rect.topleft)

        # Título Principal
        title_surf = self._render_text_with_outline(self.font_title, "COMO JOGAR", self.color_title, self.color_outline)
        title_rect = title_surf.get_rect(center=(self.window.width / 2, 80))
        self.window.screen.blit(title_surf, title_rect)

        # Textos de Instrução
        y_pos = painel_rect.y + 40
        x_pos_texto = painel_rect.x + 40
        largura_max_texto = largura_painel - 80
        
        # --- SUBTÍTULOS EM AMARELO E TEXTO COM QUEBRA DE LINHA ---
        
        # Objetivo
        header1_surf = self._render_text_with_outline(self.font_header, "OBJETIVO", self.color_title, self.color_outline)
        self.window.screen.blit(header1_surf, (x_pos_texto, y_pos))
        y_pos += 40
        
        texto_objetivo = "Desvie dos obstaculos e colete os sacos de dinheiro para maximizar sua pontuacao e desbloquear conquistas."
        linhas_objetivo = self._wrap_text(texto_objetivo, self.font_text, largura_max_texto)
        
        for line in linhas_objetivo:
            text1_surf = self.font_text.render(line, True, self.color_text)
            self.window.screen.blit(text1_surf, (x_pos_texto, y_pos))
            y_pos += 25
        y_pos += 40

        # Controles
        header2_surf = self._render_text_with_outline(self.font_header, "CONTROLES", self.color_title, self.color_outline)
        self.window.screen.blit(header2_surf, (x_pos_texto, y_pos))
        y_pos += 40

        text2_surf = self.font_text.render("- Pressione a tecla CIMA para PULAR.", True, self.color_text)
        self.window.screen.blit(text2_surf, (x_pos_texto, y_pos))
        y_pos += 35

        text3_surf = self.font_text.render("- Pressione a tecla BAIXO para AGACHAR.", True, self.color_text)
        self.window.screen.blit(text3_surf, (x_pos_texto, y_pos))
        y_pos += 35

        text4_surf = self.font_text.render("- Pressione ESC a qualquer momento para PAUSAR.", True, self.color_text)
        self.window.screen.blit(text4_surf, (x_pos_texto, y_pos))

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