from PPlay.window import *
from PPlay.sprite import *
from PPlay.gameimage import *
import pygame
import variables

class Ranking(object):
    def __init__(self, janela):
        self.janela = janela
        self.janela.set_background_color([0,0,0])
        self.teclado = self.janela.get_keyboard()
        self.ranking = None
        self.twidth = [50, 50, 50, 50, 50]
        with open("ranking.txt", 'r') as pontos:
            self.ranking = pontos.read().split('\n')
            self.ranking.pop(-1)

        self.ranking = [(e.split('#')[0], e.split('#')[1]) for e in self.ranking]
        self.ranking.sort(key=lambda x: int(x[1]), reverse=True)
        for i in range(5 if len(self.ranking) >= 5 else len(self.ranking)):
            text = f"{i+1}º - {self.ranking[i][0]} - {self.ranking[i][1]} pontos"
            font = pygame.font.Font("pricedown bl.ttf", 50)
            self.ranking[i] = font.render(text, True, (255, 255, 255))
            self.twidth[i] = font.size(text)[0]
        pass
 
    def update(self):
        for i in range(5 if len(self.ranking) >= 5 else len(self.ranking)):
            self.janela.screen.blit(self.ranking[i], [1000/2-(self.twidth[i])/2, 600/6 - 50 + (i*100)])
        if self.teclado.key_pressed("ESC"):
            variables.game_state = 1
        pass
