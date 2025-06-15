from connect4 import Connect4Game
import torch
import torch.nn as nn
import torch.optim as optim
import numpy as np
import random
from collections import deque

from player import RandomPlayer
from dqnPlayer import DQNPlayer
from dqn import Connect4DQN

ROWS, COLS = 6, 7
    
def game_to_tensor(board, player):
    tensor = np.zeros_like(board, dtype=np.float32)
    tensor[board == player] = 1
    tensor[board == (3 - player)] = -1
    return torch.tensor(tensor).unsqueeze(0).unsqueeze(0)

def train_dqn(episodes=10000):
    policy_net = Connect4DQN()
    target_net = Connect4DQN()
    opp = DQNPlayer(2,"connect4_dqn.pth")
    opp_random = RandomPlayer(2)
    target_net.load_state_dict(policy_net.state_dict())

    optimizer = optim.Adam(policy_net.parameters(), lr=1e-3)
    memory = deque(maxlen=10000)

    epsilon = 1.0
    gamma = 0.99
    batch_size = 64
    target_update_freq = 10

    for episode in range(episodes):
        game = Connect4Game()
        while not game.game_over:
            state_tensor = game_to_tensor(game.board, game.turn + 1)
            if random.random() < epsilon:
                action = random.choice(game.get_valid_moves())
            else:
                with torch.no_grad():
                    q_values = policy_net(state_tensor)[0]
                    for c in range(COLS):
                        if game.board[0][c] != 0:
                            q_values[c] = -float('inf')
                    action = torch.argmax(q_values).item()

            if game.board[0][action] != 0:
                continue

            game.play_move(action)
            reward = 0
            if game.game_over:
                reward = 1
            elif np.all(game.board != 0):
                reward = 0.5  # draw

            next_state_tensor = game_to_tensor(game.board, game.turn + 1)
            memory.append((state_tensor, action, reward, next_state_tensor, game.game_over))

            if game.game_over: break

            # Opponent (trained)
            if random.random() > 0.5:
                opp_action = opp.get_move(game, None)
            else:
                opp_action = opp_random.get_move(game, None)
            game.play_move(opp_action)
            if game.game_over:
                reward = -1

            if game.game_over: break

        # Training step
        if len(memory) >= batch_size:
            batch = random.sample(memory, batch_size)
            states, actions, rewards, next_states, dones = zip(*batch)

            states = torch.cat(states)
            next_states = torch.cat(next_states)
            actions = torch.tensor(actions)
            rewards = torch.tensor(rewards)
            dones = torch.tensor(dones, dtype=torch.float32)

            q_values = policy_net(states)
            next_q_values = target_net(next_states)

            q_value = q_values[range(batch_size), actions]
            max_next_q = next_q_values.max(dim=1)[0]
            target = rewards + gamma * max_next_q * (1 - dones)

            loss = nn.MSELoss()(q_value, target)

            optimizer.zero_grad()
            loss.backward()
            optimizer.step()

        if episode % target_update_freq == 0:
            target_net.load_state_dict(policy_net.state_dict())
            torch.save(policy_net.state_dict(), "checkpoint.pth")
            opp = DQNPlayer(2, 'checkpoint.pth')

        epsilon = max(0.1, epsilon * 0.9999)
        if episode % 100 == 0:
            print(f"Episode {episode}, Epsilon: {epsilon:.3f}")

    return policy_net

if __name__ == "__main__":
    policy = train_dqn(20000)
    torch.save(policy.state_dict(), "connect4_self.pth")