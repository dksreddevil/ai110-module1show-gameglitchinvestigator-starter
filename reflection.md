# 💭 Reflection: Game Glitch Investigator

Answer each question in 3 to 5 sentences. Be specific and honest about what actually happened while you worked. This is about your process, not trying to sound perfect.

## 1. What was broken when you started?

- What did the game look like the first time you ran it?
- List at least two concrete bugs you noticed at the start
  (for example: "the secret number kept changing" or "the hints were backwards").

**Bug 1 — Attempts counter off by one**
- **Expected:** On first load, the game should show the full number of attempts available (e.g. 8 for Normal difficulty) since the player has not guessed yet.
- **What actually happened:** The counter showed 7 on the very first load because `st.session_state.attempts` was initialized to `1` instead of `0`, so the player always appeared to have already used one attempt before making any guess.

**Bug 2 — Info bar showed wrong range**
- **Expected:** The info bar should tell the player the correct range for the selected difficulty (e.g. "between 1 and 20" for Easy).
- **What actually happened:** It always displayed "between 1 and 100" regardless of difficulty, because the values were hardcoded instead of using the `low` and `high` variables — so Easy and Hard players were given misleading information about the valid range.

**Bug 3 — Hint messages were backwards**
- **Expected:** If the guess is too high, the hint should tell the player to guess lower, and vice versa.
- **What actually happened:** The messages in `check_guess()` were swapped — guessing too high showed "Go HIGHER!" and guessing too low showed "Go LOWER!", which actively pointed the player in the wrong direction every single time.

## 2. How did you use AI as a teammate?

I used **Claude Code** as my primary AI tool throughout this project. I described bugs I was seeing, shared relevant code snippets, and asked Claude to explain what was wrong and suggest fixes — working through the problems conversationally rather than just asking for a finished solution.

**Correct suggestion — off-by-one in `update_score`:** I noticed that winning on the first attempt gave fewer points than expected. I shared the `update_score` function and Claude immediately identified that the formula used `attempt_number + 1` instead of `attempt_number`, inflating the penalty by one full attempt's worth every time. I verified it by writing `test_win_on_first_attempt_scores_90`: with `attempt_number=1` the formula `100 - 10 * 1` should return 90, and after the fix it did.

**Incorrect or misleading suggestion — even/odd secret type-cast:** Early on, Claude suggested the even-attempt string-cast bug in `check_guess` might be an intentional type-coercion fallback for edge cases, rather than deliberate sabotage. That framing was misleading — it caused me to second-guess removing the `TypeError` branch. I verified it was pure sabotage by writing a test that called `check_guess(50, 50)` with the secret as a plain int, confirmed it returned `"Win"` correctly without any casting, and then removed the entire branch with confidence.

---

## 3. Debugging and testing your fixes

A bug wasn't considered fixed until a pytest test passed that would have failed against the original code. I didn't trust visual inspection alone — too many of the bugs were subtle (like the even-attempt score reward) and easy to miss by just playing the game manually.

**Test I ran — `test_too_high_message_says_go_lower`:** I ran `pytest tests/test_game_logic.py::test_too_high_message_says_go_lower` while the swapped-arrow bug was still in place and it failed with `AssertionError: Expected 'LOWER' in message, got: '📈 Go HIGHER!'`. That failure was concrete proof the bug existed. After swapping the return strings in `check_guess`, the test passed — that was my signal the fix was real and not just a lucky manual play.

**AI helped design the `parse_guess` tests:** I described the invalid-input bug to Claude ("typing 'abc' was counting as an attempt") and Claude suggested writing separate tests for empty string, non-numeric input, a valid integer, and a decimal string like `"7.9"`. I hadn't thought to test the decimal case — that test revealed the `int(float(raw))` path needed to be explicitly preserved, which shaped how I wrote the fix.

---

## 4. What did you learn about Streamlit and state?

The secret number kept changing because Streamlit re-executes the entire script from top to bottom on every interaction — every button click, every text input, every sidebar change. In the original app, `random.randint(low, high)` was called unconditionally at the top level, so a new secret was generated on every single rerun. The player was essentially chasing a moving target.

Streamlit "reruns" are like refreshing a webpage, except they happen automatically whenever the user does anything. `st.session_state` is a dictionary that survives across those reruns — it's the one place where data persists between them. I'd explain it to a friend like this: imagine your entire Python script is a function that gets called fresh every time someone clicks a button. `session_state` is a notepad sitting outside that function — you can read and write to it, and whatever you wrote last time is still there when the function runs again.

The fix was wrapping the secret generation in a `if "secret" not in st.session_state:` guard. That way `random.randint` only runs once — the very first time the page loads — and every subsequent rerun just reads the already-stored value without generating a new one.

---

## 5. Looking ahead: your developer habits

The habit I want to keep is writing a failing test *before* claiming a bug is fixed. On this project, that discipline caught cases where my fix looked right visually but the test revealed I'd only partially solved the problem — like when I corrected the swap in `check_guess` but still had the wrong emoji on the wrong branch. Having a red test first meant I always knew exactly what "done" looked like.

Next time I work with AI on a coding task, I'd ask it to explain its reasoning before I accept a suggestion, especially for anything it labels as an "edge case" or "intentional design." On this project I trusted Claude's framing of the type-cast branch too quickly, which wasted time. A simple "why do you think this exists?" would have surfaced the doubt faster.

This project changed how I think about AI-generated code by making it concrete that AI can introduce bugs that look intentional and are hard to spot without tests. I used to assume AI output was either obviously right or obviously broken — now I know the most dangerous bugs are the subtle ones that make the code *almost* work, and that tests are the only reliable way to tell the difference.
