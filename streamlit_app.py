import os
from typing import Any, Dict, List, Optional

import streamlit as st
from dotenv import load_dotenv

from kpop_agent import SAMPLE_PROFILES, get_recommendations
from llm_client import GeminiClient, MockClient

st.set_page_config(page_title="K-pop Recommender", page_icon="🎵", layout="wide")
st.title("🎵 K-pop Song Recommender")
st.caption("Pick a sample taste profile or describe your own — Gemini recommends 4 real K-pop songs.")

load_dotenv()

# ----------------------------
# Sidebar controls
# ----------------------------
st.sidebar.header("Settings")

mode = st.sidebar.selectbox(
    "Model mode",
    ["Offline (Mock)", "Gemini (requires API key)"],
    help="Offline mode runs fully without the network. Gemini mode calls the Gemini API for real recommendations.",
)

if mode == "Gemini (requires API key)":
    st.sidebar.warning("⚠️ Gemini Free Tier has request limits. Use Offline mode for UI testing to save quota.")

model_name = st.sidebar.selectbox(
    "Gemini model",
    ["gemini-flash-lite-latest", "gemini-2.5-flash", "gemini-2.5-pro"],
    disabled=(mode != "Gemini (requires API key)"),
)

temperature = st.sidebar.slider(
    "Temperature",
    min_value=0.0,
    max_value=1.0,
    value=0.4,
    step=0.1,
    disabled=(mode != "Gemini (requires API key)"),
    help="Lower values are more consistent. Higher values are more varied/creative.",
)

st.sidebar.divider()
show_debug = st.sidebar.checkbox("Show debug details", value=False)


def build_client(mode: str, model_name: str, temperature: float) -> Optional[Any]:
    if mode == "Offline (Mock)":
        return MockClient()
    api_key = os.getenv("GEMINI_API_KEY", "").strip()
    if not api_key:
        return None
    return GeminiClient(model_name=model_name, temperature=temperature)


client = build_client(mode, model_name, temperature)
if mode == "Offline (Mock)":
    client_status = "Using MockClient. No network calls."
elif client is None:
    client_status = "Missing GEMINI_API_KEY. Add it to your .env file to use Gemini mode."
else:
    client_status = "Gemini client ready."

st.sidebar.info(client_status)

# ----------------------------
# Main input
# ----------------------------
profile_choice = st.selectbox("Choose a sample profile", ["(custom)"] + list(SAMPLE_PROFILES.keys()))

if profile_choice == "(custom)":
    profile_text = st.text_area(
        "Describe what you want",
        placeholder="e.g. I want moody, cinematic K-pop with orchestral strings and a slow build.",
        height=100,
    )
else:
    st.caption(f"Sample profile prompt: _{SAMPLE_PROFILES[profile_choice]}_")
    profile_text = SAMPLE_PROFILES[profile_choice]

run_button = st.button("Get Recommendations", type="primary")


def render_song_cards(songs: List[Dict[str, Any]]) -> None:
    cols = st.columns(4)
    for col, song in zip(cols, songs):
        with col:
            st.markdown(f"🎵 **{song['title']}**")
            st.caption(song["artist"])
            st.metric("Match score", f"{song['match_score']}/10")
            st.write(song["reason"])


# ----------------------------
# Run workflow
# ----------------------------
if run_button:
    if not profile_text.strip():
        st.warning("Enter a profile description or choose a sample profile first.")
        st.stop()

    if mode == "Gemini (requires API key)" and client is None:
        st.error("Gemini mode is selected, but no API key is available.")
        st.stop()

    with st.spinner("Asking Gemini for K-pop recommendations..."):
        result = get_recommendations(profile_text, client, max_retries=1)

    if result["attempts"] > 1:
        st.info("First response didn't match the expected format — retried once with a stricter prompt.")

    if result["status"] == "ok":
        render_song_cards(result["songs"])
    else:
        st.error(f"Gemini couldn't produce a valid 4-song list after a retry: {result['error']}")

    if show_debug:
        st.divider()
        st.subheader("Debug payload")
        st.json(result)
