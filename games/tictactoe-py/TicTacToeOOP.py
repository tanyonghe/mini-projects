########################
#   Tic-tac-toe Game   #
#          -           #
#     Tan Yong He      #
#   17 February 2019   #
########################

class PromptBox:
    def __init__(self):
        pass
    
    
    ''' Prompts player for a name.'''
    def prompt_name(self, message):
        name = input(message)
        return name


    ''' Prompts player for size of the board.'''
    def prompt_size(self, message):
        try:
            size = int(input(message))
            return size
        except:
            raise Exception("Player's board size input should be an Integer!")


class Player:
    def __init__(self, name, mark):
        self.name = name
        self.mark = mark
        
    def get_name(self):
        return self.name
    
    def get_mark(self):
        return self.mark
    
    
class TicTacToeBoard:
    def __init__(self, board_size, player_one_name, player_two_name):
        # Initialize board settings
        self.board_size = board_size
        self.num_of_cells = self.board_size ** 2
        self.cell_size = len(str(self.num_of_cells))
        self.board = self.create_board()
        self.player_turn = 0
        self.turns = 0
        self.game_over = False

        # Initialize players
        player_one = Player(player_one_name, "x".rjust(self.cell_size, " "))
        player_two = Player(player_two_name, "o".rjust(self.cell_size, " "))
        self.players = [player_one, player_two]
    
    
    ''' Creates an empty board of size: board_size * board_size. '''
    def create_board(self):
        board = [str(i+1).rjust(self.cell_size, " ") for i in range(self.num_of_cells)]
        return board

    
    ''' Checks if the game is already over. '''
    def is_game_over(self):
        return self.game_over
    
    
    ''' Checks if there are still valid moves that can be made. '''
    def has_valid_moves_left(self):
        return self.num_of_cells != self.turns

    
    ''' Prints out current board game status.'''
    def print_board(self):
        print("\n")
        horizontal_divider = "-" * (self.cell_size + 2) * self.board_size + "-" * (self.board_size - 1)

        row_vals = []
        for val in self.board:
            row_vals.append(val)
            if len(row_vals) == board_size:
                row_print = " " + " | ".join(map(str, row_vals)) + " "
                row_vals = []
                print(row_print)
                
                # add a divider if there are more rows to be printed
                if val != self.board[-1]:
                    print(horizontal_divider)
                    
                    
    ''' Checks if move is valid by making sure there is no mark on that current spot.'''
    def is_valid_move(self, move):
        if move > self.num_of_cells or move < 1:
            return False
        if self.board[move - 1].strip() == str(move):
            return True
        return False
    
    
    
    ''' Marks the board with the current player's mark '''
    def make_move(self, move):
        self.board[move - 1] = self.get_current_player_mark()
        if self.is_winning_move(move, gameboard.get_current_player_mark()):
            self.game_over = True
        else:
            gameboard.next_turn()
    
    
    ''' Get the board mark of the current player. '''
    def get_current_player_mark(self):
        return self.players[self.player_turn].get_mark()
    
    
    ''' Get the name of the current player. '''
    def get_current_player_name(self):
        return self.players[self.player_turn].get_name()
        
        
    ''' Get the current player. '''
    def get_current_player(self):
        return self.players[self.player_turn]
    
    
    ''' Checks all 24 surrounding cells for a 3-cell victory.'''
    def is_winning_move(self, move, mark):
        if self.check_horizontal(move, mark):
            return True
        if self.check_vertical(move, mark):
            return True
        if self.check_left_diagonal(move, mark):
            return True
        if self.check_right_diagonal(move, mark):
            return True
        return False

    
    def check_horizontal(self, move, mark):
        checked = []

        checks = [move - 2,
                  move - 1]
        for check in checks:
            if check > 0 and check <= self.num_of_cells and (check - 1) % self.board_size < (move - 1) % self.board_size and self.board[check - 1].strip() == mark.strip():
                checked.append(1)
            else:
                checked.append(0)


        checks = [move + 1,
                  move + 2]
        for check in checks:
            if check > 0 and check <= self.num_of_cells and (check - 1) % self.board_size > (move - 1) % self.board_size and self.board[check - 1].strip() == mark.strip():
                checked.append(1)
            else:
                checked.append(0)

        #print("checkHorizontal")
        #print(checked)

        if (checked[0] and checked[1]) or (checked[1] and checked[2]) or (checked[2] and checked[3]):
            return True
        return False


    def check_vertical(self, move, mark):
        checked = []

        checks = [move - board_size * 2,
                  move - board_size,
                  move + board_size,
                  move + board_size * 2]
        for check in checks:
            if check > 0 and check <= self.num_of_cells and self.board[check - 1].strip() == mark.strip():
                checked.append(1)
            else:
                checked.append(0)

        #print("checkVertical")
        #print(checked)

        if (checked[0] and checked[1]) or (checked[1] and checked[2]) or (checked[2] and checked[3]):
            return True
        return False


    def check_left_diagonal(self, move, mark):
        checked = []

        checks = [move - (board_size + 1) * 2,
                  move - (board_size + 1)]
        for check in checks:
            if check > 0 and check <= self.num_of_cells and (check - 1) % self.board_size < (move - 1) % self.board_size and self.board[check - 1].strip() == mark.strip():
                checked.append(1)
            else:
                checked.append(0)


        checks = [move + (board_size + 1),
                  move + (board_size + 1) * 2]
        for check in checks:
            if check > 0 and check <= self.num_of_cells and (check - 1) % self.board_size > (move - 1) % self.board_size and self.board[check - 1].strip() == mark.strip():
                checked.append(1)
            else:
                checked.append(0)

        #print("checkLeftDiagonal")
        #print(checked)

        if (checked[0] and checked[1]) or (checked[1] and checked[2]) or (checked[2] and checked[3]):
            return True
        return False


    def check_right_diagonal(self, move, mark):
        checked = []

        checks = [move - (self.board_size - 1) * 2,
                  move - (self.board_size - 1)]
        for check in checks:
            if check > 0 and check <= self.num_of_cells and (check - 1) % self.board_size > (move - 1) % self.board_size and self.board[check - 1].strip() == mark.strip():
                checked.append(1)
            else:
                checked.append(0)


        checks = [move + (self.board_size - 1),
                  move + (self.board_size - 1) * 2]
        for check in checks:
            if check > 0 and check <= self.num_of_cells and (check - 1) % self.board_size < (move - 1) % self.board_size and self.board[check - 1].strip() == mark.strip():
                checked.append(1)
            else:
                checked.append(0)

        #print("checkRightDiagonal")
        #print(checked)

        if (checked[0] and checked[1]) or (checked[1] and checked[2]) or (checked[2] and checked[3]):
            return True
        return False
    
    ''' Changes the players' turns. '''
    def next_turn(self):
        self.player_turn = (self.player_turn + 1) % 2
        self.turns += 1
        
        
    ''' Prompts player for next move and returns a Int move value.'''
    def prompt_move(self):
        message = f"\n{self.get_current_player_name()}, choose a box to place an '{self.get_current_player_mark().strip()}' into: "
        try:
            move = int(input(message))
            return move
        except:
            raise Exception("Player's board move input should be an integer!")


    ''' Prints out winning message for the winner.'''
    def print_draw_message(self):
        print("\nIt's a draw!")


    ''' Prints out winning message for the winner.'''
    def print_win_message(self):
        if self.is_game_over():
            print(f"\nCongratulations {self.get_current_player_name()}! You have won.")
        else:
            print("\n There is no winner yet!\n")
    
    
if __name__ == "__main__":
    # Initialize prompt object.
    prompt = PromptBox()
    
    # Prompts player for game information.
    board_size = prompt.prompt_size("\nEnter size of board: ")
    player_one_name = prompt.prompt_name("\nEnter name for Player 1: ")
    player_two_name = prompt.prompt_name("\nEnter name for Player 2: ")
    
    # Initialize gameboard object.
    gameboard = TicTacToeBoard(board_size, player_one_name, player_two_name)
    
    # Game loop
    while gameboard.has_valid_moves_left() and not gameboard.is_game_over():
        gameboard.print_board()
        move = gameboard.prompt_move()
        
        if gameboard.is_valid_move(move):
            gameboard.make_move(move)
        else:
            print("\nThat's not a valid move. Please try again.")
                
    # Game over
    if gameboard.is_game_over():
        gameboard.print_board()
        gameboard.print_win_message()
    else:
        gameboard.print_draw_message()