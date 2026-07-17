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

# Full Core 6 Characters for All Stories with Evidence Ties
core_characters = {
    "curse_of_the_crimson_cutlass": [
        {"name": "Captain Elias Blackthorn", "background": "Legendary retired pirate captain who runs the dinner show. He has a scar across his left eye from a duel and a commanding presence.", "motives": "Desperately searching for the lost Crimson Cutlass treasure. He was the last person to see the victim alive.", "public_info": "Charismatic host of the show. Everyone knows he was a real pirate captain.", "evidence_tie": "His pirate sword was found near the body."},
        {"name": "Lady Victoria Voss", "background": "Wealthy widow known for her elegance and sharp tongue.", "motives": "Looking for her husband's lost treasure map. She argued with the victim earlier that evening.", "public_info": "Elegant socialite always dressed in fine gowns.", "evidence_tie": "Her monogrammed handkerchief was found with the victim."},
        {"name": "Dr. Julian Crowe", "background": "Ship's doctor turned performer. Quiet and observant with a slightly unsettling smile.", "motives": "Blackmailing several guests. He supplied the poison used in the murder.", "public_info": "The ship's physician, knowledgeable about medicines and poisons.", "evidence_tie": "His medical bag was found open near the crime scene."},
        {"name": "Isabella 'Izzy' Torres", "background": "Young, fiery dancer in the show. Passionate and outspoken.", "motives": "Knows a dangerous secret about the murder and is deciding whether to reveal it.", "public_info": "Talented dancer known for her energy and charisma.", "evidence_tie": "Her red dance scarf was found clutched in the victim's hand."},
        {"name": "Mr. Reginald Hawthorne", "background": "Rich merchant with shady business dealings. Loud and arrogant.", "motives": "Owes large debts and was arguing with the victim about money.", "public_info": "Wealthy merchant known for his boasting.", "evidence_tie": "His engraved pocket watch was found at the scene."},
        {"name": "Miss Penelope Sharpe", "background": "Quiet, bookish assistant to the captain. Always watching and listening.", "motives": "Secretly in love with one of the guests and will do anything to protect them.", "public_info": "The captain's loyal assistant, known for her intelligence.", "evidence_tie": "Her ink-stained notebook was found near the body."}
    ],
    "death_on_the_azure_empress": [
        {"name": "Captain Marcus Hale", "background": "Experienced captain of the luxury cruise ship.", "motives": "Hiding illegal cargo. He was the last to see the victim.", "public_info": "Charming and authoritative leader of the ship.", "evidence_tie": "His captain's hat was found near the body."},
        {"name": "Sophia Laurent", "background": "Famous actress on vacation.", "motives": "Running from a scandal and had a public argument with the victim.", "public_info": "Glamorous and dramatic star.", "evidence_tie": "Her lipstick-stained glass was found at the crime scene."},
        {"name": "Dr. Elena Vargas", "background": "Ship's chief medical officer.", "motives": "Involved in experimental drugs that may have been used in the murder.", "public_info": "Professional and calm.", "evidence_tie": "Her medical kit was found open near the victim."},
        {"name": "Victor Kane", "background": "Billionaire businessman.", "motives": "Involved in corporate espionage and owed the victim money.", "public_info": "Arrogant and powerful.", "evidence_tie": "His monogrammed cufflinks were found at the scene."},
        {"name": "Mia Chen", "background": "Young social media influencer.", "motives": "Blackmailing guests for content.", "public_info": "Outgoing and always filming.", "evidence_tie": "Her phone was found recording near the body."},
        {"name": "Thomas Blackwell", "background": "Retired detective on the cruise.", "motives": "Investigating a cold case connected to the victim.", "public_info": "Observant and quiet.", "evidence_tie": "His detective notebook was found near the victim."}
    ],
    # Add the other two stories similarly if needed
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
    
    st.subheader("Evidence Tie")
    st.write(selected_role.get("evidence_tie", "No direct evidence tie defined."))

    st.divider()
    
    # Introduction Statement
    current_act = st.session_state.get("current_act", 0)
    if current_act == 0:
        st.subheader("Introduction Statement (Say this to the group)")
        st.info("Good evening everyone. My name is " + selected_role['name'] + ". I look forward to getting to know all of you tonight.")

    st.subheader("Questions to Ask")
    act_names = ["Introduction", "Act 1", "Act 2", "Act 3", "Accusations", "Reveal"]
    st.write(f"**{act_names[current_act]} Questions:**")
    st.write("- Question 1 to ask other characters")
    st.write("- Question 2 to ask other characters")
    st.write("- Question 3 to ask other characters")

st.caption("Do not show this page to other players!")
