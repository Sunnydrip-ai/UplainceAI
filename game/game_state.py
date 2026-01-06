"""Game state management for Rock-Paper-Scissors-Plus."""

from dataclasses import dataclass, field
from typing import Optional, List
from enum import Enum


class Move(Enum):
    """Valid game moves."""
    ROCK = "rock"
    PAPER = "paper"
    SCISSORS = "scissors"
    BOMB = "bomb"


class RoundResult(Enum):
    """Possible round outcomes."""
    USER_WIN = "user_win"
    BOT_WIN = "bot_win"
    DRAW = "draw"
    INVALID = "invalid"


@dataclass
class RoundHistory:
    """Record of a single round."""
    round_number: int
    user_move: Optional[str]
    bot_move: str
    result: RoundResult
    reason: str


@dataclass
class GameState:
    """Complete game state."""
    round_number: int = 1
    user_score: int = 0
    bot_score: int = 0
    user_bomb_used: bool = False
    bot_bomb_used: bool = False
    rounds_history: List[RoundHistory] = field(default_factory=list)
    game_over: bool = False
    
    def to_dict(self) -> dict:
        """Convert game state to dictionary."""
        return {
            "round_number": self.round_number,
            "user_score": self.user_score,
            "bot_score": self.bot_score,
            "user_bomb_used": self.user_bomb_used,
            "bot_bomb_used": self.bot_bomb_used,
            "rounds_played": len(self.rounds_history),
            "game_over": self.game_over
        }
    
    def get_winner(self) -> str:
        """Determine final game winner."""
        if self.user_score > self.bot_score:
            return "USER WINS"
        elif self.bot_score > self.user_score:
            return "BOT WINS"
        else:
            return "DRAW"
