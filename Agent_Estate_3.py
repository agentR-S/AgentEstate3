import streamlit as st
import requests
import json
import time

# Set up your Azure and OpenAI credentials
openai_api_key = "F4w0ncKnEKn54ox577yHf11Cn3fil3qP4RYl6DGizFGglot7Fv6hJQQJ99AJACYeBjFXJ3w3AAABACOGCl1Q"  # Replace with your actual OpenAI API key
azure_stt_key = "9Q1WW4Yq1xT02vn0cfPcoVAebOzXVovl3kpWYsoDZrlkbQaG7e5DJQQJ99AKACYeBjFXJ3w3AAAAACOGjlBy"  # Replace with your actual Azure Speech-to-Text API key
openai_endpoint = "https://agenta.openai.azure.com/"  # Replace with your actual OpenAI endpoint
azure_stt_endpoint = "https://eastus.stt.speech.microsoft.com"

# Define headers for the APIs
openai_headers = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {openai_api_key}"
}
azure_stt_headers = {
    "Ocp-Apim-Subscription-Key": azure_stt_key,
    "Content-Type": "audio/wav"
}

# Define the system prompt (agent characteristics and cultural contingencies)
system_prompt = """
You are an AI agent acting as a landlord in a rental negotiation.
You represent European cultural traits like professionalism, fairness, and collaboration. 
You prioritize long-term commitments and ensure timely payments. 
You are firm on rental prices but open to negotiation, as long as they don't compromise the financial stability of the landlord.
Communicate in a polite but assertive manner, aiming for a win-win outcome while ensuring the landlord's interests are protected.
"""

# Initialize conversation history
if "conversation" not in st.session_state:
    st.session_state.conversation = [{"role": "system", "content": system_prompt}]

# Function to transcribe audio using Azure Speech-to-Text
def transcribe_audio(audio_file):
    files = {"audio": ("audio.wav", audio_file, "audio/wav")}
    response = requests.post(azure_stt_endpoint, headers=azure_stt_headers, files=files, params={"language": "en-US"})
    if response.status_code == 200:
        result = response.json()
        return result.get("DisplayText", "")
    else:
        return f"Error: {response.status_code} - {response.text}"

# Function to get a response from OpenAI API
def get_openai_response(messages):
    data = {
        "messages": messages,
        "max_tokens": 150
    }
    response = requests.post(f"{openai_endpoint}/v1/chat/completions", headers=openai_headers, json=data)
    if response.status_code == 200:
        result = response.json()
        return result['choices'][0]['message']['content'].strip()
    else:
        return f"Error: {response.status_code} - {response.text}"

# Streamlit interface
st.title("AI Negotiation Assistant")

# Option to upload audio for transcription
st.header("Upload Audio for Transcription")
audio_file = st.file_uploader("Upload an audio file (WAV format)", type=["wav"])
if audio_file is not None:
    st.write("Transcribing audio...")
    transcription = transcribe_audio(audio_file)
    st.write("Transcription:", transcription)
    st.session_state.conversation.append({"role": "user", "content": transcription})

# Real-time transcription button
if "listening" not in st.session_state:
    st.session_state.listening = False

def start_listening():
    st.session_state.listening = True
    st.write("Listening for real-time transcription...")

    # Assuming we have pre-recorded audio chunks to simulate real-time transcription
    # Here, you'd normally capture audio in real-time
    for _ in range(3):  # Simulating 3 audio chunks
        st.write("Processing next audio chunk...")
        time.sleep(1)  # Simulate delay for capturing audio
        # Replace this with actual audio capture code in a real-time application
        transcription = "Simulated audio transcription chunk."
        st.session_state.conversation.append({"role": "user", "content": transcription})
        ai_response = get_openai_response(st.session_state.conversation)
        st.session_state.conversation.append({"role": "assistant", "content": ai_response})
        st.write(f"AI: {ai_response}")

# Real-time transcription control
if st.button("Start Real-Time Transcription"):
    start_listening()

# Text input for user message
st.header("Chat with the AI Negotiator")
user_input = st.text_input("You:", placeholder="Write your message here...")
if user_input:
    st.session_state.conversation.append({"role": "user", "content": user_input})
    # Get the AI response
    ai_response = get_openai_response(st.session_state.conversation)
    st.session_state.conversation.append({"role": "assistant", "content": ai_response})
    st.write(f"AI: {ai_response}")

# Display conversation history
st.header("Conversation History")
for message in st.session_state.conversation:
    role = "You" if message["role"] == "user" else "AI"
    st.write(f"{role}: {message['content']}")

# Button to ask for negotiation status
if st.button("Ask for Negotiation Status"):
    status_query = {"role": "user", "content": "Can you tell me the current status of the negotiation?"}
    st.session_state.conversation.append(status_query)
    # Get status response from the agent
    status_response = get_openai_response(st.session_state.conversation)
    st.session_state.conversation.append({"role": "assistant", "content": status_response})
    st.write(f"AI (Negotiation Status): {status_response}")

# Button to ask for suggestions
if st.button("Ask for Suggestions"):
    suggestion_query = {"role": "user", "content": "Can you provide some suggestions for the negotiation?"}
    st.session_state.conversation.append(suggestion_query)
    # Get suggestion response from the agent
    suggestion_response = get_openai_response(st.session_state.conversation)
    st.session_state.conversation.append({"role": "assistant", "content": suggestion_response})
    st.write(f"AI (Suggestions): {suggestion_response}")
