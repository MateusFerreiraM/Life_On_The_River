# Ficheiro: asset_manager.py (COMPLETO E ATUALIZADO)

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

        # Apenas um canal para o som contínuo da sirene
        self.siren_channel = pygame.mixer.Channel(0)

        self._load_fonts()
        self._load_audio()

    def _load_fonts(self):
        """Carrega todas as variações de tamanho da fonte principal."""
        try:
            for size_name, size_value in C.FONT_SIZES.items():
                self.fonts[f"pricedown_{size_name}"] = pygame.font.Font(C.FONT_PRICEDOWN, size_value)
        except FileNotFoundError:
            print(f"Aviso: Ficheiro da fonte '{C.FONT_PRICEDOWN}' não encontrado. A usar fontes padrão.")
            for size_name, size_value in C.FONT_SIZES.items():
                if size_value > 80: default_size = 90
                elif size_value > 50: default_size = 60
                else: default_size = 45
                self.fonts[f"pricedown_{size_name}"] = pygame.font.Font(None, default_size)


    def _load_audio(self):
        """Carrega os efeitos sonoros, aplica o volume, e mapeia as músicas."""
        try:
            # Carrega sons e aplica o volume
            self.sounds["lose"] = pygame.mixer.Sound(C.SFX_LOSE)
            self.sounds["lose"].set_volume(C.VOLUME_SFX)

            self.sounds["siren"] = pygame.mixer.Sound(C.SFX_SIREN_LOOP)
            self.sounds["siren"].set_volume(C.VOLUME_SFX * 0.8) # Sirene um pouco mais baixa

            # --- LINHA ALTERADA ---
            # O som do tiro agora usa a sua própria constante de volume
            self.sounds["gunshot"] = pygame.mixer.Sound(C.SFX_GUNSHOT)
            self.sounds["gunshot"].set_volume(C.VOLUME_GUNSHOT)
            
            # Mapeia músicas
            self.music_paths["menu"] = C.MUSIC_MENU
            
        except pygame.error as e:
            print(f"Erro ao carregar ficheiro de áudio: {e}")
            self.sounds = {}
            self.music_paths = {}

    def get_font(self, name):
        """Retorna uma superfície de fonte já carregada."""
        return self.fonts.get(name)

    def play_siren_loop(self):
        """Toca a sirene em loop."""
        if self.sounds.get("siren"):
            self.siren_channel.play(self.sounds["siren"], loops=-1)

    def stop_siren_loop(self):
        """Para a sirene."""
        self.siren_channel.stop()
    
    def play_music(self, music_key, loops=-1):
        """Toca uma música, aplicando o volume definido."""
        if not self.music_paths or self.current_music == music_key:
            return

        music_path = self.music_paths.get(music_key)
        if music_path:
            # Aplica o volume antes de tocar
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