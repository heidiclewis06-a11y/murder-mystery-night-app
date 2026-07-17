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
        {"name": "Captain Elias Blackthorn", "background": "Veteran stage actor who has played the pirate captain for years. He takes his role extremely seriously.", "motives": "He is obsessed with finding the real Crimson Cutlass treasure map.", "public_info": "Charismatic lead actor and host of the show."},
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

# Persistent extra characters with unique, detailed pasts
if "extra_characters" not in st.session_state or st.session_state.get("current_game_id") != game["game_id"]:
    st.session_state.extra_characters = []
    supporting_templates = [
        {
            "name": "Jamie Rivera",
            "background": "Long-time janitor for the dinner show theater. They clean up after every performance and know the layout of the ship better than most cast members.",
            "motives": "They found something important near the body but haven't told anyone because they are afraid of being blamed.",
            "public_info": "Quiet janitor who works backstage."
        },
        {
            "name": "Taylor Brooks",
            "background": "VIP guest who paid extra to attend the show and snuck backstage to meet the cast.",
            "motives": "They have a personal grudge against one of the main actors from a previous show.",
            "public_info": "Wealthy VIP guest."
        },
        {
            "name": "Casey Quinn",
            "background": "Local musician hired to play live music for the show. They have performed here many times.",
            "motives": "They overheard a heated argument between two cast members shortly before the murder.",
            "public_info": "Live musician for the show."
        },
        {
            "name": "Morgan Ellis",
            "background": "Stage technician responsible for lighting and props. They have worked on the production for three years.",
            "motives": "They tampered with a prop that may have been used in the murder to settle a personal score.",
            "public_info": "Stage technician."
        },
        {
            "name": "Riley Parker",
            "background": "Aspiring actress who was hired as a last-minute understudy for one of the smaller roles.",
            "motives": "She is jealous of the main cast and was hoping the murder would create an opportunity for her.",
            "public_info": "Understudy actress."
        },
        {
            "name": "Sam Reid",
            "background": "Local reporter who was invited to review the show but stayed longer than expected.",
            "motives": "They are investigating the show for a story and may have seen something they shouldn't have.",
            "public_info": "Local reporter covering the show."
        }
    ]
    
    random.shuffle(supporting_templates)
    for i in range(max(0, num_guests - 6)):
        template = supporting_templates[i % len(supporting_templates)]
        st.session_state.extra_characters.append({
            "name": template["name"],
            "background": template["background"],
            "motives": template["motives"],
            "public_info": template["public_info"]
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
