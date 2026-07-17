import streamlit as st
import json
import os
import random
from datetime import datetime
from groq import Groq
from dotenv import load_dotenv
import re

load_dotenv()

# Initialize Groq
groq_key = os.getenv("GROQ_API_KEY") or st.secrets.get("GROQ_API_KEY")
client = Groq(api_key=groq_key) if groq_key else None

st.set_page_config(page_title="Mystery Night AI", page_icon="🔍", layout="wide")

st.title("🔍 Mystery Night AI")
st.subheader("Live Groq AI Host")

# Load stories
@st.cache_data
def load_all_stories():
    stories = {}
    story_folder = "stories"
    if os.path.exists(story_folder):
        for filename in os.listdir(story_folder):
            if filename.endswith(".json"):
                try:
                    with open(f"{story_folder}/{filename}", "r", encoding="utf-8") as f:
                        data = json.load(f)
                        stories[data["story_id"]] = data
                except:
                    pass
    return stories

stories = load_all_stories()

if not stories:
    st.error("No stories found!")
    st.stop()

# Sidebar for game setup
with st.sidebar:
    st.header("Game Setup")
    story_options = {story["title"]: story_id for story_id, story in stories.items()}
    selected_title = st.selectbox("Choose a Mystery Story", options=list(story_options.keys()), key="story_select")

    if selected_title:
        story_id = story_options[selected_title]
        story = stories[story_id]
        
        num_guests = st.number_input("Number of Guests", min_value=6, max_value=12, value=8, key="guest_input")
        
        if st.button("🎲 Generate Game", type="primary", use_container_width=True, key="generate_btn"):
            murderer_role = random.choice(story.get("possible_murderers", []))
            st.session_state.current_game = {
                "game_id": datetime.now().strftime("%Y%m%d_%H%M%S"),
                "story_id": story_id,
                "num_guests": num_guests,
                "murderer_role": murderer_role
            }
            if "host_messages" not in st.session_state:
                st.session_state.host_messages = []
            st.success("✅ Game Created!")

# ====================== MAIN AI HOST ======================
if "current_game" in st.session_state:
    game = st.session_state.current_game
    story = stories[game["story_id"]]
    
    st.title(f"🎤 AI Host - {story['title']}")
    
    # Avatar
    if "crimson" in story["story_id"]:
        avatar = "🏴‍☠️"
        caption = "Pirate Captain"
        rate = 0.95
        pitch = 1.1
    elif "azure" in story["story_id"]:
        avatar = "🚢"
        caption = "Cruise Ship Captain"
        rate = 1.0
        pitch = 0.95
    elif "gallery" in story["story_id"]:
        avatar = "🖼️"
        caption = "Art Gallery Host"
        rate = 0.9
        pitch = 1.2
    elif "smoke" in story["story_id"]:
        avatar = "🚬"
        caption = "1920s Speakeasy Host"
        rate = 1.05
        pitch = 0.9
    else:
        avatar = "🕵️"
        caption = "AI Host"
        rate = 1.0
        pitch = 1.0

    st.markdown(f"""
    <div style="text-align: center; font-size: 110px; margin: 20px 0; animation: speak 0.5s infinite alternate;">
        {avatar}
    </div>
    """, unsafe_allow_html=True)
    st.caption(caption)

    # Auto-play Opening
    if len(st.session_state.get("host_messages", [])) == 0:
        opening = f"Welcome everyone to {story['title']}! I am your AI Host for this evening's thrilling murder mystery. Gather around, dim the lights, and let the investigation begin!"
        st.session_state.host_messages.append({"role": "host", "content": opening})
        
        clean_opening = re.sub(r'\(.*?\)', '', opening).strip()
        st.components.v1.html(f"""
        <script>
            var utterance = new SpeechSynthesisUtterance("{clean_opening.replace('"', '\\"')}");
            utterance.rate = {rate};
            utterance.pitch = {pitch};
            speechSynthesis.speak(utterance);
        </script>
        """, height=0)

    # Display messages
    for i, msg in enumerate(st.session_state.host_messages):
        if msg["role"] == "host":
            clean_text = re.sub(r'\(.*?\)', '', msg['content']).strip()
            st.markdown(f"**🗣️ AI Host:** {msg['content']}")
            if st.button(f"🔊 Speak", key=f"voice_{i}"):
                try:
                    st.components.v1.html(f"""
                    <script>
                        var utterance = new SpeechSynthesisUtterance("{clean_text.replace('"', '\\"')}");
                        utterance.rate = {rate};
                        utterance.pitch = {pitch};
                        speechSynthesis.speak(utterance);
                    </script>
                    """, height=0)
                    st.success("🔊 Speaking...")
                except:
                    st.warning("Voice playback failed.")
        else:
            st.markdown(f"**Guest:** {msg['content']}")

    user_input = st.text_input("What should the AI Host say or answer?", 
                              placeholder="Reveal next clue, answer a question, or give instructions...", 
                              key="user_input")

    if st.button("Send to AI Host", type="primary", key="send_btn"):
        if user_input:
            st.session_state.host_messages.append({"role": "player", "content": user_input})
            
            system_prompt = f"""
You are the dramatic AI Host for '{story['title']}'.

STRICT RULES:
- Speak ONLY the words you would say out loud.
- NEVER use parentheses or stage directions.
- NEVER reveal who the murderer is until the final Reveal phase.

Core Knowledge:
- Plot: {story['core_plot']}
- Victim: {story['victim']}
- Clues: {[c['clue_text'] for c in story['clues']]}
- Twist: {story['twist_ending']}
"""

            try:
                if client:
                    response = client.chat.completions.create(
                        model="llama-3.1-8b-instant",
                        messages=[
                            {"role": "system", "content": system_prompt},
                            {"role": "user", "content": user_input}
                        ],
                        temperature=0.65,
                        max_tokens=350
                    )
                    reply = response.choices[0].message.content.strip()
                else:
                    reply = "The spirits are a bit foggy tonight..."
            except:
                reply = "The spirits are a bit foggy tonight..."

            st.session_state.host_messages.append({"role": "host", "content": reply})
            st.rerun()

    # Phase Control
    st.divider()
    st.subheader("Phase Control")
    if "current_act" not in st.session_state:
        st.session_state.current_act = 0
    acts = ["Introduction", "Act 1", "Act 2", "Act 3", "Accusations", "Reveal"]
    col1, col2 = st.columns(2)
    with col1:
        if st.button("← Previous Phase"):
            if st.session_state.current_act > 0:
                st.session_state.current_act -= 1
                st.rerun()
    with col2:
        if st.button("Next Phase →", type="primary"):
            if st.session_state.current_act < len(acts)-1:
                st.session_state.current_act += 1
                st.rerun()

    st.write(f"**Current Phase:** {acts[st.session_state.current_act]}")

else:
    st.info("👈 Use the sidebar to select a story and generate a game to begin.")

st.caption("Mystery Night AI - Groq + Browser Voice")