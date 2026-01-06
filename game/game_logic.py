"""Core game logic for Rock-Paper-Scissors-Plus."""

import random
from typing import Tuple
from .game_state import GameState, Move, RoundResult, RoundHistory


class GameLogic:
    """Handles all game rules and logic."""
    
    VALID_MOVES = ["rock", "paper", "scissors", "bomb"]
    MAX_ROUNDS = 3
    
    @staticmethod
    def validate_move(move: str, game_state: GameState) -> Tuple[bool, str]:
        """
        Validate if a move is legal.
        
        Returns:
            (is_valid, reason)
        """
        move = move.lower().strip()
        
        if move not in GameLogic.VALID_MOVES:
            return False, f"Invalid move. Choose: rock, paper, scissors, or bomb"
        
        if move == "bomb" and game_state.user_bomb_used:
            return False, "Bomb already used!"
        
        return True, "Valid move"
    
    @staticmethod
    def get_bot_move(game_state: GameState) -> str:
        """
        Decide bot's move based on game state.
        
        Strategy:
        - Use bomb strategically (not in first round)
        - Random otherwise
        """
        available_moves = ["rock", "paper", "scissors"]
        
        # Bot uses bomb strategically
        if not game_state.bot_bomb_used and game_state.round_number > 1:
            # 30% chance to use bomb if not used yet
            if random.random() < 0.3:
                return "bomb"
        
        return random.choice(available_moves)
    
    @staticmethod
    def resolve_round(user_move: str, bot_move: str) -> RoundResult:
        """
        Determine round winner based on moves.
        
        Rules:
        - bomb beats everything except bomb
        - bomb vs bomb = draw
        - rock beats scissors
        - scissors beats paper
        - paper beats rock
        """
        user_move = user_move.lower()
        bot_move = bot_move.lower()
        
        # Handle bomb cases
        if user_move == "bomb" and bot_move == "bomb":
            return RoundResult.DRAW
        if user_move == "bomb":
            return RoundResult.USER_WIN
        if bot_move == "bomb":
            return RoundResult.BOT_WIN
        
        # Handle regular moves
        if user_move == bot_move:
            return RoundResult.DRAW
        
        winning_combinations = {
            ("rock", "scissors"),
            ("scissors", "paper"),
            ("paper", "rock")
        }
        
        if (user_move, bot_move) in winning_combinations:
            return RoundResult.USER_WIN
        else:
            return RoundResult.BOT_WIN
    
    @staticmethod
    def get_result_explanation(user_move: str, bot_move: str, result: RoundResult) -> str:
        """Generate human-readable explanation of round result."""
        if result == RoundResult.DRAW:
            return f"Both chose {user_move}. Draw!"
        
        if result == RoundResult.USER_WIN:
            if user_move == "bomb":
                return f"💣 Bomb destroys {bot_move}!"
            return f"{user_move.capitalize()} beats {bot_move}!"
        
        if result == RoundResult.BOT_WIN:
            if bot_move == "bomb":
                return f"💣 Bot's bomb destroys {user_move}!"
            return f"{bot_move.capitalize()} beats {user_move}!"
        
        return "Invalid round"
    
    @staticmethod
    def update_game_state(
        game_state: GameState,
        user_move: str,
        bot_move: str,
        result: RoundResult
    ) -> GameState:
        """
        Update game state after a round.
        
        This is the explicit tool function required by the assignment.
        """
        # Update bomb usage
        if user_move.lower() == "bomb":
            game_state.user_bomb_used = True
        if bot_move.lower() == "bomb":
            game_state.bot_bomb_used = True
        
        # Update scores
        if result == RoundResult.USER_WIN:
            game_state.user_score += 1
        elif result == RoundResult.BOT_WIN:
            game_state.bot_score += 1
        
        # Add to history
        explanation = GameLogic.get_result_explanation(user_move, bot_move, result)
        round_record = RoundHistory(
            round_number=game_state.round_number,
            user_move=user_move,
            bot_move=bot_move,
            result=result,
            reason=explanation
        )
        game_state.rounds_history.append(round_record)
        
        # Increment round
        game_state.round_number += 1
        
        # Check if game is over
        if game_state.round_number > GameLogic.MAX_ROUNDS:
            game_state.game_over = True
        
        return game_state
