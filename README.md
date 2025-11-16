# Sports Betting AI Bot

This bot:
- Pulls odds from The Odds API
- Generates predictions using a statistical ML-like model
- Returns ONLY picks with 70%+ confidence
- Calculates EV (Expected Value)
- Gives reasoning for each pick
- Recommends stake size using Kelly Criterion
- Only shows games occurring in the next 24-48 hours
- Refreshes every midnight

Run:
    python3 main.py
