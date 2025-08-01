from PPlay.sprite import Sprite
from PPlay.collision import Collision
from player import Player
from scenery import Scenery
from spawner import Spawner

class Gameplay:
    def __init__(self, window, game):
        """Inicializa a cena de gameplay."""
        self.window = window
        self.game = game
        self.keyboard = self.window.get_keyboard()

        self.scenery = Scenery(self.window, "Assets/Images/fundo_jogo.png", "Assets/Images/fundo_jogo1.png")
        self.player = Player(self.window)
        self.spawner = Spawner(self.window)
        
        self.game_speed = 250
        self.score = 0
        self.score_timer = 0

    def reset(self):
        """Reseta o estado da partida."""
        self.score = 0
        self.game_speed = 250
        self.player.reset()
        self.spawner.reset()

    def _check_collisions(self):
        """Verifica e trata as colisões entre o jogador e os objetos."""
        player_sprite = self.player.sprite
        
        for pool in self.spawner.object_pool.values():
            for obj in pool:
                if obj.is_active:
                    if Collision.collided(player_sprite, obj):
                        if obj.type == "obstacle" and not self.player.is_invulnerable:
                            self.game.change_state("MENU")
                            return
                        elif obj.type == "score_boost":
                            self.player.activate_score_boost()
                            obj.is_active = False
                        elif obj.type == "invulnerability":
                            self.player.activate_invulnerability()
                            obj.is_active = False

        heli_bullet = self.spawner.helicopter.bullet
        if heli_bullet.is_active and not self.player.is_invulnerable:
            if Collision.collided(player_sprite, heli_bullet):
                self.game.change_state("MENU")
                return

    def run(self):
        """Executa um único frame da lógica da partida."""
        self.game_speed += 2 * self.window.delta_time()
        
        self.scenery.update(self.game_speed, self.window.delta_time())
        self.player.update(self.keyboard, self.window.delta_time())
        self.spawner.update(self.game_speed, self.score, self.window.delta_time())

        self._check_collisions()

        score_multiplier = 2 if self.player.is_score_boosted else 1
        self.score_timer += self.window.delta_time()
        if self.score_timer >= 0.1:
            self.score += (1 * score_multiplier)
            self.score_timer = 0
        
        if self.keyboard.key_pressed("ESC"):
            self.game.change_state("MENU")

        self.scenery.draw()
        self.player.draw()
        self.spawner.draw()
        
        self.window.draw_text(f"PONTOS: {int(self.score)}", 10, 10, size=30, color=(255, 255, 255), font_name="Arial", bold=True)