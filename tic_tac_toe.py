import sys
import random
import time
import os


def init_board():
    return [['.','.','.'],['.','.','.'],['.','.','.']]


def print_board(board):
    os.system('clear')
    row_starts = ["A  ", "B  ", "C  "]
    print("   1   2   3")
    for i in range(len(board)):
        print(row_starts[i] + " | ".join(board[i]))
        print("  ---+---+---")


def get_move(player, board):
    while True:
        coordinates = input(f"PLAYER {player}: Please enter coordinates!")
        rows = ['a', 'b', 'c']
        cols = ['1', '2', '3']
        handle_quit(coordinates)
        try:
            row_col = list(coordinates)
            row_col[0] = rows.index((row_col[0]).lower())
            row_col[1] = cols.index((row_col[1]).lower())
        except (ValueError, TypeError, IndexError):
            continue
        if cell_is_empty(board, row_col):
            return row_col


def handle_quit(coordinates):
    if coordinates.upper() == "QUIT":
        print("Goodbye!")
        exit()


def mark(board, row_col, player):
    board[row_col[0]][row_col[1]] = player
    return board


def cell_is_empty(board, row_col):
    if board[row_col[0]][row_col[1]] == '.':
        return True
    return False


def has_won(board, player):
    if check_rows_whether_winning(board, player):
        return True
    if check_columns_whether_winning(board, player):
        return True
    if check_diagonal_1_whether_winning(board, player):
        return True
    if check_diagonal_2_whether_winning(board, player):
        return True
    return False


def check_rows_whether_winning(board, player):
    for row in board:
        count = 0
        for cell in row:
            if cell == player:
                count += 1
        if count == 3:
            return True
    return False


def check_columns_whether_winning(board, player):
    for j in range(len(board)):
        count = 0
        for i in range(len(board)):
            if board[i][j] == player:
                count += 1
        if count == 3:
            return True
    return False


def check_diagonal_1_whether_winning(board, player):
    count = 0
    for i in range(len(board)):
        if board[i][i] == player:
            count += 1
        if count == 3:
            return True
    return False


def check_diagonal_2_whether_winning(board, player):
    count = 0
    for i in range(len(board)):
        if board[i][len(board)-1-i] == player:
            count += 1
        if count == 3:
            return True
    return False


def is_full(board):
    for row in board:
        for cell in row:
            if cell == '.':
                return False
    return True


def print_result(winner=None):
    print("Game Over")
    if winner == 'X':
        print("X has won!")
    elif winner == 'O':
        print("0 has won!")
    else:
        print("It's a tie!")


def tictactoe_game(mode='HUMAN-HUMAN'):
    player = 'X'
    board = init_board()
    print_board(board)
    if mode == 'HUMAN-HUMAN':
        play_human_vs_human(player, board)
    elif mode == 'HUMAN-AI':
        play_human_vs_ai(player, board)
    else:
        play_ai_vs_human(player, board)


def play_human_vs_human(player, board):
    while True:
        human_turn(player, board)
        player = change_player(player)


def play_human_vs_ai(player, board):
    while True:
        human_turn(player, board)
        player = change_player(player)
        ai_turn(player, board)
        player = change_player(player)


def play_ai_vs_human(player, board):
    while True:
        ai_turn(player, board)
        player = change_player(player)
        human_turn(player, board)
        player = change_player(player)


def human_turn(player, board):
    row_col = get_move(player, board)
    mark(board, row_col, player)
    print_board(board)
    if has_won(board, player):
        print_result(player)
        exit()
    if is_full(board):
        print_result()
        exit()


def ai_turn(player, board):
    row_col = get_ai_move(player, board)
    mark(board, row_col, player)
    print_board(board)
    if has_won(board, player):
        print_result(player)
        exit()
    if is_full(board):
        print_result()
        exit()


def change_player(player):
    if player == 'X':
        player = 'O'
    else:
        player = 'X'
    return player


def get_ai_move(player, board):
    time.sleep(1)
    winning_coordinates = empty_cell_if_two_in_a_row(player, board)
    if winning_coordinates is not None:
        return winning_coordinates
    winning_coordinates_2 = empty_cell_if_two_in_a_row_for_enemy(player, board)
    if winning_coordinates_2 is not None:
        return winning_coordinates_2
    center_coordinates = check_if_center_is_empty(board)
    if center_coordinates is not None:
        return center_coordinates
    place_in_corner = empty_cell_in_corner(board)
    if place_in_corner is not None:
        return place_in_corner
    return find_random_empty_place(board)


def empty_cell_if_two_in_a_row(player, board):
    coordinates_of_empty_cell_in_row = search_rows(player, board)
    if coordinates_of_empty_cell_in_row is not None:
        return coordinates_of_empty_cell_in_row
    coordinates_of_empty_cell_in_column = search_columns(player, board)
    if coordinates_of_empty_cell_in_column is not None:
        return coordinates_of_empty_cell_in_column
    coordinates_of_empty_cell_in_diagonal = search_diagonals(player, board)
    if coordinates_of_empty_cell_in_diagonal is not None:
        return coordinates_of_empty_cell_in_diagonal
    return None


def empty_cell_if_two_in_a_row_for_enemy(player, board):
    player = change_player(player)
    return empty_cell_if_two_in_a_row(player, board)


def check_if_center_is_empty(board):
    if board[1][1] == '.':
        return [1, 1]
    return None


def empty_cell_in_corner(board):
    if board[0][0] == '.':
        return [0, 0]
    elif board[0][2] == '.':
        return [0, 2]
    elif board[2][0] == '.':
        return [2, 0]
    elif board[2][2] == '.':
        return [2, 2]
    return None


def find_random_empty_place(board):
    while True:
        row_col = []
        row_col.append(random.randint(0, 2))
        row_col.append(random.randint(0, 2))
        if cell_is_empty(board, row_col):
            return row_col


def search_rows(player, board):
    coordinates_of_empty_cell = [-1, -1]
    for i in range(len(board)):
        count_player = 0
        count_empty = 0
        for j in range(len(board[0])):
            if board[i][j] == player:
                count_player += 1
            if board[i][j] == '.':
                count_empty += 1
                coordinates_of_empty_cell[0] = i
                coordinates_of_empty_cell[1] = j
        if count_player == 2 and count_empty == 1:
            return coordinates_of_empty_cell
    return None


def search_columns(player, board):
    coordinates_of_empty_cell = [-1, -1]
    for j in range(len(board[0])):
        count_player = 0
        count_empty = 0
        for i in range(len(board)):
            if board[i][j] == player:
                count_player += 1
            if board[i][j] == '.':
                count_empty += 1
                coordinates_of_empty_cell[0] = i
                coordinates_of_empty_cell[1] = j
        if count_player == 2 and count_empty == 1:
            return coordinates_of_empty_cell
    return None


def search_diagonals(player, board):
    if search_diagonal_1(player, board) is not None:
        return search_diagonal_1(player, board)
    elif search_diagonal_2(player, board) is not None:
        return search_diagonal_2(player, board)
    else:
        return None


def search_diagonal_1(player, board):
    coordinates_of_empty_cell = [-1, -1]
    count_player = 0
    count_empty = 0
    for i in range(len(board)):
        if board[i][i] == player:
            count_player += 1
        if board[i][i] == '.':
            count_empty += 1
            coordinates_of_empty_cell[0] = i
            coordinates_of_empty_cell[1] = i
    if count_player == 2 and count_empty == 1:
        return coordinates_of_empty_cell
    return None


def search_diagonal_2(player, board):
    count_player = 0
    count_empty = 0
    coordinates_of_empty_cell = [-1, -1]
    for i in range(len(board)):
        if board[i][len(board)-1-i] == player:
            count_player += 1
        if board[i][len(board)-1-i] == '.':
            count_empty += 1
            coordinates_of_empty_cell[0] = i
            coordinates_of_empty_cell[1] = len(board)-1-i
    if count_player == 2 and count_empty == 1:
        return coordinates_of_empty_cell
    return None


def main():
    if len(sys.argv) == 1:
        handle_single_argv_input()
    elif len(sys.argv) == 2 and sys.argv[1] == 'HUMAN-HUMAN':
        tictactoe_game('HUMAN-HUMAN')
    elif len(sys.argv) == 2 and sys.argv[1] == 'HUMAN-AI':
        tictactoe_game('HUMAN-AI')
    elif len(sys.argv) == 2 and sys.argv[1] == 'AI-HUMAN':
        tictactoe_game('AI-HUMAN')
    else:
        exit()


def handle_single_argv_input():
    player_mode = input("Choose between 1 or 2 player mode!(1/2)")
    while not (player_mode == '1' or player_mode == '2'):
        player_mode = input("Choose between 1 or 2 player mode!(1/2)")
    if player_mode == '1':
        handle_player_mode_1()
    else:
        tictactoe_game()


def handle_player_mode_1():
    player_starts = None
    while player_starts != 'Y' or player_starts != 'N':
        player_starts = input("Do you want to start?(Y/N)").upper()
        if player_starts == 'Y':
            tictactoe_game('HUMAN-AI')
            break
        elif player_starts == 'N':
            tictactoe_game('AI-HUMAN')
            break


if __name__ == '__main__':
    main()
