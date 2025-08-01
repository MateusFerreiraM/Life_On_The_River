# ranking.py
# Exibe a tela de ranking lendo de um arquivo.

import pygame

class Ranking:
    # 1. Adicionamos o parâmetro 'game' aqui
    def __init__(self, window, game):
        self.window = window
        self.game = game # 2. Armazenamos a referência ao objeto principal
        self.keyboard = self.window.get_keyboard()
        
        self.ranking_data = []
        self.font = None
        
        # Carregamos a fonte uma vez para não recarregar a cada frame
        try:
            self.font = pygame.font.Font("pricedown bl.ttf", 50)
        except FileNotFoundError:
            self.font = pygame.font.Font(None, 50)

    def _load_ranking(self):
        """Carrega e formata os dados do ranking a partir do arquivo."""
        self.ranking_data = []
        try:
            with open("ranking.txt", 'r') as file:
                lines = file.read().splitlines()

            # Converte as linhas para tuplas (nome, pontos)
            scores = [(line.split('#')[0], int(line.split('#')[1])) for line in lines if '#' in line]
            
            # Ordena do maior para o menor
            scores.sort(key=lambda x: x[1], reverse=True)
            
            # Pega apenas os 5 melhores
            top_5 = scores[:5]

            # Formata o texto para exibição
            for i, (name, score) in enumerate(top_5):
                text = f"{i+1}º - {name} - {score} pontos"
                self.ranking_data.append(text)
        except FileNotFoundError:
            self.ranking_data.append("Arquivo de ranking não encontrado.")
        except Exception as e:
            self.ranking_data.append("Erro ao ler o ranking.")
            print(f"Erro no ranking: {e}")

    def _draw(self):
        """Desenha a tela de ranking."""
        self.window.set_background_color([0, 0, 0])
        
        title_text = self.font.render("RANKING", True, (255, 215, 0))
        title_rect = title_text.get_rect(center=(self.window.width / 2, 100))
        self.window.screen.blit(title_text, title_rect)
        
        for i, text in enumerate(self.ranking_data):
            score_text = self.font.render(text, True, (255, 255, 255))
            score_rect = score_text.get_rect(center=(self.window.width / 2, 200 + i * 80))
            self.window.screen.blit(score_text, score_rect)

        esc_text = self.font.render("Pressione ESC para voltar", True, (200, 200, 200))
        esc_rect = esc_text.get_rect(center=(self.window.width / 2, self.window.height - 50))
        self.window.screen.blit(esc_text, esc_rect)

    def run(self):
        """Executa a lógica da cena de ranking a cada frame."""
        # Recarrega o ranking toda vez que a cena é executada
        # para garantir que os dados estão atualizados.
        self._load_ranking()
        self._draw()

        # 3. Usa a referência 'self.game' para voltar ao menu
        if self.keyboard.key_pressed("ESC"):
            self.game.change_state("MENU")