from PPlay.window import*
from PPlay.gameimage import *
from PPlay.sprite import *
from PPlay.mouse import Mouse
from PPlay.keyboard import *
import variables

class Menu():
    def __init__(self, janela):
        self.janela = janela
        self.mouse = Mouse()
        self.titulo_menu = Sprite("Titulo_menu_projeto_final.png")
        self.jogar_menu = Sprite("jogar_menu_projetofinal.png")
        self.ranking_menu = Sprite("ranking_menu_projetofinal.png")
        self.sair_menu = Sprite("sair_menu_projetofinal.png")
        self.teclado = janela.get_keyboard()
        self.titulo_menu.set_position(140,1)
        self.jogar_menu.set_position(50,490)
        self.ranking_menu.set_position(350,490)
        self.sair_menu.set_position(750,490)
        if variables.game_state == 1:
            self._draw()
        self.menu_principal()
        
    def _draw(self):
        self.janela.set_background_color([0,0,0])
        self.titulo_menu.draw()
        self.jogar_menu.draw()
        self.ranking_menu.draw()
        self.sair_menu.draw()
        
    def menu_principal(self):
        if (self.mouse.is_button_pressed(1)):
            if (self.mouse.is_over_object(self.jogar_menu)):
                variables.game_state = 2
        if (self.mouse.is_button_pressed(1)):
            if (self.mouse.is_over_object(self.ranking_menu)):
                variables.game_state = 3
        if (self.mouse.is_button_pressed(1)):
            if (self.mouse.is_over_object(self.sair_menu)):
                variables.game_state = 4
