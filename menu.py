import pygame
from PPlay.gameimage import GameImage
from PPlay.mouse import Mouse

class Menu:
    def __init__(self, window, game):
        """Inicializa a cena do menu."""
        self.window = window
        self.game = game
        self.mouse = Mouse()

        self.background = GameImage("Assets/Images/menu_background.png")

        try:
            self.font = pygame.font.Font("Assets/Fonts/pricedown bl.ttf", 50)
        except FileNotFoundError:
            print("AVISO: Fonte 'Assets/Fonts/pricedown bl.ttf' não encontrada. Usando fonte padrão.")
            self.font = pygame.font.Font(None, 60)
        
        self.cor_texto_padrao = (255, 255, 255)
        self.cor_texto_hover = (255, 215, 0)

        self.opcoes_menu = ["Jogar", "Ranking", "Sair"]
        self.botoes = []
        self.botoes_renderizados = []
        
        self._criar_botoes()

    def _criar_botoes(self):
        """Cria os retângulos e renderiza os textos para cada botão, centralizando-os."""
        padding_vertical = 20
        
        altura_texto = self.font.get_height()
        altura_total_menu = (len(self.opcoes_menu) * altura_texto) + ((len(self.opcoes_menu) - 1) * padding_vertical)
        
        pos_y_inicial = (self.window.height - altura_total_menu) / 2

        for i, texto in enumerate(self.opcoes_menu):
            largura_texto, altura_texto_individual = self.font.size(texto)
            pos_x = (self.window.width - largura_texto) / 2
            pos_y = pos_y_inicial + i * (altura_texto_individual + padding_vertical)
            
            retangulo_botao = pygame.Rect(pos_x, pos_y, largura_texto, altura_texto_individual)
            self.botoes.append(retangulo_botao)

            texto_padrao = self.font.render(texto, True, self.cor_texto_padrao)
            texto_hover = self.font.render(texto, True, self.cor_texto_hover)
            self.botoes_renderizados.append({"padrao": texto_padrao, "hover": texto_hover})

    def _desenhar(self):
        """Desenha todos os elementos do menu na tela."""
        self.background.draw()

        for i, botao_rect in enumerate(self.botoes):
            posicao_mouse = self.mouse.get_position()
            
            if botao_rect.collidepoint(posicao_mouse):
                texto_para_desenhar = self.botoes_renderizados[i]["hover"]
            else:
                texto_para_desenhar = self.botoes_renderizados[i]["padrao"]
            
            self.window.screen.blit(texto_para_desenhar, botao_rect.topleft)

    def _verificar_cliques(self):
        """Verifica se algum botão foi clicado e muda o estado do jogo."""
        if self.mouse.is_button_pressed(1):
            posicao_mouse = self.mouse.get_position()
            
            if self.botoes[0].collidepoint(posicao_mouse):
                self.game.change_state("PLAYING")
            elif self.botoes[1].collidepoint(posicao_mouse):
                self.game.change_state("RANKING")
            elif self.botoes[2].collidepoint(posicao_mouse):
                self.game.change_state("EXIT")

    def run(self):
        """Executa a lógica do menu a cada frame."""
        self._desenhar()
        self._verificar_cliques()