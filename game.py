import pygame
from PPlay.window import Window
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
        pygame.init()
        self.window = Window(1000, 600)
        self.window.set_title("Fuga no Rio")
        
        # O estado inicial do jogo é o menu principal.
        self.game_state = "MENU"

        # --- Instâncias das Cenas ---
        # Cada cena do jogo é representada por um objeto.
        self.menu = Menu(self.window, self)
        self.gameplay = Gameplay(self.window, self)
        self.ranking = Ranking(self.window, self)
        self.game_over = GameOver(self.window, self)

    def run(self):
        """Inicia e mantém o loop principal do jogo."""
        while True:
            # --- Máquina de Estados ---
            # Verifica o estado atual e executa a cena correspondente.
            if self.game_state == "MENU":
                self.menu.run()
            elif self.game_state == "PLAYING":
                self.gameplay.run()
            elif self.game_state == "RANKING":
                self.ranking.run()
            elif self.game_state == "GAME_OVER":
                self.game_over.run()
            elif self.game_state == "EXIT":
                break  # Quebra o loop para encerrar o jogo.
            
            # Atualiza a janela no final de cada frame.
            self.window.update()

    def change_state(self, new_state, score=0, time=0):
        """
        Método central para a transição entre cenas. Pode passar dados
        como pontuação e tempo para a próxima cena.
        """
        self.game_state = new_state
        
        if new_state == "PLAYING":
            self.gameplay.reset()
        elif new_state == "GAME_OVER":
            self.game_over.set_final_stats(score, time)