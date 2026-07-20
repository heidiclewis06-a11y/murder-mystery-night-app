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
num_guests = game.get("num_guests", 6)

# Load story
story_folder = "stories"
story_path = f"{story_folder}/{story_id}.json"
if os.path.exists(story_path):
    with open(story_path, "r", encoding="utf-8") as f:
        story = json.load(f)
else:
    st.error("Story not found.")
    st.stop()

st.write(f"**Story:** {story.get('title', 'Unknown')} | **Guests:** {num_guests}")

# Evidence per Act
evidence_per_act = {
    "curse_of_the_crimson_cutlass": {
        1: ["lipstick-stained glass", "broken pocket watch", "torn piece of map"],
        2: ["monogrammed handkerchief", "gunpowder residue on glove", "empty whiskey bottle"],
        3: ["blood-stained cutlass", "hidden note with initials", "missing treasure map piece"]
    },
    # Add other stories as needed
}

# Core Characters (example for pirate story - expand as needed)
core_characters = {
    "curse_of_the_crimson_cutlass": [
        {"name": "Captain Elias Blackthorn", "background": "...", "motives": "...", "public_info": "..."},
        # ... other characters
    ]
}

# Persistent extra characters
if "extra_characters" not in st.session_state or st.session_state.get("current_game_id") != game["game_id"]:
    # ... (generate extras as before)
    st.session_state.current_game_id = game["game_id"]

roles = core_characters.get(story_id, []) + st.session_state.extra_characters

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
    
    current_act = st.session_state.get("current_act", 0)
    if current_act == 0:
        st.subheader("Introduction Statement")
        st.info(selected_role.get("introduction", f"Good evening. I am {selected_role['name']}."))
    
    if current_act > 0:
        st.subheader("Questions to Ask")
        act_name = ["Introduction", "Act 1", "Act 2", "Act 3", "Accusations", "Reveal"][current_act]
        evidence_list = evidence_per_act.get(story_id, {}).get(current_act, ["unknown evidence"])
        evidence = random.choice(evidence_list)
        other_characters = [r["name"] for r in roles if r["name"] != selected_role["name"]]
        
        st.write(f"**{act_name} - Questions about the revealed evidence ({evidence})**")
        for i in range(3):
            target = random.choice(other_characters)
            st.write(f"{i+1}. {target}, how do you explain your connection to the {evidence} that was found?")
        
        st.divider()
        
        st.subheader("What to Say If Questioned")
        st.write("**If Innocent:**")
        st.info("I had nothing to do with this. I was in my dressing room the whole time.")
        st.write("**If Guilty:**")
        st.info("I had nothing to do with this... I was in my dressing room the whole time.")

st.caption("Do not show this page to other players!")
