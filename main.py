import streamlit as st
import json
import os
import random
from datetime import datetime

st.set_page_config(page_title="Mystery Night AI", page_icon="🔍", layout="wide")

st.title("🔍 Mystery Night AI")
st.subheader("Live AI Host Murder Mystery")

# Load stories
@st.cache_data
def load_all_stories():
    stories = {}
    story_folder = "stories"
    if os.path.exists(story_folder):
        for filename in os.listdir(story_folder):
            if filename.endswith(".json"):
                try:
                    with open(f"{story_folder}/{filename}", "r", encoding="utf-8") as f:
                        data = json.load(f)
                        stories[data["story_id"]] = data
                except:
                    pass
    return stories

stories = load_all_stories()

if not stories:
    st.error("No stories found! Make sure the 'stories' folder exists with JSON files.")
    st.stop()

# Story Selection
story_options = {story["title"]: story_id for story_id, story in stories.items()}
selected_title = st.selectbox("Choose a Mystery Story", options=list(story_options.keys()))

if selected_title:
    story_id = story_options[selected_title]
    story = stories[story_id]
    
    num_guests = st.number_input("Number of Guests", min_value=6, max_value=12, value=8)
    
    if st.button("🎲 Generate Game", type="primary", use_container_width=True):
        murderer_role = random.choice(story.get("possible_murderers", []))
        st.session_state.current_game = {
            "game_id": datetime.now().strftime("%Y%m%d_%H%M%S"),
            "story_id": story_id,
            "num_guests": num_guests,
            "murderer_role": murderer_role
        }
        st.success("✅ Game Created!")

# ====================== AI HOST MODE (Simplified) ======================
if "current_game" in st.session_state:
    if st.button("🎤 Launch AI Host Mode", type="primary", use_container_width=True):
        st.session_state.host_mode = True
        if "host_messages" not in st.session_state:
            st.session_state.host_messages = []
            initial = f"Welcome everyone to {stories[st.session_state.current_game['story_id']]['title']}! I am your AI Host for this evening."
            st.session_state.host_messages.append({"role": "host", "content": initial})

if st.session_state.get("host_mode", False):
    game = st.session_state.current_game
    story = stories[game["story_id"]]
    
    st.title(f"🎤 AI Host - {story['title']}")
    
    for msg in st.session_state.host_messages:
        if msg["role"] == "host":
            st.markdown(f"**🗣️ Host:** {msg['content']}")
        else:
            st.markdown(f"**Guest:** {msg['content']}")

    user_input = st.text_input("What should the Host say or answer?")
    
    if st.button("Send", type="primary"):
        if user_input:
            st.session_state.host_messages.append({"role": "player", "content": user_input})
            st.session_state.host_messages.append({"role": "host", "content": "That's an excellent question... Let me think about that."})
            st.rerun()

    st.info("Full AI responses will be added once OpenAI is working.")
