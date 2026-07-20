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

# Evidence per Act
evidence_per_act = {
    "curse_of_the_crimson_cutlass": {
        1: ["lipstick-stained glass", "broken pocket watch", "torn piece of map"],
        2: ["monogrammed handkerchief", "gunpowder residue on glove", "empty whiskey bottle"],
        3: ["blood-stained cutlass", "hidden note with initials", "missing treasure map piece"]
    },
    "death_on_the_azure_empress": {
        1: ["broken watch strap", "monogrammed cufflink", "sedative residue in glass"],
        2: ["torn IOU note", "pearl necklace fragments", "forged guest list"],
        3: ["poison vial", "captain's log entry", "hidden safe key"]
    },
    "shadows_in_the_gallery": {
        1: ["forged security badge", "ultramarine pigment traces", "torn gallery catalog"],
        2: ["empty display case key", "paintbrush with fingerprints", "anonymous threat note"],
        3: ["stolen painting frame", "security camera memory card", "hidden vault combination"]
    },
    "whispers_in_the_smoke": {
        1: ["monogrammed flask", "pearl necklace", "broken champagne glass"],
        2: ["gun with missing bullets", "lipstick-stained cigarette", "torn betting slip"],
        3: ["hidden ledger", "blood-stained handkerchief", "speakeasy key"]
    }
}

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

# Persistent extra characters with unique details
if "extra_characters" not in st.session_state or st.session_state.get("current_game_id") != game["game_id"]:
    st.session_state.extra_characters = []
    supporting_templates = [
        {"name": "Jamie Rivera", "background": "Long-time janitor for the dinner show theater. Knows the ship layout better than most.", "motives": "Found something important near the body but is afraid to speak up.", "public_info": "Quiet janitor who works backstage."},
        {"name": "Taylor Brooks", "background": "VIP guest who paid extra to attend and snuck backstage.", "motives": "Has a personal grudge against one of the main actors.", "public_info": "Wealthy VIP guest."},
        {"name": "Casey Quinn", "background": "Local musician hired to play live music.", "motives": "Overheard a heated argument before the murder.", "public_info": "Live musician for the show."},
        {"name": "Morgan Ellis", "background": "Stage technician responsible for lighting and props.", "motives": "Tampered with a prop to settle a personal score.", "public_info": "Stage technician."},
        {"name": "Riley Parker", "background": "Aspiring actress hired as a last-minute understudy.", "motives": "Jealous of the main cast and hoping for a bigger role.", "public_info": "Understudy actress."},
        {"name": "Sam Reid", "background": "Local reporter invited to review the show.", "motives": "Investigating the show for a story and saw something suspicious.", "public_info": "Local reporter covering the show."}
    ]
    
    random.shuffle(supporting_templates)
    for i in range(max(0, num_guests - 6)):
        template = supporting_templates[i % len(supporting_templates)]
        st.session_state.extra_characters.append({
            "name": template["name"],
            "background": template["background"],
            "motives": template["motives"],
            "public_info": template["public_info"],
            "introduction": f"Good evening. I'm {template['name']}. I've been part of this production in my own way for some time now."
        })
    st.session_state.current_game_id = game["game_id"]

# Combine core + extras
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
        evidence_list = evidence_per_act.get(story_id, {}).get(current_act, ["unknown evidence"])
        evidence = random.choice(evidence_list)
        
        st.write(f"**{act_names[current_act]} - Questions about the revealed evidence ({evidence})**")
        st.write(f"1. How do you explain your connection to the {evidence} that was found?")
        st.write(f"2. What were you doing when the {evidence} appeared?")
        st.write(f"3. Do you know anything about how the {evidence} ended up at the crime scene?")

st.caption("Do not show this page to other players!")
