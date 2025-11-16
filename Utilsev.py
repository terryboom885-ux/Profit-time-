def implied_probability(decimal_odds):
    return 1 / decimal_odds

def expected_value(model_prob, odds):
    imp = implied_probability(odds)
    return (model_prob * odds) - 1
