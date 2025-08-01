from PPlay.window import *
from PPlay.gameimage import *
from PPlay.mouse import Mouse
import pygame  # Importamos pygame para usar Rect e fontes
import variables

class Menu:
    def __init__(self, janela):
        self.janela = janela
        self.mouse = Mouse()

        # Carrega a nova imagem de fundo
        self.background = GameImage("menu_background.png")

        # Configurações dos botões
        self.font_size = 50
        self.font = pygame.font.Font("pricedown bl.ttf", self.font_size)
        
        # Cores (em formato RGB)
        self.cor_texto_padrao = (255, 255, 255)  # Branco
        self.cor_texto_hover = (255, 215, 0)   # Dourado

        # Textos dos botões
        self.opcoes_menu = ["Jogar", "Ranking", "Sair"]
        self.botoes = []
        self.botoes_renderizados = []
        
        self._criar_botoes()

    def _criar_botoes(self):
        """Cria os retângulos e renderiza os textos para cada botão, centralizando o bloco na tela."""
        self.botoes = []
        self.botoes_renderizados = []
        
        padding_vertical = 20 # Espaço em pixels entre os botões
        
        # Calcula a altura total que o menu vai ocupar
        altura_texto = self.font.get_height()
        altura_total_menu = (len(self.opcoes_menu) * altura_texto) + ((len(self.opcoes_menu) - 1) * padding_vertical)
        
        # Calcula a posição Y inicial para o primeiro botão, para que o bloco todo fique centralizado
        pos_y_inicial = (self.janela.height - altura_total_menu) / 2

        for i, texto in enumerate(self.opcoes_menu):
            # Cria o retângulo que define a área do botão
            largura_texto, altura_texto_individual = self.font.size(texto)
            pos_x = (self.janela.width - largura_texto) / 2
            
            # Calcula a posição Y de cada botão
            pos_y = pos_y_inicial + i * (altura_texto_individual + padding_vertical)
            
            # Usamos o pygame.Rect para facilitar a detecção do mouse
            retangulo_botao = pygame.Rect(pos_x, pos_y, largura_texto, altura_texto_individual)
            self.botoes.append(retangulo_botao)

            # Pré-renderiza os textos para não precisar fazer isso a cada frame
            texto_padrao = self.font.render(texto, True, self.cor_texto_padrao)
            texto_hover = self.font.render(texto, True, self.cor_texto_hover)
            self.botoes_renderizados.append({"padrao": texto_padrao, "hover": texto_hover})

    def _desenhar(self):
        """Desenha o fundo e os botões na tela."""
        self.janela.set_background_color([0, 0, 0])
        self.background.draw()

        # Desenha os botões, verificando o estado do mouse (hover)
        for i, botao_rect in enumerate(self.botoes):
            posicao_mouse = self.mouse.get_position()
            
            # Se o mouse está sobre o retângulo do botão, usa o texto "hover"
            if botao_rect.collidepoint(posicao_mouse):
                texto_para_desenhar = self.botoes_renderizados[i]["hover"]
            else:
                texto_para_desenhar = self.botoes_renderizados[i]["padrao"]
            
            # Desenha o texto renderizado na tela
            self.janela.screen.blit(texto_para_desenhar, botao_rect.topleft)

    def _verificar_cliques(self):
        """Verifica se algum botão foi clicado."""
        if self.mouse.is_button_pressed(1):
            posicao_mouse = self.mouse.get_position()
            
            # Botão Jogar (índice 0)
            if self.botoes[0].collidepoint(posicao_mouse):
                variables.game_state = 2
            
            # Botão Ranking (índice 1)
            elif self.botoes[1].collidepoint(posicao_mouse):
                variables.game_state = 3
            
            # Botão Sair (índice 2)
            elif self.botoes[2].collidepoint(posicao_mouse):
                self.janela.close() # Alterado para fechar a janela diretamente

    def run(self):
        """
        Este método executa a lógica do menu a cada frame.
        Deve ser chamado dentro do loop principal do jogo.
        """
        self._desenhar()
        self._verificar_cliques()