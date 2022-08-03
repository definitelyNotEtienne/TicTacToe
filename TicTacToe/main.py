import pygame
import numpy

# dimensions
WIDTH, HEIGHT = 500, 500
LINE_WIDTH = 5
BOARD_COL = 3
BOARD_ROW = 3
SIZE = WIDTH // BOARD_COL
CIRCLE_RADIUS = SIZE // 3
CIRCLE_WIDTH = 5
SPACE = SIZE // 4

# colours
BG_COLOUR = (0, 0, 0)
LINE_COLOUR = (233, 233, 233)
CIRCLE_COLOUR = (173, 228, 149)
CROSS_COLOUR = (234, 185, 135)

# set window display size, and it's name with the background colour filled
WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Tic Tac Toe")
# makes the background colour into black
WINDOW.fill(BG_COLOUR)
TTT_board = numpy.zeros((BOARD_COL, BOARD_ROW))
player = 1
game_over = False


# the lines of the TTT board game
def draw_line():
    # vertical line 1
    pygame.draw.line(WINDOW, LINE_COLOUR, (SIZE, 0), (SIZE, HEIGHT), LINE_WIDTH)
    # vertical line 2
    pygame.draw.line(WINDOW, LINE_COLOUR, (2*SIZE, 0), (2*SIZE, HEIGHT), LINE_WIDTH)
    # horizontal line 1
    pygame.draw.line(WINDOW, LINE_COLOUR, (0, SIZE), (WIDTH, SIZE), LINE_WIDTH)
    # horizontal line 2
    pygame.draw.line(WINDOW, LINE_COLOUR, (0, 2*SIZE), (WIDTH, 2*SIZE), LINE_WIDTH)


draw_line()


# to state on console tuple that which player has selected which tuple
def spot_claim(row, col, player):
    TTT_board[row][col] = player


# to check if the tuple is available for player to claim
def spot_available(row, col):
    if TTT_board[row][col] == 0:
        return True
    else:
        return False


# to check if the board is full
def board_full():
    for row in range(BOARD_ROW):
        for col in range(BOARD_COL):
            if TTT_board[row][col] == 0:
                return False
    return True


# draws the figure of the players' mark
def figures():
    for row in range(BOARD_ROW):
        for col in range(BOARD_COL):
            if TTT_board[row][col] == 1:
                pygame.draw.line(WINDOW, CROSS_COLOUR, (col * SIZE + SPACE, row * SIZE + SIZE - SPACE),
                                 (col * SIZE + SIZE - SPACE, row * SIZE + SPACE), LINE_WIDTH)
                pygame.draw.line(WINDOW, CROSS_COLOUR, (col * SIZE + SPACE, row * SIZE + SPACE),
                                 (col * SIZE + SIZE - SPACE, row * SIZE + SIZE - SPACE), LINE_WIDTH)
            elif TTT_board[row][col] == 2:
                pygame.draw.circle(WINDOW, CIRCLE_COLOUR, (int(col * SIZE + SIZE // 2), int(row * SIZE + SIZE // 2)),
                                   CIRCLE_RADIUS, CIRCLE_WIDTH)


# check if there is a winner when 3 spots are claimed by the same player
def check_winner(player):
    for col in range(BOARD_COL):
        if TTT_board[0][col] == player and TTT_board[1][col] == player and TTT_board[2][col] == player:
            vertical_line(col, player)
            return True
    for row in range(BOARD_ROW):
        if TTT_board[row][0] == player and TTT_board[row][1] == player and TTT_board[row][2] == player:
            horizontal_line(row, player)
            return True
    if TTT_board[2][0] == player and TTT_board[1][1] == player and TTT_board[0][2] == player:
        up_diagonal(player)
        return True
    if TTT_board[2][2] == player and TTT_board[1][1] == player and TTT_board[0][0] == player:
        down_diagonal(player)
        return True

    return False


def vertical_line(col, player):
    global colour
    pos_c = col * SIZE + SIZE//2
    if player == 1:
        colour = CROSS_COLOUR
    elif player == 2:
        colour = CIRCLE_COLOUR

    pygame.draw.line(WINDOW, colour, (pos_c, 15), (pos_c, HEIGHT - 15), LINE_WIDTH)


def horizontal_line(row, player):
    global color
    pos_r = row * SIZE + SIZE//2
    if player == 1:
        color = CROSS_COLOUR
    elif player == 2:
        color = CIRCLE_COLOUR

    pygame.draw.line(WINDOW, color, (15, pos_r), (WIDTH - 15, pos_r), LINE_WIDTH)


def up_diagonal(player):
    global colour
    if player == 1:
        colour = CROSS_COLOUR
    elif player == 2:
        colour = CIRCLE_COLOUR

    pygame.draw.line(WINDOW, colour, (15, HEIGHT - 15), (WIDTH - 15, 15), LINE_WIDTH)


def down_diagonal(player):
    global colour
    if player == 1:
        colour = CROSS_COLOUR
    elif player == 2:
        colour = CIRCLE_COLOUR

    pygame.draw.line(WINDOW, colour, (15, 15), (WIDTH - 15, HEIGHT - 15), LINE_WIDTH)


def restart():
    global player
    WINDOW.fill(BG_COLOUR)
    draw_line()
    player = 1
    for row in range(BOARD_ROW):
        for col in range(BOARD_COL):
            TTT_board[row][col] = 0


def main():
    global player, game_over
    run = True
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            # linking console with the game board
            if event.type == pygame.MOUSEBUTTONDOWN and not game_over:
                mouse_x = event.pos[0]
                mouse_y = event.pos[1]

                row_click = int(mouse_y // SIZE)
                col_click = int(mouse_x // SIZE)

                if spot_available(row_click, col_click):
                    spot_claim(row_click, col_click, player)
                    if player == 1:
                        print(f"It is player 2's turn.")
                    elif player == 2:
                        print(f"It is player 1's turn.")
                    if check_winner(player):
                        game_over = True
                        print(f"Game Over. The winner is player {player}.")
                    player = player % 2 + 1

                    figures()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    restart()
                    game_over = False
                    print(f"New Game has started.")

        pygame.display.update()
    pygame.quit()


if __name__ == "__main__":
    main()
