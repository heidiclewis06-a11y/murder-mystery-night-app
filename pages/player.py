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

# Full Core 6 Characters per Story
core_characters = {
    "curse_of_the_crimson_cutlass": [
        {"name": "Captain Elias Blackthorn", "background": "Retired pirate captain who now runs the dinner show. Charismatic but haunted by his past.", "motives": "Searching for the lost Crimson Cutlass treasure.", "public_info": "Famous for his dramatic storytelling."},
        {"name": "Lady Victoria Voss", "background": "Wealthy socialite attending the show with her husband.", "motives": "Hiding a dark secret from her past.", "public_info": "Elegant and flirtatious."},
        {"name": "Dr. Julian Crowe", "background": "Ship's doctor turned performer.", "motives": "Blackmailing several guests.", "public_info": "Quiet and observant."},
        {"name": "Isabella 'Izzy' Torres", "background": "Young dancer in the show.", "motives": "Knows too much about the murder.", "public_info": "Fiery and outspoken."},
        {"name": "Mr. Reginald Hawthorne", "background": "Rich merchant with shady dealings.", "motives": "Owes money to multiple people.", "public_info": "Arrogant and loud."},
        {"name": "Miss Penelope Sharpe", "background": "Mysterious assistant to the captain.", "motives": "Secretly in love with one of the guests.", "public_info": "Shy and bookish."}
    ],
    # Add other stories similarly...
    "death_on_the_azure_empress": [
        {"name": "Captain Marcus Hale", "background": "Captain of the luxury cruise ship.", "motives": "Hiding illegal cargo.", "public_info": "Charming leader."},
        # ... (add the other 5)
    ]
    # You can expand the other stories similarly
}

roles = core_characters.get(story_id, [])
if not roles:
    st.error("Core characters not defined for this story yet. Please tell me which story you're using and I will add them.")
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
