import streamlit as st
import json
import os
import random

st.set_page_config(page_title="Player View", page_icon="📜")

st.title("📜 Character Packet")
st.subheader("Private Information - Do Not Share!")

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

st.write(f"**Story:** {story.get('title', 'Unknown')}")

# Core 6 Characters (per story)
core_characters = {
    "curse_of_the_crimson_cutlass": [
        {"name": "Captain Blackthorn", "background": "Retired pirate captain turned dinner show performer.", "motives": "Secretly searching for the lost treasure.", "public_info": "Charming but ruthless leader."},
        {"name": "Lady Victoria Voss", "background": "Wealthy widow attending the show.", "motives": "Looking for her husband's lost map.", "public_info": "Elegant and mysterious."},
        # Add more as needed...
    ],
    # Add other stories here
}

# Use core characters or fallback
roles = core_characters.get(story_id, [])
if not roles:
    st.warning("Core characters not defined for this story yet.")
    st.stop()

role_names = [role["name"] for role in roles]
selected_role_name = st.selectbox("Select Your Character", options=role_names, key="selected_role")

selected_role = next((role for role in roles if role["name"] == selected_role_name), None)

if selected_role:
    st.divider()
    st.subheader(f"Your Character: {selected_role['name']}")
    
    st.subheader("Background")
    st.write(selected_role.get("background", "Background coming soon."))
    
    st.subheader("Motives & Secrets")
    st.write(selected_role.get("motives", "Private motives coming soon."))
    
    st.subheader("Public Information")
    st.write(selected_role.get("public_info", "No public information available."))
    
    st.divider()
    
    st.subheader("Questions to Ask")
    current_act = st.session_state.get("current_act", 0)
    act_names = ["Introduction", "Act 1", "Act 2", "Act 3", "Accusations", "Reveal"]
    st.write(f"**{act_names[current_act]} Questions:**")
    st.write("- Question 1")
    st.write("- Question 2")
    st.write("- Question 3")

st.caption("Do not show this page to other players!")
