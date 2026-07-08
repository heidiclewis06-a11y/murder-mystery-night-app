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

# === IMPROVED HOST MODE ===
if "current_game" in st.session_state:
    st.divider()
    st.success("Game is Ready!")
    
    if st.button("🎤 Open Host Control Panel", type="primary", use_container_width=True):
        st.session_state.host_mode = True
        st.rerun()

# Show Host Panel
if st.session_state.get("host_mode", False) and "current_game" in st.session_state:
    game = st.session_state.current_game
    story = stories[game["story_id"]]
    
    st.divider()
    st.title(f"🎤 Host Control - {story['title']}")
    
    # Progress
    if "current_act" not in st.session_state:
        st.session_state.current_act = 0
    
    acts = ["Introduction", "Act 1", "Act 2", "Act 3", "Accusations", "Reveal & Twist"]
    current = st.session_state.current_act
    
    st.progress(current / (len(acts) - 1))
    st.subheader(f"Phase {current + 1}/6: {acts[current]}")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("← Previous", use_container_width=True):
            if current > 0:
                st.session_state.current_act -= 1
                st.rerun()
    with col2:
        if st.button("Next Phase →", type="primary", use_container_width=True):
            if current < len(acts)-1:
                st.session_state.current_act += 1
                st.rerun()
    with col3:
        if st.button("Exit Host Mode"):
            st.session_state.host_mode = False
            st.rerun()

    st.divider()

    # PHASE CONTENT
    if current == 0:        # Introduction
        st.subheader("Opening Narration")
        st.write(story["description"])
        st.write(story["core_plot"])
        st.info("**Host says:** Welcome everyone! Stay in character, enjoy dinner, and begin questioning after each clue.")

    elif current == 1:      # Act 1
        st.subheader("Act 1 - First Clue")
        clue = story["clues"][0]
        st.write(f"**Clue:** {clue['clue_text']}")
        st.caption(clue.get("importance", ""))
        st.info("**Host says:** You now have 10-12 minutes to question each other. Go!")

    elif current == 2:      # Act 2
        st.subheader("Act 2 - Second Clue")
        clue = story["clues"][1]
        st.write(f"**Clue:** {clue['clue_text']}")
        st.caption(clue.get("importance", ""))

    elif current == 3:      # Act 3
        st.subheader("Act 3 - Final Clue")
        clue = story["clues"][2]
        st.write(f"**Clue:** {clue['clue_text']}")
        st.caption(clue.get("importance", ""))

    elif current == 4:      # Accusations
        st.subheader("Accusation Phase")
        st.write(story["accusation_phase"])
        st.info("Go around the table. Have each player state their character and accusation.")

    elif current == 5:      # Reveal
        st.subheader("🎭 THE REVEAL")
        murderer_role = game["murderer_role"]
        murderer_name = next((r["default_name"] for r in story["roles"] if r["role_id"] == murderer_role), murderer_role.title())
        
        st.error(f"**THE MURDERER WAS: {murderer_name}**")
        st.write(story["reveal_phase"])
        
        if st.button("Show Final Twist"):
            st.success("**Final Twist:** " + story["twist_ending"])

    st.caption("Use the buttons above to move between phases")
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
