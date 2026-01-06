# 🎮 Rock-Paper-Scissors-Plus - AI Referee

An AI-powered game referee that manages Rock-Paper-Scissors with a special "bomb" move. Built with Python, Flask, and Hugging Face's free API.

## 🚀 Quick Start

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Get FREE Hugging Face token
# Visit: https://huggingface.co/settings/tokens
# Create token with "read" access

# 3. Configure
cp .env.example .env
# Add: HUGGINGFACE_API_KEY=hf_your_token_here

# 4. Run
python app.py
# Open: http://localhost:5000
```

## 🎯 Game Rules

- Best of 3 rounds
- Moves: rock, paper, scissors, bomb
- Bomb beats everything (use once!)
- Invalid moves waste your round

---

## 📋 Technical Design

### State Model

I kept state management simple and explicit. The `GameState` dataclass tracks everything:

```python
@dataclass
class GameState:
    round_number: int = 1          # Current round (1-3)
    user_score: int = 0            # Wins for user
    bot_score: int = 0             # Wins for bot
    user_bomb_used: bool = False   # Bomb tracking
    bot_bomb_used: bool = False    
    rounds_history: List = []      # Complete game history
    game_over: bool = False        # End condition
```

**Why this works:**
- State lives in memory (no database needed)
- Easy to serialize for API responses
- Clear separation from game logic
- Simple to test and debug

### Agent & Tool Design

I separated concerns into three layers:

**1. Game Logic (`game/game_logic.py`)**
- Pure functions for rules
- No side effects
- Easy to test

**2. Tools (`agent/tools.py`)**
- Four explicit tools as required:
  - `validate_move_tool` - Checks if move is legal
  - `resolve_round_tool` - Determines winner
  - `update_game_state_tool` - Mutates state (the key tool!)
  - `get_game_status_tool` - Returns current status

**3. Referee Agent (`agent/referee_agent.py`)**
- Orchestrates everything
- Handles user intent
- Generates responses
- Manages conversation flow

**Why this architecture:**
- Clear responsibilities
- Easy to extend (add new moves, rules)
- Tools can be tested independently
- Agent focuses on conversation, not logic

### Tradeoffs I Made

**1. Hugging Face over Google Gemini**
- Pro: 100% free, no credit card
- Con: First request is slow (model cold start)
- Decision: Worth it for accessibility

**2. In-memory state vs Database**
- Pro: Simple, fast, no setup
- Con: State lost on server restart
- Decision: Fine for demo, would add Redis for production

**3. Minimal AI usage**
- Pro: Game works even if AI is slow
- Con: Less "conversational" feel
- Decision: Reliability > fancy responses

**4. Flask over FastAPI**
- Pro: Simpler, more familiar
- Con: Less modern, no async
- Decision: Easier for others to understand

**5. Compact UI**
- Pro: More chat visible
- Con: Smaller buttons on mobile
- Decision: Chat is the main feature

### What I'd Improve With More Time

**Short term (1-2 days):**
- Add sound effects for moves
- Animate round results
- Add game statistics/history
- Better error handling for API failures
- Add loading indicators

**Medium term (1 week):**
- Multiplayer support (2 human players)
- Tournament mode (best of 5, 7)
- Difficulty levels for bot
- Persistent leaderboard
- More special moves (shield, mirror, etc.)

**Long term (2+ weeks):**
- Voice input/output
- Mobile app (React Native)
- Real-time multiplayer with WebSockets
- AI that learns your patterns
- Custom game modes
- Social features (share results, challenges)

---

## 🛠️ Tech Stack

- **Backend**: Python 3.8+, Flask
- **AI**: Hugging Face (Mistral-7B-Instruct)
- **Frontend**: Vanilla JS, HTML5, CSS3
- **State**: In-memory dataclasses
- **Font**: Space Grotesk (modern, tech-inspired)

## 📁 Project Structure

```
├── game/              # Core game logic
│   ├── game_state.py  # State management
│   └── game_logic.py  # Rules & validation
├── agent/             # AI referee
│   ├── tools.py       # 4 explicit tools
│   └── referee_agent.py  # Orchestration
├── static/            # Frontend assets
│   ├── style.css      # Dark theme UI
│   └── script.js      # Interactive features
├── templates/         # HTML
│   └── index.html     # Main page
├── app.py            # Flask server
└── main.py           # CLI version
```

## 🎨 Design Choices

**Color Scheme:**
- Black/off-white for readability
- Neon green (#00ff88) for accents
- Cyberpunk-inspired aesthetic

**UX Decisions:**
- Fullscreen layout (maximize chat)
- All 4 buttons in one row
- Compact info cards
- Clear AI/user message distinction
- Help button for first-time users

## 🧪 Testing

```bash
# Run the game
python app.py

# Test scenarios:
# 1. Valid moves (rock, paper, scissors, bomb)
# 2. Invalid moves (should waste round)
# 3. Using bomb twice (should reject)
# 4. All 3 rounds (should auto-end)
# 5. Help button (should show rules)
```

## 📝 Notes

This was built as an assignment to demonstrate:
- Clean architecture
- State management
- Tool-based agent design
- Error handling
- User experience

The focus was on **reliability and clarity** over fancy features. Every decision prioritized making the code easy to understand and extend.

## 📄 License

MIT - Feel free to use and modify!

---

Built with ☕ and 🎮 for the Upliance.ai assignment
