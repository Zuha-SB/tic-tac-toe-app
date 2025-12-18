"""
Core Tic-Tac-Toe game logic.
"""
from typing import List, Optional
import random
import math
from abc import ABC, abstractmethod


class Board:
    """Represents a tic-tac-toe board."""
    
    WINNING_LINES = [
        (0, 1, 2),  # Top row
        (3, 4, 5),  # Middle row
        (6, 7, 8),  # Bottom row
        (0, 3, 6),  # Left column
        (1, 4, 7),  # Middle column
        (2, 5, 8),  # Right column
        (0, 4, 8),  # Diagonal
        (2, 4, 6),  # Anti-diagonal
    ]
    
    def __init__(self, spaces: Optional[List[Optional[str]]] = None):
        self.spaces = spaces if spaces else [None] * 9
    
    def copy(self) -> 'Board':
        return Board(self.spaces.copy())
    
    def get_open_spaces(self) -> List[int]:
        return [i for i, space in enumerate(self.spaces) if space is None]
    
    def is_open_space(self, index: int) -> bool:
        return 0 <= index < 9 and self.spaces[index] is None
    
    def mark_space(self, index: int, mark: str) -> bool:
        if self.is_open_space(index):
            self.spaces[index] = mark
            return True
        return False
    
    def is_full(self) -> bool:
        return all(space is not None for space in self.spaces)
    
    def has_win(self, mark: str) -> bool:
        for line in self.WINNING_LINES:
            if all(self.spaces[i] == mark for i in line):
                return True
        return False
    
    def get_winner(self) -> Optional[str]:
        if self.has_win('X'):
            return 'X'
        if self.has_win('O'):
            return 'O'
        return None
    
    def is_game_over(self) -> bool:
        return self.get_winner() is not None or self.is_full()


class Player(ABC):
    """Abstract base class for all players."""
    
    def __init__(self, mark: str):
        self.mark = mark
        self.opponent_mark = 'O' if mark == 'X' else 'X'
    
    @abstractmethod
    def get_move(self, board: Board) -> int:
        pass
    
    @property
    @abstractmethod
    def name(self) -> str:
        pass
    
    @property
    @abstractmethod
    def difficulty(self) -> int:
        pass


class RandomPlayer(Player):
    """Picks a random valid move. Easiest opponent."""
    
    @property
    def name(self) -> str:
        return "Random"
    
    @property
    def difficulty(self) -> int:
        return 1
    
    def get_move(self, board: Board) -> int:
        return random.choice(board.get_open_spaces())


class GoalPlayer(Player):
    """
    Uses goal-based approach: wins if possible, blocks opponent's win,
    otherwise picks randomly. Easy-Medium difficulty.
    """
    
    @property
    def name(self) -> str:
        return "Goal-Based"
    
    @property
    def difficulty(self) -> int:
        return 2
    
    def get_move(self, board: Board) -> int:
        possible_moves = board.get_open_spaces()
        
        # Check for winning move
        for move in possible_moves:
            test_board = board.copy()
            test_board.mark_space(move, self.mark)
            if test_board.has_win(self.mark):
                return move
        
        # Block opponent's winning move
        for move in possible_moves:
            test_board = board.copy()
            test_board.mark_space(move, self.opponent_mark)
            if test_board.has_win(self.opponent_mark):
                return move
        
        return random.choice(possible_moves)


class UtilityPlayer(Player):
    """
    Uses a utility function to evaluate board positions.
    Medium difficulty.
    """
    
    @property
    def name(self) -> str:
        return "Utility-Based"
    
    @property
    def difficulty(self) -> int:
        return 3
    
    def _get_line_utility(self, board: Board, line: tuple) -> int:
        own_count = sum(1 for i in line if board.spaces[i] == self.mark)
        opp_count = sum(1 for i in line if board.spaces[i] == self.opponent_mark)
        
        utility = 0
        if opp_count == 0:  # Line still winnable for us
            if own_count == 2:
                utility += 3
            elif own_count == 1:
                utility += 1
        if own_count == 0:  # Line still winnable for opponent
            if opp_count == 2:
                utility -= 3
            elif opp_count == 1:
                utility -= 1
        return utility
    
    def _get_utility(self, board: Board) -> int:
        return sum(self._get_line_utility(board, line) for line in Board.WINNING_LINES)
    
    def get_move(self, board: Board) -> int:
        possible_moves = board.get_open_spaces()
        
        # Check for winning move
        for move in possible_moves:
            test_board = board.copy()
            test_board.mark_space(move, self.mark)
            if test_board.has_win(self.mark):
                return move
        
        # Block opponent's winning move
        for move in possible_moves:
            test_board = board.copy()
            test_board.mark_space(move, self.opponent_mark)
            if test_board.has_win(self.opponent_mark):
                return move
        
        # Pick move with highest utility
        best_move = possible_moves[0]
        best_utility = -math.inf
        
        for move in possible_moves:
            test_board = board.copy()
            test_board.mark_space(move, self.mark)
            utility = self._get_utility(test_board)
            if utility > best_utility:
                best_utility = utility
                best_move = move
        
        return best_move


class MinimaxPlayer(Player):
    """
    Uses brute-force minimax algorithm. Hard difficulty - plays optimally.
    """
    
    @property
    def name(self) -> str:
        return "Minimax"
    
    @property
    def difficulty(self) -> int:
        return 4
    
    def get_move(self, board: Board) -> int:
        _, move = self._max_value(board)
        return move
    
    def _max_value(self, state: Board):
        if state.is_game_over():
            return self._utility(state), None
        
        best_value = -math.inf
        best_move = None
        
        for move in state.get_open_spaces():
            new_state = state.copy()
            new_state.mark_space(move, self.mark)
            value, _ = self._min_value(new_state)
            if value > best_value:
                best_value = value
                best_move = move
        
        return best_value, best_move
    
    def _min_value(self, state: Board):
        if state.is_game_over():
            return self._utility(state), None
        
        best_value = math.inf
        best_move = None
        
        for move in state.get_open_spaces():
            new_state = state.copy()
            new_state.mark_space(move, self.opponent_mark)
            value, _ = self._max_value(new_state)
            if value < best_value:
                best_value = value
                best_move = move
        
        return best_value, best_move
    
    def _utility(self, state: Board) -> int:
        if state.has_win(self.mark):
            return 1
        if state.has_win(self.opponent_mark):
            return -1
        return 0


class AlphaBetaPlayer(Player):
    """
    Uses minimax with alpha-beta pruning. Hard difficulty - plays optimally
    but more efficiently than pure minimax.
    """
    
    @property
    def name(self) -> str:
        return "Alpha-Beta"
    
    @property
    def difficulty(self) -> int:
        return 5
    
    def get_move(self, board: Board) -> int:
        _, move = self._max_value(board, -math.inf, math.inf)
        return move
    
    def _max_value(self, state: Board, alpha: float, beta: float):
        if state.is_game_over():
            return self._utility(state), None
        
        best_value = -math.inf
        best_move = None
        
        for move in state.get_open_spaces():
            new_state = state.copy()
            new_state.mark_space(move, self.mark)
            value, _ = self._min_value(new_state, alpha, beta)
            if value > best_value:
                best_value = value
                best_move = move
                alpha = max(alpha, best_value)
            if best_value >= beta:
                return best_value, best_move
        
        return best_value, best_move
    
    def _min_value(self, state: Board, alpha: float, beta: float):
        if state.is_game_over():
            return self._utility(state), None
        
        best_value = math.inf
        best_move = None
        
        for move in state.get_open_spaces():
            new_state = state.copy()
            new_state.mark_space(move, self.opponent_mark)
            value, _ = self._max_value(new_state, alpha, beta)
            if value < best_value:
                best_value = value
                best_move = move
                beta = min(beta, best_value)
            if best_value <= alpha:
                return best_value, best_move
        
        return best_value, best_move
    
    def _utility(self, state: Board) -> int:
        if state.has_win(self.mark):
            return 1
        if state.has_win(self.opponent_mark):
            return -1
        return 0


# Player registry sorted by difficulty
PLAYER_TYPES = {
    'random': RandomPlayer,
    'goal': GoalPlayer,
    'utility': UtilityPlayer,
    'minimax': MinimaxPlayer,
    'alphabeta': AlphaBetaPlayer,
}

def get_player(player_type: str, mark: str) -> Player:
    """Factory function to create a player by type."""
    if player_type not in PLAYER_TYPES:
        raise ValueError(f"Unknown player type: {player_type}")
    return PLAYER_TYPES[player_type](mark)

def get_player_info() -> List[dict]:
    """Get info about all player types, sorted by difficulty."""
    info = []
    for key, cls in PLAYER_TYPES.items():
        instance = cls('X')
        info.append({
            'id': key,
            'name': instance.name,
            'difficulty': instance.difficulty,
        })
    return sorted(info, key=lambda x: x['difficulty'])

