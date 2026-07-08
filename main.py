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
    st.error("No stories found in the 'stories' folder!")
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

# ====================== LIVE AI HOST ======================
if "current_game" in st.session_state:
    if st.button("🎤 Launch Live AI Host", type="primary", use_container_width=True):
        st.session_state.host_mode = True
        if "host_messages" not in st.session_state:
            st.session_state.host_messages = []
            initial = f"Welcome, everyone! I am your AI Host for tonight's thrilling mystery: {stories[st.session_state.current_game['story_id']]['title']}. Let the investigation begin!"
            st.session_state.host_messages.append({"role": "host", "content": initial})

if st.session_state.get("host_mode", False):
    game = st.session_state.current_game
    story = stories[game["story_id"]]
    
    st.title(f"🎤 Live AI Host - {story['title']}")
    
    for msg in st.session_state.host_messages:
        if msg["role"] == "host":
            st.markdown(f"**🗣️ AI Host:** {msg['content']}")
        else:
            st.markdown(f"**Guest:** {msg['content']}")

    user_input = st.text_input("Type what the Host should say or answer:", 
                              placeholder="Welcome the guests, reveal next clue, or answer a question...")

    if st.button("Send to AI Host", type="primary"):
        if user_input:
            st.session_state.host_messages.append({"role": "player", "content": user_input})
            
            system_prompt = f"""
You are the official dramatic AI Host for the murder mystery '{story['title']}'.
Stay completely in character. Speak theatrically.

Core Knowledge (Never contradict):
- Plot: {story['core_plot']}
- Victim: {story['victim']}
- Clues so far: {[c['clue_text'] for c in story['clues']]}
- Twist Ending: {story['twist_ending']}

Rules:
- Never invent new clues or plot details.
- Never reveal who the murderer is until the final reveal phase.
- Be engaging and fun.
"""

            try:
                response = client.chat.completions.create(
                    model="gpt-4o-mini",
                    messages=[
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": user_input}
                    ],
                    temperature=0.7,
                    max_tokens=400
                )
                reply = response.choices[0].message.content.strip()
            except Exception as e:
                reply = "The spirits are a bit foggy tonight... Could you repeat that, my dear guest?"

            st.session_state.host_messages.append({"role": "host", "content": reply})
            st.rerun()
