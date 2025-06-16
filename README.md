# Connect4 AI Tournment

> This is a python-based Connect4 game engine and GUI that supports both human and AI players. The implemented AI agents are: Random Agent, Minimax + alpha-beta pruning, Heuristic Search, Monte Carlo Tree Search, and Deep Q Reinforcement Learning.  

## Description

#### Content

In the connect4Playground you can instantiaten the following game types:

1. Human v Human 
2. Human v AI
3. AI v Human
4. AI v AI

You can test your game playing skills against various AI Agents (listed below) or compare the results of each agent against each other. 

#### Available AI Agents

| Player                  | Instantiation                     | 
| ----------------------- | --------------------------------- |
| Random Agent            | Chooses the next move at random   |
| Minimax + Alpha-Beta    | Uses standard minimax to a set depth |
| Heuristic Agent         | Uses a custom heuristic to choose a move | 
| Monte Carlo Tree Search | Progressively builds a tree to explore optimal paths| 
| Reinforcement Learning  | Model trained on various iterations of game play|


## How To Use

In a new file or in connect4Playground.py ensure you have the following imports:

from connect4 import Connect4GUI, Connect4Game
from player import RandomPlayer, MousePlayer
from dqnPlayer import DQNPlayer
from heuristic_player import HeuristicPlayer
from mcts import MCTSPlayer
from alphaBeta import AlphaBetaPlayer

Players can be instantiated as follows, with the first argument indicating which player that agent will be: player 1 (1) or player 2 (2)

| Player                  | Instantiation                     | 
| ----------------------- | --------------------------------- |
| Human                   | MousePlayer(1)                    |
| Random Agent            | RandomPlayer(1)                   |
| Minimax + Alpha-Beta    | AlphaBetaPlayer(1)                |
| Heuristic Agent         | HeuristicPlayer(1)                | 
| Monte Carlo Tree Search | MCTSPlayer(1)                     | 
| Reinforcement Learning  | DQNPlayer(1, 'connect4_self.pth') |

A single game can be run with the following:

player1 = DQNPlayer(1, 'connect4_self.pth')
player2 = MousePlayer(2)

game_gui = Connect4GUI(player1, player2)
game_gui.run()

- if you are using connect4Playground, there is starter code to uncomment to play various versions of games.

- note: the first player in the Connect4GUI instantiation should always be a player instantiated with (1)

Run the file. 

If you are using connect4Playground: python connect4Playground.py










