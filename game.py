from PPlay.window import Window
from menu import Menu
from gameplay import Gameplay
from ranking import Ranking

class Game:
    def __init__(self):
        """Inicializa a janela e os componentes principais do jogo."""
        self.window = Window(1000, 600)
        self.window.set_title("Fuga no Rio")

        self.game_state = "MENU"

        self.menu = Menu(self.window, self)
        self.gameplay = Gameplay(self.window, self)
        self.ranking = Ranking(self.window, self)

    def run(self):
        """O loop principal do jogo. Executa continuamente até a janela ser fechada."""
        while True:
            if self.game_state == "MENU":
                self.menu.run()
            elif self.game_state == "PLAYING":
                self.gameplay.run()
            elif self.game_state == "RANKING":
                self.ranking.run()
            elif self.game_state == "EXIT":
                break
            
            self.window.update()

    def change_state(self, new_state):
        """
        Método central para mudar de cena.
        É chamado pelas próprias cenas. Ex: o menu chama game.change_state("PLAYING").
        """
        self.game_state = new_state
        
        if new_state == "PLAYING":
            self.gameplay.reset()

