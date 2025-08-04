import pygame
import string
from PPlay.mouse import Mouse
import constants as C

class GameOver:
    """
    Gere a cena de Game Over, mostrando estatísticas e capturando
    o nome do jogador para o ranking.
    """
    def __init__(self, window, game, asset_manager):
        self.window = window
        self.game = game
        self.keyboard = self.window.get_keyboard()
        
        self.font_title = asset_manager.get_font("pricedown_title")
        self.font_info = asset_manager.get_font("pricedown_info")
        self.font_input = asset_manager.get_font("pricedown_input")
        
        self.color_title = C.COLOR_RED
        self.color_text = C.COLOR_WHITE
        self.color_box = C.COLOR_GRAY_LIGHT
        self.color_saved = C.COLOR_GRAY_DARK

        self.player_name = ""
        self.input_box_rect = pygame.Rect(0, 0, 300, 50)
        self.input_box_rect.center = (self.window.width / 2, 325)
        self.score_saved = False

        self.final_score = 0
        self.time_survived = 0
        
        # --- Lógica de Input de Texto ---
        self.keys_to_check = list(string.ascii_lowercase + string.digits) + ["backspace", "space", "enter"]
        self.last_key_state = {key: False for key in self.keys_to_check}

    def set_final_stats(self, score, time):
        """Recebe e armazena as estatísticas finais da partida."""
        self.final_score = score
        self.time_survived = time
        self.player_name = ""
        self.score_saved = False
        self.last_key_state = {key: False for key in self.keys_to_check}

    def _handle_text_input(self):
        """Gere o input do teclado para a caixa de nome."""
        if self.score_saved: return

        for key in self.keys_to_check:
            key_is_pressed = self.keyboard.key_pressed(key)
            if key_is_pressed and not self.last_key_state[key]:
                if key == "backspace":
                    self.player_name = self.player_name[:-1]
                elif key == "space":
                    if len(self.player_name) < 12: self.player_name += " "
                elif key == "enter":
                    self.save_score_and_exit()
                elif len(self.player_name) < 12:
                    self.player_name += key.upper()
            self.last_key_state[key] = key_is_pressed

    def save_score_and_exit(self):
        """Salva a pontuação e o tempo no ficheiro e muda para a tela de ranking."""
        if self.score_saved: return
        
        name_to_save = self.player_name.strip() if self.player_name.strip() else "JOGADOR"
        try:
            with open("ranking.txt", "a") as file:
                file.write(f"{name_to_save}#{self.final_score}#{self.time_survived:.2f}\n")
            self.score_saved = True
            self.game.change_state("RANKING")
        except Exception as e:
            print(f"Erro ao salvar o ranking: {e}")

    def _draw(self):
        """Desenha todos os elementos da tela."""
        self.window.set_background_color(C.COLOR_BACKGROUND)

        title_surf = self.font_title.render("Se Ferrou!!!", True, self.color_title)
        title_rect = title_surf.get_rect(center=(self.window.width / 2, 80))
        self.window.screen.blit(title_surf, title_rect)

        score_text = f"PONTOS: {self.final_score}"
        time_text = f"TEMPO: {self.time_survived:.2f}s"
        score_surf = self.font_info.render(score_text, True, self.color_text)
        time_surf = self.font_info.render(time_text, True, self.color_text)
        score_rect = score_surf.get_rect(center=(self.window.width / 2, 180))
        time_rect = time_surf.get_rect(center=(self.window.width / 2, 230))
        self.window.screen.blit(score_surf, score_rect)
        self.window.screen.blit(time_surf, time_rect)

        pygame.draw.rect(self.window.screen, self.color_box, self.input_box_rect, 2)
        input_surf = self.font_input.render(self.player_name, True, self.color_text)
        input_rect = input_surf.get_rect(midleft=(self.input_box_rect.x + 10, self.input_box_rect.centery))
        self.window.screen.blit(input_surf, input_rect)

        save_text = "Pressione ENTER para Salvar e ver o Ranking" if not self.score_saved else "PONTUAÇÃO SALVA!"
        save_color = self.color_text if not self.score_saved else self.color_saved
        save_surf = self.font_input.render(save_text, True, save_color)
        save_rect = save_surf.get_rect(center=(self.window.width / 2, 450))
        self.window.screen.blit(save_surf, save_rect)

    def run(self):
        """Loop principal da cena de Game Over."""
        self._handle_text_input()
        self._draw()