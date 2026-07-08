import streamlit as st
import json
import os
import random
from datetime import datetime

st.set_page_config(page_title="Mystery Night AI", page_icon="🔍", layout="wide")

st.title("🔍 Mystery Night AI")
st.subheader("AI-Powered Murder Mystery Host")

# Load stories (same as before)
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

# Story selection and game creation (same as before - abbreviated)
if stories:
    story_options = {story["title"]: story_id for story_id, story in stories.items()}
    selected_title = st.selectbox("Choose a Mystery Story", options=list(story_options.keys()))

    if selected_title:
        story_id = story_options[selected_title]
        story = stories[story_id]
        
        num_guests = st.number_input("Number of Guests", min_value=6, max_value=12, value=8)
        
        if st.button("🎲 Generate Game", type="primary"):
            murderer_role = random.choice(story.get("possible_murderers", []))
            st.session_state.current_game = {
                "game_id": datetime.now().strftime("%Y%m%d_%H%M%S"),
                "story_id": story_id,
                "num_guests": num_guests,
                "murderer_role": murderer_role
            }
            st.success("Game Created!")

# ==================== HOST MODE ====================
if "current_game" in st.session_state:
    if st.button("🎤 Launch AI Host Mode", type="primary", use_container_width=True):
        st.session_state.host_mode = True
        st.rerun()

if st.session_state.get("host_mode", False):
    game = st.session_state.current_game
    story = stories[game["story_id"]]
    
    st.title(f"🎤 AI Host - {story['title']}")
    st.caption("The AI Host will speak narration and answer questions")

    # Simple AI Host Chat
    if "host_messages" not in st.session_state:
        st.session_state.host_messages = []

    # Display previous messages
    for msg in st.session_state.host_messages:
        if msg["role"] == "host":
            st.markdown(f"**Host:** {msg['content']}")
        else:
            st.markdown(f"**Player:** {msg['content']}")

    # Player question input
    player_question = st.text_input("Type a player question (or what the Host should say next):")
    
    if st.button("Send to AI Host"):
        if player_question:
            st.session_state.host_messages.append({"role": "player", "content": player_question})
            
            # Call AI (using Grok/Claude/ChatGPT style prompt)
            prompt = f"""
You are an immersive AI Host for the murder mystery '{story['title']}'.
Stay completely in character. Speak naturally and dramatically.
Current story knowledge: {story['core_plot']}
Clues so far: {[clue['clue_text'] for clue in story['clues']]}
Twist: {story['twist_ending']}

Player asked: {player_question}

Respond in character as the host:
"""
            # For now, we'll simulate. Later we'll connect real LLM
            response = "Interesting question... Let me think about that."  # Placeholder
            
            st.session_state.host_messages.append({"role": "host", "content": response})
            st.rerun()

    st.info("In the final version, this will use voice + avatar (HeyGen, D-ID, or ElevenLabs + Streamlit).")
