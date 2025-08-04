import random
import pygame
from PPlay.sprite import Sprite

class MovingObject(Sprite):
    """
    Classe base para todos os objetos que se movem da direita para a esquerda.
    """
    def __init__(self, image_path, object_type):
        super().__init__(image_path)
        self.type = object_type
        self.is_active = False
        self.speed = 0

    def get_hitbox(self):
        """Retorna um retângulo de colisão mais justo para o objeto."""
        hitbox_width = self.width * 0.85
        hitbox_height = self.height * 0.85
        hitbox_x = self.x + (self.width - hitbox_width) / 2
        hitbox_y = self.y + (self.height - hitbox_height) / 2
        return pygame.Rect(hitbox_x, hitbox_y, hitbox_width, hitbox_height)

    def spawn(self, window, speed, y_pos):
        """Ativa o objeto, colocando-o no início da tela."""
        self.is_active = True
        self.speed = speed
        self.x = window.width
        self.y = y_pos - self.height

    def update(self, game_speed, delta_time):
        """Move o objeto para a esquerda com base na velocidade atual do jogo."""
        if self.is_active:
            self.speed = game_speed
            self.x -= self.speed * delta_time
            if self.x < -self.width:
                self.is_active = False
    
    def draw(self):
        if self.is_active:
            super().draw()

class Spawner:
    """
    Gere a criação de todos os obstáculos e itens, controlando a frequência
    e a dificuldade com base na pontuação do jogador.
    """
    def __init__(self, window):
        self.window = window
        
        # Define as "camadas" verticais para o spawn dos objetos
        self.layers = {
            "ground": self.window.height,
            "head": self.window.height - 90,
        }
        
        # "Object Pooling": pré-carrega os objetos para reutilização
        self.object_pool = {}
        self._load_objects()

        # Define a probabilidade de cada objeto aparecer
        self.spawn_chance_pool = [
            "police_car", "police_car", "police_car",
            "bullet", "bullet", "bullet",
            "money_bag"
        ]

        # Controlo de tempo entre spawns
        self.spawn_timer = 0.0
        self.min_spawn_cooldown = 2.0
        self.max_spawn_cooldown = 3.5
        self.time_to_next_spawn = random.uniform(self.min_spawn_cooldown, self.max_spawn_cooldown)

    def _load_objects(self):
        """Cria as instâncias dos objetos que podem ser gerados."""
        self.object_pool["police_car"] = [MovingObject("Assets/Images/viatura.png", "obstacle") for _ in range(3)]
        self.object_pool["bullet"] = [MovingObject("Assets/Images/bala_projetofinal.png", "obstacle") for _ in range(3)]
        self.object_pool["money_bag"] = [MovingObject("Assets/Images/saco_de_dinheiro.png", "score_boost") for _ in range(2)]

    def update(self, game_speed, score, delta_time):
        """Verifica se é hora de gerar um novo objeto e atualiza os ativos."""
        self.spawn_timer += delta_time
        
        # --- Lógica de Dificuldade Progressiva ---
        difficulty_factor = score // 100
        current_min_cooldown = max(0.7, self.min_spawn_cooldown - difficulty_factor * 0.15)
        current_max_cooldown = max(1.4, self.max_spawn_cooldown - difficulty_factor * 0.15)

        if self.spawn_timer >= self.time_to_next_spawn:
            self.spawn_timer = 0
            self.time_to_next_spawn = random.uniform(current_min_cooldown, current_max_cooldown)
            object_type_to_spawn = random.choice(self.spawn_chance_pool)
            self.spawn_object(object_type_to_spawn, game_speed)

        for pool in self.object_pool.values():
            for obj in pool:
                obj.update(game_speed, delta_time)

    def spawn_object(self, object_type, game_speed):
        """Ativa um objeto inativo do tipo e camada corretos."""
        layer_y = self.layers["ground"]
        if object_type == "bullet":
            layer_y = self.layers["head"]

        for obj in self.object_pool[object_type]:
            if not obj.is_active:
                obj.spawn(self.window, game_speed, layer_y)
                break

    def draw(self):
        for pool in self.object_pool.values():
            for obj in pool:
                obj.draw()

    def reset(self):
        """Desativa todos os objetos para o reinício do jogo."""
        for pool in self.object_pool.values():
            for obj in pool:
                obj.is_active = False
        self.spawn_timer = 0
        self.time_to_next_spawn = random.uniform(self.min_spawn_cooldown, self.max_spawn_cooldown)
