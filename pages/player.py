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
    1: ["lipstick-stained glass", "broken pocket watch", "torn piece of map"],
    2: ["monogrammed handkerchief", "gunpowder residue on glove", "empty whiskey bottle"],
    3: ["blood-stained cutlass", "hidden note with initials", "missing treasure map piece"]
}

# Full Character Data with Personality-Driven, Balanced Accusations
characters = {
    "Captain Elias Blackthorn": {
        "background": "Veteran stage actor who has played the pirate captain for years.",
        "motives": "He is obsessed with finding the real Crimson Cutlass treasure map.",
        "public_info": "Charismatic lead actor and host of the show.",
        "introduction": "Ladies and gentlemen, I am Captain Elias Blackthorn. I never imagined our performance would turn into a real tragedy tonight.",
        "questions": {
            1: ["Lady Victoria, what were you doing near the lipstick-stained glass?", "Dr. Crowe, did you see who broke the pocket watch?"],
            2: ["Izzy, why was your scarf near the gunpowder residue?", "Mr. Hawthorne, did you touch the empty whiskey bottle?"],
            3: ["Miss Sharpe, how did the blood-stained cutlass end up in your area?"]
        },
        "innocent_response": "I had nothing to do with this. As the captain of this show, I was busy preparing for the grand finale the entire time.",
        "guilty_response": "I had nothing to do with this... I mean, as the captain, I was busy preparing for the grand finale. Why would anyone think I had anything to do with it?"
    },
    "Lady Victoria Voss": {
        "background": "Experienced actress playing the wealthy widow.",
        "motives": "She is looking for the lost treasure map prop.",
        "public_info": "Elegant and flirtatious actress always dressed in stunning gowns.",
        "introduction": "Good evening. I am Lady Victoria Voss. This night has taken a dreadful turn.",
        "questions": {
            1: ["Captain Blackthorn, why was your watch found near the victim?", "Dr. Crowe, did you see anyone with the torn map piece?"],
            2: ["Izzy, why was your scarf near the gunpowder?", "Miss Sharpe, did you see who left the handkerchief?"],
            3: ["Mr. Hawthorne, how did your note end up with the cutlass?"]
        },
        "innocent_response": "I had nothing to do with this. I was in my dressing room the whole time, preparing for my next scene.",
        "guilty_response": "I had nothing to do with this... I was in my dressing room. Why on earth would anyone accuse me?"
    },
    "Dr. Julian Crowe": {
        "background": "Character actor playing the ship's doctor.",
        "motives": "Blackmailing several cast members.",
        "public_info": "The ship's physician.",
        "introduction": "Good evening. I am Dr. Julian Crowe. What has happened here tonight is deeply disturbing.",
        "questions": {
            1: ["Captain Blackthorn, why was your watch found near the victim?", "Lady Victoria, did you see who broke the pocket watch?"],
            2: ["Izzy, why was your scarf near the gunpowder?", "Mr. Hawthorne, did you touch the empty whiskey bottle?"],
            3: ["Miss Sharpe, how did the blood-stained cutlass end up in your area?"]
        },
        "innocent_response": "I had nothing to do with this. As the ship's physician, I was attending to a guest the entire time.",
        "guilty_response": "I had nothing to do with this... I was attending to a guest. I don't know why anyone would point fingers at me."
    },
    "Isabella 'Izzy' Torres": {
        "background": "Young, fiery dancer and actress.",
        "motives": "She knows a dangerous secret about the murder.",
        "public_info": "Talented dancer.",
        "introduction": "Hi everyone... I'm Izzy Torres. I can't believe this is happening.",
        "questions": {
            1: ["Captain Blackthorn, why was your watch found near the victim?", "Lady Victoria, did you see who broke the pocket watch?"],
            2: ["Dr. Crowe, why was your medical bag near the gunpowder?", "Mr. Hawthorne, did you touch the empty whiskey bottle?"],
            3: ["Miss Sharpe, how did the blood-stained cutlass end up in your area?"]
        },
        "innocent_response": "I had nothing to do with this. I was practicing my dance routine backstage the whole time.",
        "guilty_response": "I had nothing to do with this... I was practicing my dance routine. Why would anyone think I was involved?"
    },
    "Mr. Reginald Hawthorne": {
        "background": "Actor playing the wealthy merchant.",
        "motives": "He owes large debts.",
        "public_info": "Boastful merchant.",
        "introduction": "This is outrageous! I am Reginald Hawthorne. I demand to know what is going on here.",
        "questions": {
            1: ["Captain Blackthorn, why was your watch found near the victim?", "Lady Victoria, did you see who broke the pocket watch?"],
            2: ["Izzy, why was your scarf near the gunpowder?", "Dr. Crowe, did you see anyone with the empty whiskey bottle?"],
            3: ["Miss Sharpe, how did your note end up with the cutlass?"]
        },
        "innocent_response": "I had nothing to do with this. I was in the dining hall entertaining guests the entire time.",
        "guilty_response": "I had nothing to do with this... I was in the dining hall. How dare anyone suggest I had anything to do with it!"
    },
    "Miss Penelope Sharpe": {
        "background": "Quiet actress playing the captain's assistant.",
        "motives": "Secretly in love with one of the guests.",
        "public_info": "Bookish assistant.",
        "introduction": "Hello... I'm Penelope Sharpe. I don't know what to say about what happened.",
        "questions": {
            1: ["Captain Blackthorn, why was your watch found near the victim?", "Lady Victoria, did you see who broke the pocket watch?"],
            2: ["Izzy, why was your scarf near the gunpowder?", "Dr. Crowe, did you see anyone with the empty whiskey bottle?"],
            3: ["Mr. Hawthorne, how did your note end up with the cutlass?"]
        },
        "innocent_response": "I had nothing to do with this. I was organizing props backstage the entire time.",
        "guilty_response": "I had nothing to do with this... I was organizing props backstage. Please, I don't want any trouble."
    }
}

role_names = list(characters.keys())
selected_role_name = st.selectbox("Select Your Character", options=role_names, key="selected_role")

selected_role = characters.get(selected_role_name)

if selected_role:
    st.divider()
    st.subheader(f"Your Character: {selected_role_name}")
    
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
        st.info(selected_role.get("introduction", f"Good evening. I am {selected_role_name}."))

    if current_act > 0:
        st.subheader("Questions to Ask")
        evidence_list = evidence_per_act.get(current_act, ["unknown evidence"])
        evidence = random.choice(evidence_list)
        st.write(f"**Act {current_act} - Questions about the revealed evidence ({evidence})**")
        for q in selected_role.get("questions", {}).get(current_act, ["How do you explain this evidence?"]):
            st.write(f"- {q}")
        
        st.divider()
        
        st.subheader("What to Say If Questioned")
        st.write("**If Innocent:**")
        st.info(selected_role.get("innocent_response", "I had nothing to do with this."))
        st.write("**If Guilty:**")
        st.info(selected_role.get("guilty_response", "I had nothing to do with this..."))

st.caption("Do not show this page to other players!")