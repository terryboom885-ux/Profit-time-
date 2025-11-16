import time
from api.odds_api import get_all_sports, get_odds, filter_upcoming_games
from model.predictor import SimplePredictor
from utils.ev import expected_value
from utils.probability import meet_confidence
from utils.formatting import format_pick_output
from bankroll.kelly import recommended_stake

BANKROLL = 250  # you may change this
MODEL = SimplePredictor()

def generate_reasoning(stats):
    return (
        f"{stats['team']} enters with a rating advantage of "
        f"{stats['rating_diff']}, recent form advantage of "
        f"{stats['form_diff']}, and overall matchup edge."
    )

def analyze_game(event):
    picks = []
    for bookmaker in event["bookmakers"]:
        for market in bookmaker["markets"]:
            if market["key"] == "h2h":  # moneyline
                for outcome in market["outcomes"]:
                    team = outcome["name"]
                    odds = float(outcome["price"])

                    stats = {
                        "team": team,
                        "rating_diff": 0.10,  # placeholder
                        "form_diff": 0.15     # placeholder
                    }

                    prob = MODEL.predict_win_probability(stats)
                    if not meet_confidence(prob):
                        continue

                    ev = expected_value(prob, odds)
                    if ev <= 0:
                        continue

                    stake = recommended_stake(BANKROLL, prob, odds)
                    reasoning = generate_reasoning(stats)

                    picks.append(
                        format_pick_output(team, prob, odds, ev, reasoning, stake)
                    )
    return picks

def main():
    print("Fetching sports...")
    sports = get_all_sports()

    final_picks = []
    for sport in sports:
        key = sport["key"]
        print(f"Checking {key}...")

        events = get_odds(key)
        if not isinstance(events, list):
            continue

        upcoming = filter_upcoming_games(events)

        for event in upcoming:
            game_picks = analyze_game(event)
            final_picks.extend(game_picks)

    if not final_picks:
        print("\nNo high-confidence picks in the next 24–48 hours.")
    else:
        print("\n=== TODAY'S AI PICKS ===\n")
        for p in final_picks:
            print(p)

if __name__ == "__main__":
    main()
