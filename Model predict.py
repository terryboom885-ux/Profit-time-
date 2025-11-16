import numpy as np

class SimplePredictor:
    def predict_win_probability(self, team_stats):
        base = 0.50
        rating_adjustment = (team_stats["rating_diff"] * 0.12)
        form_adjustment = (team_stats["form_diff"] * 0.10)
        final_prob = base + rating_adjustment + form_adjustment
        return float(np.clip(final_prob, 0.05, 0.95))
