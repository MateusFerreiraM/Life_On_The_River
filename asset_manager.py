# Ficheiro: asset_manager.py (COMPLETO E CORRIGIDO)

import pygame
import constants as C

class AssetManager:
    """
    Carrega e gere todos os assets (fontes, sons, música) para que sejam
    carregados e controlados de forma centralizada.
    """
    def __init__(self):
        self.fonts = {}
        self.sounds = {}
        self.music_paths = {}
        self.current_music = None

        self.siren_channel = pygame.mixer.Channel(0)

        self._load_fonts()
        self._load_audio()

    def _load_fonts(self):
        """Carrega todas as variações de tamanho da fonte principal."""
        try:
            # --- LÓGICA CORRIGIDA ---
            # Este loop agora carrega CADA tamanho definido em FONT_SIZES
            for size_name, size_value in C.FONT_SIZES.items():
                # A chave será o nome da fonte mais o nome do tamanho, ex: "pricedown_instructions_text"
                font_key = f"pricedown_{size_name}"
                self.fonts[font_key] = pygame.font.Font(C.FONT_PRICEDOWN, size_value)

        except FileNotFoundError:
            print(f"Aviso: Ficheiro da fonte '{C.FONT_PRICEDOWN}' não encontrado. A usar fontes padrão.")
            for size_name, size_value in C.FONT_SIZES.items():
                font_key = f"pricedown_{size_name}"
                self.fonts[font_key] = pygame.font.Font(None, size_value + 4) # Ajuste para fontes padrão

    def _load_audio(self):
        """Carrega os efeitos sonoros, aplica o volume, e mapeia as músicas."""
        try:
            self.sounds["lose"] = pygame.mixer.Sound(C.SFX_LOSE)
            self.sounds["lose"].set_volume(C.VOLUME_SFX)
            self.sounds["siren"] = pygame.mixer.Sound(C.SFX_SIREN_LOOP)
            self.sounds["siren"].set_volume(C.VOLUME_SFX * 0.8)
            self.sounds["gunshot"] = pygame.mixer.Sound(C.SFX_GUNSHOT)
            self.sounds["gunshot"].set_volume(C.VOLUME_GUNSHOT)
            self.music_paths["menu"] = C.MUSIC_MENU
        except pygame.error as e:
            print(f"Erro ao carregar ficheiro de áudio: {e}")
            self.sounds = {}
            self.music_paths = {}

    def get_font(self, name):
        """Retorna uma superfície de fonte já carregada."""
        return self.fonts.get(name) # .get() retorna None se a chave não for encontrada

    def play_siren_loop(self):
        """Toca a sirene em loop."""
        if self.sounds.get("siren"):
            self.siren_channel.play(self.sounds["siren"], loops=-1)

    def stop_all_sfx(self):
        """Para todos os efeitos sonoros que estão a tocar."""
        for sound in self.sounds.values():
            sound.stop()

    def play_music(self, music_key, loops=-1):
        """Toca uma música, aplicando o volume definido."""
        if not self.music_paths or self.current_music == music_key:
            return
        music_path = self.music_paths.get(music_key)
        if music_path:
            pygame.mixer.music.set_volume(C.VOLUME_MUSIC)
            pygame.mixer.music.load(music_path)
            pygame.mixer.music.play(loops)
            self.current_music = music_key

    def stop_music(self):
        """Para a música que estiver a tocar."""
        pygame.mixer.music.stop()
        self.current_music = None

    def play_sound(self, sound_key):
        """Toca um efeito sonoro de uso único (como o tiro ou a derrota)."""
        sound = self.sounds.get(sound_key)
        if sound:
            sound.play()