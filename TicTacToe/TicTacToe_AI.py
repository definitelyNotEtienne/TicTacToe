# Imports
import copy
import sys
import pygame
import random
import numpy

# Dimension
WIDTH = 500
HEIGHT = WIDTH
LINE_WIDTH = 5
BOARD_ROWS = 3
BOARD_COLS = 3
CIRCLE_WIDTH = 5
SIZE = WIDTH // BOARD_COLS
CIRCLE_RADIUS = SIZE // 3
SPACE = SIZE // 4
# Colours
BG_COLOUR = (0, 0, 0)
LINE_COLOUR = (233, 233, 233)
CIRCLE_COLOUR = (173, 228, 149)
CROSS_COLOUR = (234, 185, 135)

# Game setup
pygame.init()
WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Tic Tac Toe')
WINDOW.fill(BG_COLOUR)


class Model:
    def __init__(self):
        self.spots = numpy.zeros((BOARD_ROWS, BOARD_COLS))
        self.empty_spots = self.spots  # [spots]
        self.claimed_spot = 0

    def final_state(self, show=False):
        # vertical
        for col in range(BOARD_COLS):
            if self.spots[0][col] == self.spots[1][col] == self.spots[2][col] != 0:
                if show:
                    color = CIRCLE_COLOUR if self.spots[0][col] == 2 else CROSS_COLOUR
                    initial_position = (col * SIZE + SIZE // 2, 20)
                    final_position = (col * SIZE + SIZE // 2, HEIGHT - 20)
                    pygame.draw.line(WINDOW, color, initial_position, final_position, LINE_WIDTH)
                return self.spots[0][col]
        # horizontal
        for row in range(BOARD_ROWS):
            if self.spots[row][0] == self.spots[row][1] == self.spots[row][2] != 0:
                if show:
                    color = CIRCLE_COLOUR if self.spots[row][0] == 2 else CROSS_COLOUR
                    initial_position = (20, row * SIZE + SIZE // 2)
                    final_position = (WIDTH - 20, row * SIZE + SIZE // 2)
                    pygame.draw.line(WINDOW, color, initial_position, final_position, LINE_WIDTH)
                return self.spots[row][0]
        # desc diagonal
        if self.spots[0][0] == self.spots[1][1] == self.spots[2][2] != 0:
            if show:
                color = CIRCLE_COLOUR if self.spots[1][1] == 2 else CROSS_COLOUR
                initial_position = (20, 20)
                final_position = (WIDTH - 20, HEIGHT - 20)
                pygame.draw.line(WINDOW, color, initial_position, final_position, LINE_WIDTH)
            return self.spots[1][1]
        # asc diagonal
        if self.spots[2][0] == self.spots[1][1] == self.spots[0][2] != 0:
            if show:
                color = CIRCLE_COLOUR if self.spots[1][1] == 2 else CROSS_COLOUR
                initial_position = (20, HEIGHT - 20)
                final_position = (WIDTH - 20, 20)
                pygame.draw.line(WINDOW, color, initial_position, final_position, LINE_WIDTH)
            return self.spots[1][1]
        # no winners yet
        return 0

    def spot_claim(self, row, col, player):
        # tuples will be marked by whichever player has claimed it
        self.spots[row][col] = player
        self.claimed_spot += 1

    def spot_available(self, row, col):
        # to check if the tuple is available for player to claim
        if self.spots[row][col] == 0:
            return True
        else:
            return False

    def board_full(self):
        # to check if the board is full
        for row in range(BOARD_ROWS):
            for col in range(BOARD_COLS):
                if self.spots[row][col] == 0:
                    return False
                # after going through all the row and col and if all the [][] == 1 then it will straight
                # away return True
            return True

    def empty_spot(self, row, col):
        # when spot is not claimed by any player
        return self.spots[row][col] == 0

    def get_empty_spots(self):
        empty_spots = []
        for row in range(BOARD_ROWS):
            for col in range(BOARD_COLS):
                if self.empty_spot(row, col):
                    empty_spots.append((row, col))

        return empty_spots

    def full_board(self):
        # board is full
        return self.claimed_spot == 9

    def empty_board(self):
        # board is empty
        return self.claimed_spot == 0

    def spots(self, row, col, player):
        self.spots[row][col] = player


class AI:
    def __init__(self, level=1, player=2):
        self.level = level
        self.player = player

    # random AI
    @staticmethod
    def rnd(model):
        empty_spots = model.get_empty_spots()
        idx = random.randrange(0, len(empty_spots))

        return empty_spots[idx]  # (row, col)

    # minimax AI
    def minimax(self, model, maximizing):

        # terminal case
        case = model.final_state()
        # when player 1 wins
        if case == 1:
            return 1, None  # evaluation, move
        # when player 2 wins (the AI)
        if case == 2:
            return -1, None  # evaluation, move
        # when there is no winner
        elif model.full_board():
            return 0, None  # evaluation, move

        if maximizing:
            max_evaluation = -100
            best_move = None
            empty_spots = model.get_empty_spots()

            for (row, col) in empty_spots:
                temp_board = copy.deepcopy(model)
                temp_board.spot_claim(row, col, 1)
                evaluation = self.minimax(temp_board, False)[0]
                if evaluation > max_evaluation:
                    max_evaluation = evaluation
                    best_move = (row, col)

            return max_evaluation, best_move

        elif not maximizing:
            min_evaluation = 100
            best_move = None
            empty_spots = model.get_empty_spots()

            for (row, col) in empty_spots:
                temp_board = copy.deepcopy(model)
                temp_board.spot_claim(row, col, self.player)
                evaluation = self.minimax(temp_board, True)[0]
                if evaluation < min_evaluation:
                    min_evaluation = evaluation
                    best_move = (row, col)

            return min_evaluation, best_move

    # main evaluation
    def evaluation(self, main_board):
        if self.level == 0:
            # random choice
            evaluation = 'random'
            move = self.rnd(main_board)
        else:
            # minimax choice
            evaluation, move = self.minimax(main_board, False)  # AI is minimizing
        print(f'AI has chosen to claim the spot in pos {move} with an evaluation: {evaluation}')
        return move  # row, col


class View:
    @staticmethod
    def ttt_grids():
        # fills the initial screen and background with black colour
        WINDOW.fill(BG_COLOUR)
        # vertical 1 & 2
        pygame.draw.line(WINDOW, LINE_COLOUR, (SIZE, 0), (SIZE, HEIGHT), LINE_WIDTH)
        pygame.draw.line(WINDOW, LINE_COLOUR, (WIDTH - SIZE, 0), (WIDTH - SIZE, HEIGHT), LINE_WIDTH)
        # horizontal 1 & 2
        pygame.draw.line(WINDOW, LINE_COLOUR, (0, SIZE), (WIDTH, SIZE), LINE_WIDTH)
        pygame.draw.line(WINDOW, LINE_COLOUR, (0, HEIGHT - SIZE), (WIDTH, HEIGHT - SIZE), LINE_WIDTH)

    # draws the player's mark
    @staticmethod
    def figures(row, col, player):
        if player == 1:
            # draw cross
            start_desc = (col * SIZE + SPACE, row * SIZE + SPACE)
            end_desc = (col * SIZE + SIZE - SPACE, row * SIZE + SIZE - SPACE)
            pygame.draw.line(WINDOW, CROSS_COLOUR, start_desc, end_desc, LINE_WIDTH)
            start_asc = (col * SIZE + SPACE, row * SIZE + SIZE - SPACE)
            end_asc = (col * SIZE + SIZE - SPACE, row * SIZE + SPACE)
            pygame.draw.line(WINDOW, CROSS_COLOUR, start_asc, end_asc, LINE_WIDTH)

        elif player == 2:
            # draw circle
            center = (col * SIZE + SIZE // 2, row * SIZE + SIZE // 2)
            pygame.draw.circle(WINDOW, CIRCLE_COLOUR, center, CIRCLE_RADIUS, CIRCLE_WIDTH)


class Controller:
    def __init__(self):
        self.model = Model()  # linking board class
        self.ai = AI()  # linking AI class
        self.view = View()  # linking View class
        self.gamemode = 'ai'  # pvp or ai mode
        self.player = 1  # player 1 = cross and player 2 = circle
        self.running = True
        self.view.ttt_grids()

    def move(self, row, col):
        # when player makes a move on the ttt board, it claims the tuple then marks it
        self.model.spot_claim(row, col, self.player)
        self.view.figures(row, col, self.player)
        self.next()

    def next(self):
        # next player
        if self.player == 1:
            print(f"It is player 2's turn.")
        elif self.player == 2:
            print(f"It is player 1's turn.")
        self.player = self.player % 2 + 1

    def change_gamemode(self):
        self.gamemode = 'ai' if self.gamemode == 'pvp' else 'pvp'

    def gameover(self):
        return self.model.final_state(show=True) != 0 or self.model.full_board()

    def restart(self):
        print(f"New game has started.")
        self.__init__()


def main():
    game = Controller()  # linking Controller class
    board = game.model  # linking board class from Controller class
    ai = game.ai  # linking AI class from Controller class

    # mainloop
    while True:
        # pygame events
        for event in pygame.event.get():
            # quit event
            if event.type == pygame.QUIT:
                print(f"The game has been exited.")
                pygame.quit()
                sys.exit()
            # keydown event using keyboard keys
            if event.type == pygame.KEYDOWN:
                # player vs player mode
                if event.key == pygame.K_g:
                    print(f"It is now PVP mode.")
                    game.change_gamemode()
                # restart
                if event.key == pygame.K_r:
                    game.restart()
                    board = game.model
                    ai = game.ai
                # player vs random AI
                if event.key == pygame.K_0:
                    print(f"It is now player vs random AI mode.")
                    ai.level = 0
                # player vs unbeatable AI
                if event.key == pygame.K_1:
                    print(f"It is now player vs unbeatable AI mode.")
                    ai.level = 1
            # click event using mouse
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = event.pos
                row = pos[1] // SIZE
                col = pos[0] // SIZE
                # player claim move
                if board.empty_spot(row, col) and game.running:
                    game.move(row, col)
                    if game.gameover():
                        game.running = False
        # AI initial call
        if game.gamemode == 'ai' and game.player == ai.player and game.running:
            # update the WINDOW
            pygame.display.update()
            # evaluation
            row, col = ai.evaluation(board)
            game.move(row, col)
            if game.gameover():
                game.running = False

        pygame.display.update()


if __name__ == "__main__":
    main()
