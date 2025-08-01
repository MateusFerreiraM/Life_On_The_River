import random
from PPlay.sprite import Sprite

class MovingObject(Sprite):
    """Classe para objetos que se movem da direita para a esquerda."""
    def __init__(self, image_path, object_type):
        super().__init__(image_path)
        self.type = object_type
        self.is_active = False

    def spawn(self, window, speed, y_pos):
        self.is_active = True
        self.speed = speed
        self.x = window.width
        self.y = y_pos - self.height

    def update(self, delta_time):
        if self.is_active:
            self.x -= self.speed * delta_time
            if self.x < -self.width:
                self.is_active = False
    
    def draw(self):
        if self.is_active:
            super().draw()

class Helicopter(Sprite):
    """Classe especial para o helicóptero, com movimento e tiro próprios."""
    def __init__(self, image_path, bullet_image_path):
        super().__init__(image_path, 3)
        self.set_total_duration(400)
        self.type = "helicopter"
        self.is_active = False

        self.bullet = MovingObject(bullet_image_path, "obstacle")
        self.bullet_speed_x = 200
        self.bullet_speed_y = 150

        self.direction = -1
        self.speed = 100

        self.active_duration = 5.0
        self.active_timer = 0.0

    def spawn(self, window, speed, y_pos):
        self.is_active = True
        self.active_timer = 0.0
        self.x = window.width - 200
        self.y = y_pos
        self.min_x = window.width - 300
        self.max_x = window.width

    def update(self, delta_time, game_speed):
        if not self.is_active:
            return

        self.active_timer += delta_time
        if self.active_timer >= self.active_duration:
            self.reset()
            return

        self.x += self.speed * self.direction * delta_time
        if self.x <= self.min_x:
            self.direction = 1
        elif self.x >= self.max_x - self.width:
            self.direction = -1
        
        if not self.bullet.is_active:
            if random.random() < 0.015:
                self.bullet.is_active = True
                self.bullet.x = self.x + self.width / 2
                self.bullet.y = self.y + self.height * 0.6
                self.bullet.speed = game_speed + self.bullet_speed_x

        if self.bullet.is_active:
            self.bullet.x -= self.bullet.speed * delta_time
            self.bullet.y += self.bullet_speed_y * delta_time
            if self.bullet.x < -self.bullet.width or self.bullet.y > 800:
                self.bullet.is_active = False

        super().update()

    def draw(self):
        if self.is_active:
            super().draw()
            self.bullet.draw()

    def reset(self):
        self.is_active = False
        self.bullet.is_active = False
        self.active_timer = 0.0