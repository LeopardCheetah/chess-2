class ChessGame:
    # game class has a board and other features

    game_board = None
    white_king_check = False # is white king in check?
    black_king_check = False 
    white_turn = True # is it white's move?
    move_number = 1

    last_pawn_move = 'z0' # used for en passant, z0 is a null value -- this is where the en passant square IS (e.g. c7 --> c5 would make this c6)
    white_kingside_castling = True # true if white can still castle kingside at any given moment
    white_queenside_castling = True
    black_kingside_castling = True
    black_queenside_castling = True 

    white_piece_locations = []
    black_piece_locations = []

    half_move_clock = 0 # yeah idk tinker with this later -- see https://en.wikipedia.org/wiki/Forsyth%E2%80%93Edwards_Notation

    def __init__(self):
        import board
        self.game_board = board.Board()

        self.game_board.reset_board()
        self.white_turn = True
        self.white_piece_locations = ['a1', 'b1', 'c1', 'd1', 'e1', 'f1', 'g1', 'h1'] + ['a2', 'b2', 'c2', 'd2', 'e2', 'f2', 'g2', 'h2']
        self.black_piece_locations = ['a8', 'b8', 'c8', 'd8', 'e8', 'f8', 'g8', 'h8'] + ['a7', 'b7', 'c7', 'd7', 'e7', 'f7', 'g7', 'h7']
    
    
    def is_white_king_in_check(self, white_piece_positions=None):
        white_piece_location_list = []
        if white_piece_positions is None:
            white_piece_location_list = self.white_piece_locations
        else:
            white_piece_location_list = white_piece_positions
        # todo
        # check's if in current position, white king is in check
        # returns true/false

        
        # basically, from position, see if white king is in check
        # check all legal moves of all black pieces!

        white_king_location = ""
        

        for piece_location in white_piece_location_list:
            if self.game_board.get_piece_type_atsq(piece_location) == 'K':
                white_king_location = piece_location
                break
        
        white_king_file = white_king_location[0]
        white_king_rank = white_king_location[1]

        # check for 8 knights, then each direction infinitely
        # check for knights
        for pair in [(-1, 2), (-1, -2), (1, 2), (1, -2), (2, -1), (2, 1), (-2, 1), (-2, -1)]:

            try:
                black_kn_file = chr(ord(white_king_file) + pair[0]) 
                black_kn_rank = chr(ord(white_king_rank) + pair[1])
                if self.game_board.get_piece_type_atsq(black_kn_file + black_kn_rank) == 'N' and self.game_board.get_piece_color_atsq(black_kn_file + black_kn_rank) == 'b':
                    return True # yeah there's a knight
            except:
                pass # lmao don't worry about this -- if it errors then it's out of bounds and we're fine
            

        # check in the other 8 directions infinitely
        # since this is where the king can move, kings can potentially touch here so we have to check that
        
        # check king's top right diagonal

        num_rank = int(white_king_rank)
        num_file = 8 - (ord('h') - ord(white_king_file))

        king_top_right_count = min(8 - num_rank, 8 - num_file)

        for ind in range(1, king_top_right_count + 1):
            piece_color_at_sq = self.game_board.get_piece_color_atsq(chr(ord(white_king_file) + ind) + str(num_rank + ind))

            if piece_color_at_sq == 'w':
                break # king is safe -- for now.
            
            if piece_color_at_sq == 'b':
                piece_type_at_sq = self.game_board.get_piece_type_atsq(chr(ord(white_king_file) + ind) + str(num_rank + ind))
                if piece_type_at_sq == 'B' or piece_type_at_sq == 'Q':
                    return True # we out
                
                if (piece_type_at_sq == 'K' or piece_type_at_sq == 'P') and ind == 1:
                    return True
                
                break # we are far enough away from other pieces so everything is fine
            continue
                

        # check top left
        king_top_left_count = min(8 - num_rank, num_file - 1)

        for ind in range(1, king_top_left_count + 1):
            king_str = chr(ord(white_king_file) - ind) + str(num_rank + ind)
            piece_color_at_sq = self.game_board.get_piece_color_atsq(king_str)

            if piece_color_at_sq == 'w':
                break 
            
            if piece_color_at_sq == 'b':
                piece_type_at_sq = self.game_board.get_piece_type_atsq(king_str)
                if piece_type_at_sq == 'B' or piece_type_at_sq == 'Q':
                    return True # we out
                
                if (piece_type_at_sq == 'K' or piece_type_at_sq == 'P') and ind == 1:
                    return True # pawns are menacing beings
                
                break

            continue


        # check bottom left
        king_bottom_left_count = min(num_rank - 1, num_file - 1)

        for ind in range(1, king_bottom_left_count + 1):
            king_str = chr(ord(white_king_file) - ind) + str(num_rank - ind)
            piece_color_at_sq = self.game_board.get_piece_color_atsq(king_str)

            if piece_color_at_sq == 'w':
                break 
            
            if piece_color_at_sq == 'b':
                piece_type_at_sq = self.game_board.get_piece_type_atsq(king_str)
                if piece_type_at_sq == 'B' or piece_type_at_sq == 'Q':
                    return True 
                
                if piece_type_at_sq == 'K' and ind == 1:
                    return True 
                
                break
            continue


        # check bottom right
        queen_bottom_right_count = min(num_rank - 1, 8 - num_file)

        for ind in range(1, queen_bottom_right_count + 1):
            queen_str = chr(ord(white_king_file) + ind) + str(num_rank - ind)
            piece_color_at_sq = self.game_board.get_piece_color_atsq(king_str)

            if piece_color_at_sq == 'w':
                break 
            
            if piece_color_at_sq == 'b':
                piece_type_at_sq = self.game_board.get_piece_type_atsq(king_str)
                if piece_type_at_sq == 'B' or piece_type_at_sq == 'Q':
                    return True 
                
                if piece_type_at_sq == 'K' and ind == 1:
                    return True 
                
                break
            
            continue 


        
        # from rook code
        # if-statement to check the 4 bounds of the king -- upper, lower, left, right

        # check limits of the top squares
        for sq_rank in range(num_rank + 1, 8 + 1):
            if self.game_board.get_piece_color_atsq(white_king_file + str(sq_rank)) == 'w':
                break # end immediately; break only breaks out of one loop so we're fine 
            
            if self.game_board.get_piece_color_atsq(white_king_file + str(sq_rank)) == 'b':
                if self.game_board.get_piece_type_atsq(white_king_file + str(sq_rank)) in ['R', 'Q']:
                    return True
                
                if self.game_board.get_piece_type_atsq(white_king_file + str(sq_rank)) == 'K' and (sq_rank - num_rank) == 1:
                    return True
                
                break
            continue 
        

        # check bottom
        for sq_rank in range(num_rank - 1, 0, -1): # backwards loop
            if self.game_board.get_piece_color_atsq(white_king_file + str(sq_rank)) == 'w':
                break # end immediately; break only breaks out of one loop so we're fine 
            
            if self.game_board.get_piece_color_atsq(white_king_file + str(sq_rank)) == 'b':
                if self.game_board.get_piece_type_atsq(white_king_file + str(sq_rank)) in ['R', 'Q']:
                    return True
                
                if self.game_board.get_piece_type_atsq(white_king_file + str(sq_rank)) == 'K' and (num_rank - sq_rank) == 1:
                    return True
                
                break
            continue 
        

        # check right
        # rank stays constant
        for sq_file_ord in range(ord(white_king_file) + 1, ord('h') + 1):
            # use chr(x) whenever
            if self.game_board.get_piece_color_atsq(chr(sq_file_ord) + white_king_rank) == 'w':
                break
            
            if self.game_board.get_piece_color_atsq(chr(sq_file_ord) + white_king_rank) == 'b':
                enemy_piece_type = self.game_board.get_piece_type_atsq(chr(sq_file_ord) + white_king_rank)
                if enemy_piece_type == 'R' or enemy_piece_type == 'Q' or (enemy_piece_type == 'K' and sq_file_ord - ord(white_king_file) == 1):
                    return True
                
                break
            continue
        
        for sq_file_ord in range(ord(white_king_file) - 1, ord('a') - 1, -1):
            # use chr(x) whenever
        
            if self.game_board.get_piece_color_atsq(chr(sq_file_ord) + white_king_rank) == 'w':
                break
            
            if self.game_board.get_piece_color_atsq(chr(sq_file_ord) + white_king_rank) == 'b':
                enemy_piece_type = self.game_board.get_piece_type_atsq(chr(sq_file_ord) + white_king_rank)
                if enemy_piece_type == 'R' or enemy_piece_type == 'Q' or (enemy_piece_type == 'K' and ord(white_king_file) - sq_file_ord == 1):
                    return True
                
                break
            continue

        # end of checking if king is in check
        return False

    # todo!
    def is_black_king_in_check(self):
        # basically the same as the method above
        # these 2 methods should really only be used by the chess game class

        # from current position, check if black king is in check
        return

    

    def printboard(self): 
        # should only be used for debugging
        self.game_board.printboard()
        return



    # also add castling in here
    def generate_white_candidate_moves(self):

        # candidate_moves is a list of all possible candidate moves
        # candidate_moves is a list of pairs, (a, b, c) where a is the starting square and b is the ending square of a piece
        # and c is the type of piece to promote to (N, B, R, Q) upon promotion if it is a pawn. otherwise it does not exist.
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

        
        # check legality of all moves
        # check if anything is pinned + if king is in check

        # NOTE -- this works even if the king is already in check -- as it will automatically reject anything that leaves the king in check

        # idea: move piece to location, then check if white king is in check at that point in time
        actual_candidate_moves = []

        for pair in candidate_moves:
            # move piece to location then reset it
            final_square_piece_type = self.game_board.get_piece_type_atsq(pair[1])
            
            final_square_piece_color = self.game_board.get_piece_color_atsq(pair[1])

            # move piece to square and check if king is in check
            self.game_board.move_piece(pair[0], pair[1])


            # modify the list of pieces if anything's moved etc etc so everything makes more sense
            piece_list = self.white_piece_locations.copy() # do a deep copy
            piece_list.pop(self.white_piece_locations.index(pair[0]))
            piece_list.append(pair[1])
            


            if self.is_white_king_in_check(piece_list):
                # don't add the pair
                pass 
            else:
                actual_candidate_moves.append(pair)
            
            # reset position
            if final_square_piece_type != -1:
                # piece exists
                self.game_board.move_piece(pair[1], pair[0])
                self.game_board.set_piece_tosq(pair[1], final_square_piece_type, final_square_piece_color)
                continue
            else:
                self.game_board.move_piece(pair[1], pair[0])
            continue # end for loop

        return actual_candidate_moves       
        # end white_candidate_moves
        

    # todo
    def generate_black_candidate_moves(self):
        # ehrm tbd
        pass 
   


    def send_white_move(self, start_sq, end_sq, pawn_promotion=None):
        # check legality of move
        # pawn_promotion is a string like 'Q' or 'N' -- piece to promote to
        
        if pawn_promotion is None and (start_sq, end_sq) not in self.generate_white_candidate_moves():
            # ehrm move is bad
            return -1
        
        if pawn_prmotion is not None and (start_sq, end_sq, pawn_promotion) not in self.generate_white_candidate_moves():
            # move is still bad
            return -1
        
        # ok move seems legit
        self.game_board.send_move(start_sq, end_sq)
        if end_sq in self.black_piece_locations:
            self.black_piece_locations.remove(end_sq) # piece is captured
        
        self.white_piece_locations.remove(start_sq)
        self.white_piece_locations.append(end_sq)
        
        self.white_turn = False
        
        # ok eval board
        if self.is_black_king_in_check():
            self.black_king_check = True


        # update last_pawn_move (if pawn moved from e.g. c2 to c4)
        if self.game_board.get_piece_type_atsq(end_sq) == 'P' and start_sq[1] == '2' and start_sq[0] == end_sq[0]:
            # chat im pretty sure the pawn just moved two squares
            self.last_pawn_move = start_sq[0] + chr(ord(start_sq[1]) + 1) # yippee
        else:
            self.last_pawn_move = 'z0' # null value

        
        # update castling -- TODO
        if self.game_board.get_piece_type_atsq(end_sq) == 'K':
            # no castling
            self.white_kingside_castling = False
            self.white_queenside_castling = False 
        
        # ehrm add section about if a rook moves + the castling priviledges there + if captured + all that stuff


        
        return
    
    # todo
    def send_black_move(self, start_sq, end_sq):
        return



    def load_pos_from_fen(self, fen):
        # fen is the string
        # idea: reset board, then add pieces and update everything else accordingly


        # reset everything
        self.game_board.clear_board() # back to dots
        self.white_piece_locations = []
        self.black_piece_locations = []

        self.white_kingside_castling = False
        self.white_queenside_castling = False
        self.black_kingside_castling = False
        self.black_queenside_castling = False 
        


        fen_components = fen.split() # is list of length 6
        # fen[0] -- the actual fen string
        # fen[1] -- turn? (w/b)
        # fen[2] -- castling priviledge? KQ -- white can kingside queenside, k -- black can kingside, can be '-' for none
        # fen[3] -- en passant target square -- e.g. c6 if c7 --> c5 last move
        # fen[4] -- halfmove clock
        # fen[5] -- move number


        # tackle fen string, fen[0]
        # starts from rank 8 and works downward to rank 1
        # uppercase --> black piece, lowercase --> white piece
        rank_pointer = 0
        file_pointer = 0 # pointers -- (0, 0) means a8, (2, 3) means d6 -- c3 = file/rank

        for char in fen_components[0]:
            if char == '/':
                # move on yippee
                rank_pointer += 1
                file_pointer = 0
                continue

            if ord(char) > 48 and ord(char) < 57:
                # char is a number between 1 and 8
                file_pointer += int(char)
                continue
            
            
            if char.lower() == char:
                # is a black piece
                
                # convert (rank_pointer, file_pointer) to actual square
                actual_rank = str(8 - rank_pointer)
                actual_col = chr(ord('a') + file_pointer)
                self.black_piece_locations.append(actual_col + actual_rank) # file, rank

                # put piece on board
                self.game_board.set_piece_tosq(actual_col + actual_rank, char.upper(), 'b')
                file_pointer += 1
                continue
            
            # piece is a white piece
            actual_rank = str(8 - rank_pointer)
            actual_col = chr(ord('a') + file_pointer)
            self.white_piece_locations.append(actual_col + actual_rank)

            self.game_board.set_piece_tosq(actual_col + actual_rank, char, 'w')
            file_pointer += 1
            continue
        

        # tackle fen[1] --> fen[5]
        # from above:
        # fen[1] -- turn? (w/b)
        # fen[2] -- castling priviledge? KQ -- white can kingside queenside, k -- black can kingside, can be '-' for none
        # fen[3] -- en passant target square -- e.g. c6 if c7 --> c5 last move
        # fen[4] -- halfmove clock
        # fen[5] -- move number


    
        self.white_turn = (fen[1] == 'w') # fen[1]
        

        # castling priviledges
        if fen[2].find('K') != -1:
            self.white_kingside_castling = True
            
        if fen[2].find('Q') != -1:
            self.white_queenside_castling = True

        if fen[2].find('k') != -1:
            self.black_kingside_castling = True

        if fen[2].find('q') != -1:
            self.black_queenside_castling = True


        # target square en passant -- fen[3]
        if fen[3] == '-':
            self.last_pawn_move = 'z0'
        else:
            self.last_pawn_move = fen[3] # :D
        
        
        # halfmove clock, fen[4]
        self.half_move_clock = fen[4]

        self.move_number = fen[5]
        return #! we done




        

        


    
    # end class


game = ChessGame()
game.load_pos_from_fen('rn2kb1r/p2p1ppp/q3p3/1Rpn4/2K1P3/1PP5/1P1P1PPP/1NBQ1BNR w kq - 5 12')
game.printboard()
print(game.generate_white_candidate_moves())
print(game.is_white_king_in_check())