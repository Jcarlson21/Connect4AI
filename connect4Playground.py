from connect4 import Connect4GUI, Connect4Game
from player import RandomPlayer, MousePlayer

'''
# Uncomment this section to play against someone bad
player1 = RandomPlayer(1)
player2 = MousePlayer(2)
game_gui = Connect4GUI(player1, player2)
game_gui.run()
'''

'''
# Uncomment this section for GUI of AI vs AI
player1 = RandomPlayer(1)
player2 = RandomPlayer(2)
game_gui = Connect4GUI(player1, player2)
game_gui.run()
'''

# Probably most useful for comparisons.
players = [RandomPlayer(1),RandomPlayer(2)]
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
    if i % 1000 == 0:
        print("total:", i)
        print("player 1 wins:", player1_wins)
        print("player 2 wins:", player2_wins)
        print("ties:", i - player2_wins - player1_wins)
        print("\n\n")