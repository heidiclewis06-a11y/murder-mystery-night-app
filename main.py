            if elevenlabs_key and st.button(f"🔊 Play Voice", key=f"play_{i}"):
                try:
                    voice_id = "EXAVITQu4vr4xnSDxMaL"  # Bella voice (very reliable)
                    response = requests.post(
                        f"https://api.elevenlabs.io/v1/text-to-speech/{voice_id}",
                        json={
                            "text": msg['content'],
                            "model_id": "eleven_monolingual_v1"
                        },
                        headers={
                            "Accept": "audio/mpeg",
                            "xi-api-key": elevenlabs_key,
                            "Content-Type": "application/json"
                        }
                    )
                    
                    if response.status_code == 200:
                        st.audio(response.content, format="audio/mp3")
                        st.success("🔊 Playing voice...")
                    else:
                        st.error(f"ElevenLabs Error: {response.status_code}")
                        st.write(response.text[:200])
                except Exception as e:
                    st.error(f"Voice playback failed: {str(e)}")