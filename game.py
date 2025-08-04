import pygame
from PPlay.window import Window
import constants as C
from asset_manager import AssetManager
from menu import Menu
from gameplay import Gameplay
from ranking import Ranking
from game_over import GameOver

class Game:
    """
    Classe principal que gere a janela, o loop de jogo e os estados (cenas).
    """
    def __init__(self):
        # --- Inicialização do Pygame e da Janela ---
        pygame.mixer.pre_init(44100, -16, 2, 512)
        pygame.init()
        pygame.mixer.set_num_channels(8) # Define o número de canais de som
        self.window = Window(C.SCREEN_WIDTH, C.SCREEN_HEIGHT)
        self.window.set_title(C.WINDOW_TITLE)
        
        # --- Gestor de Assets ---
        self.asset_manager = AssetManager()

        # O estado inicial do jogo é o menu principal.
        self.game_state = "MENU"
        self.asset_manager.play_music("menu")

        # --- Instâncias das Cenas ---
        self.menu = Menu(self.window, self, self.asset_manager)
        self.gameplay = Gameplay(self.window, self, self.asset_manager)
        self.ranking = Ranking(self.window, self, self.asset_manager)
        self.game_over = GameOver(self.window, self, self.asset_manager)

    def run(self):
        """Inicia e mantém o loop principal do jogo."""
        while True:
            if self.game_state == "MENU":
                self.menu.run()
            elif self.game_state == "PLAYING":
                self.gameplay.run()
            elif self.game_state == "RANKING":
                self.ranking.run()
            elif self.game_state == "GAME_OVER":
                self.game_over.run()
            elif self.game_state == "EXIT":
                break
            
            self.window.update()

    def change_state(self, new_state, score=0, time=0):
        """
        Método central para a transição entre cenas.
        """
        # --- Lógica para parar sons do estado anterior ---
        if self.game_state == "PLAYING":
            self.asset_manager.stop_siren_loop() # ALTERADO

        # --- Mudar para o novo estado ---
        self.game_state = new_state
        
        # --- Lógica para iniciar sons do novo estado ---
        if new_state == "PLAYING":
            self.asset_manager.stop_music()
            self.asset_manager.play_siren_loop() # ALTERADO
            self.gameplay.reset()
            
        elif new_state == "GAME_OVER":
            self.asset_manager.play_sound("lose")
            self.game_over.set_final_stats(score, time)

        elif new_state == "MENU":
            self.asset_manager.play_music("menu")

        elif new_state == "RANKING":
             self.asset_manager.play_music("menu")