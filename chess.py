# goal: get the chess bot going

class color:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    WARNING = '\033[93m'
    OKGREEN = '\033[92m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    GRAY = '\033[2m'
    UNDERLINE = '\033[4m'


class Board:
    board = [["." for a in range(8)] for b in range(8)] # generic

    def __init__(self):
        self.board[4][5] = 'X'
    
    def printboard(self):
        print()
        print('  +-----------------+')
        c = 8
        for row in self.board:
            print(c, '|', end=' ')
            c -= 1
            for item in row:
                print(item, end=' ')
            
            print('|')
        
        print('  +-----------------+')
        print('    a b c d e f g h')
        return


    def move_piece(self, starting_sq, final_sq):
        # using chess notation
        
        start_row, start_col = self.convert_coord_to_index(starting_sq)
        end_row, end_col = self.convert_coord_to_index(final_sq)

        self.board[end_row][end_col], self.board[start_row][start_col] = self.board[start_row][start_col], "."
        return 
    
    def convert_coord_to_index(self, square):
        # convert a chess coordinate (e.g. f4) into a list index (e.g. [4][5])
        # input: square (string) from a1 -- h8

        sq_rank = int(square[1])
        sq_file = square[0]

        return (8 - sq_rank), int(ord(sq_file) - ord('a'))


board = Board()
board.printboard()
board.move_piece('f4', 'h3')
board.printboard()