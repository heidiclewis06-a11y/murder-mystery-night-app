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

# Core Characters with Modern Actor Flavor
core_characters = {
    "curse_of_the_crimson_cutlass": [
        {
            "name": "Captain Elias Blackthorn",
            "background": "A veteran stage actor who plays the role of the legendary pirate captain in the dinner show. He brings dramatic energy to every performance and takes his role very seriously.",
            "motives": "He is desperately searching for the legendary Crimson Cutlass treasure map prop that was supposedly hidden on this ship years ago. He believes finding it will make the show legendary.",
            "public_info": "Charismatic lead actor and host of the show. Known for his booming voice and commanding stage presence.",
            "introduction": "Ladies and gentlemen, welcome aboard! I am Captain Elias Blackthorn, master of this fine vessel and your host for this evening's thrilling adventure. Let the show begin!"
        },
        {
            "name": "Lady Victoria Voss",
            "background": "An experienced actress who plays the wealthy widow in the dinner show. She is elegant on stage but can be quite sharp and competitive behind the scenes.",
            "motives": "She is looking for the lost treasure map prop that she believes her character’s husband hid. She wants to be the star of the show.",
            "public_info": "Elegant and flirtatious actress always dressed in stunning period gowns.",
            "introduction": "Good evening, everyone. I am Lady Victoria Voss. It is an absolute pleasure to be performing with all of you tonight."
        },
        {
            "name": "Dr. Julian Crowe",
            "background": "A character actor who plays the ship's doctor. He is quiet and intellectual on stage, but has a slightly unsettling intensity that makes him memorable.",
            "motives": "He is blackmailing several other cast members with secrets he discovered during rehearsals.",
            "public_info": "The ship's doctor in the show, known for his calm demeanor and medical knowledge.",
            "introduction": "Good evening, everyone. I am Dr. Julian Crowe, the ship's physician. I look forward to an... enlightening evening together."
        },
        {
            "name": "Isabella 'Izzy' Torres",
            "background": "A young, energetic dancer and actress who plays the fiery dancer role. She is passionate and full of life both on and off stage.",
            "motives": "She knows a dangerous secret about the plot and is deciding whether to reveal it or use it to steal the spotlight.",
            "public_info": "Talented dancer known for her fiery personality and captivating performances.",
            "introduction": "¡Hola everyone! I'm Izzy Torres, the star dancer of this show! Let's make this night unforgettable!"
        },
        {
            "name": "Mr. Reginald Hawthorne",
            "background": "A character actor who plays the wealthy merchant. He is loud, arrogant, and loves to ham it up on stage.",
            "motives": "He owes large debts in real life and sees this show as a chance to turn his luck around.",
            "public_info": "Wealthy merchant known for his booming voice and over-the-top personality.",
            "introduction": "Good evening, ladies and gentlemen! I am Reginald Hawthorne, successful merchant and man of considerable means. A pleasure to meet you all!"
        },
        {
            "name": "Miss Penelope Sharpe",
            "background": "A quiet, bookish actress who plays the captain's assistant. She is often overlooked but notices everything.",
            "motives": "She is secretly in love with one of the other actors and will do anything to protect them.",
            "public_info": "The captain's loyal assistant, known for her intelligence and quiet nature.",
            "introduction": "Hello everyone... I'm Penelope Sharpe, assistant to Captain Blackthorn. I hope you all enjoy the show tonight."
        }
    ],
    # Add the other stories when ready
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
