import json
import os
import re
from typing import Any, Dict, List, Optional, Tuple

PROMPTS_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "prompts")

# Shared between the Streamlit dropdown and the agent so they can't drift apart.
SAMPLE_PROFILES: Dict[str, str] = {
    "K-pop rock": "I love high-energy K-pop with rock/band instrumentation, electric guitars, and powerful vocals.",
    "K-pop pop": "I want bright, upbeat, radio-friendly K-pop dance-pop with catchy hooks.",
    "K-pop ballad": "I'm in the mood for slow, emotional K-pop ballads with soft vocals.",
    "K-pop hip-hop": "Recommend K-pop songs with strong hip-hop/rap sections and a heavy beat.",
    "K-pop retro/nostalgic": "I like K-pop with a retro, 90s/2000s-inspired or nostalgic sound.",
}


def _load_prompt(filename: str) -> str:
    with open(os.path.join(PROMPTS_DIR, filename), "r", encoding="utf-8") as f:
        return f.read()


def build_user_prompt(profile_text: str) -> str:
    template = _load_prompt("kpop_recommender_user.txt")
    return template.replace("{{PROFILE}}", profile_text.strip())


def _strip_code_fences(text: str) -> str:
    text = text.strip()
    match = re.search(r"```(?:json)?\s*(.*?)\s*```", text, flags=re.DOTALL | re.IGNORECASE)
    return match.group(1) if match else text


def _extract_first_json_array(s: str) -> Optional[str]:
    start = s.find("[")
    if start == -1:
        return None
    depth = 0
    for i in range(start, len(s)):
        if s[i] == "[":
            depth += 1
        elif s[i] == "]":
            depth -= 1
            if depth == 0:
                return s[start:i + 1]
    return None


def _try_json_loads(s: Optional[str]) -> Any:
    if s is None:
        return None
    try:
        return json.loads(s)
    except Exception:
        return None


def validate_songs(raw_text: str) -> Tuple[Optional[List[Dict[str, Any]]], Optional[str]]:
    """
    Parses and validates model output against the required schema: a JSON
    array of exactly 4 {title, artist, reason, match_score} objects, non-empty
    title/artist/reason strings, match_score an integer 1-10, no duplicate
    (title, artist) pairs (case-insensitive).

    Returns (songs, None) on success, or (None, error_message) on failure.
    """
    cleaned = _strip_code_fences(raw_text).strip()
    parsed = _try_json_loads(cleaned)
    if not isinstance(parsed, list):
        array_str = _extract_first_json_array(cleaned)
        parsed = _try_json_loads(array_str)

    if not isinstance(parsed, list):
        return None, "Response was not a parseable JSON array."

    if len(parsed) != 4:
        return None, f"Expected exactly 4 songs, got {len(parsed)}."

    songs: List[Dict[str, Any]] = []
    seen = set()
    for item in parsed:
        if not isinstance(item, dict):
            return None, "Each entry must be a JSON object."
        title = str(item.get("title", "")).strip()
        artist = str(item.get("artist", "")).strip()
        reason = str(item.get("reason", "")).strip()
        if not title or not artist:
            return None, "Every song needs a non-empty title and artist."
        if not reason:
            return None, "Every song needs a non-empty reason."

        match_score = item.get("match_score")
        if isinstance(match_score, bool) or not isinstance(match_score, (int, float)):
            return None, "match_score must be a number."
        match_score = int(match_score)
        if not 1 <= match_score <= 10:
            return None, "match_score must be between 1 and 10."

        key = (title.lower(), artist.lower())
        if key in seen:
            return None, "Duplicate song detected in the response."
        seen.add(key)
        songs.append({"title": title, "artist": artist, "reason": reason, "match_score": match_score})

    return songs, None


def get_recommendations(profile_text: str, client: Any, max_retries: int = 1) -> Dict[str, Any]:
    """
    Calls the client, validates the response, and retries once (with a
    stricter system prompt) if validation fails. Fails gracefully after
    the retry is exhausted.
    """
    logs: List[Dict[str, str]] = []
    system_prompt = _load_prompt("kpop_recommender_system.txt")
    user_prompt = build_user_prompt(profile_text)

    attempt = 1
    raw = client.complete(system_prompt=system_prompt, user_prompt=user_prompt)
    logs.append({"attempt": str(attempt), "raw": raw})
    songs, error = validate_songs(raw)

    if songs is not None:
        logs.append({"attempt": str(attempt), "result": "valid"})
        return {"status": "ok", "songs": songs, "attempts": attempt, "error": None, "logs": logs}

    logs.append({"attempt": str(attempt), "result": f"invalid: {error}"})

    if max_retries >= 1:
        attempt = 2
        retry_system_prompt = _load_prompt("kpop_recommender_retry_system.txt")
        raw2 = client.complete(system_prompt=retry_system_prompt, user_prompt=user_prompt)
        logs.append({"attempt": str(attempt), "raw": raw2})
        songs2, error2 = validate_songs(raw2)

        if songs2 is not None:
            logs.append({"attempt": str(attempt), "result": "valid"})
            return {"status": "ok", "songs": songs2, "attempts": attempt, "error": None, "logs": logs}

        logs.append({"attempt": str(attempt), "result": f"invalid: {error2}"})
        return {"status": "failed", "songs": [], "attempts": attempt, "error": error2, "logs": logs}

    return {"status": "failed", "songs": [], "attempts": attempt, "error": error, "logs": logs}
