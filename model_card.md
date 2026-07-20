# 🎧 Model Card: Music Recommender Simulation

## 1. Model Name

Give your model a short, descriptive name.  
Example: **Very Flawed Music Recommender 1.0**

---

## 2. Intended Use

Describe what your recommender is designed to do and who it is for.

Prompts:

- What kind of recommendations does it generate
- What assumptions does it make about the user
- Is this for real users or classroom exploration

This recommender takes a user's favorite genre, mood, and energy level and returns a short ranked list of songs from the catalog that best match those preferences. It assumes the user already knows what they want and can describe it, rather than learning their taste from listening history like a real streaming app would. This is a classroom project meant to explore how recommendation scoring works, not a system built for real listeners.

---

## 3. How the Model Works

Explain your scoring approach in simple language.

Prompts:

- What features of each song are used (genre, energy, mood, etc.)
- What user preferences are considered
- How does the model turn those into a score
- What changes did you make from the starter logic

Avoid code here. Pretend you are explaining the idea to a friend who does not program.

The recommender is content-based: it scores each song by comparing genre, mood, energy, and danceability against a taste profile (favorite genre: k-pop, favorite mood: energetic, target energy: 0.85, target danceability: 0.85). Genre and mood are scored as exact matches (1 if it matches your favorite, 0 otherwise), while energy and danceability use a "closer is better" formula (1 - distance²) that rewards songs near your target values rather than simply higher or lower. These per-feature scores are combined into one weighted total, and songs are ranked highest-to-lowest to produce the final recommendations.

- At the moment, I'm putting more emphasis on similar genre, so it'll have more points in our scoring system.

---

## 4. Data

Describe the dataset the model uses.

Prompts:

- How many songs are in the catalog
- What genres or moods are represented
- Did you add or remove data
- Are there parts of musical taste missing in the dataset

The catalog has 18 songs covering 12 genres like pop, lofi, k-pop, anime, rock, and jazz, but most genres only have 1 or 2 songs, so the choices within any single genre are pretty limited. I didn't add or remove any songs, so this is just the starter dataset. It's missing things like lyrics, language, or artist popularity, and it has no record of what a real user has actually listened to before, so it can only compare stated preferences to song tags rather than real listening habits.

---

## 5. Strengths

Where does your system seem to work well

Prompts:

- User types for which it gives reasonable results
- Any patterns you think your scoring captures correctly
- Cases where the recommendations matched your intuition

It works best for users who know their favorite genre and mood, since a song that matches both usually gets a high score and lands near the top of the list. The energy scoring also makes sense to me, since it gives higher points to songs closer to the target energy instead of just picking the highest energy song. Overall, when a user's genre, mood, and energy all line up with a real song in the catalog, the top recommendation feels like a genuinely good match.

---

## 6. Limitations and Bias

Where the system struggles or behaves unfairly.

Prompts:

- Features it does not consider
- Genres or moods that are underrepresented
- Cases where the system overfits to one preference
- Ways the scoring might unintentionally favor some users

Mood is exact-string-match only. "Energetic" and "intense" are conceptually close (both high-arousal), but our system treats them as totally unrelated (0 credit) the same way it treats "energetic" vs. "chill" (also 0 credit).
A single-genre preference only helps when actual k-pop/anime tracks appear. If the whole catalog were non-k-pop or non-anime, then we risk not even recommending anything to the user, or at most recommending them unrelated songs altogether.

This comes into play if our dataset wasn't so diverse. If our dataset only had one genre like rock, or our there was only one Mood in our dataset chill, and our user profile was set to energetic kpop, then our recommender would not be able to recommend any music in the catalogue.

Genre is still the most dominant attribute when it comes to which songs to recommend. Because of the 2:1 ratio of the scoring, the mood/energy/acoustic traits points will be negligible as long as the genre is a perfect match for the user. Users who don't specify a genre are generally at a disadvantaged

---

## 7. Evaluation

How you checked whether the recommender behaved as expected.

Prompts:

- Which user profiles you tested
- What you looked for in the recommendations
- What surprised you
- Any simple tests or comparisons you ran

No need for numeric metrics unless you created some.

```
user_prefs = {"genre": "anime", "mood": "sad", "energy": 0.3}
user_prefs = {"genre": "k-pop", "mood": "energetic", "energy": 0.9}
user_prefs = {"genre": "pop", "mood": "happy", "energy": 0.8}
```

**anime/sad/0.3 vs. pop/happy/0.8** — Anime has no "sad" song in the catalog, so its top picks (Cherry Blossom Vow, 2.94) win on genre+energy alone with zero mood bonus, while pop's top pick (Sunrise City, 4.00) gets a genuine 3-for-3 match. Same algorithm, very different match quality, just because of which moods happen to exist per genre.

**k-pop/energetic/0.9 vs. pop/happy/0.8** — Using `"genre": "kpop"` (no hyphen) surprisingly scored zero genre bonus for any k-pop song, because the catalog spells it `"k-pop"` and matching is exact-string — no error, just a silent miss. Correcting to `"k-pop"` fixed it immediately (Neon Dream/Overdrive Anthem hit 4.00, matching pop's quality), showing exact-string matching isn't so reliable.

---

## 8. Future Work

Ideas for how you would improve the model next.

Prompts:

- Additional features or preferences
- Better ways to explain recommendations
- Improving diversity among the top results
- Handling more complex user tastes

I'd want to make genre and mood matching case-insensitive and a little more forgiving of small typos or spelling variants, since the "kpop" vs "k-pop" test showed how easily an exact-string match can silently fail. I'd also add a rule that limits how many songs from the same artist can appear in one top-5 list, so a user doesn't just get 3 songs from the same artist because that artist happens to dominate their favorite genre. It would help to let mood partially match related moods (like "energetic" and "intense") instead of an all-or-nothing match, and to let a user list a couple of genres or moods instead of just one, so people with broader or mixed taste aren't ignored.

I'd also like to lower how much genre matching dominates the score and give more credit to mood, energy, and acousticness, since right now a genre match almost always wins out over everything else and that just keeps recommending the same familiar genre instead of encouraging discovery. On top of that, I'd add some intentional variety into the top results, like reserving a slot or two for a well-matched song outside the user's stated genre, so the recommender nudges people toward new artists and genres instead of just reinforcing what they already listen to.

---

## 9. Personal Reflection

A few sentences about your experience.

Prompts:

- What you learned about recommender systems
- Something unexpected or interesting you discovered
- How this changed the way you think about music recommendation apps

Building this made me realize that even though there are tons of streaming services out there, the way each one handles recommendations under the hood can be really different depending on how their scoring is set up. Mine ended up with an inherent bias toward genre since I weighted it the heaviest, but a different service could just as easily be biased toward something like energy, tempo, or how popular a song already is, and a listener would probably never know which one they're getting. The most unexpected thing I found while testing was that typing "kpop" instead of "k-pop" made every k-pop song lose its genre match completely, with no error or warning, it just quietly swapped in other songs that only happened to share a similar energy value. That was a good reminder that these systems only "understand" exactly what's typed, not what's meant, so a tiny typo can completely change someone's results without them ever knowing why. It made me think that the recommendations we get every day aren't neutral, they're a reflection of whatever the designer decided mattered most, and that can quietly shape what kind of music we end up discovering or never discovering at all.
