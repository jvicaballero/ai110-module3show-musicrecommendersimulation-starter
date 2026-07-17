# 🎧 Model Card: Music Recommender Simulation

## 1. Model Name

Give your model a short, descriptive name.  
Example: **VibeFinder 1.0**

---

## 2. Intended Use

Describe what your recommender is designed to do and who it is for.

Prompts:

- What kind of recommendations does it generate
- What assumptions does it make about the user
- Is this for real users or classroom exploration

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

---

## 5. Strengths

Where does your system seem to work well

Prompts:

- User types for which it gives reasonable results
- Any patterns you think your scoring captures correctly
- Cases where the recommendations matched your intuition

---

## 6. Limitations and Bias

Where the system struggles or behaves unfairly.

Prompts:

- Features it does not consider
- Genres or moods that are underrepresented
- Cases where the system overfits to one preference
- Ways the scoring might unintentionally favor some users

Mood is exact-string-match only. "Energetic" and "intense" are conceptually close (both high-arousal), but our system treats them as totally unrelated (0 credit) the same way it treats "energetic" vs. "chill" (also 0 credit).
A single-genre preference only helps when actual k-pop/anime tracks appear. For everything else, genre is a wash. If your whole catalog were non-k-pop

This comes into play if our dataset wasn't so diverse. If our dataset only had one genre like rock, or our there was only one Mood in our dataset chill, and our user profile was set to energetic kpop, then our recommender would not be able to recommend any music in the catalogue.

---

## 7. Evaluation

How you checked whether the recommender behaved as expected.

Prompts:

- Which user profiles you tested
- What you looked for in the recommendations
- What surprised you
- Any simple tests or comparisons you ran

No need for numeric metrics unless you created some.

---

## 8. Future Work

Ideas for how you would improve the model next.

Prompts:

- Additional features or preferences
- Better ways to explain recommendations
- Improving diversity among the top results
- Handling more complex user tastes

---

## 9. Personal Reflection

A few sentences about your experience.

Prompts:

- What you learned about recommender systems
- Something unexpected or interesting you discovered
- How this changed the way you think about music recommendation apps
