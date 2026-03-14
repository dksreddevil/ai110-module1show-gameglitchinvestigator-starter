from logic_utils import check_guess, get_range_for_difficulty, update_score, parse_guess


# ── Existing starter tests (fixed to unpack the (outcome, message) tuple) ──────

def test_winning_guess():
    outcome, _ = check_guess(50, 50)
    assert outcome == "Win"

def test_guess_too_high():
    outcome, _ = check_guess(60, 50)
    assert outcome == "Too High"

def test_guess_too_low():
    outcome, _ = check_guess(40, 50)
    assert outcome == "Too Low"


# ── Bug: Hard difficulty range was 1–50 (easier than Normal 1–100) ─────────────

def test_hard_range_is_harder_than_normal():
    _, normal_high = get_range_for_difficulty("Normal")
    _, hard_high = get_range_for_difficulty("Hard")
    assert hard_high > normal_high, (
        f"Hard range top ({hard_high}) should exceed Normal ({normal_high})"
    )

def test_easy_range_is_smaller_than_normal():
    _, easy_high = get_range_for_difficulty("Easy")
    _, normal_high = get_range_for_difficulty("Normal")
    assert easy_high < normal_high


# ── Bug: check_guess emoji arrows were swapped ────────────────────────────────

def test_too_high_message_says_go_lower():
    # Guess (80) > secret (50) → hint must tell player to go lower
    _, message = check_guess(80, 50)
    assert "LOWER" in message, f"Expected 'LOWER' in message, got: {message!r}"

def test_too_low_message_says_go_higher():
    # Guess (20) < secret (50) → hint must tell player to go higher
    _, message = check_guess(20, 50)
    assert "HIGHER" in message, f"Expected 'HIGHER' in message, got: {message!r}"


# ── Bug: update_score Win used attempt_number+1, inflating the penalty ────────

def test_win_on_first_attempt_scores_90():
    # attempt 1 → 100 - 10*1 = 90 points
    score = update_score(0, "Win", attempt_number=1)
    assert score == 90, f"Expected 90, got {score}"

def test_win_on_second_attempt_scores_80():
    score = update_score(0, "Win", attempt_number=2)
    assert score == 80

def test_win_score_floor_is_10():
    # attempt 10+ → should floor at 10, not go negative
    score = update_score(0, "Win", attempt_number=15)
    assert score == 10


# ── Bug: update_score awarded +5 on even-numbered Too High guesses ────────────

def test_too_high_on_even_attempt_deducts_score():
    # attempt 2 (even) used to award +5; should always deduct 5
    score = update_score(100, "Too High", attempt_number=2)
    assert score == 95, f"Expected 95 (deduct 5), got {score}"

def test_too_high_on_odd_attempt_deducts_score():
    score = update_score(100, "Too High", attempt_number=3)
    assert score == 95

def test_too_low_always_deducts_score():
    score = update_score(100, "Too Low", attempt_number=2)
    assert score == 95


# ── Bug: invalid input still counted as an attempt ───────────────────────────

def test_parse_guess_rejects_empty_string():
    ok, value, err = parse_guess("")
    assert not ok
    assert value is None
    assert err is not None

def test_parse_guess_rejects_non_numeric():
    ok, value, _ = parse_guess("abc")
    assert not ok
    assert value is None

def test_parse_guess_accepts_valid_integer():
    ok, value, err = parse_guess("42")
    assert ok
    assert value == 42
    assert err is None

def test_parse_guess_accepts_decimal_string():
    # "7.9" should parse to int 7
    ok, value, err = parse_guess("7.9")
    assert ok
    assert value == 7
