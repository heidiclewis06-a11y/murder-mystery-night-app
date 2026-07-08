import streamlit as st
import json
import os
import random
from datetime import datetime

# Page Configuration
st.set_page_config(
    page_title="Mystery Night AI",
    page_icon="🔍",
    layout="wide"
)

st.title("🔍 Mystery Night AI")
st.subheader("Create unforgettable murder mystery dinner parties with AI")

# Sidebar
st.sidebar.header("How to Play")
st.sidebar.info("""
1. Choose a story  
2. Enter number of guests  
3. Generate the game  
4. Use Host Mode on one device  
5. Players open the link on their phones
""")

# Load stories
@st.cache_data
def load_all_stories():
    stories = {}
    story_folder = "stories"
    if os.path.exists(story_folder):
        for filename in os.listdir(story_folder):
            if filename.endswith(".json"):
                filepath = os.path.join(story_folder, filename)
                try:
                    with open(filepath, "r", encoding="utf-8") as f:
                        data = json.load(f)
                        stories[data["story_id"]] = data
                except Exception as e:
                    st.warning(f"Error loading {filename}: {e}")
    return stories

stories = load_all_stories()

if not stories:
    st.error("No stories found! Please create a 'stories' folder and add your JSON files.")
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
        
        num_guests = st.number_input(
            "Number of Guests", 
            min_value=story["generation_rules"]["min_players"],
            max_value=story["generation_rules"]["max_players"],
            value=8
        )
        
        if st.button("🎲 Generate Game", type="primary", use_container_width=True):
            # Randomly select murderer
            murderer_role = random.choice(story["possible_murderers"])
            
            game_session = {
                "game_id": datetime.now().strftime("%Y%m%d_%H%M%S"),
                "story_id": story_id,
                "num_guests": num_guests,
                "murderer_role": murderer_role,
                "created_at": datetime.now().isoformat()
            }
            
            st.session_state.current_game = game_session
            st.success(f"✅ Game Created! The murderer has been secretly chosen.")
            st.balloons()
            
            st.subheader("Game Ready!")
            st.write(f"**Story:** {story['title']}")
            st.write(f"**Players:** {num_guests}")
            st.info("Share this link with your guests. One person should use **Host Mode**.")

    with col2:
        st.subheader("Game Info")
        st.write(f"**Duration:** ~{story['duration_minutes']} minutes")
        st.write(f"**Theme:** {story['theme']}")
        st.write(f"**Core Roles:** {len(story['roles'])}")
        st.write(f"**Max Players:** {story['generation_rules']['max_players']}")

# Show current game if exists
if "current_game" in st.session_state:
    game = st.session_state.current_game
    st.divider()
    st.success("Current Game Active")
    
    col_a, col_b = st.columns(2)
    with col_a:
        if st.button("🕹️ Open Host Mode", use_container_width=True):
            st.switch_page("pages/host.py")  # We'll create this later
    with col_b:
        if st.button("📱 Player View Demo", use_container_width=True):
            st.info("In the final version, each player will open the app and see only their character.")

# Footer
st.caption("Mystery Night AI — Built as a summer learning project")
