"""ADK tools for game management."""

from typing import Dict, Any
from game.game_state import GameState
from game.game_logic import GameLogic


class GameTools:
    """Collection of tools for the AI agent."""
    
    def __init__(self, game_state: GameState):
        self.game_state = game_state
        self.game_logic = GameLogic()
    
    def validate_move_tool(self, move: str) -> Dict[str, Any]:
        """
        Tool: Validate if a move is legal.
        
        Args:
            move: The move to validate
            
        Returns:
            Dictionary with validation result
        """
        is_valid, reason = self.game_logic.validate_move(move, self.game_state)
        
        return {
            "valid": is_valid,
            "reason": reason,
            "move": move.lower() if is_valid else None
        }
    
    def resolve_round_tool(self, user_move: str) -> Dict[str, Any]:
        """
        Tool: Resolve a complete round.
        
        Args:
            user_move: The user's move
            
        Returns:
            Dictionary with round results
        """
        # Get bot move
        bot_move = self.game_logic.get_bot_move(self.game_state)
        
        # Resolve round
        result = self.game_logic.resolve_round(user_move, bot_move)
        
        # Get explanation
        explanation = self.game_logic.get_result_explanation(user_move, bot_move, result)
        
        return {
            "user_move": user_move,
            "bot_move": bot_move,
            "result": result.value,
            "explanation": explanation,
            "round_number": self.game_state.round_number
        }
    
    def update_game_state_tool(
        self,
        user_move: str,
        bot_move: str,
        result_value: str
    ) -> Dict[str, Any]:
        """
        Tool: Update game state after a round.
        
        This is the explicit state mutation tool required by the assignment.
        
        Args:
            user_move: User's move
            bot_move: Bot's move
            result_value: Result as string
            
        Returns:
            Updated game state as dictionary
        """
        from game.game_state import RoundResult
        
        # Convert string result to enum
        result = RoundResult(result_value)
        
        # Update state
        self.game_state = self.game_logic.update_game_state(
            self.game_state,
            user_move,
            bot_move,
            result
        )
        
        return {
            "game_state": self.game_state.to_dict(),
            "game_over": self.game_state.game_over,
            "winner": self.game_state.get_winner() if self.game_state.game_over else None
        }
    
    def get_game_status_tool(self) -> Dict[str, Any]:
        """
        Tool: Get current game status.
        
        Returns:
            Current game state information
        """
        return {
            "round": self.game_state.round_number,
            "score": f"{self.game_state.user_score}-{self.game_state.bot_score}",
            "user_bomb_available": not self.game_state.user_bomb_used,
            "game_over": self.game_state.game_over
        }
