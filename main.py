# ====================== LIVE AI HOST MODE ======================
if "current_game" in st.session_state:
    if st.button("🎤 Launch Live AI Host", type="primary", use_container_width=True):
        st.session_state.host_mode = True
        if "host_messages" not in st.session_state:
            st.session_state.host_messages = []
            initial = f"Welcome, everyone! I am your AI Host for tonight's thrilling mystery: {stories[st.session_state.current_game['story_id']]['title']}. Let the investigation begin!"
            st.session_state.host_messages.append({"role": "host", "content": initial})

if st.session_state.get("host_mode", False):
    game = st.session_state.current_game
    story = stories[game["story_id"]]
    
    st.title(f"🎤 Live AI Host - {story['title']}")
    
    # Display conversation history
    for msg in st.session_state.host_messages:
        if msg["role"] == "host":
            st.markdown(f"**🗣️ AI Host:** {msg['content']}")
        else:
            st.markdown(f"**Guest:** {msg['content']}")

    # Navigation
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Next Phase", type="primary"):
            if "current_act" not in st.session_state:
                st.session_state.current_act = 0
            st.session_state.current_act = min(st.session_state.current_act + 1, 5)
            st.rerun()
    with col2:
        if st.button("Reset Conversation"):
            st.session_state.host_messages = []
            st.rerun()

    # AI Input
    user_input = st.text_input("What should the AI Host say or answer?", 
                              placeholder="Welcome guests, reveal next clue, or answer a player's question...")

    if st.button("Send to AI Host", type="primary"):
        if user_input:
            st.session_state.host_messages.append({"role": "player", "content": user_input})
            
            # Strong system prompt for consistency
            system_prompt = f"""
You are the official dramatic AI Host for the murder mystery '{story['title']}'.
Stay completely in character. Speak theatrically and immersively.

Core Knowledge (Never contradict these):
- Plot: {story['core_plot']}
- Victim: {story['victim']}
- Clues revealed so far: {[c['clue_text'] for c in story['clues']]}
- Twist Ending: {story['twist_ending']}

Rules:
- Never invent new clues or plot details.
- Never reveal who the murderer is until the final reveal phase.
- If asked about unknown information, respond mysteriously in character.
- Be fun, engaging, and theatrical.
"""

            try:
                response = client.chat.completions.create(
                    model="gpt-4o-mini",
                    messages=[
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": user_input}
                    ],
                    temperature=0.75,
                    max_tokens=400
                )
                reply = response.choices[0].message.content.strip()
            except:
                reply = "The spirits are a bit foggy tonight... Could you repeat that, my dear guest?"

            st.session_state.host_messages.append({"role": "host", "content": reply})
            st.rerun()
