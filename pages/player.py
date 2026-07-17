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

# Core 6 Characters
core_characters = {
    "curse_of_the_crimson_cutlass": [
        {"name": "Captain Elias Blackthorn", "background": "Veteran stage actor playing the pirate captain. Commanding presence.", "motives": "Searching for the treasure map prop.", "public_info": "Lead actor and host of the show."},
        {"name": "Lady Victoria Voss", "background": "Experienced actress playing the wealthy widow.", "motives": "Looking for the lost map.", "public_info": "Elegant socialite."},
        {"name": "Dr. Julian Crowe", "background": "Character actor playing the ship's doctor.", "motives": "Blackmailing cast members.", "public_info": "Calm physician."},
        {"name": "Isabella 'Izzy' Torres", "background": "Young dancer and actress.", "motives": "Knows a dangerous secret.", "public_info": "Fiery performer."},
        {"name": "Mr. Reginald Hawthorne", "background": "Actor playing the wealthy merchant.", "motives": "Owes large debts.", "public_info": "Loud and arrogant."},
        {"name": "Miss Penelope Sharpe", "background": "Quiet actress playing the captain's assistant.", "motives": "Secretly in love with a guest.", "public_info": "Bookish and observant."}
    ],
    "death_on_the_azure_empress": [
        {"name": "Captain Marcus Hale", "background": "Actor playing the ship captain.", "motives": "Hiding illegal cargo.", "public_info": "Authoritative leader."},
        {"name": "Sophia Laurent", "background": "Actress playing the famous star.", "motives": "Running from a scandal.", "public_info": "Glamorous performer."},
        {"name": "Dr. Elena Vargas", "background": "Actress playing the chief medical officer.", "motives": "Involved in experimental drugs.", "public_info": "Professional doctor."},
        {"name": "Victor Kane", "background": "Actor playing the billionaire.", "motives": "Corporate espionage.", "public_info": "Arrogant businessman."},
        {"name": "Mia Chen", "background": "Young actress playing the influencer.", "motives": "Blackmailing guests.", "public_info": "Outgoing social media star."},
        {"name": "Thomas Blackwell", "background": "Actor playing the retired detective.", "motives": "Investigating a cold case.", "public_info": "Observant and quiet."}
    ]
    # Add other stories as needed
}

roles = core_characters.get(story_id, [])
if not roles:
    st.error("Core characters not defined for this story yet.")
    st.stop()

# Generate additional characters if needed
extra_characters = []
if num_guests > len(roles):
    extra_names = ["Alex Rivera", "Jordan Blake", "Taylor Morgan", "Casey Quinn", "Riley Brooks", "Sam Parker"]
    extra_roles = ["Waiter", "Bartender", "Stagehand", "Musician", "Guest", "Crew Member"]
    for i in range(num_guests - len(roles)):
        extra_characters.append({
            "name": extra_names[i % len(extra_names)],
            "background": f"Supporting actor playing a {extra_roles[i % len(extra_roles)]} in the show.",
            "motives": "Has their own secrets and connections to the main cast.",
            "public_info": "Supporting cast member."
        })

all_roles = roles + extra_characters

role_names = [role["name"] for role in all_roles]
selected_role_name = st.selectbox("Select Your Character", options=role_names, key="selected_role")

selected_role = next((role for role in all_roles if role["name"] == selected_role_name), None)

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
    
    # Introduction Statement (only for Introduction phase)
    current_act = st.session_state.get("current_act", 0)
    if current_act == 0:
        st.subheader("Introduction Statement (Say this to the group)")
        st.info(f"Good evening. I am {selected_role['name']}. I never imagined our performance would turn into a real tragedy tonight.")

    # Questions (hidden during Introduction)
    if current_act > 0:
        st.subheader("Questions to Ask")
        act_names = ["Introduction", "Act 1", "Act 2", "Act 3", "Accusations", "Reveal"]
        st.write(f"**{act_names[current_act]} Questions:**")
        st.write("- Question 1 to ask other characters")
        st.write("- Question 2 to ask other characters")
        st.write("- Question 3 to ask other characters")

st.caption("Do not show this page to other players!")
