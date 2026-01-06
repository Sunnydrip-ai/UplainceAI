"""AI Referee Agent using Hugging Face."""

import requests
from typing import Optional
from game.game_state import GameState
from agent.tools import GameTools


class RefereeAgent:
    """AI agent that acts as game referee."""
    
    SYSTEM_PROMPT = """You are a friendly game referee for Rock-Paper-Scissors-Plus.

RULES (explain in ≤5 lines):
1. Best of 3 rounds. Valid moves: rock, paper, scissors, bomb
2. bomb beats all moves except bomb. bomb vs bomb = draw
3. Each player can use bomb ONCE per game
4. Invalid input wastes the round
5. Game ends automatically after 3 rounds

YOUR ROLE:
- Validate user moves
- Announce round results clearly
- Track score and rounds
- Keep responses concise and engaging
- Use emojis occasionally 🎮🎯💣

RESPONSE FORMAT:
- Always show: Round #, Moves, Result, Score
- Be encouraging but fair
- Announce winner clearly at game end"""
    
    def __init__(self, api_key: str):
        """Initialize the referee agent."""
        self.api_key = api_key
        self.api_url = "https://api-inference.huggingface.co/models/mistralai/Mistral-7B-Instruct-v0.2"
        self.game_state = GameState()
        self.tools = GameTools(self.game_state)
        self.conversation_history = []
    
    def _call_huggingface(self, prompt: str) -> str:
        """Call Hugging Face API."""
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "inputs": prompt,
            "parameters": {
                "max_new_tokens": 150,
                "temperature": 0.7,
                "top_p": 0.9,
                "return_full_text": False
            }
        }
        
        try:
            response = requests.post(self.api_url, headers=headers, json=payload, timeout=30)
            if response.status_code == 200:
                result = response.json()
                if isinstance(result, list) and len(result) > 0:
                    return result[0].get("generated_text", "").strip()
            return ""
        except Exception as e:
            print(f"API Error: {e}")
            return ""
    
    def get_welcome_message(self) -> str:
        """Generate welcome message with rules."""
        return """🎮 Rock-Paper-Scissors-Plus

Best of 3 rounds • Use 💣 bomb once to beat anything!
Invalid moves waste your round.

Ready? Make your first move!"""
    
    def process_move(self, user_input: str) -> str:
        """
        Process user input and return response.
        
        This handles:
        1. Intent understanding (what did user try?)
        2. Game logic (is it valid? who won?)
        3. Response generation (what to show user?)
        """
        # Check if game is over
        if self.game_state.game_over:
            return "Game is over! Type 'new game' to play again."
        
        # Extract move from input
        user_input_lower = user_input.lower().strip()
        
        # Handle special commands
        if user_input_lower in ["quit", "exit", "stop"]:
            return "Thanks for playing! 👋"
        
        # Validate move
        validation = self.tools.validate_move_tool(user_input_lower)
        
        if not validation["valid"]:
            # Invalid move wastes the round
            response = f"❌ {validation['reason']}\n"
            response += f"Round {self.game_state.round_number} wasted!"
            
            # Still increment round
            self.game_state.round_number += 1
            
            if self.game_state.round_number > 3:
                self.game_state.game_over = True
                response += f"\n\n{self._generate_final_result()}"
            
            return response
        
        # Resolve round
        round_result = self.tools.resolve_round_tool(validation["move"])
        
        # Update game state
        state_update = self.tools.update_game_state_tool(
            round_result["user_move"],
            round_result["bot_move"],
            round_result["result"]
        )
        
        # Generate response
        response = self._format_round_result(round_result, state_update)
        
        return response
    
    def _format_round_result(self, round_result: dict, state_update: dict) -> str:
        """Format round result for display."""
        response = f"🎯 Round {round_result['round_number']}\n"
        response += f"You: {round_result['user_move'].upper()} • Bot: {round_result['bot_move'].upper()}\n\n"
        response += f"{round_result['explanation']}\n\n"
        response += f"Score: {self.game_state.user_score}-{self.game_state.bot_score}"
        
        if self.game_state.game_over:
            response += f"\n\n{self._generate_final_result()}"
        else:
            if not self.game_state.user_bomb_used:
                response += f"\n\n💣 Bomb still available!"
        
        return response
    
    def _generate_final_result(self) -> str:
        """Generate final game result."""
        result = f"🏁 GAME OVER\n\n"
        result += f"Final: {self.game_state.user_score}-{self.game_state.bot_score}\n\n"
        
        winner = self.game_state.get_winner()
        
        if winner == "USER WINS":
            result += "🎉 You Win! Great job!"
        elif winner == "BOT WINS":
            result += "🤖 Bot Wins! Try again?"
        else:
            result += "🤝 Draw! Well played!"
        
        return result
    
    def reset_game(self) -> str:
        """Reset game state for new game."""
        self.game_state = GameState()
        self.tools = GameTools(self.game_state)
        self.conversation_history = []
        return self.get_welcome_message()
