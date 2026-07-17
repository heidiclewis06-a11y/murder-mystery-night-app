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

# Core Characters with Rich Details
core_characters = {
    "curse_of_the_crimson_cutlass": [
        {
            "name": "Captain Elias Blackthorn",
            "background": "A legendary retired pirate captain who now runs the Crimson Cutlass Dinner Show. He is known for his booming voice, theatrical flair, and a mysterious scar across his left eye from a long-ago duel. He commands respect from the crew and guests alike.",
            "motives": "He is desperately searching for the legendary Crimson Cutlass treasure map that was supposedly hidden on this very ship years ago. He believes it will restore his lost fortune.",
            "public_info": "Charismatic leader of the show, famous for his dramatic storytelling and commanding presence. Everyone knows he was once a real pirate captain."
        },
        {
            "name": "Lady Victoria Voss",
            "background": "A wealthy and elegant widow in her mid-40s who frequently attends high-society events. She carries herself with grace but has a sharp tongue when provoked. She travels with a fortune in jewels.",
            "motives": "She is looking for her late husband's lost treasure map, which she believes is connected to this ship. She will stop at nothing to find it.",
            "public_info": "Elegant, flirtatious socialite always dressed in the finest gowns and jewels."
        },
        {
            "name": "Dr. Julian Crowe",
            "background": "The ship's doctor turned performer. A quiet, intellectual man in his 50s with a slightly unsettling smile and sharp eyes that miss nothing.",
            "motives": "He is blackmailing several guests on board with secrets he discovered during medical examinations.",
            "public_info": "The ship's physician, known for his calm demeanor and extensive knowledge of medicines and poisons."
        },
        {
            "name": "Isabella 'Izzy' Torres",
            "background": "A young, fiery dancer in the dinner show. She is passionate, outspoken, and full of energy, often the center of attention.",
            "motives": "She knows a dangerous secret about the murder and is trying to decide whether to reveal it or use it to her advantage.",
            "public_info": "Talented dancer known for her fiery personality and captivating performances."
        },
        {
            "name": "Mr. Reginald Hawthorne",
            "background": "A rich merchant with shady business dealings. Loud, arrogant, and always boasting about his wealth and connections.",
            "motives": "He owes large debts to multiple people and is desperate to find a way out of his financial troubles.",
            "public_info": "Wealthy merchant known for his booming voice and expensive taste."
        },
        {
            "name": "Miss Penelope Sharpe",
            "background": "The captain's quiet and bookish assistant. She is always watching and listening, often overlooked by others.",
            "motives": "She is secretly in love with one of the guests and will do anything to protect them.",
            "public_info": "The captain's loyal assistant, known for her intelligence and quiet nature."
        }
    ],
    "death_on_the_azure_empress": [
        {
            "name": "Captain Marcus Hale",
            "background": "Experienced captain of the luxury cruise ship the Azure Empress. He has sailed these waters for over 20 years.",
            "motives": "He is hiding illegal cargo on board and was the last person to see the victim alive.",
            "public_info": "Charming and authoritative leader of the ship."
        },
        {
            "name": "Sophia Laurent",
            "background": "Famous actress on vacation. Known for her beauty and dramatic personality.",
            "motives": "She is running from a major scandal and had a public argument with the victim.",
            "public_info": "Glamorous and dramatic star."
        },
        {
            "name": "Dr. Elena Vargas",
            "background": "Ship's chief medical officer. Highly respected but has a secretive side.",
            "motives": "Involved in experimental drugs that may have been used in the murder.",
            "public_info": "Professional and calm."
        },
        {
            "name": "Victor Kane",
            "background": "Billionaire businessman known for his ruthless business tactics.",
            "motives": "Involved in corporate espionage and owed the victim a large sum of money.",
            "public_info": "Arrogant and powerful."
        },
        {
            "name": "Mia Chen",
            "background": "Young social media influencer always looking for the next big story.",
            "motives": "Blackmailing guests for content and clout.",
            "public_info": "Outgoing and always filming."
        },
        {
            "name": "Thomas Blackwell",
            "background": "Retired detective on the cruise for relaxation.",
            "motives": "Investigating a cold case connected to the victim.",
            "public_info": "Observant and quiet."
        }
    ],
    # Add the other two stories as needed
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
    
    # Introduction Statement (only for Introduction phase)
    current_act = st.session_state.get("current_act", 0)
    if current_act == 0:
        st.subheader("Introduction Statement (Say this to the group)")
        st.info(f"Good evening everyone. My name is {selected_role['name']}. I look forward to getting to know all of you tonight.")

    st.subheader("Questions to Ask")
    act_names = ["Introduction", "Act 1", "Act 2", "Act 3", "Accusations", "Reveal"]
    st.write(f"**{act_names[current_act]} Questions:**")
    st.write("- Question 1 to ask other characters")
    st.write("- Question 2 to ask other characters")
    st.write("- Question 3 to ask other characters")

st.caption("Do not show this page to other players!")
