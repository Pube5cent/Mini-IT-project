def check_rebirth_eligibility(score, threshold=1000):
    """Return True if score meets rebirth threshold."""
    return score >= threshold

def perform_rebirth(player_state):
    """
    Resets score and boosts multipliers or adds perks.
    Modify player_state dict in-place.
    """
    if not check_rebirth_eligibility(player_state["score"]):
        return False

    # Reset score and add rebirth bonuses
    player_state["rebirths"] += 1
    player_state["score"] = 0
    player_state["multiplier"] += 2.0  # Increase score gain rate

    return True
