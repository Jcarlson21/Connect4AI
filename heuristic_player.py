"""
Heuristic Player for Connect4

This module implements a heuristic-based AI player for Connect4 that uses a weighted
scoring system to evaluate board positions and choose optimal moves.

The heuristic evaluates:
- Immediate winning opportunities (4 in a row)
- Three-in-a-row threats with one empty space
- Two-in-a-row opportunities with two empty spaces
- Center control bonus
- Opponent threat assessment
"""

import random
import copy
from player import Player

class HeuristicPlayer(Player):
    """A Connect Four player using an optimized heuristic for board evaluation."""
    
    def __init__(self, piece):
        super().__init__(piece)
        self.winning_lines = self._generate_winning_lines()
        self.weights = {
            'my_four': 1000000,    # Immediate win
            'my_three': 10000,     # Three with one empty
            'my_two': 200,         # Two with two empty
            'opp_four': -1000000,  # Immediate loss
            'opp_three': -15000,   # Opponent's three
            'opp_two': -300,       # Opponent's two
            'center_bonus': 8      # Center control
        }

    def _generate_winning_lines(self):
        """Generate all possible winning lines on a 6x7 board."""
        lines = []
        for r in range(6):  # Horizontal
            for c in range(4):
                lines.append([(r, c), (r, c+1), (r, c+2), (r, c+3)])
        for c in range(7):  # Vertical
            for r in range(3):
                lines.append([(r, c), (r+1, c), (r+2, c), (r+3, c)])
        for r in range(3):  # Diagonal /
            for c in range(4):
                lines.append([(r, c), (r+1, c+1), (r+2, c+2), (r+3, c+3)])
        for r in range(3, 6):  # Diagonal \
            for c in range(4):
                lines.append([(r, c), (r-1, c+1), (r-2, c+2), (r-3, c+3)])
        return lines

    def _score_pattern(self, my_count, opp_count, empty_count):
        """Calculate score for a line pattern based on piece counts."""
        if my_count and not opp_count:
            if my_count == 4: return self.weights['my_four']
            if my_count == 3 and empty_count == 1: return self.weights['my_three']
            if my_count == 2 and empty_count == 2: return self.weights['my_two']
        elif opp_count and not my_count:
            if opp_count == 4: return self.weights['opp_four']
            if opp_count == 3 and empty_count == 1: return self.weights['opp_three']
            if opp_count == 2 and empty_count == 2: return self.weights['opp_two']
        return 0

    def evaluate(self, board, player):
        """Score the board state based on heuristic weights."""
        opponent = 3 - player
        score = 0
        for line in self.winning_lines:
            my_count = sum(1 for r, c in line if board[r][c] == player)
            opp_count = sum(1 for r, c in line if board[r][c] == opponent)
            empty_count = 4 - my_count - opp_count
            score += self._score_pattern(my_count, opp_count, empty_count)
        # Center bonus: score only for player's pieces
        for r in range(6):
            for c in range(7):
                if board[r][c] == player:
                    score += max(self.weights['center_bonus'] - abs(c - 3), 0)
        return score

    def get_move(self, game, events):
        """Choose the best move based on immediate board evaluation."""
        valid_moves = game.get_valid_moves()
        if not valid_moves:
            return None
        best_score = -float('inf')
        best_moves = []
        for col in valid_moves:
            temp_game = copy.deepcopy(game)
            temp_game.play_move(col)
            score = (self.weights['my_four'] if (temp_game.game_over and temp_game.turn == self.piece - 1)
                     else self.evaluate(temp_game.board, self.piece))
            if score > best_score:
                best_score = score
                best_moves = [col]
            elif score == best_score:
                best_moves.append(col)
        return min(best_moves, key=lambda col: abs(col - 3))