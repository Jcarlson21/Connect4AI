from connect4 import Connect4GUI, Connect4Game
from player import RandomPlayer, MousePlayer
from dqnPlayer import DQNPlayer
from heuristic_player import HeuristicPlayer
from mcts import MCTSPlayer
<<<<<<< HEAD
=======
from alphaBeta import AlphaBetaPlayer
>>>>>>> 69b7e08c701402369f1415e5317377a8bfdb5328

'''
# Uncomment this section to play human vs human
player1 = MousePlayer(1)
player2 = MousePlayer(2)
game_gui = Connect4GUI(player1, player2)
game_gui.run()
'''
<<<<<<< HEAD
'''
# Uncomment this section for GUI of AI vs AI
player1 = DQNPlayer(1,"maxwin.pth")
player2 = RandomPlayer(2)
=======

'''
# Uncomment this section to play human vs AI
player1 = MousePlayer(1)
player2 = HeuristicPlayer(2)
game_gui = Connect4GUI(player1, player2)
game_gui.run()
'''

'''
# Uncomment this section for GUI of AI vs AI
player1 = MCTSPlayer(1)
player2 = AlphaBetaPlayer(2)
game_gui = Connect4GUI(player1, player2)
game_gui.run()
'''
>>>>>>> 69b7e08c701402369f1415e5317377a8bfdb5328

'''
# Uncomment to run many games of the specified agents (no gui)

player1 = HeuristicPlayer(1)
player2 = AlphaBetaPlayer(2)

# Probably most useful for comparisons.
player1 = MCTSPlayer(1)
player2 = MCTSPlayer(2)
players = [player1,player2]
player1_wins = 0
player2_wins = 0

for i in range(10001):
    game = Connect4Game()
    while not game.game_over:
        move = players[game.turn].get_move(game, None)
        game.play_move(move)

    
    if game.turn == 0:
        player1_wins += 1
    elif game.turn == 1:
        player2_wins += 1
    if i % 100 == 0:
        print("total:", i)
        print("player 1 wins:", player1_wins)
        print("player 2 wins:", player2_wins)
        print("ties:", i - player2_wins - player1_wins)
        print("\n\n")
'''