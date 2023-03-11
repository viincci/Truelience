from flask import Flask, request, jsonify
import uuid

app = Flask(__name__)

# The API key that Trulience will use to authenticate with your endpoint
REST_AGENT_API_KEY = 'my-api-key-will-die-to-live-13-17-21'

# In-memory session store to map Trulience session IDs to session data
session_store = {}


@app.route('/api/session', methods=['POST'])
def create_session():
    # Validate the REST Agent API Key
    if request.headers.get('Authorization') != REST_AGENT_API_KEY:
        return jsonify({'status': 'FAIL', 'statusMessage': 'Unauthorized'}), 401

    # Create a new session ID and store it in the session store
    session_id = str(uuid.uuid4())
    session_store[session_id] = {'userId': request.json.get('userId'), 'locale': request.json.get('locale')}

    # Return the session ID to Trulience
    return jsonify({'sessionId': session_id, 'status': 'OK', 'statusMessage': 'Session Created'})


@app.route('/api/chat', methods=['POST'])
def handle_chat_message():
    # Validate the REST Agent API Key
    if request.headers.get('Authorization') != REST_AGENT_API_KEY:
        return jsonify({'status': 'FAIL', 'statusMessage': 'Unauthorized'}), 401

    # Retrieve the session ID from the request
    session_id = request.json.get('sessionId')

    # Look up the session data in the session store
    session_data = session_store.get(session_id)
    if session_data is None:
        return jsonify({'status': 'FAIL', 'statusMessage': 'Session Not Found'}), 404

    # Echo back the user's message as a reply
    reply = request.json.get('message')

    # Return the reply to Trulience
    return jsonify({'sessionId': session_id, 'reply': reply, 'status': 'OK', 'statusMessage': 'Reply Sent'})


if __name__ == '__main__':
    app.run(ssl_context='adhoc', debug=True)
