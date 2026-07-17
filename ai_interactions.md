# AI Interactions Log

> **Stretch features only.** Only fill in the sections that apply to stretch features you attempted. If you did not attempt a stretch feature, leave its section blank or delete it. This file is not required for the core project.

---

## Agentic Workflow (SF8)

> Document your experience using an AI agent (e.g., Cursor Agent, Claude, Copilot) to make multi-step changes autonomously.

**What task did you give the agent?**

<!-- Describe the goal you asked the agent to accomplish -->

One of the prompts was to generate another new dataset of songs to add on to songs.csv. I specifically wanted some kpop songs and anime songs!

**Prompts used:**

<!-- Paste the key prompts you gave the agent -->

I have a CSV file of songs with the header: id,title,artist,genre,mood,energy,tempo_bpm,valence,danceability,acousticness. The existing genres are pop, lofi, rock, ambient, jazz, synthwave, and indie pop, and existing moods are happy, chill, intense, relaxed, moody, and focused.

Generate 5-10 additional songs in valid CSV format, using the same header and column order. Requirements:

Include at least 2 K-pop songs and 2 anime/anime-soundtrack style songs (genres like "k-pop" and "anime" or "j-pop")
Cover moods not already in the dataset (e.g., nostalgic, triumphant, romantic, melancholic, energetic)
Continue the id numbering from 11 onward
Keep all numeric fields (energy, valence, danceability, acousticness) as decimals between 0.0 and 1.0
Keep tempo_bpm as a realistic integer (roughly 60-180)
Make sure the numeric values are internally consistent with the mood/genre (e.g., a "triumphant" anime opening should have high energy and tempo, not low)
Output only the raw CSV rows (no header repeated, no explanation) so they can be appended directly to the existing file

I need to Define a specific "taste profile" that your recommender will use for its comparisons. This profile should be a dictionary containing target values for the features you identified. My favorite genre will be kpop, my favorite mood will be like energetic and danceable.. will these specific preferences will allow the system to differentiate between "intense rock" and "chill lofi," or if the profile is too narrow.

**What did the agent generate or change?**

<!-- List the files edited, code generated, or commands run -->

Edits on songs.csv
11,Neon Dream,Astra Nine,k-pop,energetic,0.88,126,0.82,0.90,0.08
12,Firework Heart,Astra Nine,k-pop,triumphant,0.85,132,0.75,0.86,0.10
13,Cherry Blossom Vow,Yui Kanzaki,anime,romantic,0.55,96,0.70,0.60,0.45
14,Rising Sun Oath,Kensho Battalion,anime,triumphant,0.90,150,0.68,0.72,0.15
15,Faded Photographs,Wistful Radio,indie folk,nostalgic,0.30,68,0.35,0.40,0.80
16,Velvet Confession,Moonlace,r&b,romantic,0.45,84,0.66,0.55,0.55
17,Empty Platform,Grey Static,shoegaze,melancholic,0.38,74,0.28,0.42,0.60
18,Overdrive Anthem,Astra Nine,k-pop,energetic,0.95,140,0.80,0.92,0.05

The taste profile dictionary

taste_profile = {
"favorite_genre": "k-pop",
"favorite_mood": "energetic",
"target_energy": 0.85,
"target_danceability": 0.85,
"likes_acoustic": False,
}
Note: target_danceability isn't currently a field in UserProfile in recommender.py — you'd need to add it since "danceable" is part of your stated preference and isn't covered by the existing four fields.

Testing it against "intense rock" vs "chill lofi"
Using Storm Runner (rock/intense: genre=rock, mood=intense, energy=0.91, danceability=0.66) and Midnight Coding (lofi/chill: genre=lofi, mood=chill, energy=0.42, danceability=0.62):

Feature Storm Runner Midnight Coding
genre match 0 (rock ≠ k-pop) 0 (lofi ≠ k-pop)
mood match 0 (intense ≠ energetic) 0 (chill ≠ energetic)
energy score (1-d², target 0.85) 1 - 0.06² ≈ 0.996 1 - 0.43² ≈ 0.815
danceability score (target 0.85) 1 - 0.19² ≈ 0.964 1 - 0.23² ≈ 0.947
Yes, it differentiates them — Storm Runner comes out ahead overall because its energy and danceability are much closer to your target. The numeric features are doing the real work here.

But here's the narrowness problem
Notice that genre and mood both score 0 for both songs. Your profile can only ever produce a positive genre/mood score for actual k-pop, actually-labeled-"energetic" tracks. Every other genre (rock, jazz, lofi, ambient) and every other mood (intense, chill, relaxed, moody) collapses to the exact same "0" — meaning genre and mood contribute zero differentiating power among all your non-k-pop songs. Rock and lofi only get separated because of the numeric features, not because your profile understands that rock is "louder/different" than lofi.

This exposes two real limitations:

Mood is exact-string-match only. "Energetic" and "intense" are conceptually close (both high-arousal), but your system treats them as totally unrelated (0 credit) the same way it treats "energetic" vs. "chill" (also 0 credit). A more nuanced system would give partial credit for semantically similar moods.
A single-genre preference only helps when actual k-pop/anime tracks appear. For everything else, genre is a wash. If your whole catalog were non-k-pop (as it mostly is right now), genre would never differentiate anything.
Bottom line: your profile isn't too narrow to differentiate rock from lofi — the energy/danceability numbers alone are doing that correctly. But it is narrow in the sense that genre and mood only "activate" for one specific value each, so most of your discriminating power currently rests on just two numeric features rather than four balanced ones.

**What did you verify or fix manually?**

<!-- Describe anything the agent got wrong or that required human review -->

I just made sure that the format of the new data matches the current format of the csv, and that the dataset wasn't too close to what already existed.

---

## Design Pattern (SF10)

> Document how AI helped you choose or implement a design pattern.

**Which design pattern did you use?**

<!-- e.g., Strategy, Factory, Observer, etc. -->

**How did AI help you brainstorm or implement it?**

<!-- Describe the conversation or suggestions that led to your decision -->

**How does the pattern appear in your final code?**

<!-- Point to the relevant class or method -->
