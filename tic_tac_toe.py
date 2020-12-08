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
        if player == 'X':
            coordinates = input("PLAYER X: Please enter coordinates!")
        else:
            coordinates = input("PLAYER O: Please enter coordinates!")
        rows = ['a', 'b', 'c']
        cols = ['1', '2', '3']
        if coordinates.upper() == "QUIT":
            print("Goodbye!")
            exit()
        try:
            row_col = list(coordinates)
            row_col[0] = rows.index((row_col[0]).lower())
            row_col[1] = cols.index((row_col[1]).lower())
        except (ValueError, TypeError, IndexError):
            continue
        if cell_is_empty(board, row_col):
            board = mark(board, row_col, player)
            return board


def mark(board, row_col, player):
    board[row_col[0]][row_col[1]] = player
    return board


def cell_is_empty(board, row_col):
    if board[row_col[0]][row_col[1]] == '.':
        return True
    return False


def has_won(board, player):
    #rows
    for row in board:
        count = 0
        for cell in row:
            if cell == player:
                count += 1
        if count == 3:
            return True
    #cols
    for j in range(len(board)):
        count = 0
        for i in range(len(board)):
            if board[i][j] == player:
                count += 1
        if count == 3:
            return True
    #diagonal 1
    count = 0
    for i in range(len(board)):
        if board[i][i] == player:
            count += 1
        if count == 3:
            return True
    #diagonal 2
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


def print_result(board):
    print("Game Over")
    if has_won(board, 'X'):
        print("X has won!")
    elif has_won(board, 'O'):
        print("0 has won!")
    else:
        print("It's a tie!")


def tictactoe_game():
    board = init_board()
    print_board(board)
    while True:
        board = get_move('X', board)
        print_board(board)
        if has_won(board, 'X') or is_full(board):
            print_result(board)
            break
        board = get_move('O', board)
        print_board(board)
        if has_won(board, 'O') or is_full(board):
            print_result(board)
            break


def tictactoe_game_ai_1():
    board = init_board()
    print_board(board)
    while True:
        board = get_ai_move('X', board)
        print_board(board)
        if has_won(board, 'X') or is_full(board):
            print_result(board)
            break
        board = get_move('O', board)
        print_board(board)
        if has_won(board, 'O') or is_full(board):
            print_result(board)
            break


def tictactoe_game_ai_2():
    board = init_board()
    print_board(board)
    while True:
        board = get_move('X', board)
        print_board(board)
        if has_won(board, 'X') or is_full(board):
            print_result(board)
            break
        board = get_ai_move('O', board)
        print_board(board)
        if has_won(board, 'O') or is_full(board):
            print_result(board)
            break


def get_ai_move(player, board):
    time.sleep(1)
    winning_coordinates = empty_cell_if_two_in_a_row(player, board)
    if winning_coordinates is not None:
        board = mark(board, winning_coordinates, player)
        return board
    while True:
        row_col = []
        #check_if_two_in_a_row_for_enemy
        #check_if_middle_is_empty
        #place_in_corner
        
        row_col.append(random.randint(0, 2))
        row_col.append(random.randint(0, 2))
        if cell_is_empty(board, row_col):
            board = mark(board, row_col, player)
            return board
    return board


def empty_cell_if_two_in_a_row(player, board):
    #rows
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
    #cols
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
    # #diagonals
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
    if len(sys.argv) == 2 and sys.argv[1] == 'HUMAN-AI':
        tictactoe_game_ai_2()
    elif len(sys.argv) == 2 and sys.argv[1] == 'AI-HUMAN':
        tictactoe_game_ai_1()
    if len(sys.argv) == 1:
        player_mode = input("Choose between 1 or 2 player mode!(1/2)")
        while not (player_mode == '1' or player_mode == '2'):
            player_mode = input("Choose between 1 or 2 player mode!(1/2)")
        if player_mode == '1':
            tictactoe_game_ai_2()
        else:
            tictactoe_game()


if __name__ == '__main__':
    main()