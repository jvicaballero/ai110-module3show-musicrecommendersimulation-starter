from kpop_agent import get_recommendations, validate_songs

VALID_JSON = (
    '[{"title":"Dynamite","artist":"BTS","reason":"High-energy, upbeat pop.","match_score":9},'
    '{"title":"How You Like That","artist":"BLACKPINK","reason":"Powerful, anthemic chorus.","match_score":8},'
    '{"title":"Next Level","artist":"aespa","reason":"Driving, energetic production.","match_score":8},'
    '{"title":"God\'s Menu","artist":"Stray Kids","reason":"Aggressive, high-tempo energy.","match_score":7}]'
)


class GoodClient:
    def complete(self, system_prompt, user_prompt):
        return VALID_JSON


class BadThenGoodClient:
    """Returns malformed output on the first call, valid JSON on the retry."""

    def __init__(self):
        self.calls = 0

    def complete(self, system_prompt, user_prompt):
        self.calls += 1
        if self.calls == 1:
            return "Sure, here are some songs: Dynamite by BTS..."
        return VALID_JSON


class AlwaysBadClient:
    def complete(self, system_prompt, user_prompt):
        return "not json at all"


def test_valid_response_returns_ok_on_first_attempt():
    result = get_recommendations("energetic k-pop", GoodClient())
    assert result["status"] == "ok"
    assert result["attempts"] == 1
    assert len(result["songs"]) == 4
    assert result["songs"][0]["reason"]
    assert 1 <= result["songs"][0]["match_score"] <= 10


def test_malformed_first_response_triggers_retry_and_succeeds():
    result = get_recommendations("energetic k-pop", BadThenGoodClient())
    assert result["status"] == "ok"
    assert result["attempts"] == 2


def test_always_bad_response_fails_gracefully_after_retry():
    result = get_recommendations("energetic k-pop", AlwaysBadClient())
    assert result["status"] == "failed"
    assert result["attempts"] == 2
    assert result["songs"] == []


def test_validate_songs_rejects_duplicates():
    dup = (
        '[{"title":"A","artist":"X","reason":"r","match_score":5},'
        '{"title":"A","artist":"X","reason":"r","match_score":5},'
        '{"title":"B","artist":"Y","reason":"r","match_score":5},'
        '{"title":"C","artist":"Z","reason":"r","match_score":5}]'
    )
    songs, error = validate_songs(dup)
    assert songs is None
    assert "Duplicate" in error


def test_validate_songs_rejects_wrong_count():
    only_two = (
        '[{"title":"A","artist":"X","reason":"r","match_score":5},'
        '{"title":"B","artist":"Y","reason":"r","match_score":5}]'
    )
    songs, error = validate_songs(only_two)
    assert songs is None
    assert "Expected exactly 4" in error


def test_validate_songs_rejects_missing_reason():
    missing_reason = (
        '[{"title":"A","artist":"X","match_score":5},'
        '{"title":"B","artist":"Y","reason":"r","match_score":5},'
        '{"title":"C","artist":"Z","reason":"r","match_score":5},'
        '{"title":"D","artist":"W","reason":"r","match_score":5}]'
    )
    songs, error = validate_songs(missing_reason)
    assert songs is None
    assert "reason" in error


def test_validate_songs_rejects_out_of_range_match_score():
    bad_score = (
        '[{"title":"A","artist":"X","reason":"r","match_score":11},'
        '{"title":"B","artist":"Y","reason":"r","match_score":5},'
        '{"title":"C","artist":"Z","reason":"r","match_score":5},'
        '{"title":"D","artist":"W","reason":"r","match_score":5}]'
    )
    songs, error = validate_songs(bad_score)
    assert songs is None
    assert "match_score" in error
