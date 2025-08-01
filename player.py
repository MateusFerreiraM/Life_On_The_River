from PPlay.sprite import Sprite

class Player:
    def __init__(self, window):
        """Inicializa o jogador."""
        self.window = window
        
        self.run_sprite = Sprite("Assets/Images/burglar.png", 9)
        self.duck_sprite = Sprite("Assets/Images/burglar_state2.png")
        self.car_sprite = Sprite("Assets/Images/carroinvertido.png")
        
        self.run_sprite.set_sequence(0, 4, True)
        self.run_sprite.set_total_duration(800)
        
        self.gravity = 1800 
        self.jump_velocity = -900
        
        self.velocity_y = 0
        
        self.ground_y = self.window.height - self.run_sprite.height
        self.duck_y = self.window.height - self.duck_sprite.height
        self.car_y = self.window.height - self.car_sprite.height - 10

        self.is_invulnerable = False
        self.invulnerable_timer = 0
        self.invulnerable_duration = 10

        self.is_score_boosted = False
        self.score_boost_timer = 0
        self.score_boost_duration = 10

        self.reset()

    def reset(self):
        """Reseta o jogador para o estado inicial."""
        self.sprite = self.run_sprite
        self.sprite.set_position(100, self.ground_y)
        self.is_ducking = False
        self.velocity_y = 0
        self.is_invulnerable = False
        self.invulnerable_timer = 0
        self.is_score_boosted = False
        self.score_boost_timer = 0

    def _handle_powerups(self, delta_time):
        """Gerencia os timers dos power-ups."""
        if self.is_invulnerable:
            self.invulnerable_timer += delta_time
            if self.invulnerable_timer >= self.invulnerable_duration:
                self.is_invulnerable = False
                self.invulnerable_timer = 0
                self.sprite = self.run_sprite
                self.sprite.set_position(100, self.ground_y)

        if self.is_score_boosted:
            self.score_boost_timer += delta_time
            if self.score_boost_timer >= self.score_boost_duration:
                self.is_score_boosted = False
                self.score_boost_timer = 0

    def update(self, keyboard, delta_time):
        """Atualiza a lógica do jogador a cada frame."""
        self._handle_powerups(delta_time)

        if self.is_invulnerable:
            return

        self.velocity_y += self.gravity * delta_time
        self.sprite.y += self.velocity_y * delta_time

        current_ground_level = self.duck_y if self.is_ducking else self.ground_y
        
        if self.sprite.y >= current_ground_level:
            self.sprite.y = current_ground_level
            self.velocity_y = 0

        if self.velocity_y == 0:
            if keyboard.key_pressed("DOWN"):
                if not self.is_ducking:
                    current_x = self.sprite.x
                    self.is_ducking = True
                    self.sprite = self.duck_sprite
                    self.sprite.set_position(current_x, self.duck_y)
            else:
                if self.is_ducking:
                    current_x = self.sprite.x
                    self.is_ducking = False
                    self.sprite = self.run_sprite
                    self.sprite.set_position(current_x, self.ground_y)

            if not self.is_ducking and keyboard.key_pressed("UP"):
                self.velocity_y = self.jump_velocity

        if not self.is_ducking and self.velocity_y == 0:
            self.sprite.update()

    def activate_invulnerability(self):
        self.is_invulnerable = True
        self.invulnerable_timer = 0
        self.sprite = self.car_sprite
        self.sprite.set_position(100, self.car_y)

    def activate_score_boost(self):
        self.is_score_boosted = True
        self.score_boost_timer = 0

    def draw(self):
        """Desenha o jogador na tela."""
        self.sprite.draw()