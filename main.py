import streamlit as st
import json
import os
import random
from datetime import datetime
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

# Initialize Gemini with stable model
gemini_key = os.getenv("GEMINI_API_KEY") or st.secrets.get("GEMINI_API_KEY")
if gemini_key:
    genai.configure(api_key=gemini_key)
    model = genai.GenerativeModel('gemini-pro')   # Stable model
else:
    model = None

st.set_page_config(page_title="Mystery Night AI", page_icon="🔍", layout="wide")

st.title("🔍 Mystery Night AI")
st.subheader("Live Gemini AI Host Murder Mystery")

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
selected_title = st.selectbox("Choose a Mystery Story", options=list(story_options.keys()), key="story_select")

if selected_title:
    story_id = story_options[selected_title]
    story = stories[story_id]
    
    num_guests = st.number_input("Number of Guests", min_value=6, max_value=12, value=8, key="guest_input")
    
    if st.button("🎲 Generate Game", type="primary", use_container_width=True, key="generate_btn"):
        murderer_role = random.choice(story.get("possible_murderers", []))
        st.session_state.current_game = {
            "game_id": datetime.now().strftime("%Y%m%d_%H%M%S"),
            "story_id": story_id,
            "num_guests": num_guests,
            "murderer_role": murderer_role
        }
        st.success("✅ Game Created!")

# ====================== LIVE GEMINI AI HOST ======================
if "current_game" in st.session_state:
    if st.button("🎤 Launch Live Gemini AI Host", type="primary", use_container_width=True, key="host_btn"):
        st.session_state.host_mode = True
        if "host_messages" not in st.session_state:
            st.session_state.host_messages = []
            initial = f"Welcome everyone! I am your Gemini AI Host for tonight's thrilling mystery: {stories[st.session_state.current_game['story_id']]['title']}. Let the investigation begin!"
            st.session_state.host_messages.append({"role": "host", "content": initial})

if st.session_state.get("host_mode", False):
    game = st.session_state.current_game
    story = stories[game["story_id"]]
    
    st.title(f"🎤 Live Gemini AI Host - {story['title']}")
    
    for msg in st.session_state.host_messages:
        if msg["role"] == "host":
            st.markdown(f"**🗣️ Gemini Host:** {msg['content']}")
        else:
            st.markdown(f"**Guest:** {msg['content']}")

    user_input = st.text_input("What should the Gemini Host say or answer?", 
                              placeholder="Welcome guests, reveal next clue, or answer a question...", 
                              key="user_input")

    if st.button("Send to Gemini Host", type="primary", key="send_btn"):
        if user_input:
            st.session_state.host_messages.append({"role": "player", "content": user_input})
            
            system_prompt = f"""
You are the dramatic Gemini AI Host for the murder mystery '{story['title']}'.
Stay completely in character. Speak theatrically and engagingly.

Core Knowledge (Never break these):
- Plot: {story['core_plot']}
- Victim: {story['victim']}
- Clues: {[c['clue_text'] for c in story['clues']]}
- Twist: {story['twist_ending']}

Rules:
- Never invent new clues or plot details.
- Never reveal the murderer until the final reveal.
- Be fun, witty, and immersive.
"""

            try:
                if model:
                    response = model.generate_content(system_prompt + "\n\nUser input: " + user_input)
                    reply = response.text
                else:
                    reply = "The spirits are a bit foggy tonight... Could you repeat that?"
            except Exception as e:
                reply = f"The spirits are a bit foggy tonight... (Error: {str(e)[:100]})"

            st.session_state.host_messages.append({"role": "host", "content": reply})
            st.rerun()

st.caption("Mystery Night AI - Powered by Google Gemini")