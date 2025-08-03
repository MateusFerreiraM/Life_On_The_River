# scenery.py
# Gerencia o fundo de tela contínuo (scrolling).

from PPlay.sprite import Sprite

class Scenery:
    def __init__(self, window, image_path1, image_path2):
        """Inicializa o cenário com duas imagens diferentes que se alternarão."""
        self.bg1 = Sprite(image_path1)
        self.bg2 = Sprite(image_path2)
        
        self.bg1.x = 0
        self.bg2.x = self.bg1.width

    def update(self, move_delta):
        """Move o cenário para a esquerda com base no deslocamento recebido."""
        self.bg1.x -= move_delta
        self.bg2.x -= move_delta
        
        if self.bg1.x <= -self.bg1.width:
            self.bg1.x = self.bg2.x + self.bg2.width - 1

        if self.bg2.x <= -self.bg2.width:
            self.bg2.x = self.bg1.x + self.bg1.width - 1
            
    def draw(self):
        """Desenha as duas imagens de fundo na tela."""
        self.bg1.draw()
        self.bg2.draw()