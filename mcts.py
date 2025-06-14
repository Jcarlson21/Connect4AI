import random
import time
import math
from copy import deepcopy

class ConnectState:
    def __init__(self, game=None):
        self.board = [row[:] for row in game.board] if game else [[0]*7 for _ in range(6)]
        self.turn = game.turn if game else 0
        self.game_over_flag = game.game_over if game else False
        self.pieces_placed = game.pieces_placed if game else 0

    def move(self, col):
        if self.game_over_flag:
            return
        for row in range(5, -1, -1):
            if self.board[row][col] == 0:
                self.board[row][col] = self.turn + 1
                self.turn = (self.turn + 1) % 2
                self.pieces_placed += 1
                self.game_over_flag = self.check_win(row, col) or self.pieces_placed == 42
                return
        raise Exception(f"Invalid move in column {col}")

    def check_win(self, row, col):
        player = self.board[row][col]
        if player == 0:
            return False
        directions = [(0, 1), (1, 0), (1, 1), (1, -1)]
        for dr, dc in directions:
            count = 1
            for d in [1, -1]:
                r, c = row + dr * d, col + dc * d
                while 0 <= r < 6 and 0 <= c < 7 and self.board[r][c] == player:
                    count += 1
                    r += dr * d
                    c += dc * d
            if count >= 4:
                return True
        return False


class Node:
    def __init__(self, move, parent):
        self.move = move
        self.parent = parent
        self.N = 0
        self.Q = 0
        self.children = {}

    def add_children(self, children):
        for child in children:
            self.children[child.move] = child

    def value(self, explore=math.sqrt(2)):
        if self.N == 0:
            return float('inf') if explore > 0 else 0
        return self.Q / self.N + explore * math.sqrt(math.log(self.parent.N) / self.N)


class MCTS:
    def __init__(self, state):
        self.root_state = deepcopy(state)
        self.root = Node(None, None)
        self.run_time = 0
        self.num_rollouts = 0

    # Selects a node to be used as a move
    def select_node(self):
        node = self.root
        state = deepcopy(self.root_state)

        while node.children:
            values = [n.value() for n in node.children.values()]
            max_val = max(values)
            best = [n for n in node.children.values() if n.value() == max_val]
            node = random.choice(best)
            state.move(node.move)
            if node.N == 0:
                return node, state

        if not state.game_over_flag:
            self.expand(node, state)
            if node.children:
                node = random.choice(list(node.children.values()))
                state.move(node.move)

        return node, state

    # Adds all possible moves to parent node through children node
    def expand(self, node, state):
        moves = [c for c in range(7) if state.board[0][c] == 0]
        children = [Node(move, node) for move in moves]
        node.add_children(children)

    # Simulates future moves of entire game from given state when game is not over
    def roll_out(self, state):
        while not state.game_over_flag:
            moves = [c for c in range(7) if state.board[0][c] == 0]
            state.move(random.choice(moves))
        for r in range(6):
            for c in range(7):
                if state.board[r][c] != 0 and state.check_win(r, c):
                    return state.board[r][c] - 1
        return -1 if state.pieces_placed == 42 else None  # Draw if full

    # Propagates the winner of simulated game through all ancestors of selected node
    def back_propagate(self, node, player, outcome):
        if outcome == -1:
            reward = 0.5
        else:
            reward = 1 if outcome == player else 0

        while node is not None:
            node.N += 1
            node.Q += reward
            reward = 1 - reward if outcome != -1 else 0.5
            node = node.parent

    # Perfoms above functions for a specified time (10-15 seconds is ideal)
    # For sake of efficiency for project, use 1 seconds
    def search(self, time_limit):
        start = time.process_time()
        rollouts = 0

        while time.process_time() - start < time_limit:
            node, state = self.select_node()
            outcome = self.roll_out(state)
            self.back_propagate(node, (state.turn + 1) % 2, outcome)
            rollouts += 1

        self.run_time = time.process_time() - start
        self.num_rollouts = rollouts

    # Finds best move by looking at most visited children nodes
    def best_move(self):
        if not self.root.children:
            return random.choice([c for c in range(7) if self.root_state.board[0][c] == 0])
        max_N = max(n.N for n in self.root.children.values())
        best_nodes = [n for n in self.root.children.values() if n.N == max_N]
        return random.choice(best_nodes).move

    # If a child node exists for a given move then go there
    def move(self, move):
        if move in self.root.children:
            self.root_state.move(move)
            self.root = self.root.children[move]
        else:
            self.root_state.move(move)
            self.root = Node(None, None)


class MCTSPlayer:
    def __init__(self, piece, time_limit=1.0):
        self.piece = piece
        self.time_limit = time_limit
        self.mcts = None

    def get_move(self, game, events):
        state = ConnectState(game)
        self.mcts = MCTS(state)
        self.mcts.search(self.time_limit)
        move = self.mcts.best_move()
        self.mcts.move(move)
        return move
