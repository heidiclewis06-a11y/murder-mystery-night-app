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
        {"name": "Captain Elias Blackthorn", "background": "Veteran stage actor who has played the pirate captain for years. He takes his role extremely seriously.", "motives": "He is obsessed with finding the real Crimson Cutlass treasure map.", "public_info": "Charismatic lead actor and host."},
        {"name": "Lady Victoria Voss", "background": "Experienced actress playing the wealthy widow. Elegant but competitive.", "motives": "She is looking for the lost treasure map prop.", "public_info": "Elegant socialite actress."},
        {"name": "Dr. Julian Crowe", "background": "Character actor playing the ship's doctor. Quiet and intellectual.", "motives": "Blackmailing several cast members.", "public_info": "The ship's physician."},
        {"name": "Isabella 'Izzy' Torres", "background": "Young, fiery dancer and actress.", "motives": "She knows a dangerous secret about the murder.", "public_info": "Talented dancer."},
        {"name": "Mr. Reginald Hawthorne", "background": "Actor playing the wealthy merchant. Loud and arrogant.", "motives": "He owes large debts.", "public_info": "Boastful merchant."},
        {"name": "Miss Penelope Sharpe", "background": "Quiet actress playing the captain's assistant.", "motives": "Secretly in love with one of the guests.", "public_info": "Bookish assistant."}
    ],
    "death_on_the_azure_empress": [
        {"name": "Captain Marcus Hale", "background": "Seasoned actor playing the ship captain.", "motives": "Hiding illegal cargo.", "public_info": "Authoritative leader."},
        {"name": "Sophia Laurent", "background": "Famous actress playing the star passenger.", "motives": "Running from a scandal.", "public_info": "Glamorous performer."},
        {"name": "Dr. Elena Vargas", "background": "Actress playing the chief medical officer.", "motives": "Involved in experimental drugs.", "public_info": "Professional doctor."},
        {"name": "Victor Kane", "background": "Actor playing the billionaire businessman.", "motives": "Corporate espionage.", "public_info": "Arrogant businessman."},
        {"name": "Mia Chen", "background": "Young actress playing the influencer.", "motives": "Blackmailing guests.", "public_info": "Outgoing social media star."},
        {"name": "Thomas Blackwell", "background": "Actor playing the retired detective.", "motives": "Investigating a cold case.", "public_info": "Observant and quiet."}
    ]
}

# Persistent extra characters with unique, detailed backgrounds
if "extra_characters" not in st.session_state or st.session_state.get("current_game_id") != game["game_id"]:
    st.session_state.extra_characters = []
    supporting_templates = [
        {"role": "Bartender", "background": "Long-time supporting actor who has worked on the show for three seasons. They know many cast secrets from late-night conversations at the bar.", "motives": "They are deeply in debt and have been stealing small items from the cast to sell."},
        {"role": "Musician", "background": "Talented jazz musician turned actor. They provide live music for the show and have a calm, observant personality.", "motives": "They overheard something incriminating the night of the murder and are trying to decide what to do with the information."},
        {"role": "Stage Technician", "background": "Behind-the-scenes technician who knows every inch of the set. Quiet but extremely detail-oriented.", "motives": "They have a grudge against one of the main cast members and may have tampered with props."},
        {"role": "Guest Entertainer", "background": "Visiting performer who was brought in for this special show. Charismatic but somewhat mysterious.", "motives": "They are hiding their true identity and connection to the victim."},
        {"role": "Ship Crew Member", "background": "Actor playing a crew member. Practical and no-nonsense, they help keep the show running smoothly.", "motives": "They discovered the victim arguing with someone shortly before the murder."},
        {"role": "Local Artist", "background": "Local artist hired to create set pieces for the show. Creative and free-spirited.", "motives": "They are in a secret romantic relationship with one of the main suspects."}
    ]
    
    random.shuffle(supporting_templates)
    for i in range(max(0, num_guests - 6)):
        template = supporting_templates[i % len(supporting_templates)]
        first_names = ["Alex", "Jordan", "Taylor", "Casey", "Riley", "Sam", "Morgan", "Jamie"]
        last_names = ["Rivera", "Blake", "Morgan", "Quinn", "Brooks", "Parker", "Ellis", "Reid"]
        name = f"{random.choice(first_names)} {random.choice(last_names)}"
        
        st.session_state.extra_characters.append({
            "name": name,
            "background": template["background"],
            "motives": template["motives"],
            "public_info": f"Supporting cast member playing a {template['role'].lower()}."
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
