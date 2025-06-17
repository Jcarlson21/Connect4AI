# Connect4 AI Tournment

> This is a python-based Connect4 game engine and GUI that supports both human and AI players. The implemented AI agents are: Random Agent, Minimax + alpha-beta pruning, Heuristic Search, Monte Carlo Tree Search, and Deep Q Reinforcement Learning.  

## Content

In the connect4Playground you can instantiaten the following game types:

1. Human v Human 
2. Human v AI
3. AI v Human
4. AI v AI

You can test your game playing skills against various AI Agents (listed below) or compare the results of each agent against each other. 

#### Available AI Agents

| Player                  | Decision Process                     | 
| ----------------------- | --------------------------------- |
| Random Agent            | Chooses the next move at random   |
| Minimax + Alpha-Beta    | Uses standard minimax to a set depth |
| Heuristic Agent         | Uses a custom heuristic to choose a move | 
| Monte Carlo Tree Search | Progressively builds a tree to explore optimal paths| 
| Reinforcement Learning  | Model trained on various iterations of game play|

#### File Breakdown

- **alphaBeta.py:** Player class that implements the minimax algorithm with alpha beta pruning
- **checkpoint.pth:**
- **connect4_self.pth:**
- **connect4.py:** Defines the connect4 game and GUI
- **connect4Playground.py:** Central place to initialize games 
- **dqn.py:** 
- **dqnPlayer.py:** Player class that
- **heuristic.py:** Player class that
- **mcts.py:** Player class that
- **player.py:** Holds the abstract player class that all other agents use, as well as random and mouse player
- **traning.py:**

## How To Use

### Requirements

The following are required to run this game:

- Python 3+ 
- torch
- matplotlib
- numpy

### Installation

The following instructions are for saving the repository to play games locally.

1. Clone the repository:
   ```bash
   git clone https://github.com/Jcarlson21/Connect4AI.git
   ```

2. Ensure you are in the correct folder (./Connect4AI)

3. Install the required packages:
   ```bash
   pip install -r requirements.txt
   ```

4. Follow the steps below to choose which game play mode you would like

5. Run the connect4Playground:
   ```bash
   python connect4Playground.py
   ```

#### Choosing the game mode

The following is information for changing/editing/adding to **connect4Playground.py**.

Players can be instantiated as follows, with the first argument indicating which player that agent will be: player 1 (1) or player 2 (2)

| Player                  | Instantiation                     | 
| ----------------------- | --------------------------------- |
| Human                   | MousePlayer(1)                    |
| Random Agent            | RandomPlayer(1)                   |
| Minimax + Alpha-Beta    | AlphaBetaPlayer(1)                |
| Heuristic Agent         | HeuristicPlayer(1)                | 
| Monte Carlo Tree Search | MCTSPlayer(1)                     | 
| Reinforcement Learning  | DQNPlayer(1, 'connect4_self.pth') |

A single game is run with the following:

``` python
game_gui = Connect4GUI(player1, player2)
game_gui.run()
```

Where **player1** and **player2** are instances of any of the Players defined above. 

> ***Note:*** the first argument in the Connect4GUI instantiation should always be a player instantiated with (1)

The connect4Playground has various pieces of starter code that can be uncommented to play different games. (Human vs Human, Human vs AI, etc)

Uncomment an existing game initialization or use the script above to create your own before running the file (see instructions above).












