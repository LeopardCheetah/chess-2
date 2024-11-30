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
        self.white_turn = True
        self.white_piece_locations = ['a1', 'b1', 'c1', 'd1', 'e1', 'f1', 'g1', 'h1'] + ['a2', 'b2', 'c2', 'd2', 'e2', 'f2', 'g2', 'h2']
        self.black_piece_locations = ['a8', 'b8', 'c8', 'd8', 'e8', 'f8', 'g8', 'h8'] + ['a7', 'b7', 'c7', 'd7', 'e7', 'f7', 'g7', 'h7']
    
    
    def generate_white_candidate_moves(self):

        # candidate_moves is a list of all possible candidate moves
        # candidate_moves is a list of pairs, (a, b, c) where a is the starting square and b is the ending square of a piece
        # c is the type of piece to promote to (N, B, R, Q) upon promotion if it is a pawn. otherwise it is simply '.' most of the time
        candidate_moves = [] 

        # generate all possible moves for each piece + start pruning
        # just query all the pieces at each of the white squares

        # todo - encode castling

        for square in self.white_piece_locations:
            # square is now a 2-digit thing
            piece_type = self.game_board.get_piece_type_atsq(square)
            file = square[0]
            rank = square[1]


            num_file = 8 - (ord('h') - ord(file))
            num_rank = int(rank)


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
                    candidate_moves.append((file + rank, chr(ord(file) - 1) + str(int(rank) + 1), '.'))
                
                # top right
                if file != 'h' and self.game_board.get_piece_color_atsq(chr(ord(file) + 1) + str(int(rank) + 1)) == 'b':
                    candidate_moves.append((file + rank, chr(ord(file) + 1) + str(int(rank) + 1), '.'))
                

                # check for en passant
                # en passant to the left
                if rank == '5' and self.last_pawn_move[0] == chr(ord(file) - 1):
                    candidate_moves.append((file + rank, chr(ord(file) - 1) + str(int(rank) + 1), '.'))
                
                # en passant to the right

                if rank == '5' and self.last_pawn_move[0] == chr(ord(file) + 1):
                    candidate_moves.append((file + rank, chr(ord(file) + 1) + str(int(rank) + 1), '.'))
                
                # :)
                continue


            if piece_type == 'N':
                # idea: square = numbers, then generate based on numbers
                # a --> 1, h --> 8
                # 1 --> 8
                new_file = 8 - (ord('h') - ord(file))
                new_rank = int(rank)

                # treat new_file, new_rank as a pair
                possible_knight_squares = [(new_file - 2, new_rank - 1), (new_file + 2, new_rank - 1)] + [(new_file - 2, new_rank + 1), (new_file + 2, new_rank + 1)]
                possible_knight_squares += [(new_file - 1, new_rank + 2), (new_file + 1, new_rank + 2)] + [(new_file - 1, new_rank - 2), (new_file + 1, new_rank - 2)]
        
                # now parse pairs
                more_possible_kn_moves = []
                for pair in possible_knight_squares:
                    if pair[0] < 1 or pair[0] > 8 or pair[1] < 1 or pair[1] > 8:
                        continue
                    
                    more_possible_kn_moves.append(pair)
                

                # now check if there's a piece at that location
                for pair in more_possible_kn_moves:
                    # convert back to normal coordinates
                    new_file = chr(ord('a') - 1 + pair[0]) # 1 --> a, 2 --> b, etc.
                    new_rank = pair[1]

                    if self.game_board.get_piece_color_atsq(new_file + str(new_rank)) == 'w':
                        continue
                    
                    candidate_moves.append((file + rank, new_file + str(new_rank))) # doesn't matter if it's a capture or not
                
                continue
                    


            if piece_type == 'B':
                # uhh check the 4 intersecting diagonal things

                # piece is at file, rank
                # check top right diagonal

                bish_top_right_count = min(8 - num_rank, 8 - num_file)

                for ind in range(1, bish_top_right_count + 1):
                    # move up and to the right 1 sq and check the piece there
                    piece_type_at_sq = self.game_board.get_piece_color_atsq(chr(ord(file) + ind) + str(num_rank + ind))

                    if piece_type_at_sq == 'w':
                        break # bishop is hemmed in by own piece
                    
                    if piece_type_at_sq == 'b':
                        candidate_moves.append((file + rank, chr(ord(file) + ind) + str(num_rank + ind)))
                        break

                    candidate_moves.append((file + rank, chr(ord(file) + ind) + str(num_rank + ind)))
                    continue
                


                # check top left
                bish_top_left_count = min(8 - num_rank, num_file - 1)

                for ind in range(1, bish_top_left_count + 1):
                    bish_str = chr(ord(file) - ind) + str(num_rank + ind)
                    piece_type_at_sq = self.game_board.get_piece_color_atsq(bish_str)

                    if piece_type_at_sq == 'w':
                        break # bishop is hemmed in by own piece
                    
                    if piece_type_at_sq == 'b':
                        candidate_moves.append((file + rank, bish_str))
                        break

                    candidate_moves.append((file + rank, bish_str))
                    continue


                # check bottom left
                bish_bottom_left_count = min(num_rank - 1, num_file - 1)

                for ind in range(1, bish_bottom_left_count + 1):
                    bish_str = chr(ord(file) - ind) + str(num_rank - ind)
                    piece_type_at_sq = self.game_board.get_piece_color_atsq(bish_str)

                    if piece_type_at_sq == 'w':
                        break # bishop is hemmed in by own piece
                    
                    if piece_type_at_sq == 'b':
                        candidate_moves.append((file + rank, bish_str))
                        break

                    candidate_moves.append((file + rank, bish_str))
                    continue


                # check bottom right
                bish_bottom_right_count = min(num_rank - 1, 8 - num_file)

                for ind in range(1, bish_bottom_right_count + 1):
                    bish_str = chr(ord(file) + ind) + str(num_rank - ind)
                    piece_type_at_sq = self.game_board.get_piece_color_atsq(bish_str)

                    if piece_type_at_sq == 'w':
                        break # bishop is hemmed in by own piece
                    
                    if piece_type_at_sq == 'b':
                        candidate_moves.append((file + rank, bish_str))
                        break

                    candidate_moves.append((file + rank, bish_str))
                    continue

                continue


            if piece_type == 'R':
                # if-statement to check the 4 bounds of the rook -- upper, lower, left, right

                # check limits of the top squares
                for sq_rank in range(num_rank + 1, 8 + 1):
                    if self.game_board.get_piece_color_atsq(file + str(sq_rank)) == 'w':
                        break # end immediately; break only breaks out of one loop so we're fine 
                    
                    if self.game_board.get_piece_color_atsq(file + str(sq_rank)) == 'b':
                        candidate_moves.append((file + rank, file + str(sq_rank)))
                        break

                    candidate_moves.append((file + rank, file + str(sq_rank))) # business as usual
                    continue 
                
                # check bottom
                for sq_rank in range(num_rank - 1, 0, -1): # backwards loop
                    if self.game_board.get_piece_color_atsq(file + str(sq_rank)) == 'w':
                        break 

                    if self.game_board.get_piece_color_atsq(file + str(sq_rank)) == 'b':
                        candidate_moves.append((file + rank, file + str(sq_rank)))
                        break

                    candidate_moves.append((file + rank, file + str(sq_rank)))
                    continue
                

                # check right
                # rank stays constant
                for sq_file_ord in range(ord(file) + 1, ord('h') + 1):
                    # use chr(x) whenever
                    if self.game_board.get_piece_color_atsq(chr(sq_file_ord) + rank) == 'w':
                        break
                    
                    if self.game_board.get_piece_color_atsq(chr(sq_file_ord) + rank) == 'b':
                        candidate_moves.append((file + rank, chr(sq_file_ord) + rank))
                        break
                    
                    candidate_moves.append((file + rank, chr(sq_file_ord) + rank))
                    continue
                
                for sq_file_ord in range(ord(file) - 1, ord('a') - 1, -1):
                    if self.game_board.get_piece_color_atsq(chr(sq_file_ord) + rank) == 'w':
                        break
                    
                    if self.game_board.get_piece_color_atsq(chr(sq_file_ord) + rank) == 'b':
                        candidate_moves.append((file + rank, chr(sq_file_ord) + rank))
                        break
                    
                    candidate_moves.append((file + rank, chr(sq_file_ord) + rank))
                    continue 

                # mk we done
                continue


            if piece_type == 'Q':
                # just copy over rook + queen code and combine it
                # 
                # 
                #
                #
                # from bishop code
                queen_top_right_count = min(8 - num_rank, 8 - num_file)

                for ind in range(1, queen_top_right_count + 1):
                    # move up and to the right 1 sq and check the piece there
                    piece_type_at_sq = self.game_board.get_piece_color_atsq(chr(ord(file) + ind) + str(num_rank + ind))

                    if piece_type_at_sq == 'w':
                        break # bishop is hemmed in by own piece
                    
                    if piece_type_at_sq == 'b':
                        candidate_moves.append((file + rank, chr(ord(file) + ind) + str(num_rank + ind)))
                        break

                    candidate_moves.append((file + rank, chr(ord(file) + ind) + str(num_rank + ind)))
                    continue
                


                # check top left
                queen_top_left_count = min(8 - num_rank, num_file - 1)

                for ind in range(1, queen_top_left_count + 1):
                    queen_str = chr(ord(file) - ind) + str(num_rank + ind)
                    piece_type_at_sq = self.game_board.get_piece_color_atsq(queen_str)

                    if piece_type_at_sq == 'w':
                        break 
                    
                    if piece_type_at_sq == 'b':
                        candidate_moves.append((file + rank, queen_str))
                        break

                    candidate_moves.append((file + rank, queen_str))
                    continue


                # check bottom left
                queen_bottom_left_count = min(num_rank - 1, num_file - 1)

                for ind in range(1, queen_bottom_left_count + 1):
                    queen_str = chr(ord(file) - ind) + str(num_rank - ind)
                    piece_type_at_sq = self.game_board.get_piece_color_atsq(queen_str)

                    if piece_type_at_sq == 'w':
                        break 
                    
                    if piece_type_at_sq == 'b':
                        candidate_moves.append((file + rank, queen_str))
                        break

                    candidate_moves.append((file + rank, queen_str))
                    continue


                # check bottom right
                queen_bottom_right_count = min(num_rank - 1, 8 - num_file)

                for ind in range(1, queen_bottom_right_count + 1):
                    queen_str = chr(ord(file) + ind) + str(num_rank - ind)
                    piece_type_at_sq = self.game_board.get_piece_color_atsq(queen_str)

                    if piece_type_at_sq == 'w':
                        break 
                    
                    if piece_type_at_sq == 'b':
                        candidate_moves.append((file + rank, queen_str))
                        break

                    candidate_moves.append((file + rank, queen_str))
                    continue
                #
                #
                #
                #
                #
                # from rook code
                # if-statement to check the 4 bounds of the queen -- upper, lower, left, right

                # check limits of the top squares
                for sq_rank in range(num_rank + 1, 8 + 1):
                    if self.game_board.get_piece_color_atsq(file + str(sq_rank)) == 'w':
                        break # end immediately; break only breaks out of one loop so we're fine 
                    
                    if self.game_board.get_piece_color_atsq(file + str(sq_rank)) == 'b':
                        candidate_moves.append((file + rank, file + str(sq_rank)))
                        break

                    candidate_moves.append((file + rank, file + str(sq_rank))) # business as usual
                    continue 
                
                # check bottom
                for sq_rank in range(num_rank - 1, 0, -1): # backwards loop
                    if self.game_board.get_piece_color_atsq(file + str(sq_rank)) == 'w':
                        break 

                    if self.game_board.get_piece_color_atsq(file + str(sq_rank)) == 'b':
                        candidate_moves.append((file + rank, file + str(sq_rank)))
                        break

                    candidate_moves.append((file + rank, file + str(sq_rank)))
                    continue
                

                # check right
                # rank stays constant
                for sq_file_ord in range(ord(file) + 1, ord('h') + 1):
                    # use chr(x) whenever
                    if self.game_board.get_piece_color_atsq(chr(sq_file_ord) + rank) == 'w':
                        break
                    
                    if self.game_board.get_piece_color_atsq(chr(sq_file_ord) + rank) == 'b':
                        candidate_moves.append((file + rank, chr(sq_file_ord) + rank))
                        break
                    
                    candidate_moves.append((file + rank, chr(sq_file_ord) + rank))
                    continue
                
                for sq_file_ord in range(ord(file) - 1, ord('a') - 1, -1):
                    if self.game_board.get_piece_color_atsq(chr(sq_file_ord) + rank) == 'w':
                        break
                    
                    if self.game_board.get_piece_color_atsq(chr(sq_file_ord) + rank) == 'b':
                        candidate_moves.append((file + rank, chr(sq_file_ord) + rank))
                        break
                    
                    candidate_moves.append((file + rank, chr(sq_file_ord) + rank))
                    continue 

                # end of queen if-statement
                continue


            if piece_type == 'K':
                is_at_top = 0 if rank == '8' else 1 # inverted so i dont need to put nots
                is_at_bottom = 0 if rank == '1' else 1
                is_at_left = 0 if file == 'a' else 1
                is_at_right = 0 if file == 'h' else 1

                # check top left
                if is_at_top and is_at_left and self.game_board.get_piece_color_atsq(chr(ord(file) - 1) + str(int(rank) + 1)) != 'w':
                    # add possible square move
                    # we are not looking at putting the king in check yet
                    candidate_moves.append((file + rank, chr(ord(file) - 1) + str(int(rank) + 1)))
                
                # check top
                if is_at_top and self.game_board.get_piece_color_atsq(file + str(int(rank) + 1)) != 'w':
                    candidate_moves.append((file + rank, file + str(int(rank) + 1)))
                
                # check top right
                if is_at_top and is_at_right and self.game_board.get_piece_color_atsq(chr(ord(file) + 1) + str(int(rank) + 1)) != 'w':
                    candidate_moves.append((file + rank, chr(ord(file) + 1) + str(int(rank) + 1)))
                

                # check directly left
                if is_at_left and self.game_board.get_piece_color_atsq(chr(ord(file) - 1) + rank) != 'w':
                    candidate_moves.append((file + rank, chr(ord(file) - 1) + rank))
                
                # check directly right 
                if is_at_right and self.game_board.get_piece_color_atsq(chr(ord(file) + 1) + rank) != 'w':
                    candidate_moves.append((file + rank, chr(ord(file) + 1) + rank))
                

                # check bottom left
                if is_at_bottom and is_at_left and self.game_board.get_piece_color_atsq(chr(ord(file) - 1) + str(int(rank) - 1)) != 'w':
                    candidate_moves.append((file + rank, chr(ord(file) - 1) + str(int(rank) - 1)))
                
                # check bottom
                if is_at_bottom and self.game_board.get_piece_color_atsq(file + str(int(rank) - 1)) != 'w':
                    candidate_moves.append((file + rank, file + str(int(rank) - 1)))
                
                # check bttom right
                if is_at_bottom and is_at_right and self.game_board.get_piece_color_atsq(chr(ord(file) + 1) + str(int(rank) - 1)) != 'w':
                    candidate_moves.append((file + rank, chr(ord(file) + 1) + str(int(rank) - 1)))
                

                continue #! am done with king!
            



            # ehrm code should never reach here
            raise ValueError("Piece at location", square, "does not exist.")

        return candidate_moves       
        # check if anything is pinned + if king is in check


    def generate_black_candidate_moves(self):
        # ehrm tbd
        pass 
    



    def send_move(self, start_sq, end_sq):
        self.game_board.send_move(start_sq, end_sq)
        # update last move, ply, white piece locations, etc.
        # also check legality
        return



    def load_pos_from_fen(self, fen):
        # fen is the string
        # idea: reset board, then add pieces and update everything else accordingly

        self.game_board.reset_board() # back to dots

    
    # end class


