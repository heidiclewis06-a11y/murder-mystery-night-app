import streamlit as st
import json
import os
import random
from datetime import datetime
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()
client = OpenAI()

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
    st.error("No stories found!")
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
        st.success("✅ Game Created! Launch the AI Host below.")

# ====================== AI HOST MODE ======================
if "current_game" in st.session_state:
    if st.button("🎤 Launch Live AI Host", type="primary", use_container_width=True):
        st.session_state.host_mode = True
        if "host_messages" not in st.session_state:
            st.session_state.host_messages = []
            # Initial greeting
            initial_greeting = f"Welcome everyone to {stories[st.session_state.current_game['story_id']]['title']}! I am your host for tonight's mystery..."
            st.session_state.host_messages.append({"role": "host", "content": initial_greeting})

if st.session_state.get("host_mode", False):
    game = st.session_state.current_game
    story = stories[game["story_id"]]
    
    st.title(f"🎤 Live AI Host - {story['title']}")
    
    # Display conversation
    for msg in st.session_state.host_messages:
        if msg["role"] == "host":
            st.markdown(f"**🗣️ AI Host:** {msg['content']}")
        else:
            st.markdown(f"**Guest:** {msg['content']}")

    # Controls
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Next Phase", type="primary"):
            if "current_act" not in st.session_state:
                st.session_state.current_act = 0
            st.session_state.current_act = min(st.session_state.current_act + 1, 5)
            st.rerun()
    with col2:
        if st.button("Reset Host"):
            st.session_state.host_messages = []
            st.rerun()

    # User input for host
    user_input = st.text_input("What should the AI Host say or answer?", 
                              placeholder="Welcome the guests, reveal next clue, or answer a player's question...")

    if st.button("Send to AI Host", type="primary"):
        if user_input:
            st.session_state.host_messages.append({"role": "player", "content": user_input})
            
            # Strong system prompt for consistency
            system_prompt = f"""
You are the official dramatic AI Host for '{story['title']}'.
Stay completely in character. Speak with personality and flair.

Core Knowledge You Must Never Contradict:
- Plot: {story['core_plot']}
- Victim: {story['victim']}
- Clues: {[c['clue_text'] for c in story['clues']]}
- Twist: {story['twist_ending']}
- You know who the murderer is but never reveal it until the final reveal.

Rules:
- Never invent new clues, motives, or plot details.
- If you don't know something, respond mysteriously in character.
- Be engaging and theatrical.
"""

            try:
                response = client.chat.completions.create(
                    model="gpt-4o-mini",
                    messages=[
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": f"Current phase: {st.session_state.get('current_act', 0)}. User says: {user_input}"}
                    ],
                    temperature=0.7,
                    max_tokens=400
                )
                ai_reply = response.choices[0].message.content.strip()
            except Exception as e:
                ai_reply = "My apologies, dear guests... There seems to be a small disturbance in the spirits tonight."

            st.session_state.host_messages.append({"role": "host", "content": ai_reply})
            st.rerun()
