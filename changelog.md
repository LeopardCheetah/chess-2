Changelog -- where I'll keep progress updates.

11/26 23:53 -- Repo was created 
            -- Added everything else I need from LeopardBot

11/29 15:41 -- finished board.py (I think). Am starting on getting an actual chess game.    
11/29 17:14 -- in the middle of generating all candidate moves     
11/29 17:28 -- finished generating all possible pawn moves (+ en passant, promotion)    
    
11/29 19:09 -- finished up knight possible moves    
    
<Note: I just coded something cool so maybe I should do a massive overhaul of the code i just wrote but nah>    
11/29 23:40 -- finished up king, rook, bishop, queen moves (in that order). IT WORKS! (also haven't accounted for checks and the like)    
11/30 00:47 -- finished up load from FEN!!        


11/30 13:24 -- finished isWhiteKingInCheck command
11/30 14:33 -- finished whiteCandidateMoves!! -- note that castling is still **impossible** and i really have no intention of doing it

12/02 00:16 -- finished send_white_move (now just needa do send_black_move); seems like all there is to do is to code everything for black and then win!!

----

12/08 12:23 -- updated is_black_king_in_check and black_candidate_moves
12/08 12:52 -- debugged black_king_in_check (it was a variable error bruh) and did send_black_move. i think random bot is ready to be coded :D 


todolist (so i dont forget when i wake up):    
- finish everything for black
- make random mover bot!  
- make a wrapper class (again) to actually play chess

- deploy to lichess?

other also kinda important:
- incorporate castling
- figure out the half move clock ( + 50 move rule, 3-fold repetition)
    

    