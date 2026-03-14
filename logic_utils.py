def get_range_for_difficulty(difficulty: str):
    """Return (low, high) inclusive range for a given difficulty."""
    if difficulty == "Easy":
        return 1, 20
    if difficulty == "Normal":
        return 1, 100
    # Fix: Hard was 1–50 (easier than Normal!). I spotted the logic error;
    # AI confirmed it should exceed Normal's range and suggested 1–200.
    if difficulty == "Hard":
        return 1, 200
    return 1, 100


def parse_guess(raw: str):
    """
    Parse user input into an int guess.

    Returns: (ok: bool, guess_int: int | None, error_message: str | None)
    """
    if raw is None:
        return False, None, "Enter a guess."

    if raw == "":
        return False, None, "Enter a guess."

    try:
        if "." in raw:
            value = int(float(raw))
        else:
            value = int(raw)
    except Exception:
        return False, None, "That is not a number."

    return True, value, None


def check_guess(guess, secret):
    """
    Compare guess to secret and return (outcome, message).

    outcome examples: "Win", "Too High", "Too Low"
    """
    if guess == secret:
        return "Win", "🎉 Correct!"
    # Fix: emoji arrows were swapped — "Too High" said Go HIGHER and vice versa.
    # I wrote a failing test to prove it; AI helped correct the messages.
    if guess > secret:
        return "Too High", "📉 Go LOWER!"
    return "Too Low", "📈 Go HIGHER!"


def update_score(current_score: int, outcome: str, attempt_number: int):
    """Update score based on outcome and attempt number."""
    if outcome == "Win":
        # Fix: original used attempt_number+1, which over-penalized every win.
        # AI caught the off-by-one; I verified with a test at attempt 1 expecting 90.
        points = 100 - 10 * attempt_number
        if points < 10:
            points = 10
        return current_score + points

    # Fix: original gave +5 points on even-numbered Too High guesses (a hidden reward bug).
    # I noticed scores were sometimes going up on wrong guesses; AI simplified to always deduct 5.
    if outcome in ("Too High", "Too Low"):
        return current_score - 5

    return current_score
