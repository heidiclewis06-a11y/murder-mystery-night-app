import streamlit as st
import json
import os

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

# Full Core 6 Characters for All Stories
core_characters = {
    "curse_of_the_crimson_cutlass": [
        {"name": "Captain Elias Blackthorn", "background": "Retired pirate captain who now runs the dinner show. Charismatic but haunted by his past.", "motives": "Secretly searching for the lost Crimson Cutlass treasure.", "public_info": "Famous for his dramatic storytelling and commanding presence."},
        {"name": "Lady Victoria Voss", "background": "Wealthy widow attending the show.", "motives": "Looking for her husband's lost treasure map.", "public_info": "Elegant and flirtatious socialite."},
        {"name": "Dr. Julian Crowe", "background": "Ship's doctor turned performer.", "motives": "Blackmailing several guests on board.", "public_info": "Quiet, observant, and slightly unsettling."},
        {"name": "Isabella 'Izzy' Torres", "background": "Young dancer in the dinner show.", "motives": "Knows a dangerous secret about the murder.", "public_info": "Fiery, outspoken, and full of energy."},
        {"name": "Mr. Reginald Hawthorne", "background": "Rich merchant with shady business dealings.", "motives": "Owes large debts to multiple people.", "public_info": "Arrogant, loud, and boastful."},
        {"name": "Miss Penelope Sharpe", "background": "Mysterious assistant to the captain.", "motives": "Secretly in love with one of the guests.", "public_info": "Shy, bookish, and always watching."}
    ],
    "death_on_the_azure_empress": [
        {"name": "Captain Marcus Hale", "background": "Experienced captain of the luxury cruise ship.", "motives": "Hiding illegal cargo on board.", "public_info": "Charming and authoritative leader."},
        {"name": "Sophia Laurent", "background": "Famous actress on vacation.", "motives": "Running from a scandal.", "public_info": "Glamorous and dramatic."},
        {"name": "Dr. Elena Vargas", "background": "Ship's chief medical officer.", "motives": "Involved in experimental drugs.", "public_info": "Professional and calm."},
        {"name": "Victor Kane", "background": "Billionaire businessman.", "motives": "Involved in corporate espionage.", "public_info": "Arrogant and powerful."},
        {"name": "Mia Chen", "background": "Young social media influencer.", "motives": "Blackmailing guests for content.", "public_info": "Outgoing and always filming."},
        {"name": "Thomas Blackwell", "background": "Retired detective on the cruise.", "motives": "Investigating a cold case.", "public_info": "Observant and quiet."}
    ],
    "shadows_in_the_gallery": [
        {"name": "Dr. Alexander Voss", "background": "Curator of the art museum.", "motives": "Selling forged paintings.", "public_info": "Knowledgeable and refined."},
        {"name": "Isabella Moreau", "background": "Famous art collector.", "motives": "Trying to steal a valuable painting.", "public_info": "Elegant and sophisticated."},
        # Add the remaining 4...
    ],
    "whispers_in_the_smoke": [
        {"name": "Vinny Russo", "background": "Owner of the speakeasy.", "motives": "Involved in illegal activities.", "public_info": "Charismatic but dangerous."},
        # Add the remaining 5...
    ]
}

roles = core_characters.get(story_id, [])
if not roles:
    st.error(f"Core characters not defined for '{story.get('title', story_id)}' yet.")
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
    st.write("- Question 1 to ask other characters")
    st.write("- Question 2 to ask other characters")
    st.write("- Question 3 to ask other characters")

st.caption("Do not show this page to other players!")
