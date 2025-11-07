"""Streamlit Chat Application with WebSocket LLM Backend
This application provides a chat interface that communicates with an LLMvia WebSocket connections. Messages are sent to AWS API Gateway and responsesare received asynchronously through a background thread."""

import streamlit as st
import json
import websocket
import logging
import threading
import time
from queue import Queue, Empty

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# ============================================================================
# SESSION STATE INITIALIZATION
# ============================================================================

# Store conversation history
if 'messages' not in st.session_state:
    st.session_state.messages = []

# Track if we're waiting for an LLM response
if 'waiting_for_response' not in st.session_state:
    st.session_state.waiting_for_response = False

# ============================================================================
# WEBSOCKET SETUP
# ============================================================================

@st.cache_resource
def init_websocket():
    """    Initialize WebSocket connection and response queue.
    Uses @st.cache_resource to maintain a single persistent connection    across Streamlit reruns. The queue enables thread-safe communication    between the WebSocket background thread and Streamlit's main thread.
    Returns:        tuple: (WebSocket connection, Queue for responses)    """
    response_queue = Queue()

    # WebSocket event handlers
    def on_message(ws, message):
        """Handle incoming messages from the WebSocket"""
        try:
            response = json.loads(message)

            # Only process content chunks (ignore end/status messages)
            if response.get('type') == 'chunk':
                content = response.get('content', '')
                response_queue.put(content)
                logger.info(f"Received response ({len(content)} chars)")
        except Exception as e:
            logger.error(f"Error processing message: {e}")

    def on_error(ws, error):
        """Handle WebSocket errors"""
        logger.error(f"WebSocket error: {error}")

    def on_close(ws, close_status_code, close_msg):
        """Handle WebSocket disconnection"""
        logger.warning(f"WebSocket closed: {close_status_code}")

    def on_open(ws):
        """Handle successful WebSocket connection"""
        logger.info("WebSocket connected")

    # Create WebSocket connection (use your API Gateway URL)
    ws = websocket.WebSocketApp(
        "wss://p1z2w9z8ph.execute-api.us-east-1.amazonaws.com/production/",
        on_message=on_message,
        on_error=on_error,
        on_close=on_close,
        on_open=on_open    )

    # Run WebSocket in background daemon thread
    wst = threading.Thread(target=ws.run_forever)
    wst.daemon = True
    wst.start()

    return ws, response_queue
# Initialize WebSocket connection (only runs once)
if "ws" not in st.session_state:
    st.session_state.ws, st.session_state.response_queue = init_websocket()

# ============================================================================
# RESPONSE HANDLING
# ============================================================================

# Get response queue reference
response_queue = st.session_state.response_queue
# Check if a response has arrived while we're waiting
if st.session_state.waiting_for_response:
    try:
        # Non-blocking check for response in queue
        current_response = response_queue.get_nowait()

        # Add assistant's response to conversation history
        st.session_state.messages.append({
            "role": "assistant",
            "content": current_response        })

        # Stop waiting
        st.session_state.waiting_for_response = False
        logger.info("Response received and added to chat")

    except Empty:
        # No response yet, continue waiting
        pass

# ============================================================================
# UI RENDERING
# ============================================================================

st.title("Chat with League LLM")

# Display conversation history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Show "Thinking..." indicator while waiting for response
if st.session_state.waiting_for_response:
    with st.chat_message("assistant"):
        st.write("Thinking...")

    # Poll every 0.5 seconds to check for new responses
    time.sleep(0.5)
    st.rerun()

# ============================================================================
# USER INPUT HANDLING
# ============================================================================

# Handle new user messages
if prompt := st.chat_input("What would you like to know?"):
    logger.info(f"User sent: {prompt}")

    # Add user message to conversation history
    st.session_state.messages.append({
        "role": "user",
        "content": prompt    })

    # Clear any stale responses from the queue
    while not response_queue.empty():
        try:
            response_queue.get_nowait()
        except Empty:
            break

    # Prepare message payload with full conversation context
    message_data = {
        "messages": [
            {"role": m["role"], "content": m["content"]}
            for m in st.session_state.messages        ]
    }

    # Send message to LLM via WebSocket
    st.session_state.ws.send(json.dumps(message_data))

    # Set waiting state and refresh UI
    st.session_state.waiting_for_response = True
    st.rerun()