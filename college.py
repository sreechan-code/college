import streamlit as st
import google.generativeai as genai

# Configure the API key directly
genai.configure(api_key="AIzaSyBN9ZlpzLLoHklPYo7d_7y7Uw9UW1wlE9E")

# Function to load the Gemini Pro model and get a response
model = genai.GenerativeModel("gemini-pro")
chat = model.start_chat(history=[])

def get_gemini_response(question):
    # Request a response without max_tokens or temperature, as they are unsupported
    response = chat.send_message(question, stream=True)
    return response

# Streamlit app setup with page title and header styling
st.set_page_config(page_title="College Enquiry Chatbot", page_icon="🎓")
st.markdown(
    """
    <style>
    /* Custom image positioning */
    .top-image {
        position: absolute;
        top: 20px;
        left: 20px;
        z-index: 10;
    }

    /* Chatbot container styling */
    .chat-container {
        max-width: 800px;
        margin: auto;
        padding: 20px;
        border-radius: 10px;
        background-color: #F8F9FA;
        margin-top: 100px; /* Adjust for the header space */
    }

    /* Message bubbles */
    .user-message, .bot-message {
        padding: 10px 15px;
        border-radius: 10px;
        margin: 10px 0;
        max-width: 75%;
        font-size: 16px;
    }
    .user-message {
        background-color: #DCF8C6;
        align-self: flex-end;
        text-align: right;
    }
    .bot-message {
        background-color: #E8EAF6;
        align-self: flex-start;
        text-align: left;
    }

    /* Button styling */
    .stButton>button {
        background-color: #4CAF50;
        color: white;
        padding: 10px 24px;
        font-size: 16px;
        border: none;
        border-radius: 5px;
    }

    /* General styling */
    body {
        background-color: #F0F2F6;
        font-family: Arial, sans-serif;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Display the image at the top-left corner
st.markdown('<div class="top-image">', unsafe_allow_html=True)
st.image("image.png", width=350)  # Adjust the width as needed
st.markdown('</div>', unsafe_allow_html=True)

# Chatbot container with background and header
st.markdown("<div class='chat-container'>", unsafe_allow_html=True)
st.header("🎓 College Inquiry Chatbot")

# Initialize session state for chat history if it does not exist
if 'chat_history' not in st.session_state:
    st.session_state['chat_history'] = []

# Input and button for submitting questions
input_text = st.text_input("Ask about our college programs, admissions, or campus life:")
submit = st.button("ASK THE QUESTION")

# Clear chat button
clear_chat = st.button("Clear Chat")
if clear_chat:
    st.session_state['chat_history'] = []

# Display chat history
for role, text in st.session_state['chat_history']:
    bubble_class = "user-message" if role == "You" else "bot-message"
    st.markdown(f"<div class='{bubble_class}'>{role}: {text}</div>", unsafe_allow_html=True)

# Handle user input and bot response
if submit and input_text:
    # Add user's question to chat history
    st.session_state['chat_history'].append(("You", input_text))
    
    # Get the response from the bot
    response = get_gemini_response(input_text)
    bot_response_text = ""
    
    # Collect the bot's response and add it to the chat history
    if response:
        for chunk in response:
            if hasattr(chunk, 'text') and chunk.text:
                bot_response_text += chunk.text
        st.session_state['chat_history'].append(("Bot", bot_response_text))
    else:
        bot_response_text = "I couldn't find a response. Please try asking about admissions, courses, or campus life."
        st.session_state['chat_history'].append(("Bot", bot_response_text))

# Display end of chat container div
st.markdown("</div>", unsafe_allow_html=True)
