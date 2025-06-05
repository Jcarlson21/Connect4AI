import random

import pygame

# abstract class to represent any player that implements function get_move
class Player:
    def __init__(self, piece):
        self.piece = piece

    def get_move(self, game, events):
        raise NotImplementedError()

# class for playing by mouseclick
class MousePlayer(Player):
    def get_move(self, game, events):
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                posx = event.pos[0]
                col = posx // 100  # Assuming square size 100px
                if game.is_valid_move(col):
                    return col
        return None

# plays a random valid move
class RandomPlayer(Player):
    def get_move(self, game, events):
        valid_moves = game.get_valid_moves()
        if valid_moves:
            return random.choice(valid_moves)
        return None
