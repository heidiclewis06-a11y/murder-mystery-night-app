import streamlit as st
import json
import os

st.set_page_config(page_title="Player View", page_icon="🕵️", layout="centered")

st.title("🕵️ Your Private Character Packet")
st.caption("Do not show this to other players")

if "current_game" not in st.session_state:
    st.warning("No active game. Ask the host to generate one first.")
    st.stop()

game = st.session_state.current_game
story_id = game["story_id"]

try:
    with open(f"stories/{story_id}.json", "r", encoding="utf-8") as f:
        story = json.load(f)
except:
    st.error("Could not load story.")
    st.stop()

# Character Selection
st.write("**Select your character:**")
character_options = [r["default_name"] for r in story["roles"]]
selected_name = st.selectbox("Your Character", options=character_options)

role = next((r for r in story["roles"] if r["default_name"] == selected_name), None)

if role:
    st.subheader(f"You are **{role['default_name']}**")
    
    # Public Background
    st.write("**Public Background:**")
    st.info(role.get("personality", "A key member of the cast"))
    
    # Private Background
    st.write("**Private Information:**")
    st.write(role.get("key_relationships", "You have important connections..."))
    
    # Current Act
    current_act = st.session_state.get("current_act", 0)
    act_names = ["Introduction", "Act 1", "Act 2", "Act 3", "Accusations", "Reveal"]
    st.write(f"**Current Phase:** {act_names[current_act]}")
    
    # Act-specific Questions and Guidance
    if 1 <= current_act <= 3:
        act_num = current_act
        st.subheader(f"Act {act_num} - Your Questions & Suggested Responses")
        
        st.write("**Questions you should ask others:**")
        st.info("Ask about the latest clue and people's relationships. Be clever and in character.")
        
        st.write("**How to answer when asked:**")
        st.info("Stay in character. Sound defensive if you are the murderer, natural if innocent.")
        
        st.caption("Use the latest clue to guide your questions.")
    
    elif current_act == 4:
        st.subheader("Accusation Phase")
        st.info("Prepare your accusation. Decide who you think the murderer is and why.")
    
    elif current_act == 5:
        st.subheader("Final Reveal")
        st.info("The host will reveal the murderer soon. Be ready to react in character.")

    # Reveal Fate Button
    if st.button("🔍 Reveal My Fate (Private)", type="primary"):
        murderer_role = game["murderer_role"]
        is_murderer = role["role_id"] == murderer_role
        
        if is_murderer:
            st.error("**You are the MURDERER.**")
            confession = story["confessions"][role["role_id"]]["guilty"]
        else:
            st.success("**You are INNOCENT.**")
            confession = story["confessions"][role["role_id"]]["innocent"]
        
        st.write("**Your Full Confession:**")
        st.write(confession)
    
    st.caption("Refresh this page when the host advances to the next act.")

else:
    st.error("Character not found.")

st.caption("Mystery Night AI - Player View")
