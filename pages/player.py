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
        {"name": "Captain Elias Blackthorn", "background": "Veteran stage actor who has played the pirate captain for years. He takes his role extremely seriously.", "motives": "He is obsessed with finding the real Crimson Cutlass treasure map.", "public_info": "Charismatic lead actor and host of the show.", "introduction": "Ladies and gentlemen, I am Captain Elias Blackthorn. I've sailed these theatrical seas for many years now, and I must say, tonight has taken an unexpected turn."},
        {"name": "Lady Victoria Voss", "background": "Experienced actress playing the wealthy widow. Elegant but competitive.", "motives": "She is looking for the lost treasure map prop.", "public_info": "Elegant socialite actress.", "introduction": "Good evening. I am Lady Victoria Voss. I've performed in many grand productions, but nothing quite like this."},
        {"name": "Dr. Julian Crowe", "background": "Character actor playing the ship's doctor. Quiet and intellectual.", "motives": "Blackmailing several cast members.", "public_info": "The ship's physician.", "introduction": "Good evening. I am Dr. Julian Crowe, the ship's physician in this production. I have seen many strange things in my career, but this..." },
        {"name": "Isabella 'Izzy' Torres", "background": "Young, fiery dancer and actress.", "motives": "She knows a dangerous secret about the murder.", "public_info": "Talented dancer.", "introduction": "Hey everyone, I'm Izzy Torres, the dancer in the show. I've been performing since I was little, but tonight feels different."},
        {"name": "Mr. Reginald Hawthorne", "background": "Actor playing the wealthy merchant. Loud and arrogant.", "motives": "He owes large debts.", "public_info": "Boastful merchant.", "introduction": "I am Reginald Hawthorne, the wealthy merchant in tonight's performance. I've made my fortune through hard work and sharp deals."},
        {"name": "Miss Penelope Sharpe", "background": "Quiet actress playing the captain's assistant.", "motives": "Secretly in love with one of the guests.", "public_info": "Bookish assistant.", "introduction": "Hello... I'm Penelope Sharpe, assistant to Captain Blackthorn in the show. I've always preferred to stay behind the scenes."}
    ],
    "death_on_the_azure_empress": [
        {"name": "Captain Marcus Hale", "background": "Seasoned actor playing the ship captain.", "motives": "Hiding illegal cargo.", "public_info": "Authoritative leader.", "introduction": "Good evening. I am Captain Marcus Hale. I've captained many ships on stage and off, but this night is unlike any other."},
        {"name": "Sophia Laurent", "background": "Famous actress playing the star passenger.", "motives": "Running from a scandal.", "public_info": "Glamorous performer.", "introduction": "Darlings, I am Sophia Laurent. I've graced many stages, but I never expected to be part of a real-life drama."}
    ]
}

# Persistent extra characters with unique speaking styles
if "extra_characters" not in st.session_state or st.session_state.get("current_game_id") != game["game_id"]:
    st.session_state.extra_characters = []
    supporting_templates = [
        {
            "name": "Jamie Rivera",
            "background": "Long-time janitor for the dinner show theater. They clean up after every performance and know the layout of the ship better than most cast members.",
            "motives": "They found something important near the body but haven't told anyone because they need the job.",
            "public_info": "Quiet janitor who works backstage.",
            "introduction": "Uh, hi everyone. I'm Jamie Rivera. I clean up after the shows here. Been doing it for years. Never seen anything like this."
        },
        {
            "name": "Taylor Brooks",
            "background": "VIP guest who paid extra to attend the show and snuck backstage to meet the cast.",
            "motives": "They have a personal grudge against one of the main actors from a previous show.",
            "public_info": "Wealthy VIP guest.",
            "introduction": "Hello, I'm Taylor Brooks. I paid quite a bit to be here tonight as a special guest. This is certainly not what I expected."
        },
        {
            "name": "Casey Quinn",
            "background": "Local musician hired to play live music for the show. They have performed here many times.",
            "motives": "They overheard a heated argument between two cast members shortly before the murder.",
            "public_info": "Live musician for the show.",
            "introduction": "Hey folks, I'm Casey Quinn. I play the piano and saxophone for the show. Been doing gigs like this for a long time."
        },
        {
            "name": "Morgan Ellis",
            "background": "Stage technician responsible for lighting and props. They have worked on the production for three years.",
            "motives": "They tampered with a prop that may have been used in the murder to settle a personal score.",
            "public_info": "Stage technician.",
            "introduction": "I'm Morgan Ellis. I handle the lights and props backstage. Been with this production since it started."
        },
        {
            "name": "Riley Parker",
            "background": "Aspiring actress who was hired as a last-minute understudy for one of the smaller roles.",
            "motives": "She is jealous of the main cast and was hoping the murder would create an opportunity for her.",
            "public_info": "Understudy actress.",
            "introduction": "Hi, I'm Riley Parker. I was brought in as an understudy. This is my first big show like this."
        },
        {
            "name": "Sam Reid",
            "background": "Local reporter who was invited to review the show but stayed longer than expected.",
            "motives": "They are investigating the show for a story and may have seen something they shouldn't have.",
            "public_info": "Local reporter covering the show.",
            "introduction": "Good evening. I'm Sam Reid, a reporter for the local paper. I was here to review the show tonight."
        }
    ]
    
    random.shuffle(supporting_templates)
    for i in range(max(0, num_guests - 6)):
        template = supporting_templates[i % len(supporting_templates)]
        st.session_state.extra_characters.append({
            "name": template["name"],
            "background": template["background"],
            "motives": template["motives"],
            "public_info": template["public_info"],
            "introduction": template["introduction"]
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
        st.info(selected_role.get("introduction", f"Good evening. I am {selected_role['name']}."))

    if current_act > 0:
        st.subheader("Questions to Ask")
        act_names = ["Introduction", "Act 1", "Act 2", "Act 3", "Accusations", "Reveal"]
        st.write(f"**{act_names[current_act]} Questions:**")
        st.write("- Question 1 to ask other characters")
        st.write("- Question 2 to ask other characters")
        st.write("- Question 3 to ask other characters")

st.caption("Do not show this page to other players!")
