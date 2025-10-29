import json
import os
from datetime import datetime

class ScoreManager:
    def __init__(self, scores_file="scores.json"):
        self.scores_file = scores_file
        self.scores = []
        self.load_scores()
    
    def load_scores(self):
        try:
            if os.path.exists(self.scores_file):
                with open(self.scores_file, 'r', encoding='utf-8') as f:
                    self.scores = json.load(f)
                print(f"Pontuações carregadas: {len(self.scores)} registros")
            else:
                self.scores = []
                print("Nenhum arquivo de pontuações encontrado, criando novo")
        except Exception as e:
            print(f"Erro ao carregar pontuações: {e}")
            self.scores = []
    
    def save_scores(self):
        try:
            with open(self.scores_file, 'w', encoding='utf-8') as f:
                json.dump(self.scores, f, ensure_ascii=False, indent=2)
            print(f"Pontuações salvas: {len(self.scores)} registros")
            return True
        except Exception as e:
            print(f"Erro ao salvar pontuações: {e}")
            return False
    
    def add_score(self, player_name, song_name, score):
        score_entry = {
            "player_name": player_name,
            "song_name": song_name,
            "score": score,
            "date": datetime.now().strftime("%d/%m/%Y %H:%M"),
            "timestamp": datetime.now().timestamp()
        }
        
        self.scores.append(score_entry)
        self.scores.sort(key=lambda x: x['score'], reverse=True)
        
        if len(self.scores) > 50:
            self.scores = self.scores[:50]
        
        self.save_scores()
        print(f"Nova pontuação adicionada: {player_name} - {song_name} - {score}")
    
    def get_top_scores(self, limit=10):
        return self.scores[:limit]
    
    def get_player_scores(self, player_name):
        return [score for score in self.scores if score['player_name'].lower() == player_name.lower()]
    
    def get_song_scores(self, song_name):
        return [score for score in self.scores if song_name.lower() in score['song_name'].lower()]
    
    def clear_scores(self):
        self.scores = []
        self.save_scores()
        print("Todas as pontuações foram limpas")
    
    def get_stats(self):
        if not self.scores:
            return {
                "total_scores": 0,
                "best_score": 0,
                "average_score": 0,
                "unique_players": 0,
                "unique_songs": 0
            }
        
        total_scores = len(self.scores)
        best_score = max(self.scores, key=lambda x: x['score'])['score']
        average_score = sum(score['score'] for score in self.scores) / total_scores
        
        unique_players = len(set(score['player_name'] for score in self.scores))
        unique_songs = len(set(score['song_name'] for score in self.scores))
        
        return {
            "total_scores": total_scores,
            "best_score": best_score,
            "average_score": round(average_score, 2),
            "unique_players": unique_players,
            "unique_songs": unique_songs
        }
