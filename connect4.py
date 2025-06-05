import pygame
import sys

from player import MousePlayer, RandomPlayer


class Connect4Game:
    ROWS = 6
    COLS = 7

    def __init__(self):
        self.board = [[0 for _ in range(self.COLS)] for _ in range(self.ROWS)]
        self.game_over = False
        self.turn = 0
        self.MAX = self.ROWS * self.COLS
        self.pieces_placed = 0

    def is_valid_move(self, col):
        return self.board[0][col] == 0

    def get_next_open_row(self, col):
        if col >= self.COLS or col < 0:
            raise Exception("Invalid move, column:", col, self.board)
        for r in range(self.ROWS - 1, -1, -1):
            if self.board[r][col] == 0:
                return r

    def play_move(self, col):
        row = self.get_next_open_row(col)
        if row is not None:
            self.board[row][col] = self.turn + 1
            self.pieces_placed += 1
            self.turn = (1 + self.turn) % 2
            if self.check_win(row, col):
                self.game_over = True
                self.turn = (1 + self.turn) % 2
            if self.pieces_placed == self.MAX:
                self.game_over = True
                self.turn = -1
            return self.board, row, col

        for i in range(6):
            print(self.board[i])
        raise Exception("Invalid move, row:", row, col)

    def check_win(self, row, col):
        player = self.board[row][col]
        if player == 0:
            return False

        def count_direction(delta_row, delta_col):
            count = 0
            r, c = row + delta_row, col + delta_col
            while 0 <= r < self.ROWS and 0 <= c < self.COLS and self.board[r][c] == player:
                count += 1
                r += delta_row
                c += delta_col
            return count

        directions = [(0, 1), (1, 0), (1, 1), (1, -1)]

        for dr, dc in directions:
            total = 1 + count_direction(dr, dc) + count_direction(-dr, -dc)
            if total >= 4:
                return True
        return False

    def get_valid_moves(self):
        return [c for c in range(self.COLS) if self.is_valid_move(c)]


class Connect4GUI:
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    BLUE = (0, 0, 255)
    RED = (255, 0, 0)
    YELLOW = (255, 255, 0)
    SQUARESIZE = 100
    WIDTH = 7 * SQUARESIZE
    HEIGHT = (6 + 1) * SQUARESIZE  # extra row for dropping piece
    RADIUS = int(SQUARESIZE / 2 - 5)

    def __init__(self, player1, player2):
        pygame.init()
        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        pygame.display.set_caption("Connect Four")
        self.font = pygame.font.SysFont("monospace", 75)

        self.game = Connect4Game()
        self.players = [player1, player2]
        self.game_over = False

        self.draw_board()

    def draw_board(self):
        self.screen.fill(self.WHITE)
        for c in range(7):
            for r in range(6):
                pygame.draw.rect(self.screen, self.BLUE, (c * self.SQUARESIZE, (r + 1) * self.SQUARESIZE, self.SQUARESIZE, self.SQUARESIZE))
                color = self.WHITE
                piece = self.game.board[r][c]
                if piece == 1:
                    color = self.RED
                elif piece == 2:
                    color = self.YELLOW
                pygame.draw.circle(self.screen, color, (int(c * self.SQUARESIZE + self.SQUARESIZE / 2), int((r + 1) * self.SQUARESIZE + self.SQUARESIZE / 2)), self.RADIUS)
        pygame.display.update()

    def run(self):
        clock = pygame.time.Clock()

        while True:
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            if not self.game_over:
                current_player = self.players[self.game.turn]
                col = current_player.get_move(self.game, events)

                if col is not None:
                    _, row, col = self.game.play_move(col)

                    self.draw_board()

                    if self.game.check_win(row, col):
                        label = self.font.render(f"Player {self.game.turn + 1} wins!", 1, self.RED if current_player.piece == 1 else self.YELLOW)
                        self.screen.blit(label, (40, 10))
                        self.game_over = True

                # Add a small delay for AI moves
                if isinstance(self.players[self.game.turn], RandomPlayer) and not self.game_over:
                    pygame.time.wait(200)

            else:
                pygame.display.update()
                pygame.time.wait(3000)
                pygame.quit()
                return self.game

            clock.tick(60)


if __name__ == "__main__":
    # Examples of any combination of players:
    player1 = MousePlayer(1)
    player2 = RandomPlayer(2)

    game_gui = Connect4GUI(player1, player2)
    game_gui.run()