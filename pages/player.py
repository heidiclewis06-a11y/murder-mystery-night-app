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
        {"name": "Captain Elias Blackthorn", "background": "A veteran stage actor who has played the pirate captain for years. He takes his role extremely seriously and has become somewhat consumed by the character.", "motives": "He is obsessed with finding the real Crimson Cutlass treasure map that he believes is hidden somewhere on the ship.", "public_info": "Charismatic lead actor and host of the show."},
        {"name": "Lady Victoria Voss", "background": "An experienced actress known for playing wealthy widows. She has a refined presence but a sharp, competitive edge when it comes to getting the best roles.", "motives": "She is convinced the lost treasure map belongs to her character's family and will do anything to claim it.", "public_info": "Elegant and flirtatious actress always in stunning gowns."},
        {"name": "Dr. Julian Crowe", "background": "A quiet, intellectual character actor who has specialized in mysterious doctor roles for over a decade.", "motives": "He has been blackmailing several cast members with secrets he uncovered during late-night rehearsals.", "public_info": "The ship's doctor in the show, known for his calm and slightly unsettling demeanor."},
        {"name": "Isabella 'Izzy' Torres", "background": "A passionate young dancer and actress who brings high energy to every performance.", "motives": "She accidentally discovered a dangerous secret about the murder and is torn about what to do with it.", "public_info": "Fiery and charismatic dancer."},
        {"name": "Mr. Reginald Hawthorne", "background": "A loud, boastful character actor who loves playing wealthy, arrogant roles.", "motives": "He is deeply in debt and was arguing with the victim about money before the murder.", "public_info": "Wealthy merchant known for his booming voice and over-the-top personality."},
        {"name": "Miss Penelope Sharpe", "background": "A quiet, observant actress who often plays supporting roles. She notices details others miss.", "motives": "She is secretly in love with one of the other actors and will protect them at all costs.", "public_info": "The captain's loyal assistant, known for her intelligence."}
    ],
    "death_on_the_azure_empress": [
        {"name": "Captain Marcus Hale", "background": "A seasoned actor who has played ship captains for years. He brings natural authority to the role.", "motives": "He is hiding illegal cargo on the ship to make extra money.", "public_info": "Authoritative and charming captain of the cruise ship."},
        # ... (add more if needed)
    ]
}

# Generate realistic additional characters
def generate_extra_character(index):
    first_names = ["Alex", "Jordan", "Taylor", "Casey", "Riley", "Sam", "Morgan", "Jamie"]
    last_names = ["Rivera", "Blake", "Morgan", "Quinn", "Brooks", "Parker", "Ellis", "Reid"]
    roles = ["Bartender", "Musician", "Waitstaff", "Stage Technician", "Guest Entertainer", "Ship Crew Member", "Local Artist", "Journalist"]
    
    name = f"{random.choice(first_names)} {random.choice(last_names)}"
    role = random.choice(roles)
    
    return {
        "name": name,
        "background": f"An experienced supporting actor who plays a {role.lower()} in the show. They have been part of the production for several seasons and know many behind-the-scenes secrets.",
        "motives": f"They have a complicated history with several members of the main cast and are hiding a significant personal secret.",
        "public_info": f"Supporting cast member playing a {role}."
    }

# Combine core + extra characters
roles = core_characters.get(story_id, [])
extra_count = max(0, num_guests - len(roles))
for i in range(extra_count):
    roles.append(generate_extra_character(i))

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
