import json

class AchievementManager:
    """
    Gere a definição, o progresso e o salvamento/carregamento das conquistas
    e das estatísticas persistentes do jogador.
    """
    def __init__(self, file_path='achievements.json'):
        self.file_path = file_path
        self.achievements = self._define_achievements()
        self.stats = {
            "total_score": 0,
            "total_time_survived": 0,
            "total_money_bags": 0,
            "total_cars_dodged": 0,
            "total_bullets_dodged": 0,
            "highest_score": 0
        }
        self.load_progress()

    def _define_achievements(self):
        """Define todas as conquistas disponíveis no jogo."""
        return {
            "survive_60s": {"title": "Sobrevivente", "desc": "Sobreviva por 60 segundos numa partida.", "unlocked": False},
            "score_3k": {"title": "Milionário", "desc": "Alcance 5.000 pontos numa partida.", "unlocked": False},
            "collect_100_bags": {"title": "Coletor de Tesouros", "desc": "Colete um total de 100 sacos de dinheiro.", "unlocked": False},
            "dodge_500_cars": {"title": "Mestre do Volante", "desc": "Desvie de um total de 500 viaturas.", "unlocked": False},
            "dodge_500_bullets": {"title": "À Prova de Bala", "desc": "Desvie de um total de 500 tiros.", "unlocked": False},
        }

    def save_progress(self):
        """Salva o estado atual das conquistas e estatísticas em JSON."""
        data_to_save = {
            "stats": self.stats,
            "achievements_unlocked": {key: data["unlocked"] for key, data in self.achievements.items()}
        }
        with open(self.file_path, 'w') as f:
            json.dump(data_to_save, f, indent=4)

    def load_progress(self):
        """Carrega o progresso a partir do ficheiro JSON."""
        try:
            with open(self.file_path, 'r') as f:
                data = json.load(f)
                self.stats = data.get("stats", self.stats)
                
                achievements_unlocked = data.get("achievements_unlocked", {})
                for key, unlocked_status in achievements_unlocked.items():
                    if key in self.achievements:
                        self.achievements[key]["unlocked"] = unlocked_status
        except (FileNotFoundError, json.JSONDecodeError):
            self.save_progress() # Cria um ficheiro novo se não existir ou estiver corrompido

    def process_game_session(self, session_stats):
        """
        Processa as estatísticas de uma partida, atualiza os totais,
        e verifica se alguma conquista foi desbloqueada.
        Retorna uma lista de títulos de conquistas recém-desbloqueadas.
        """
        # Atualiza estatísticas totais
        self.stats["total_money_bags"] += session_stats.get("money_bags", 0)
        self.stats["total_cars_dodged"] += session_stats.get("cars_dodged", 0)
        self.stats["total_bullets_dodged"] += session_stats.get("bullets_dodged", 0)
        self.stats["total_time_survived"] += session_stats.get("time", 0)
        
        if session_stats.get("score", 0) > self.stats["highest_score"]:
            self.stats["highest_score"] = session_stats.get("score", 0)

        newly_unlocked = []

        # Verifica cada conquista
        for key, data in self.achievements.items():
            if not data["unlocked"]:
                unlocked = False
                if key == "survive_60s" and session_stats.get("time", 0) >= 60:
                    unlocked = True
                elif key == "score_3k" and session_stats.get("score", 0) >= 5000:
                    unlocked = True
                elif key == "collect_100_bags" and self.stats["total_money_bags"] >= 100:
                    unlocked = True
                elif key == "dodge_500_cars" and self.stats["total_cars_dodged"] >= 500:
                    unlocked = True
                elif key == "dodge_500_bullets" and self.stats["total_bullets_dodged"] >= 500:
                    unlocked = True
                
                if unlocked:
                    data["unlocked"] = True
                    newly_unlocked.append(data["title"])

        if newly_unlocked:
            self.save_progress()
            
        return newly_unlocked