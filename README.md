# 🎮 Rock-Paper-Scissors-Plus - AI Referee

A conversational Rock-Paper-Scissors game with a twist! Features an AI referee powered by Hugging Face's FREE Inference API (Mistral-7B).

## 🎯 Game Features

- **Best of 3 rounds** - Quick and exciting gameplay
- **Special bomb move** - Use once per game, beats everything!
- **AI Referee** - Powered by Hugging Face Mistral-7B (100% FREE!)
- **Smart validation** - Handles invalid inputs gracefully
- **Clear feedback** - Round-by-round results with emojis
- **Auto-end** - Game ends automatically after 3 rounds

## 📋 Game Rules

1. **Valid moves**: rock, paper, scissors, bomb
2. **bomb** beats all moves except bomb
3. **bomb vs bomb** = draw
4. Each player can use **bomb ONCE** per game
5. Invalid input **wastes the round**
6. Game **auto-ends** after 3 rounds

## 🚀 Quick Start

### Prerequisites

- Python 3.8 or higher
- Free Hugging Face account (no credit card needed!)

### Installation

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Get FREE Hugging Face API Token
# Follow steps below ⬇️

# 3. Create .env file
cp .env.example .env

# 4. Add your token to .env
# Edit .env and add: HUGGINGFACE_API_KEY=hf_your_token_here
```

### Run the Game

**Option 1: Web UI (Recommended)** 🌐
```bash
python app.py
```
Then open: http://localhost:5000

**Option 2: CLI** 💻
```bash
python main.py
```

## 🔑 How to Get Hugging Face API Token (FREE!)

### Step-by-Step Guide:

1. **Create Account** (if you don't have one)
   - Visit: https://huggingface.co/join
   - Sign up with email (NO credit card required!)

2. **Go to Token Settings**
   - Visit: https://huggingface.co/settings/tokens
   - Or: Click your profile → Settings → Access Tokens

3. **Create New Token**
   - Click "New token" button
   - Name it: `rock-paper-scissors` (or any name)
   - Select: **Read** access (that's all you need!)
   - Click "Generate token"

4. **Copy Your Token**
   - Copy the token (starts with `hf_...`)
   - Keep it safe!

5. **Add to .env File**
   ```bash
   # Create .env file
   cp .env.example .env
   
   # Edit .env and add your token:
   HUGGINGFACE_API_KEY=hf_your_token_here
   ```

**That's it! No credit card, no payment, 100% FREE!** 🎉

## 🎮 How to Play

### Web UI (Beautiful Interface) 🌐

1. **Start Server**: `python app.py`
2. **Open Browser**: http://localhost:5000
3. **Click Buttons**: Choose your move!

**Features:**
- 🎨 Beautiful gradient design
- 📱 Mobile responsive
- 🎯 Click-to-play buttons
- 📊 Live score tracking
- 💣 Bomb status indicator
- 🔄 Easy reset button

### CLI (Terminal) 💻

```
🎮 Welcome to Rock-Paper-Scissors-Plus!

RULES:
• Best of 3 rounds
• Moves: rock, paper, scissors, bomb (💣 use once!)
• bomb beats all except bomb
• Invalid input = wasted round
• Game auto-ends after 3 rounds

Let's play! What's your move for Round 1?

> rock

🎯 ROUND 1
========================================
You played: ROCK
Bot played: SCISSORS

Rock beats scissors. You win!

📊 Score: You 1 - 0 Bot

========================================
Round 2 - What's your move? (💣 bomb available!)
```

## 📁 Project Structure

```
rock-paper-scissors-plus/
├── game/
│   ├── __init__.py
│   ├── game_state.py      # Game state management
│   └── game_logic.py      # Core game rules & logic
├── agent/
│   ├── __init__.py
│   ├── tools.py           # ADK tools (validate, resolve, update)
│   └── referee_agent.py   # AI referee agent
├── main.py                # Main game loop
├── requirements.txt       # Python dependencies
├── .env.example          # Environment template
├── .gitignore            # Git ignore rules
└── README.md             # This file
```

## 🛠️ Technical Stack

- **Language**: Python 3.8+
- **AI API**: Hugging Face Inference API
- **AI Model**: Mistral-7B-Instruct-v0.2 (free tier)
- **State Management**: Dataclasses
- **Architecture**: Clean separation of concerns

## 🏗️ Architecture

### 1. Intent Understanding
- Parse user input
- Extract move from natural language
- Handle special commands (quit, new game)

### 2. Game Logic (`game/game_logic.py`)
- Validate moves
- Resolve rounds (who wins?)
- Update game state
- Check game-over conditions

### 3. Response Generation (`agent/referee_agent.py`)
- Format round results
- Generate clear feedback
- Show scores and status
- Announce final winner

### Tools (Required by Assignment)

1. **`validate_move_tool`** - Validates if move is legal
2. **`resolve_round_tool`** - Determines round winner
3. **`update_game_state_tool`** - Mutates game state (explicit tool)
4. **`get_game_status_tool`** - Returns current status

## 🎯 Assignment Requirements Met

✅ **Python** - Pure Python implementation  
✅ **Free API** - Hugging Face (no credit card!)  
✅ **Explicit Tools** - 4 tools defined (validate, resolve, update, status)  
✅ **State Management** - State persists across turns (not in prompt)  
✅ **Clean Architecture** - Separated intent/logic/response  
✅ **Rule Enforcement** - All game rules implemented  
✅ **Error Handling** - Graceful handling of invalid inputs  
✅ **Auto-end** - Game ends after 3 rounds  
✅ **Clear Output** - Round-by-round feedback with scores  

## 💰 Why Hugging Face?

- **100% FREE** - No credit card required
- **No rate limits** - Generous free tier
- **Powerful AI** - Mistral-7B is excellent for conversations
- **Easy setup** - Just create account and get token
- **Open Source** - Community-driven models

## 🎮 Commands

- Type your move: `rock`, `paper`, `scissors`, `bomb`
- New game: `new game`, `restart`, `reset`
- Quit: `quit`, `exit`, `bye`

## 🔧 Troubleshooting

### "HUGGINGFACE_API_KEY not found"
```bash
# Make sure .env file exists
cp .env.example .env

# Edit .env and add your token
# HUGGINGFACE_API_KEY=hf_your_token_here
```

### "Module not found"
```bash
pip install -r requirements.txt
```

### "API Error" or "Model loading"
- First request may take 20-30 seconds (model cold start)
- This is normal for free tier!
- Subsequent requests will be faster
- Check your token at: https://huggingface.co/settings/tokens

### "Permission denied"
```bash
chmod +x main.py
python main.py
```

## 📝 Game Logic Details

### Move Resolution

```python
# bomb beats all except bomb
bomb vs rock/paper/scissors → bomb wins
bomb vs bomb → draw

# Standard rules
rock beats scissors
scissors beats paper
paper beats rock
same vs same → draw
```

### State Tracking

- Round number (1-3)
- User score
- Bot score
- Bomb usage (user & bot)
- Round history
- Game over flag

## 🚀 Running the Game

```bash
# Simple run
python main.py

# With virtual environment (recommended)
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
python main.py
```

## 🔒 Security Notes

- API token stored in `.env` (not committed to git)
- No external APIs except Hugging Face
- No database required
- No long-running servers
- Simple CLI interface

## 📄 License

MIT License - Feel free to use and modify!

## 🎯 Next Steps

1. Get your FREE Hugging Face token
2. Install dependencies
3. Configure `.env` file
4. Run and play the game!
5. Review the code architecture
6. Try modifying game rules

Enjoy the game! 🎮🎯💣
