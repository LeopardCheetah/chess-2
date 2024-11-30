# goal: get the chess bot going

class color:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    WARNING = '\033[93m'
    GREEN = '\033[92m'
    FAIL = '\033[91m'
    ENDCOLOR = '\033[0m'
    BOLD = '\033[1m'
    GRAY = '\033[2m'
    UNDERLINE = '\033[4m'


class Board:
    board = [["." for a in range(8)] for b in range(8)] # generic


    def __init__(self):
        return 


    
    def printboard(self):
        # print the chess board
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
        # using chess notation, move a piece
        # physically swap a piece from starting square to final square
        
        start_row, start_col = self.convert_coord_to_index(starting_sq)
        end_row, end_col = self.convert_coord_to_index(final_sq)

        self.board[end_row][end_col], self.board[start_row][start_col] = self.board[start_row][start_col], "."
        return 


    
    def change_square(self, final_square, piece_after):
        # change square from what it is to piece_after
        # square is a square in chess notation (like c3)
        # (useful in pawn promotions or in crazyhouse or something)
        
        end_row, end_col = self.convert_coord_to_index(final_square)
        self.board[end_row][end_col] = piece_after
        return
    


    def convert_coord_to_index(self, square):
        # convert a chess coordinate (e.g. f4) into a list index (e.g. [4][5])
        # input: square (string) from a1 -- h8

        sq_rank = int(square[1])
        sq_file = square[0]

        return (8 - sq_rank), int(ord(sq_file) - ord('a'))



    def reset_board(self):
        # reset board to starting position of normal chess

        # add pieces
        starting_ls = ['R', 'N', 'B', 'Q', 'K', 'B', 'N', 'R']
        pointer = 'a'
        for piece in starting_ls:
            self.change_square(pointer+'1', f'{color.BLUE}' + piece + f'{color.ENDCOLOR}')
            self.change_square(pointer+'8', f'{color.GREEN}' + piece + f'{color.ENDCOLOR}')
            pointer = chr(ord(pointer) + 1) # increment pointer
        
        pointer = 'a'
        # add pawns
        for _ in range(8):
            self.change_square(pointer+'2', f'{color.BLUE}P{color.ENDCOLOR}')
            self.change_square(pointer+'7', f'{color.GREEN}P{color.ENDCOLOR}')
            pointer = chr(ord(pointer) + 1) # increment pointer
        
        return #!!



    def send_move(self, start_sq, end_sq):
        # use this command to submit a move
        self.move_piece(start_sq, end_sq)
        self.printboard()
        return
    
    
    def get_board(self):
        return self.board




    def get_piece_color_atsq(self, square):
        # note if the piece at square x is black or white or none.
        row, col = self.convert_coord_to_index(square)
        if self.board[row][col] == ".":
            return -1
    

        return 'w' if self.board[row][col][3] == '4' else 'b' # some interesting string stuff going on here
    


    def get_piece_type_atsq(self, square):
        row, col = self.convert_coord_to_index(square)
        if self.board[row][col] == ".":
            return -1
        
        return self.board[row][col][5]



    # sample text


# sample commands
# board = Board()
# board.send_move('e2', 'e4')
# board.send_move('c7', 'c5')
# board.send_move('g1', 'f3')

board = Board()
board.reset_board()
board.send_move('b2', 'b4')


print(board.get_piece_color_atsq('b3'), board.get_piece_type_atsq('b3'))
