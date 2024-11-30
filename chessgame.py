class ChessGame:
    # game class has a board and other features

    game_board = None
    white_king_check = False # is white king in check?
    black_king_check = False 
    white_turn = None # is it white's move?
    move_number = 1

    last_pawn_move = 'z0' # used for en passant, z0 is a null value
    white_rook_movement = (False, False) # used for white castling
    white_king_moved = False 
    black_rook_movement = (False, False) # used for black castling
    black_king_moved = False 

    white_piece_locations = []
    black_piece_locations = []

    def __init__(self):
        import board
        self.game_board = board.Board()

        self.game_board.reset_board()
        white_turn = True
        white_piece_locations = ['a1', 'b1', 'c1', 'd1', 'e1', 'f1', 'g1', 'h1'] + ['a2', 'b2', 'c2', 'd2', 'e2', 'f2', 'g2', 'h2']
        black_piece_locations = ['a8', 'b8', 'c8', 'd8', 'e8', 'f8', 'g8', 'h8'] + ['a7', 'b7', 'c7', 'd7', 'e7', 'f7', 'g7', 'h7']
    
    
    def generate_white_candidate_moves(self):

        # candidate_moves is a list of all possible candidate moves
        # candidate_moves is a list of pairs, (a, b, c) where a is the starting square and b is the ending square of a piece
        # c is the type of piece to promote to (N, B, R, Q) upon promotion if it is a pawn. otherwise it is simply '.' most of the time
        candidate_moves = [] 

        # generate all possible moves for each piece + start pruning
        # just query all the pieces at each of the white squares


        # todo - encode castling

        for square in white_piece_locations:
            # square is now a 2-digit thing
            piece_type = game_board.get_piece_type_atsq(square)
            file = square[0]
            rank = square[1]

            if piece_type == 'P':
                # pawn is at (file, rank)
                
                if rank == '7':
                    # check regular moves + pawn promotion moves

                    # check forward mobility
                    if self.game_board.get_piece_color_atsq(file + '8') == -1:
                        candidate_moves.append((file + '7', file + '8', 'Q'))
                        candidate_moves.append((file + '7', file + '8', 'R'))
                        candidate_moves.append((file + '7', file + '8', 'B'))
                        candidate_moves.append((file + '7', file + '8', 'N'))
                    
                    # check capture mobility
                    # check top left square
                    if file != 'a' and self.game_board.get_piece_color_atsq(chr(ord(file) - 1) + '8') == 'b':
                        candidate_moves.append((file + '7', chr(ord(file) - 1) + '8', 'Q'))
                        candidate_moves.append((file + '7', chr(ord(file) - 1) + '8', 'R'))
                        candidate_moves.append((file + '7', chr(ord(file) - 1) + '8', 'B'))
                        candidate_moves.append((file + '7', chr(ord(file) - 1) + '8', 'N'))
                    
                    if file != 'h' and self.game_board.get_piece_color_atsq(chr(ord(file) + 1) + '8') == 'b':
                        candidate_moves.append((file + '7', chr(ord(file) + 1) + '8', 'Q'))
                        candidate_moves.append((file + '7', chr(ord(file) + 1) + '8', 'R'))
                        candidate_moves.append((file + '7', chr(ord(file) + 1) + '8', 'B'))
                        candidate_moves.append((file + '7', chr(ord(file) + 1) + '8', 'N'))

                    continue



                # check if pawn can move up
                if self.game_board.get_piece_color_atsq(file + str(int(rank) + 1)) == -1:
                    # pawn is free to move up (technically -- if not pinned)
                    candidate_moves.append((file + rank, file + str(int(rank) + 1), '.'))

                    if rank == '2' and self.game_board.get_piece_color_atsq(file + '4') == -1:
                        # we can move 2 squares yippee
                        candidate_moves.append((file + '2', file + '4', '.')) # move from x2 --> x4 (e.g. e2 --> e4)

                
                # check top left + top right of pawn for captures
                # top left
                if file != 'a' and self.game_board.get_piece_color_atsq(chr(ord(file) - 1) + str(int(rank) + 1)) == 'b':
                    # eat 
                    candidate_moves.append((file + rank, file + 'x' + chr(ord(file) - 1) + str(int(rank) + 1), '.'))
                
                # top right
                if file != 'h' and self.game_board.get_piece_color_atsq(chr(ord(file) + 1) + str(int(rank) + 1)) == 'b':
                    candidate_moves.append((file + rank, file + 'x' + chr(ord(file) + 1) + str(int(rank) + 1), '.'))
                

                # check for en passant
                # en passant to the left
                if rank == '5' and last_pawn_move[0] == chr(ord(file) - 1):
                    candidate_moves.append((file + rank, file + 'x' + chr(ord(file) - 1) + str(int(rank) + 1), '.'))
                
                # en passant to the right
                if rank == '5' and last_pawn_move[0] == chr(ord(file) + 1):
                    candidate_moves.append((file + rank, file + 'x' + chr(ord(file) + 1) + str(int(rank) + 1), '.'))
                
                # :)
                continue

            if piece_type == 'N':
                continue
        
            if piece_type == 'B':
                continue

            if piece_type == 'R':
                continue

            if piece_type == 'Q':
                continue

            if piece_type == 'K':
                continue
                # yippee the simplest
            
            # ehrm code should never reach here
            raise ValueError("Piece at location", square, "does not exist.")
        

        # check if anything is pinned + if king is in check

    
    def generate_black_candidate_moves(self):
        # ehrm tbd
        pass 
    
    # end class



game = ChessGame()
