# 🎵 Music Recommender Simulation

## Project Summary

In this project you will build and explain a small music recommender system.

Your goal is to:

- Represent songs and a user "taste profile" as data
- Design a scoring rule that turns that data into recommendations
- Evaluate what your system gets right and wrong
- Reflect on how this mirrors real world AI recommenders

Replace this paragraph with your own summary of what your version does.

---

## How The System Works

Explain your design in plain language.

Some prompts to answer:

- What features does each `Song` use in your system
  - For example: genre, mood, energy, tempo
- What information does your `UserProfile` store
- How does your `Recommender` compute a score for each song
- How do you choose which songs to recommend

You can include a simple diagram or bullet list if helpful.

- From how popular streaming platforms work (I.e Spotify and Youtube Premium), the recommender uses collaborative filtering which looks at the users prefernces in music by checking the history of what they listened to, and check other users' history who have a similar history and will recommend songs based on this historical data. There is also a content-based filtering which analyzes a song's own attributes (genre, tempo, mood) and try to recommend songs that are a close match to these traits, as well as to match the theme with a user's past preferences.

- I will be focused more on the content-based filtering since we have more to work with on our starter code for that data set at a smaller scale. It represents each Song by its genre, mood, energy, and acousticness, and represents the user as a UserProfile with a favorite genre, favorite mood, a target energy level

- The Recommender scores each song ( max of 4.5 points) by rewarding exact matches on genre and mood, and rewarding energy values that are close to the user's target rather than simply higher or lower, then ranks all songs by that score and returns the top matches. For this specific scoring system, genre matching has the most weight in the score at the moment, since in my mind, a Kpop listener would be more biased to listen to more kpop songs than wanting to listen to more Musical themed songs. This in turn might diminish the other attributes that factor in to the score such as mood match and energy since it has a little less weight and leeway when it comes to how it is scored. Genre outweighs mood 2:1 since it's the more stable identity signal, while energy is continuous rather than all-or-nothing so it can differentiate songs within the same genre/mood.

---

## Getting Started

### Setup

1. Create a virtual environment (optional but recommended):

   ```bash
   python -m venv .venv
   source .venv/bin/activate      # Mac or Linux
   .venv\Scripts\activate         # Windows

   ```

2. Install dependencies

```bash
pip install -r requirements.txt
```

3. Run the app:

```bash
python -m src.main
```

### Running Tests

Run the starter tests with:

```bash
pytest
```

You can add more tests in `tests/test_recommender.py`.

---

## Sample Recommendation Output

Paste a sample of your recommender's output here as a text block so a reader can see what it produces:

```
# e.g.:
# User profile: genre=indie, mood=chill, energy=low
# Recommendations:
#   1. ...
#   2. ...
#   3. ...
```

```
1. Sunrise City by Neon Echo
   Score: 4.00
   Reasons:
     - genre match: pop (+2.0)
     - mood match: happy (+1.0)
     - energy 0.82 close to target 0.80 (+1.00)

2. Gym Hero by Max Pulse
   Score: 2.98
   Reasons:
     - genre match: pop (+2.0)
     - energy 0.93 close to target 0.80 (+0.98)

3. Rooftop Lights by Indigo Parade
   Score: 2.00
   Reasons:
     - mood match: happy (+1.0)
     - energy 0.76 close to target 0.80 (+1.00)

4. Firework Heart by Astra Nine
   Score: 1.00
   Reasons:
     - energy 0.85 close to target 0.80 (+1.00)

5. Night Drive Loop by Neon Echo
   Score: 1.00
   Reasons:
     - energy 0.75 close to target 0.80 (+1.00)
```

**Screenshot or video** _(optional)_: <!-- Insert a screenshot or demo video link here -->

---

## Experiments You Tried

Use this section to document the experiments you ran. For example:

- What happened when you changed the weight on genre from 2.0 to 0.5
- What happened when you added tempo or valence to the score
- How did your system behave for different types of users

---

## Limitations and Risks

Summarize some limitations of your recommender.

Examples:

- It only works on a tiny catalog
- It does not understand lyrics or language
- It might over favor one genre or mood

You will go deeper on this in your model card.

---

## Reflection

Read and complete `model_card.md`:

[**Model Card**](model_card.md)

Write 1 to 2 paragraphs here about what you learned:

- about how recommenders turn data into predictions
- about where bias or unfairness could show up in systems like this
