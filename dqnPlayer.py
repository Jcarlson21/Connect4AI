import numpy as np
import torch
from dqn import Connect4DQN
from player import Player


class DQNPlayer(Player):
    def __init__(self, piece, model_path):
        self.piece = piece
        self.policy_net = Connect4DQN()  # Define same architecture used during training
        self.policy_net.load_state_dict(torch.load(model_path))
        self.policy_net.eval()  # Inference mode

    def get_move(self, game, events):
        board = game.board  # Assuming game.board is a 2D NumPy array
        valid_moves = game.get_valid_moves()
        if not valid_moves:
            return None

        # Convert board to tensor from the perspective of self.player_id
        state_tensor = self.board_to_tensor(board, game.turn + 1)
        q_values = self.policy_net(state_tensor)[0].detach().clone()

        # Mask out invalid moves
        for c in range(7):
            if c not in valid_moves:
                q_values[c] = -float("inf")

        return torch.argmax(q_values).item()

    def board_to_tensor(self, board, turn):
        tensor = np.zeros_like(board, dtype=np.float32)
        tensor[board == turn] = 1
        tensor[board == (3 - turn)] = -1
        return torch.tensor(tensor).unsqueeze(0).unsqueeze(0)