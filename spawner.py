import random
from game_object import MovingObject, Helicopter

class Spawner:
    def __init__(self, window):
        self.window = window
        
        self.layers = {
            "ground": self.window.height,
            "head": self.window.height - 90,
            "sky": 80
        }
        
        self.object_pool = {}
        self._load_objects()

        self.spawn_chance_pool = [
            "police_car", "police_car", "police_car", "police_car",
            "police_car", "police_car", "police_car", "police_car",
            "bullet", "bullet", "bullet", "bullet",
            "bullet", "bullet", "bullet", "bullet",
            "car_powerup", "car_powerup",
            "money_bag", "money_bag",
            "helicopter"
        ]

        self.spawn_timer = 0.0
        self.min_spawn_cooldown = 2.0
        self.max_spawn_cooldown = 3.5
        self.time_to_next_spawn = random.uniform(self.min_spawn_cooldown, self.max_spawn_cooldown)

    def _load_objects(self):
        """Cria as instâncias dos objetos que podem ser gerados."""
        self.object_pool["police_car"] = [MovingObject("Assets/Images/viatura.png", "obstacle") for _ in range(3)]
        self.object_pool["bullet"] = [MovingObject("Assets/Images/bala_projetofinal.png", "obstacle") for _ in range(3)]
        self.object_pool["money_bag"] = [MovingObject("Assets/Images/saco_de_dinheiro.png", "score_boost") for _ in range(2)]
        self.object_pool["car_powerup"] = [MovingObject("Assets/Images/carro.png", "invulnerability") for _ in range(2)]
        self.helicopter = Helicopter("Assets/Images/helicoptero.png", "Assets/Images/helicopter_bullet.png")

    def update(self, game_speed, score, delta_time):
        """Verifica se é hora de gerar um novo objeto e atualiza os ativos."""
        self.spawn_timer += delta_time
        
        difficulty_factor = score // 200
        current_min_cooldown = max(0.8, self.min_spawn_cooldown - difficulty_factor * 0.1)
        current_max_cooldown = max(1.5, self.max_spawn_cooldown - difficulty_factor * 0.1)

        if self.spawn_timer >= self.time_to_next_spawn:
            self.spawn_timer = 0
            self.time_to_next_spawn = random.uniform(current_min_cooldown, current_max_cooldown)
            
            object_type_to_spawn = random.choice(self.spawn_chance_pool)
            self.spawn_object(object_type_to_spawn, game_speed)

        for pool in self.object_pool.values():
            for obj in pool:
                if obj.is_active:
                    obj.speed = game_speed
                    obj.update(delta_time)
        
        self.helicopter.update(delta_time, game_speed)

    def spawn_object(self, object_type, game_speed):
        """Ativa um objeto inativo do tipo e camada corretos."""
        if object_type == "helicopter":
            if not self.helicopter.is_active:
                self.helicopter.spawn(self.window, game_speed, self.layers["sky"])
            return

        layer_y = self.layers["ground"]
        if object_type == "bullet":
            layer_y = self.layers["head"]

        for obj in self.object_pool[object_type]:
            if not obj.is_active:
                obj.spawn(self.window, game_speed, layer_y)
                break

    def draw(self):
        """Desenha todos os objetos ativos."""
        for pool in self.object_pool.values():
            for obj in pool:
                obj.draw()
        self.helicopter.draw()

    def reset(self):
        """Desativa todos os objetos para o reinício do jogo."""
        for pool in self.object_pool.values():
            for obj in pool:
                obj.is_active = False
        self.helicopter.reset()
        self.spawn_timer = 0
        self.time_to_next_spawn = random.uniform(self.min_spawn_cooldown, self.max_spawn_cooldown)