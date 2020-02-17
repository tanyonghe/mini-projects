########################
#   Tic-tac-toe Game   #
#          -           #
#     Tan Yong He      #
#   17 February 2019   #
########################

def check_right_diagonal(board, board_size, num_of_cells, move, mark):
    checked = []
    
    checks = [move - (board_size - 1) * 2,
              move - (board_size - 1)]
    for check in checks:
        if check > 0 and check <= num_of_cells and (check - 1) % board_size > (move - 1) % board_size and board[check - 1].strip() == mark.strip():
            checked.append(1)
        else:
            checked.append(0)
            
            
    checks = [move + (board_size - 1),
              move + (board_size - 1) * 2]
    for check in checks:
        if check > 0 and check <= num_of_cells and (check - 1) % board_size < (move - 1) % board_size and board[check - 1].strip() == mark.strip():
            checked.append(1)
        else:
            checked.append(0)
         
    #print("checkRightDiagonal")
    #print(checked)
    
    if (checked[0] and checked[1]) or (checked[1] and checked[2]) or (checked[2] and checked[3]):
        return True
    return False


def check_left_diagonal(board, board_size, num_of_cells, move, mark):
    checked = []
    
    checks = [move - (board_size + 1) * 2,
              move - (board_size + 1)]
    for check in checks:
        if check > 0 and check <= num_of_cells and (check - 1) % board_size < (move - 1) % board_size and board[check - 1].strip() == mark.strip():
            checked.append(1)
        else:
            checked.append(0)
            
            
    checks = [move + (board_size + 1),
              move + (board_size + 1) * 2]
    for check in checks:
        if check > 0 and check <= num_of_cells and (check - 1) % board_size > (move - 1) % board_size and board[check - 1].strip() == mark.strip():
            checked.append(1)
        else:
            checked.append(0)
            
    #print("checkLeftDiagonal")
    #print(checked)
    
    if (checked[0] and checked[1]) or (checked[1] and checked[2]) or (checked[2] and checked[3]):
        return True
    return False


def check_vertical(board, board_size, num_of_cells, move, mark):
    checked = []
    
    checks = [move - board_size * 2,
              move - board_size,
              move + board_size,
              move + board_size * 2]
    for check in checks:
        if check > 0 and check <= num_of_cells and board[check - 1].strip() == mark.strip():
            checked.append(1)
        else:
            checked.append(0)
            
    #print("checkVertical")
    #print(checked)
    
    if (checked[0] and checked[1]) or (checked[1] and checked[2]) or (checked[2] and checked[3]):
        return True
    return False


def check_horizontal(board, board_size, num_of_cells, move, mark):
    checked = []
    
    checks = [move - 2,
              move - 1]
    for check in checks:
        if check > 0 and check <= num_of_cells and (check - 1) % board_size < (move - 1) % board_size and board[check - 1].strip() == mark.strip():
            checked.append(1)
        else:
            checked.append(0)
            
            
    checks = [move + 1,
              move + 2]
    for check in checks:
        if check > 0 and check <= num_of_cells and (check - 1) % board_size > (move - 1) % board_size and board[check - 1].strip() == mark.strip():
            checked.append(1)
        else:
            checked.append(0)
            
    #print("checkHorizontal")
    #print(checked)
    
    if (checked[0] and checked[1]) or (checked[1] and checked[2]) or (checked[2] and checked[3]):
        return True
    return False


''' Checks all 24 surrounding cells for a 3-cell victory.'''
def is_winning_move(board, board_size, num_of_cells, move, mark):
    if check_horizontal(board, board_size, num_of_cells, move, mark):
        return True
    if check_vertical(board, board_size, num_of_cells, move, mark):
        return True
    if check_left_diagonal(board, board_size, num_of_cells, move, mark):
        return True
    if check_right_diagonal(board, board_size, num_of_cells, move, mark):
        return True
    return False


''' Marks the board with the current player's mark '''
def make_move(board, move, mark):
    board[move - 1] = mark

    
''' Checks if move is valid by making sure there is no mark on that current spot.'''
def is_valid_move(board, board_size, num_of_cells, move):
    if move > num_of_cells or move < 1:
        return False
    if board[move - 1].strip() == str(move):
        return True
    return False


''' Prints out current board game status.'''
def print_board(board, board_size, num_of_cells, cell_size):
    print("\n")
    horizontal_print = "-" * (cell_size + 2) * board_size + "-" * (board_size - 1)
    
    row_vals = []
    for val in board:
        row_vals.append(val)
        if len(row_vals) == board_size:
            row_print = " " + " | ".join(map(str, row_vals)) + " "
            row_vals = []
            print(row_print)
            
            if val != board[-1]:
                print(horizontal_print)


''' Prints out winning message for the winner.'''
def print_draw_message():
    print("\nIt's a draw!")

    
''' Prints out winning message for the winner.'''
def print_win_message(winner_name):
    print(f"\nCongratulations {winner_name}! You have won.")
    
    
''' Creates an empty board of size: board_size * board_size. '''
def create_board(board_size, num_of_cells, cell_size):
    board = [str(i+1).rjust(cell_size, " ") for i in range(num_of_cells)]
    return board


''' Prompts player for next move and returns a Int move value.'''
def prompt_move(message):
    try:
        move = int(input(message))
        return move
    except:
        raise Exception("Player's board move input should be an integer!")


''' Prompts player for a name.'''
def prompt_name(message):
    name = input(message)
    return name


''' Prompts player for size of the board.'''
def prompt_size(message):
    try:
        size = int(input(message))
        return size
    except:
        raise Exception("Player's board size input should be an integer!")


if __name__ == "__main__":
    # Prompts player for game information.
    board_size = prompt_size("\nEnter size of board: ")
    player_one_name = prompt_name("\nEnter name for Player 1: ")
    player_two_name = prompt_name("\nEnter name for Player 2: ")
    
    # Initialize game settings.
    num_of_cells = board_size ** 2
    cell_size = len(str(num_of_cells))
    player_marks = ["x".rjust(cell_size, " "), "o".rjust(cell_size, " ")]
    player_names = [player_one_name, player_two_name]
    player_turn = 0
    num_of_turns = 0
    board = create_board(board_size, num_of_cells, cell_size)
    game_over = False
    
    # Game loop
    while not game_over and num_of_turns != num_of_cells:
        print_board(board, board_size, num_of_cells, cell_size)
        move = prompt_move(f"\n{player_names[player_turn]}, choose a box to place an '{player_marks[player_turn].strip()}' into: ")
        
        if is_valid_move(board, board_size, num_of_cells, move):
            make_move(board, move, player_marks[player_turn])
            num_of_turns += 1
            if is_winning_move(board, board_size, num_of_cells, move, player_marks[player_turn]):
                game_over = True
            else:
                player_turn = (player_turn + 1) % 2
        else:
            print("\nThat's not a valid move. Please try again.")
                
    # Game over
    if game_over:
        winner_name = player_names[player_turn]
        print_board(board, board_size, num_of_cells, cell_size)
        print_win_message(winner_name)
    else:
        print_draw_message()
