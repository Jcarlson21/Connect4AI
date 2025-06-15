from connect4 import Connect4GUI, Connect4Game
from player import Player, MousePlayer
import random
import copy

class AlphaBetaPlayer(Player):
  def __init__(self, piece, depth=6):
        super().__init__(piece)
        self.piece = piece 
        self.depth = depth
        self.opponent = 1 if piece == 2 else 2
        self.WINDOW_LENGTH = 4

  def get_move(self, game, events):
    score, col = self.alphaBeta(game, self.depth, float('-inf'), float('inf'), True)
    return col
  
  def alphaBeta(self, game, depth, alpha, beta, maxPlayer):
    valid_moves = game.get_valid_moves()

    if depth == 0 or not valid_moves or game.game_over:
      return self.utility(game), None
    
    if maxPlayer:
      max_util = float('-inf')
      move = random.choice(valid_moves)
      top_moves = []

      for col in valid_moves:
        temp_game = copy.copy(game)
        temp_game.board = [row[:] for row in game.board]
        row = temp_game.get_next_open_row(col)
        temp_game.board[row][col] = self.piece
        temp_game.pieces_placed += 1

        if temp_game.check_win(row, col) or temp_game.pieces_placed == temp_game.MAX:
          temp_game.game_over = True
        
        util, best_col = self.alphaBeta(temp_game, depth - 1, alpha, beta, False)

        if util > max_util:
          max_util = util
          best_moves = [col]
        elif util == max_util:
          best_moves.append(col)
        
        alpha = max(alpha, max_util)

        if beta <= alpha:
          break
      best_moves.sort(key=lambda col: abs(col - game.COLS // 2))
      return max_util, best_moves[0]
    
    else:
      min_util = float('inf')
      move = random.choice(valid_moves)

      for col in valid_moves:
        temp_game = copy.copy(game)
        temp_game.board = [row[:] for row in game.board]
        row = temp_game.get_next_open_row(col)
        temp_game.board[row][col] = self.opponent
        temp_game.pieces_placed += 1

        if temp_game.check_win(row, col) or temp_game.pieces_placed == temp_game.MAX:
          temp_game.game_over = True
        
        util, best_col = self.alphaBeta(temp_game, depth - 1, alpha, beta, True)

        if util < min_util:
          min_util = util
          move = col
        
        beta = min(beta, min_util)

        if beta <= alpha:
          break

      return min_util, move

  def utility(self, game):
    if game.game_over:
      winner = self.get_winner(game)
      if winner == self.piece:
        return 1000000
      elif winner == self.opponent:
        return -1000000
      else:
        return 0

    util = 0

    # center bias
    center_col = game.COLS // 2
    for r in range(game.ROWS):
        if game.board[r][center_col] == self.piece:
            util += 10

    # horizontal check
    for r in range(game.ROWS):
      row_array = [game.board[r][c] for c in range(game.COLS)]
      for c in range(game.COLS - 3):
        window = row_array[c: c + self.WINDOW_LENGTH]
        util += self.check_window(window, self.piece)
        util -= self.check_window(window, self.opponent)
    
    # vertical check
    for c in range(game.COLS):
      col_array = [game.board[r][c] for r in range(game.ROWS)]
      for r in range(game.ROWS - 3):
        window = col_array[r: r + 4]
        util += self.check_window(window, self.piece)
        util -= self.check_window(window, self.opponent)

    # diagonal positive
    for r in range(game.ROWS - 3):
      for c in range(game.COLS - 3):
        window = [game.board[r + i][c + i] for i in range(4)]
        util += self.check_window(window, self.piece)
        util -= self.check_window(window, self.opponent)

    # diagonal negative
    for r in range(3, game.ROWS):
      for c in range(game.COLS - 3):
        window = [game.board[r - i][c + i] for i in range(4)]
        util += self.check_window(window, self.piece)
        util -= self.check_window(window, self.opponent)

    return util

  def check_window(self, window, piece):
    opponent_piece = piece % 2 + 1
    util = 0
    max_piece = window.count(piece)
    empty = window.count(0)
    min_piece = window.count(opponent_piece)
    
    if max_piece == 4 and empty == 0:
      util += 1000000
    elif max_piece == 3 and empty == 1:
      util += 500

    if min_piece == 4 and empty == 0:
      util -= 1000000
    elif min_piece == 3 and empty == 1:
      util -= 1000
    
    return util

  def get_winner(self, game):
    for r in range(game.ROWS):
        for c in range(game.COLS):
            if game.board[r][c] != 0:
                if game.check_win(r, c): 
                    return game.board[r][c]
    return None 



