import random
import pygame
from PPlay.sprite import Sprite

class MovingObject(Sprite):
    """
    Classe base para objetos que se movem da direita para a esquerda.
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

# --- NOVA CLASSE APENAS PARA O HELICÓPTERO ---
class Helicopter(Sprite):
    """
    Classe específica para o helicóptero, para gerir a sua animação.
    """
    def __init__(self, image_path, object_type):
        # Inicializa o Sprite com 3 frames de animação
        super().__init__(image_path, 3)
        self.type = object_type
        self.is_active = False
        self.speed = 0
        
        # Configura a animação das hélices
        self.set_sequence(0, 2, True) # Loop contínuo dos frames 0, 1 e 2
        self.set_total_duration(300)  # Velocidade da animação em milissegundos

    def get_hitbox(self):
        """Retorna um retângulo de colisão mais justo para o objeto."""
        # A hitbox aqui é um pouco diferente porque o sprite animado tem uma largura total
        # diferente de um frame individual.
        frame_width = self.width / 3 # Largura de um único frame
        hitbox_width = frame_width * 0.85
        hitbox_height = self.height * 0.85
        hitbox_x = self.x + (frame_width - hitbox_width) / 2
        hitbox_y = self.y + (self.height - hitbox_height) / 2
        return pygame.Rect(hitbox_x, hitbox_y, hitbox_width, hitbox_height)

    def spawn(self, window, speed, y_pos):
        """Ativa o objeto, colocando-o no início da tela."""
        self.is_active = True
        self.speed = speed
        self.x = window.width
        self.y = y_pos - self.height

    def update(self, game_speed, delta_time):
        """Move o objeto e atualiza a sua animação."""
        if self.is_active:
            self.speed = game_speed
            self.x -= self.speed * delta_time
            
            # Atualiza o frame da animação
            super().update()
            
            if self.x < - (self.width / 3):
                self.is_active = False
    
    def draw(self):
        if self.is_active:
            super().draw()


class Spawner:
    """
    Gere a criação de todos os obstáculos e itens.
    """
    def __init__(self, window):
        self.window = window
        
        self.layers = {
            "ground": self.window.height,
            "head": self.window.height - 100,
            "sky": self.window.height / 2 + 40
        }
        
        self.object_pool = {}
        self._load_objects()

        self.phase1_pool = ["police_car", "police_car", "police_car", "money_bag"]
        self.phase2_pool = self.phase1_pool + ["bullet", "bullet", "bullet"]
        self.phase3_pool = self.phase2_pool + ["helicopter"]

        self.spawn_timer = 0.0
        self.min_spawn_cooldown = 2.0
        self.max_spawn_cooldown = 3.5
        self.time_to_next_spawn = random.uniform(self.min_spawn_cooldown, self.max_spawn_cooldown)

    def _load_objects(self):
        """Cria as instâncias dos objetos que podem ser gerados."""
        self.object_pool["police_car"] = [MovingObject("Assets/Images/viatura.png", "obstacle") for _ in range(3)]
        self.object_pool["bullet"] = [MovingObject("Assets/Images/bala_projetofinal.png", "obstacle") for _ in range(3)]
        self.object_pool["money_bag"] = [MovingObject("Assets/Images/saco_de_dinheiro.png", "score_boost") for _ in range(2)]
        self.object_pool["helicopter"] = [Helicopter("Assets/Images/helicoptero.png", "obstacle")]

    def update(self, game_speed, score, delta_time):
        """Verifica se é hora de gerar um novo objeto e atualiza os ativos."""
        self.spawn_timer += delta_time
        
        difficulty_factor = score // 100
        current_min_cooldown = max(0.7, self.min_spawn_cooldown - difficulty_factor * 0.15)
        current_max_cooldown = max(1.4, self.max_spawn_cooldown - difficulty_factor * 0.15)

        if self.spawn_timer >= self.time_to_next_spawn:
            self.spawn_timer = 0
            self.time_to_next_spawn = random.uniform(current_min_cooldown, current_max_cooldown)
            
            if score < 5:
                current_pool = self.phase1_pool
            elif score < 10:
                current_pool = self.phase2_pool
            else:
                current_pool = self.phase3_pool
                
            object_type_to_spawn = random.choice(current_pool)
            self.spawn_object(object_type_to_spawn, game_speed)

        for pool in self.object_pool.values():
            for obj in pool:
                obj.update(game_speed, delta_time)

    def spawn_object(self, object_type, game_speed):
        """Ativa um objeto inativo do tipo e camada corretos."""
        layer_y = self.layers["ground"]
        if object_type == "bullet":
            layer_y = self.layers["head"]
        elif object_type == "helicopter":
            layer_y = self.layers["sky"]

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