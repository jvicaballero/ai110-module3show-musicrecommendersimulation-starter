import csv
from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass

@dataclass
class Song:
    """
    Represents a song and its attributes.
    Required by tests/test_recommender.py
    """
    id: int
    title: str
    artist: str
    genre: str
    mood: str
    energy: float
    tempo_bpm: float
    valence: float
    danceability: float
    acousticness: float

@dataclass
class UserProfile:
    """
    Represents a user's taste preferences.
    Required by tests/test_recommender.py
    """
    favorite_genre: str
    favorite_mood: str
    target_energy: float
    likes_acoustic: bool

class Recommender:
    """
    OOP implementation of the recommendation logic.
    Required by tests/test_recommender.py
    """
    def __init__(self, songs: List[Song]):
        self.songs = songs

    def recommend(self, user: UserProfile, k: int = 5) -> List[Song]:
        # TODO: Implement recommendation logic
        return self.songs[:k]

    def explain_recommendation(self, user: UserProfile, song: Song) -> str:
        # TODO: Implement explanation logic
        return "Explanation placeholder"

def load_songs(csv_path: str) -> List[Dict]:
    """Reads a songs CSV into a list of dicts with numeric fields cast to int/float."""
    songs = []
    with open(csv_path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            songs.append({
                "id": int(row["id"]),
                "title": row["title"],
                "artist": row["artist"],
                "genre": row["genre"],
                "mood": row["mood"],
                "energy": float(row["energy"]),
                "tempo_bpm": float(row["tempo_bpm"]),
                "valence": float(row["valence"]),
                "danceability": float(row["danceability"]),
                "acousticness": float(row["acousticness"]),
            })
    return songs

def score_song(user_prefs: Dict, song: Dict) -> Tuple[float, List[str]]:
    """Scores one song against user_prefs (genre, mood, energy, acoustic) and returns (score, reasons)."""
    score = 0.0
    reasons = []

    if user_prefs.get("genre") is not None and song["genre"] == user_prefs["genre"]:
        score += 2.0
        reasons.append(f"genre match: {song['genre']} (+2.0)")

    if user_prefs.get("mood") is not None and song["mood"] == user_prefs["mood"]:
        score += 1.0
        reasons.append(f"mood match: {song['mood']} (+1.0)")

    target_energy = user_prefs.get("energy")
    if target_energy is not None:
        energy_points = max(0.0, 1.0 - (song["energy"] - target_energy) ** 2)
        score += energy_points
        reasons.append(f"energy {song['energy']:.2f} close to target {target_energy:.2f} (+{energy_points:.2f})")

    likes_acoustic = user_prefs.get("acoustic")
    if likes_acoustic is not None:
        song_is_acoustic = song["acousticness"] > 0.6
        if song_is_acoustic == likes_acoustic:
            score += 0.5
            reasons.append("acousticness matches your preference (+0.5)")

    return score, reasons

def recommend_songs(user_prefs: Dict, songs: List[Dict], k: int = 5) -> List[Tuple[Dict, float, str]]:
    """Scores every song, sorts by score descending, and returns the top k with explanations."""
    scored = [(song, *score_song(user_prefs, song)) for song in songs]
    scored.sort(key=lambda entry: entry[1], reverse=True)

    return [
        (song, score, "; ".join(reasons) if reasons else "no strong matches")
        for song, score, reasons in scored[:k]
    ]
