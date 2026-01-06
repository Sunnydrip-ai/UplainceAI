"""
Flask web application for Rock-Paper-Scissors-Plus
"""

import os
from flask import Flask, render_template, request, jsonify, session
from dotenv import load_dotenv
from agent.referee_agent import RefereeAgent
import secrets

load_dotenv()

app = Flask(__name__)
app.secret_key = secrets.token_hex(16)

# Store game sessions
game_sessions = {}


def get_agent(session_id):
    """Get or create agent for session."""
    if session_id not in game_sessions:
        api_key = os.getenv("HUGGINGFACE_API_KEY")
        game_sessions[session_id] = RefereeAgent(api_key)
    return game_sessions[session_id]


@app.route('/')
def index():
    """Render main game page."""
    if 'session_id' not in session:
        session['session_id'] = secrets.token_hex(8)
    return render_template('index.html')


@app.route('/api/start', methods=['POST'])
def start_game():
    """Start a new game."""
    session_id = session.get('session_id')
    agent = get_agent(session_id)
    
    # Reset game
    agent.reset_game()
    
    return jsonify({
        'message': agent.get_welcome_message(),
        'game_state': agent.game_state.to_dict()
    })


@app.route('/api/move', methods=['POST'])
def make_move():
    """Process a move."""
    session_id = session.get('session_id')
    agent = get_agent(session_id)
    
    data = request.json
    user_move = data.get('move', '')
    
    response = agent.process_move(user_move)
    
    return jsonify({
        'message': response,
        'game_state': agent.game_state.to_dict()
    })


@app.route('/api/reset', methods=['POST'])
def reset_game():
    """Reset the game."""
    session_id = session.get('session_id')
    agent = get_agent(session_id)
    
    message = agent.reset_game()
    
    return jsonify({
        'message': message,
        'game_state': agent.game_state.to_dict()
    })


if __name__ == '__main__':
    app.run(debug=True, port=5000)
