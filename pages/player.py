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

# Core Characters with Tense, Murder-Suspect Introductions
core_characters = {
    "curse_of_the_crimson_cutlass": [
        {
            "name": "Captain Elias Blackthorn",
            "background": "A veteran stage actor who plays the role of the legendary pirate captain in the dinner show. He takes his role very seriously and has a commanding presence.",
            "motives": "He is desperately searching for the legendary Crimson Cutlass treasure map prop. He was one of the last to see the victim alive.",
            "public_info": "Charismatic lead actor and host of the show. Known for his dramatic storytelling.",
            "introduction": "Everyone... I am Captain Elias Blackthorn. I can't believe what has happened tonight. One of us is responsible for this."
        },
        {
            "name": "Lady Victoria Voss",
            "background": "An experienced actress who plays the wealthy widow. She is elegant on stage but can be quite sharp and competitive behind the scenes.",
            "motives": "She is looking for the lost treasure map prop and had a heated argument with the victim earlier.",
            "public_info": "Elegant and flirtatious actress always dressed in stunning period gowns.",
            "introduction": "Good evening. I am Lady Victoria Voss. This is a nightmare. I never thought something like this would happen during one of our shows."
        },
        {
            "name": "Dr. Julian Crowe",
            "background": "A character actor who plays the ship's doctor. He is quiet and intellectual with a slightly unsettling intensity.",
            "motives": "He is blackmailing several cast members and may have supplied something used in the murder.",
            "public_info": "The ship's doctor in the show, known for his calm demeanor.",
            "introduction": "I am Dr. Julian Crowe, the ship's physician in this production. What has happened here tonight is deeply disturbing."
        },
        {
            "name": "Isabella 'Izzy' Torres",
            "background": "A young, fiery dancer and actress. She is passionate and outspoken both on and off stage.",
            "motives": "She knows a dangerous secret about the murder and is deciding whether to reveal it.",
            "public_info": "Talented dancer known for her fiery personality.",
            "introduction": "I'm Izzy Torres, the dancer in the show. I still can't believe one of us did this..."
        },
        {
            "name": "Mr. Reginald Hawthorne",
            "background": "A character actor who plays the wealthy merchant. He is loud and arrogant on stage.",
            "motives": "He owed the victim money and was arguing with him before the murder.",
            "public_info": "Wealthy merchant known for his booming voice.",
            "introduction": "I am Reginald Hawthorne, the wealthy merchant in tonight's show. This is an outrage. We need to get to the bottom of this immediately."
        },
        {
            "name": "Miss Penelope Sharpe",
            "background": "A quiet, bookish actress who plays the captain's assistant. She notices everything.",
            "motives": "She is secretly in love with one of the guests and will do anything to protect them.",
            "public_info": "The captain's loyal assistant, known for her intelligence.",
            "introduction": "I'm Penelope Sharpe, assistant to Captain Blackthorn in the show. I... I don't know what to say about what happened."
        }
    ],
    # Add other stories as needed
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
        st.info(selected_role.get("introduction", "Introduce yourself to the group."))

    # Questions (hidden during Introduction)
    if current_act > 0:
        st.subheader("Questions to Ask")
        act_names = ["Introduction", "Act 1", "Act 2", "Act 3", "Accusations", "Reveal"]
        st.write(f"**{act_names[current_act]} Questions:**")
        st.write("- Question 1 to ask other characters")
        st.write("- Question 2 to ask other characters")
        st.write("- Question 3 to ask other characters")

st.caption("Do not show this page to other players!")
