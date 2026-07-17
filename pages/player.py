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

# Expanded Core 6 Characters
core_characters = {
    "curse_of_the_crimson_cutlass": [
        {
            "name": "Captain Elias Blackthorn",
            "background": "A legendary retired pirate captain who now runs the Crimson Cutlass Dinner Show. He is known for his booming voice and theatrical flair, but carries the weight of a dark past involving lost treasure and betrayal.",
            "motives": "He is desperately searching for the legendary Crimson Cutlass treasure map that was supposedly hidden on this very ship years ago.",
            "public_info": "Charismatic leader of the show, famous for his dramatic storytelling and commanding presence.",
            "introduction": "Ahoy there, mateys! I be Captain Elias Blackthorn, master of this fine vessel and your host for this evening's adventure!"
        },
        {
            "name": "Lady Victoria Voss",
            "background": "A wealthy and elegant widow who frequently attends high-society events. She travels with a fortune in jewels and a mysterious past.",
            "motives": "She is looking for her late husband's lost treasure map, which she believes is connected to this ship.",
            "public_info": "Elegant, flirtatious, and always dressed in the finest gowns.",
            "introduction": "Good evening, darlings. I am Lady Victoria Voss. It's a pleasure to be among such distinguished company tonight."
        },
        # Add more characters as needed...
    ],
    # You can expand the other stories similarly
}

roles = core_characters.get(story_id, [])
if not roles:
    st.error(f"Core characters not defined for this story yet.")
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
    
    # Introduction Statement (only for Introduction phase)
    current_act = st.session_state.get("current_act", 0)
    if current_act == 0:
        st.subheader("Introduction Statement (Say this to the group)")
        st.info(selected_role.get("introduction", "Introduce yourself dramatically to the group."))
    
    st.subheader("Questions to Ask")
    act_names = ["Introduction", "Act 1", "Act 2", "Act 3", "Accusations", "Reveal"]
    st.write(f"**{act_names[current_act]} Questions:**")
    st.write("- Question 1 to ask other characters")
    st.write("- Question 2 to ask other characters")
    st.write("- Question 3 to ask other characters")

st.caption("Do not show this page to other players!")
