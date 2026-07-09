import streamlit as st
import json

st.set_page_config(page_title="Host Control", page_icon="🎤", layout="wide")

st.title("🎤 Mystery Night Host Control Panel")

if "current_game" not in st.session_state:
    st.warning("No active game. Please generate a game from the main page first.")
    st.stop()

game = st.session_state.current_game
story_id = game["story_id"]

try:
    with open(f"stories/{story_id}.json", "r", encoding="utf-8") as f:
        story = json.load(f)
except:
    st.error("Could not load story.")
    st.stop()

# Progress tracking
if "current_act" not in st.session_state:
    st.session_state.current_act = 0

acts = ["Introduction", "Act 1", "Act 2", "Act 3", "Accusations", "Reveal & Twist"]
current = st.session_state.current_act

st.progress(current / (len(acts) - 1))
st.subheader(f"Phase {current + 1}/6: {acts[current]}")

# Navigation
col1, col2, col3 = st.columns(3)
with col1:
    if st.button("← Previous Phase", use_container_width=True):
        if current > 0:
            st.session_state.current_act -= 1
            st.rerun()
with col2:
    if st.button("Next Phase →", type="primary", use_container_width=True):
        if current < len(acts)-1:
            st.session_state.current_act += 1
            st.rerun()
with col3:
    if st.button("Exit Host Mode", use_container_width=True):
        st.session_state.host_mode = False
        st.rerun()

st.divider()

# PHASE CONTENT
if current == 0:  # Introduction
    st.subheader("Opening")
    st.write(story["description"])
    st.write(story["core_plot"])
    st.info("**Say:** Welcome everyone! Stay in character and enjoy the dinner.")

elif current == 1:  # Act 1
    st.subheader("Act 1")
    clue = story["clues"][0]
    st.write(f"**Clue 1:** {clue['clue_text']}")
    st.caption(clue.get("importance", ""))
    st.info("**Say:** You now have 10-12 minutes to question each other.")

elif current == 2:  # Act 2
    st.subheader("Act 2")
    clue = story["clues"][1]
    st.write(f"**Clue 2:** {clue['clue_text']}")
    st.caption(clue.get("importance", ""))

elif current == 3:  # Act 3
    st.subheader("Act 3")
    clue = story["clues"][2]
    st.write(f"**Clue 3:** {clue['clue_text']}")
    st.caption(clue.get("importance", ""))

elif current == 4:  # Accusations
    st.subheader("Accusation Phase")
    st.write(story["accusation_phase"])

elif current == 5:  # Reveal
    st.subheader("🎭 THE REVEAL")
    murderer_role = game["murderer_role"]
    murderer_name = next((r["default_name"] for r in story["roles"] if r["role_id"] == murderer_role), murderer_role.title())
    
    st.error(f"**THE MURDERER WAS: {murderer_name}**")
    st.write(story["reveal_phase"])
    
    if st.button("Show Final Twist"):
        st.success("**Final Twist:** " + story["twist_ending"])

st.caption("Use the buttons above to advance phases")
