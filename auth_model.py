# auth_model.py
import random

def analyze_touch(base_similarity):
    """
    Simulates a trained model analyzing touch patterns.
    It returns a slightly randomized similarity score to make the
    simulation more dynamic.

    Args:
        base_similarity (float): The base similarity score from the scenario.

    Returns:
        float: A simulated, randomized similarity score.
    """
    # A normal touch pattern has very little variance in its score
    if base_similarity > 0.5:
        variance = random.uniform(-0.03, 0.02) # 0.50 -> 0.47 to 0.52
    # An anomalous touch has more variance, as it's less predictable
    else:
        variance = random.uniform(-0.05, 0.05) # 0.25 -> 0.20 to 0.30

    # Calculate the final simulated score
    simulated_score = base_similarity + variance
    
    # Ensure the score stays within the logical bounds of 0.0 and 1.0
    return max(0.0, min(1.0, simulated_score))