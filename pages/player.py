import streamlit as st
import json
import os

st.set_page_config(page_title="Player View", page_icon="📜")

st.title("📜 Character Packet")
st.subheader("Private Information - Do Not Share!")

# Load current game
if "current_game" not in st.session_state:
    st.error("No game in progress. Please generate a game from the main page first.")
    st.stop()

game = st.session_state.current_game
story_id = game["story_id"]

# Load story
story_folder = "stories"
story_path = f"{story_folder}/{story_id}.json"
if os.path.exists(story_path):
    with open(story_path, "r", encoding="utf-8") as f:
        story = json.load(f)
else:
    st.error("Story not found.")
    st.stop()

# Placeholder for character selection (expand later with full packets)
st.write(f"**Story:** {story['title']}")
st.write(f"**Your Role:** [Character Name]")

st.divider()

st.subheader("Background")
st.write("[Full background story here - innocent or guilty version]")

st.subheader("Motives & Secrets")
st.write("[Private motives and secrets]")

st.divider()

st.subheader("Questions to Ask Other Players")

act_names = ["Introduction", "Act 1", "Act 2", "Act 3", "Accusations", "Reveal"]
current_act = st.session_state.get("current_act", 0)
act_name = act_names[current_act]

st.write(f"**{act_name} - Questions to Ask:**")
st.write("1. [Question 1]")
st.write("2. [Question 2]")
st.write("3. [Question 3]")

st.divider()

st.subheader("Public Information (Safe to Share)")
st.write("[Information other players can know]")

st.caption("Remember: Do not show this page to other players!")
