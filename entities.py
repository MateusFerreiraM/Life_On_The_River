import random
import pygame
from PPlay.sprite import Sprite
import constants as C

class MovingObject(Sprite):
    """
    Classe base para objetos que se movem da direita para a esquerda.
    """
    def __init__(self, image_path, object_type, num_frames=1):
        super().__init__(image_path, num_frames)
        self.image_path = image_path      
        self.type = object_type
        self.is_active = False
        self.speed = 0

    def get_hitbox(self):
        """Retorna um retângulo de colisão mais justo para o objeto."""
        hitbox_width = self.width * C.OBJECT_HITBOX_SCALE[0]
        hitbox_height = self.height * C.OBJECT_HITBOX_SCALE[1]
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
        """
        Move o objeto para a esquerda.
        Retorna True se o objeto saiu da tela (foi desviado).
        """
        if self.is_active:
            self.speed = game_speed
            self.x -= self.speed * delta_time
            if self.x < -self.width:
                self.is_active = False
                return True # Objeto saiu da tela
        return False    
    
    def draw(self):
        if self.is_active:
            super().draw()

class Helicopter(MovingObject):
    """
    Classe específica para o helicóptero, que herda de MovingObject
    e adiciona a sua própria lógica de animação.
    """
    def __init__(self, image_path, object_type):
        # Inicializa o MovingObject com o número correto de frames
        super().__init__(image_path, object_type, C.HELICOPTER_FRAMES)
        
        # Configura a animação das hélices
        self.set_sequence(0, 2, True)
        self.set_total_duration(C.HELICOPTER_ANIM_DURATION)

    def get_hitbox(self):
        """Retorna um retângulo de colisão mais justo para o objeto animado."""
        frame_width = self.width / C.HELICOPTER_FRAMES
        hitbox_width = frame_width * C.OBJECT_HITBOX_SCALE[0]
        hitbox_height = self.height * C.OBJECT_HITBOX_SCALE[1]
        hitbox_x = self.x + (frame_width - hitbox_width) / 2
        hitbox_y = self.y + (self.height - hitbox_height) / 2
        return pygame.Rect(hitbox_x, hitbox_y, hitbox_width, hitbox_height)

    def update(self, game_speed, delta_time):
        """Move o objeto, atualiza a sua animação e verifica a desativação."""
        if self.is_active:
            self.speed = game_speed
            self.x -= self.speed * delta_time
            
            # Atualiza o frame da animação (método da classe PPlay.Sprite)
            super(MovingObject, self).update()
            
            # Condição de desativação específica para o sprite animado
            frame_width = self.width / C.HELICOPTER_FRAMES
            if self.x < -frame_width:
                self.is_active = False

class Spawner:
    """
    Gere a criação de todos os obstáculos e itens.
    """
    def __init__(self, window):
        self.window = window
        
        self.layers = {
            "ground": C.LAYER_Y_GROUND,
            "head": C.LAYER_Y_HEAD,
            "sky": C.LAYER_Y_SKY
        }
        
        self.object_pool = {}
        self._load_objects()

        # No __init__ da classe Spawner
        self.phase1_pool = ["police_car", "police_car", "police_car", "money_bag"]
        self.phase2_pool = self.phase1_pool + ["bullet", "bullet", "bullet"]
        self.phase3_pool = self.phase2_pool + ["helicopter", "helicopter"]

        self.spawn_timer = 0.0
        self.min_spawn_cooldown = C.MIN_SPAWN_COOLDOWN
        self.max_spawn_cooldown = C.MAX_SPAWN_COOLDOWN
        self.time_to_next_spawn = random.uniform(self.min_spawn_cooldown, self.max_spawn_cooldown)

    def _load_objects(self):
        """Cria as instâncias dos objetos que podem ser gerados."""
        self.object_pool["police_car"] = [MovingObject(C.IMG_POLICE_CAR, "obstacle") for _ in range(3)]
        self.object_pool["bullet"] = [MovingObject(C.IMG_BULLET, "obstacle") for _ in range(3)]
        self.object_pool["money_bag"] = [MovingObject(C.IMG_MONEY_BAG, "score_boost") for _ in range(1)]
        self.object_pool["helicopter"] = [Helicopter(C.IMG_HELICOPTER, "obstacle")]

    def update(self, game_speed, score, delta_time):
        """Verifica se é hora de gerar um novo objeto e atualiza os ativos."""
        self.spawn_timer += delta_time
        
        difficulty_factor = score // 100
        current_min_cooldown = max(C.MIN_COOLDOWN_CAP, self.min_spawn_cooldown - difficulty_factor * C.DIFFICULTY_COOLDOWN_FACTOR)
        current_max_cooldown = max(C.MAX_COOLDOWN_CAP, self.max_spawn_cooldown - difficulty_factor * C.DIFFICULTY_COOLDOWN_FACTOR)

        if self.spawn_timer >= self.time_to_next_spawn:
            self.spawn_timer = 0
            self.time_to_next_spawn = random.uniform(current_min_cooldown, current_max_cooldown)
            
            if score < 500:
                current_pool = self.phase1_pool
            elif score < 1000:
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