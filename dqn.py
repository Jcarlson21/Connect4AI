import torch.nn as nn
import torch.nn.functional as F

ROWS, COLS = 6, 7

class Connect4DQN(nn.Module):
    def __init__(self):
        super().__init__()
        self.net = nn.Sequential(
            nn.Flatten(),
            nn.Linear(ROWS * COLS, 128),
            nn.ReLU(),
            nn.Linear(128, 64),
            nn.ReLU(),
            nn.Linear(64, COLS)
        )

    def forward(self, x):
        return self.net(x)