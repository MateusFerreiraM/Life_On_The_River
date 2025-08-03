# game.py
# Gerencia a janela, o loop principal e as diferentes cenas do jogo.

import pygame
from PPlay.window import Window
from menu import Menu
from gameplay import Gameplay
from ranking import Ranking
from game_over import GameOver # Importa a nova cena

class Game:
    def __init__(self):
        """Inicializa a janela e os componentes principais do jogo."""
        pygame.init() # Inicializa o pygame para o input de texto
        self.window = Window(1000, 600)
        self.window.set_title("Fuga no Rio")
        
        self.game_state = "MENU"

        # Cria instâncias de todas as cenas
        self.menu = Menu(self.window, self)
        self.gameplay = Gameplay(self.window, self)
        self.ranking = Ranking(self.window, self)
        self.game_over = GameOver(self.window, self) # Cria a instância do Game Over

    def run(self):
        """O loop principal do jogo."""
        while True:
            if self.game_state == "MENU":
                self.menu.run()
            elif self.game_state == "PLAYING":
                self.gameplay.run()
            elif self.game_state == "RANKING":
                self.ranking.run()
            elif self.game_state == "GAME_OVER": # Adiciona o novo estado
                self.game_over.run()
            elif self.game_state == "EXIT":
                break
            
            self.window.update()

    def change_state(self, new_state, score=0, time=0):
        """
        Método central para mudar de cena, agora pode passar dados.
        """
        self.game_state = new_state
        
        if new_state == "PLAYING":
            self.gameplay.reset()
        elif new_state == "GAME_OVER":
            # Passa as estatísticas para a tela de Game Over
            self.game_over.set_final_stats(score, time)