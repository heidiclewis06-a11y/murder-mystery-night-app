import streamlit as st
import json
import os
import random
from datetime import datetime

st.set_page_config(page_title="Mystery Night AI", page_icon="🔍", layout="wide")

st.title("🔍 Mystery Night AI")
st.subheader("Host unforgettable murder mystery parties")

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
    
    col1, col2 = st.columns([3, 2])
    
    with col1:
        st.subheader(story["title"])
        st.write(story["description"])
        
        num_guests = st.number_input("Number of Guests", min_value=6, max_value=12, value=8)
        
        if st.button("🎲 Generate Game", type="primary", use_container_width=True):
            murderer_role = random.choice(story.get("possible_murderers", []))
            
            game_session = {
                "game_id": datetime.now().strftime("%Y%m%d_%H%M%S"),
                "story_id": story_id,
                "num_guests": num_guests,
                "murderer_role": murderer_role,
                "created_at": datetime.now().isoformat()
            }
            
            st.session_state.current_game = game_session
            st.success("✅ Game Created!")
            st.balloons()

    with col2:
        st.subheader("Game Info")
        st.write(f"**Duration:** ~{story['duration_minutes']} minutes")
        st.write(f"**Theme:** {story['theme']}")

# === HOST MODE BUTTON (Fixed) ===
if "current_game" in st.session_state:
    st.divider()
    st.success("Game is Ready!")
    
    if st.button("🎤 Open Host Control Panel", type="primary", use_container_width=True):
        st.session_state.host_mode = True
        st.rerun()

# Show Host Panel in the same app (simpler method)
if st.session_state.get("host_mode", False) and "current_game" in st.session_state:
    st.divider()
    st.title("🎤 Host Control Panel")
    game = st.session_state.current_game
    story = stories[game["story_id"]]
    
    # Progress
    if "current_act" not in st.session_state:
        st.session_state.current_act = 0
        
    acts = ["Introduction", "Act 1", "Act 2", "Act 3", "Accusations", "Reveal"]
    current = st.session_state.current_act
    
    st.subheader(f"Phase: {acts[current]}")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("← Previous Phase"):
            if current > 0:
                st.session_state.current_act -= 1
                st.rerun()
    with col2:
        if st.button("Next Phase →", type="primary"):
            if current < len(acts)-1:
                st.session_state.current_act += 1
                st.rerun()
    with col3:
        if st.button("Exit Host Mode"):
            st.session_state.host_mode = False
            st.rerun()

    # Show content based on phase (same as before)
    # ... (I can expand this part if needed)

st.caption("Mystery Night AI")
