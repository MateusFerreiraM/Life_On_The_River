import pygame

# --- CONFIGURAÇÕES DA JANELA ---
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 600
WINDOW_TITLE = "Fuga no Rio"

# --- CORES ---
COLOR_WHITE = (255, 255, 255)
COLOR_BLACK = (0, 0, 0)
COLOR_RED = (255, 0, 0)
COLOR_GOLD = (255, 215, 0)
COLOR_GRAY_LIGHT = (150, 150, 150)
COLOR_GRAY_DARK = (100, 100, 100)
COLOR_BACKGROUND = [20, 20, 20]
OVERLAY_COLOR = (0, 0, 0, 150)
COLOR_ACH_UNLOCKED = (118, 255, 122) # Verde para conquistas
COLOR_ACH_LOCKED = (150, 150, 150)   # Cinza para conquistas

# --- CAMINHOS DOS ASSETS ---
# Fontes
FONT_PRICEDOWN = "Assets/Fonts/pricedown bl.ttf"

# Imagens
IMG_MENU_BACKGROUND = "Assets/Images/menu_background.png"
IMG_GAME_BACKGROUND_1 = "Assets/Images/fundo_jogo.png"
IMG_GAME_BACKGROUND_2 = "Assets/Images/fundo_jogo1.png"
IMG_PLAYER_RUN = "Assets/Images/burglar.png"
IMG_PLAYER_DUCK = "Assets/Images/burglar_state2.png"
IMG_POLICE_CAR = "Assets/Images/viatura.png"
IMG_BULLET = "Assets/Images/bala_projetofinal.png"
IMG_MONEY_BAG = "Assets/Images/saco_de_dinheiro.png"
IMG_HELICOPTER = "Assets/Images/helicoptero.png"
IMG_TROPHY = "Assets/Images/trophy.png"

# Áudio
MUSIC_MENU = "Assets/Audio/menu_theme.ogg"
SFX_LOSE = "Assets/Audio/lose_effect.wav"
SFX_SIREN_LOOP = "Assets/Audio/siren_loop.ogg"
# ALTERADO: O som do tiro agora é um efeito único
SFX_GUNSHOT = "Assets/Audio/gunshot.wav" 

# --- NOVO: CONFIGURAÇÕES DE ÁUDIO ---
VOLUME_MUSIC = 0.1  # 50% do volume máximo
VOLUME_SFX = 0.1    # 60% do volume máximo para sons gerais (derrota, sirene)
VOLUME_GUNSHOT = 0.02 # NOVO: Volume específico para o tiro (30%)
GUNSHOT_INTERVAL = 6.0 # Intervalo em segundos


# --- CONFIGURAÇÕES DE FONTE ---
FONT_SIZES = {
    "title": 80,
    "game_title": 100,
    "info": 40,
    "input": 35,
    "header": 30,
    "score": 40,
    "button": 50,
    "pause_button": 40,
    "hud": 40,
    "ach_title_small": 28,
    "ach_desc_small": 22,
    "instructions_text": 26,      # Novo tamanho para a descrição da conquista
}

# --- CONFIGURAÇÕES DO JOGADOR ---
PLAYER_GRAVITY = 2400
PLAYER_JUMP_VELOCITY = -1100
PLAYER_RUN_FRAMES = 9
PLAYER_RUN_DURATION = 800
SCORE_BOOST_DURATION = 10
PLAYER_HITBOX_SCALE = (0.85, 0.90)

# --- CONFIGURAÇÕES DO SPAWNER ---
LAYER_Y_GROUND = SCREEN_HEIGHT
LAYER_Y_HEAD = SCREEN_HEIGHT - 100
LAYER_Y_SKY = SCREEN_HEIGHT / 2 + 90

MIN_SPAWN_COOLDOWN = 2.0
MAX_SPAWN_COOLDOWN = 3.5
DIFFICULTY_COOLDOWN_FACTOR = 0.15
MIN_COOLDOWN_CAP = 0.7
MAX_COOLDOWN_CAP = 1.4

# --- CONFIGURAÇÕES DOS OBJETOS ---
HELICOPTER_FRAMES = 3
HELICOPTER_ANIM_DURATION = 300
OBJECT_HITBOX_SCALE = (0.85, 0.85)

# --- CONFIGURAÇÕES DO JOGO ---
INITIAL_GAME_SPEED = 300
GAME_SPEED_INCREASE_FACTOR = 10
GAME_SPEED_SCORE_INTERVAL = 50
CLICK_COOLDOWN = 0.5