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

# Core Characters
core_characters = {
    "curse_of_the_crimson_cutlass": [
        {"name": "Captain Elias Blackthorn", "background": "A veteran stage actor who plays the pirate captain. He takes his role very seriously.", "motives": "He is obsessed with finding the real Crimson Cutlass treasure map.", "public_info": "Charismatic lead actor and host of the show."},
        {"name": "Lady Victoria Voss", "background": "An experienced actress playing the wealthy widow. Elegant but competitive.", "motives": "She is looking for the lost treasure map prop.", "public_info": "Elegant socialite actress."},
        {"name": "Dr. Julian Crowe", "background": "Character actor playing the ship's doctor. Quiet and intellectual.", "motives": "Blackmailing several cast members.", "public_info": "The ship's physician."},
        {"name": "Isabella 'Izzy' Torres", "background": "Young, fiery dancer and actress.", "motives": "She knows a dangerous secret about the murder.", "public_info": "Talented dancer."},
        {"name": "Mr. Reginald Hawthorne", "background": "Actor playing the wealthy merchant. Loud and arrogant.", "motives": "He owes large debts.", "public_info": "Boastful merchant."},
        {"name": "Miss Penelope Sharpe", "background": "Quiet actress playing the captain's assistant.", "motives": "Secretly in love with one of the guests.", "public_info": "Bookish assistant."}
    ],
    # Add other stories as needed
}

# Persistent extra characters (generated once per game)
if "extra_characters" not in st.session_state or st.session_state.get("current_game_id") != game["game_id"]:
    st.session_state.extra_characters = []
    first_names = ["Alex", "Jordan", "Taylor", "Casey", "Riley", "Sam", "Morgan", "Jamie"]
    last_names = ["Rivera", "Blake", "Morgan", "Quinn", "Brooks", "Parker", "Ellis", "Reid"]
    roles = ["Bartender", "Musician", "Waitstaff", "Stage Technician", "Guest Entertainer", "Ship Crew Member"]
    
    for i in range(max(0, num_guests - 6)):
        name = f"{random.choice(first_names)} {random.choice(last_names)}"
        role = random.choice(roles)
        st.session_state.extra_characters.append({
            "name": name,
            "background": f"An experienced supporting actor who has been with the production for several seasons playing a {role.lower()}. They know many behind-the-scenes secrets.",
            "motives": f"They have a complicated personal history with several members of the main cast and are hiding a significant secret of their own.",
            "public_info": f"Supporting cast member playing a {role}."
        })
    st.session_state.current_game_id = game["game_id"]

# Combine core + persistent extras
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
        st.subheader("Introduction Statement (Say this to the group)")
        st.info(f"Good evening. I am {selected_role['name']}. I never imagined our performance would turn into a real tragedy tonight.")

    if current_act > 0:
        st.subheader("Questions to Ask")
        act_names = ["Introduction", "Act 1", "Act 2", "Act 3", "Accusations", "Reveal"]
        st.write(f"**{act_names[current_act]} Questions:**")
        st.write("- Question 1 to ask other characters")
        st.write("- Question 2 to ask other characters")
        st.write("- Question 3 to ask other characters")

st.caption("Do not show this page to other players!")
