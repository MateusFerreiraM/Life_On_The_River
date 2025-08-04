# Ficheiro: game.py (COMPLETO E ATUALIZADO COM TRANSIÇÕES)

import pygame
from PPlay.window import Window
import constants as C
from asset_manager import AssetManager
from achievement_manager import AchievementManager
from menu import Menu
from gameplay import Gameplay
from ranking import Ranking
from game_over import GameOver
from achievements_scene import AchievementsScene
from instructions_scene import InstructionsScene
from notification import Notification

# --- 1. NOVA CLASSE PARA GERIR O EFEITO DE FADE ---
class Transition:
    def __init__(self, fade_speed, screen_width, screen_height):
        self.fade_speed = fade_speed
        self.fade_surface = pygame.Surface((screen_width, screen_height))
        self.fade_surface.fill((0, 0, 0))
        self.alpha = 0
        self.fading_out = False
        self.fading_in = False
        self.on_fade_complete = None

    def start_fade_out(self, on_complete):
        """Inicia o escurecimento da tela."""
        self.fading_out = True
        self.fading_in = False
        self.alpha = 0
        self.on_fade_complete = on_complete

    def start_fade_in(self):
        """Inicia o clareamento da tela."""
        self.fading_in = True
        self.fading_out = False
        self.alpha = 255

    def update(self, delta_time):
        """Atualiza a transparência do fade."""
        if self.fading_out:
            self.alpha += self.fade_speed * delta_time
            if self.alpha >= 255:
                self.alpha = 255
                self.fading_out = False
                if self.on_fade_complete:
                    self.on_fade_complete() # Executa a função de callback (troca de cena)
        
        elif self.fading_in:
            self.alpha -= self.fade_speed * delta_time
            if self.alpha <= 0:
                self.alpha = 0
                self.fading_in = False

    def draw(self, screen):
        """Desenha a superfície de fade na tela."""
        if self.alpha > 0:
            self.fade_surface.set_alpha(self.alpha)
            screen.blit(self.fade_surface, (0, 0))


class Game:
    """
    Classe principal que gere a janela, o loop de jogo e os estados (cenas).
    """
    def __init__(self):
        # --- Inicialização ---
        pygame.mixer.pre_init(44100, -16, 2, 512)
        pygame.init()
        pygame.mixer.set_num_channels(8)
        self.window = Window(C.SCREEN_WIDTH, C.SCREEN_HEIGHT)
        self.window.set_title(C.WINDOW_TITLE)
        
        # --- Gestores ---
        self.asset_manager = AssetManager()
        self.achievement_manager = AchievementManager()

        # --- Estado do Jogo ---
        self.game_state = "MENU"
        self.target_state = "" # Para onde vamos após a transição
        self.asset_manager.play_music("menu")
        self.notifications = []
        
        # --- 2. INSTANCIAR A CLASSE DE TRANSIÇÃO ---
        self.transition = Transition(fade_speed=900, screen_width=C.SCREEN_WIDTH, screen_height=C.SCREEN_HEIGHT)

        # --- Instâncias das Cenas ---
        self.menu = Menu(self.window, self, self.asset_manager)
        self.gameplay = Gameplay(self.window, self, self.asset_manager, self.achievement_manager)
        self.ranking = Ranking(self.window, self, self.asset_manager)
        self.game_over = GameOver(self.window, self, self.asset_manager)
        self.achievements_scene = AchievementsScene(self.window, self, self.asset_manager, self.achievement_manager)
        self.instructions_scene = InstructionsScene(self.window, self, self.asset_manager)

    def run(self):
        """Inicia e mantém o loop principal do jogo."""
        while True:
            # --- 3. LÓGICA DE ESTADOS ATUALIZADA ---
            # O jogo continua a desenhar a cena atual por baixo, mesmo durante a transição
            if self.game_state == "MENU":
                self.menu.run()
            elif self.game_state == "PLAYING":
                self.gameplay.run()
            elif self.game_state == "RANKING":
                self.ranking.run()
            elif self.game_state == "GAME_OVER":
                self.game_over.run()
            elif self.game_state == "ACHIEVEMENTS":
                self.achievements_scene.run()
            elif self.game_state == "INSTRUCTIONS":
                self.instructions_scene.run()
            elif self.game_state == "EXIT":
                break

            # --- ATUALIZA E DESENHA TRANSIÇÕES E NOTIFICAÇÕES (SEMPRE POR CIMA) ---
            delta_time = self.window.delta_time()
            self.transition.update(delta_time)
            
            for notif in self.notifications[:]:
                if notif.is_active:
                    notif.update(delta_time)
                    notif.draw(self.window)
                else:
                    self.notifications.remove(notif)
            
            self.transition.draw(self.window.screen)
            
            self.window.update()

    def _perform_state_change(self):
        """
        Esta função é chamada no meio do fade, quando a tela está preta.
        Ela efetivamente troca a cena e inicia o fade_in.
        """
        session_stats = self._session_stats_buffer # Recupera os dados da sessão
        new_state = self.target_state

        # Lógica de parar sons do estado anterior
        if self.game_state == "PLAYING":
            self.asset_manager.stop_all_sfx()

        # Processar conquistas ao sair do gameplay
        if self.game_state == "PLAYING" and new_state == "GAME_OVER":
            if session_stats:
                new_achievements = self.achievement_manager.process_game_session(session_stats)
                for ach_title in new_achievements:
                    self.notifications.append(Notification(ach_title, self.asset_manager))
                
                score = session_stats.get("score", 0)
                time = session_stats.get("time", 0)
                self.game_over.set_final_stats(score, time)
        
        self.game_state = new_state
        
        # Lógica para iniciar sons do novo estado
        if new_state == "PLAYING":
            self.asset_manager.stop_music()
            self.asset_manager.play_siren_loop()
            self.gameplay.reset()
        elif new_state == "GAME_OVER":
            self.asset_manager.play_sound("lose")
        elif new_state == "MENU":
            self.asset_manager.play_music("menu")
        elif new_state == "RANKING":
             self.asset_manager.play_music("menu")

        self.transition.start_fade_in() # Inicia o clareamento

    def change_state(self, new_state, session_stats=None):
        """
        --- 4. MÉTODO ATUALIZADO ---
        Em vez de mudar o estado diretamente, agora inicia o fade-out.
        """
        if self.transition.fading_out or self.transition.fading_in:
            return # Ignora se uma transição já estiver a acontecer

        self.target_state = new_state
        self._session_stats_buffer = session_stats # Guarda os dados da sessão temporariamente
        self.transition.start_fade_out(on_complete=self._perform_state_change)