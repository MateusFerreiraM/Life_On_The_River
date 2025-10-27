import pygame
from PPlay.sprite import Sprite
from PPlay.collision import Collision
from PPlay.mouse import Mouse
from entities import Spawner
import constants as C

# --- Componentes Internos da Cena de Gameplay ---
class Scenery:
    """Gere o fundo de ecrã contínuo com efeito de parallax."""
    def __init__(self, window):
        self.bg1 = Sprite(C.IMG_GAME_BACKGROUND_1)
        self.bg2 = Sprite(C.IMG_GAME_BACKGROUND_2)
        self.bg1.x = 0
        self.bg2.x = self.bg1.width

    def update(self, move_delta):
        self.bg1.x -= move_delta
        self.bg2.x -= move_delta
        if self.bg1.x <= -self.bg1.width:
            self.bg1.x = self.bg2.x + self.bg2.width - 1
        if self.bg2.x <= -self.bg2.width:
            self.bg2.x = self.bg1.x + self.bg1.width - 1
            
    def draw(self):
        self.bg1.draw()
        self.bg2.draw()

class Player:
    """Gere o estado, as ações (pulo, agachar) e a física do jogador."""
    def __init__(self, window):
        self.window = window
        self.run_sprite = Sprite(C.IMG_PLAYER_RUN, C.PLAYER_RUN_FRAMES)
        self.duck_sprite = Sprite(C.IMG_PLAYER_DUCK)
        self.run_sprite.set_sequence(0, 4, True)
        self.run_sprite.set_total_duration(C.PLAYER_RUN_DURATION)
        
        self.gravity = C.PLAYER_GRAVITY
        self.jump_velocity = C.PLAYER_JUMP_VELOCITY
        self.velocity_y = 0
        
        self.ground_y = self.window.height - self.run_sprite.height
        self.duck_y = self.window.height - self.duck_sprite.height

        self.is_score_boosted = False
        self.score_boost_timer = 0
        self.score_boost_duration = C.SCORE_BOOST_DURATION
        
        self.up_key_was_pressed = False
        self.reset()

    def reset(self):
        self.sprite = self.run_sprite
        self.sprite.set_position(100, self.ground_y)
        self.is_ducking = False
        self.velocity_y = 0
        self.is_score_boosted = False
        self.score_boost_timer = 0
        self.up_key_was_pressed = False

    def get_hitbox(self):
        hitbox_width = self.sprite.width * C.PLAYER_HITBOX_SCALE[0]
        hitbox_height = self.sprite.height * C.PLAYER_HITBOX_SCALE[1]
        hitbox_x = self.sprite.x + (self.sprite.width - hitbox_width) / 2
        hitbox_y = self.sprite.y + (self.sprite.height - hitbox_height) / 2
        return pygame.Rect(hitbox_x, hitbox_y, hitbox_width, hitbox_height)

    def _handle_powerups(self, delta_time):
        if self.is_score_boosted:
            self.score_boost_timer += delta_time
            if self.score_boost_timer >= self.score_boost_duration:
                self.is_score_boosted = False
                self.score_boost_timer = 0

    def update(self, keyboard, delta_time):
        self._handle_powerups(delta_time)
        self.velocity_y += self.gravity * delta_time
        self.sprite.y += self.velocity_y * delta_time
        current_ground_level = self.duck_y if self.is_ducking else self.ground_y
        if self.sprite.y >= current_ground_level:
            self.sprite.y = current_ground_level
            self.velocity_y = 0
        up_key_is_pressed = keyboard.key_pressed("UP")
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
            if not self.is_ducking and up_key_is_pressed and not self.up_key_was_pressed:
                self.velocity_y = self.jump_velocity
        self.up_key_was_pressed = up_key_is_pressed
        if not self.is_ducking and self.velocity_y == 0:
            self.sprite.update()

    def activate_score_boost(self):
        self.is_score_boosted = True
        self.score_boost_timer = 0

    def draw(self):
        self.sprite.draw()

class PauseMenu:
    """Gere a tela de pausa que aparece sobre a cena de gameplay."""
    def __init__(self, window, gameplay_instance, asset_manager):
        self.window = window
        self.gameplay = gameplay_instance
        self.mouse = Mouse()
        
        self.font_title = asset_manager.get_font("pricedown_title")
        self.font_button = asset_manager.get_font("pricedown_pause_button")
        
        self.color_title = C.COLOR_GOLD
        self.color_text = C.COLOR_WHITE
        self.color_hover = C.COLOR_GOLD

        self.overlay = pygame.Surface((self.window.width, self.window.height), pygame.SRCALPHA)
        self.overlay.fill(C.OVERLAY_COLOR)

        self.buttons = {}
        self.button_surfaces = {}
        self._create_buttons()
        self.click_cooldown = C.CLICK_COOLDOWN
        self.last_click_time = 0

    def _create_buttons(self):
        button_texts = {"continue": "CONTINUAR", "restart": "RECOMEÇAR", "main_menu": "VOLTAR AO MENU"}
        y_pos = self.window.height / 2 - 50
        for key, text in button_texts.items():
            rect = pygame.Rect(0, 0, 400, 50)
            rect.center = (self.window.width / 2, y_pos)
            self.buttons[key] = rect
            text_normal = self.font_button.render(text, True, self.color_text)
            text_hover = self.font_button.render(text, True, self.color_hover)
            self.button_surfaces[key] = {"normal": text_normal, "hover": text_hover}
            y_pos += 80

    def _check_clicks(self):
        self.last_click_time += self.window.delta_time()
        if self.mouse.is_button_pressed(1) and self.last_click_time > self.click_cooldown:
            self.last_click_time = 0
            mouse_pos = self.mouse.get_position()
            if self.buttons["continue"].collidepoint(mouse_pos):
                self.gameplay.unpause()
            elif self.buttons["restart"].collidepoint(mouse_pos):
                self.gameplay.restart()
            elif self.buttons["main_menu"].collidepoint(mouse_pos):
                self.gameplay.go_to_main_menu()

    def _draw(self):
        self.window.screen.blit(self.overlay, (0, 0))
        title_surf = self.font_title.render("PAUSA", True, self.color_title)
        title_rect = title_surf.get_rect(center=(self.window.width / 2, 150))
        self.window.screen.blit(title_surf, title_rect)
        mouse_pos = self.mouse.get_position()
        for key, rect in self.buttons.items():
            text_surf = self.button_surfaces[key]["hover"] if rect.collidepoint(mouse_pos) else self.button_surfaces[key]["normal"]
            text_rect = text_surf.get_rect(center=rect.center)
            self.window.screen.blit(text_surf, text_rect)

    def run(self):
        self._check_clicks()
        self._draw()

# --- Classe Principal da Cena de Gameplay ---
class Gameplay:
    """
    Classe principal que orquestra todos os elementos da partida.
    """
    def __init__(self, window, game, asset_manager, achievement_manager):
        self.window = window
        self.game = game
        self.asset_manager = asset_manager
        self.achievement_manager = achievement_manager
        self.keyboard = self.window.get_keyboard()

        self.scenery = Scenery(self.window)
        self.player = Player(self.window)
        self.spawner = Spawner(self.window)
        self.pause_menu = PauseMenu(self.window, self, asset_manager)
                
        self.is_paused = False
        self.esc_was_pressed = False
        
        self.hud_font = asset_manager.get_font("pricedown_hud")
        self.color_text = C.COLOR_WHITE
        self.color_outline = C.COLOR_BLACK

        self.session_stats = {}
        self.reset()

    def unpause(self): self.is_paused = False
    def restart(self): self.unpause(); self.reset()
    def go_to_main_menu(self): self.unpause(); self.game.change_state("MENU")
    
    def reset(self):
        self.score = 0
        self.time_survived = 0
        self.game_speed = C.INITIAL_GAME_SPEED
        self.player.reset()
        self.spawner.reset()
        self.gunshot_timer = C.GUNSHOT_INTERVAL
        # Reinicia as estatísticas da sessão
        self.session_stats = {
            "score": 0, "time": 0, "money_bags": 0,
            "cars_dodged": 0, "bullets_dodged": 0
        }

    def _render_text_with_outline(self, font, text, color, outline_color, outline_width=2):
        text_surface = font.render(text, True, color)
        outline_surface = font.render(text, True, outline_color)
        final_surface = pygame.Surface((text_surface.get_width() + outline_width * 2, text_surface.get_height() + outline_width * 2), pygame.SRCALPHA)
        positions = [(0, 0), (outline_width, 0), (outline_width * 2, 0), (0, outline_width), (outline_width * 2, outline_width), (0, outline_width * 2), (outline_width, outline_width * 2), (outline_width * 2, outline_width * 2)]
        for pos in positions: final_surface.blit(outline_surface, pos)
        final_surface.blit(text_surface, (outline_width, outline_width))
        return final_surface

    def _check_collisions(self):
        player_hitbox = self.player.get_hitbox()
        all_objects = []
        for pool in self.spawner.object_pool.values(): all_objects.extend(pool)
        for obj in all_objects:
            if obj.is_active:
                obj_hitbox = obj.get_hitbox()
                if player_hitbox.colliderect(obj_hitbox):
                    if obj.type == "score_boost":
                        self.player.activate_score_boost()
                        self.session_stats["money_bags"] += 1
                        obj.is_active = False
                    elif obj.type == "obstacle":
                        # --- Apenas atualiza as estatísticas e muda o estado ---
                        self.session_stats["score"] = int(self.score)
                        self.session_stats["time"] = self.time_survived
                        
                        # Passa o dicionário completo para a classe Game
                        self.game.change_state("GAME_OVER", session_stats=self.session_stats)
                        return
                    
    def _handle_timed_sfx(self, delta_time):
        self.gunshot_timer += delta_time
        if self.gunshot_timer >= C.GUNSHOT_INTERVAL:
            self.gunshot_timer = 0 # Reinicia o timer
            self.asset_manager.play_sound("gunshot") # Toca o som

    def run(self):
        esc_is_pressed = self.keyboard.key_pressed("ESC")
        if esc_is_pressed and not self.esc_was_pressed:
            self.is_paused = not self.is_paused
        self.esc_was_pressed = esc_is_pressed

        if not self.is_paused:
            delta_time = self.window.delta_time()
            self.game_speed = C.INITIAL_GAME_SPEED + (self.score // C.GAME_SPEED_SCORE_INTERVAL) * C.GAME_SPEED_INCREASE_FACTOR
            self.time_survived += delta_time
            scenery_move_delta = (self.game_speed * 0.5) * delta_time

            # Atualizações
            self.scenery.update(scenery_move_delta)
            self.player.update(self.keyboard, delta_time)
            
            # Atualiza spawner e conta objetos desviados
            dodged_objects = self.spawner.update_and_count_dodges(self.game_speed, self.score, delta_time)
            for obj_type in dodged_objects:
                if obj_type == "viatura":
                    self.session_stats["cars_dodged"] += 1
                elif obj_type == "helicoptero":
                    self.session_stats["cars_dodged"] += 1  # Helicópteros contam como carros
                elif obj_type == "bullet":
                    self.session_stats["bullets_dodged"] += 1
            
            self._handle_timed_sfx(delta_time) # Chama o gestor do tiro
            
            # Colisões e Pontuação
            self._check_collisions()
            score_multiplier = 3 if self.player.is_score_boosted else 1
            self.score += (1 * score_multiplier) * delta_time * 20
        
        # Desenhos
        self.scenery.draw()
        self.player.draw()
        self.spawner.draw()
        
        score_text = f"PONTOS: {int(self.score)}"
        score_surf = self._render_text_with_outline(self.hud_font, score_text, self.color_text, self.color_outline)
        self.window.screen.blit(score_surf, (10, 10))

        if self.is_paused:
            self.pause_menu.run()