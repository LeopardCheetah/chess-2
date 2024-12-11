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
       
12/08 14:30 -- RANDOM MOVER BOT IS DONE!! YOU CAN NOW PLAY CHESS AGAINST IT       
12/08 14:40 -- Fixed en passant bug RRRRRRAAAAHHHHHHHHHH      
     
12/09 15:45 -- (in class) -- start castling implementation; did white_candidate_moves. need to do white_send_move, black_candidate_moves, black_send_moves, and update random mover bot.       
     
12/10 12:52 -- (in stats) -- finish black_candidate_moves with castling     
12/10 13:36 -- finished white_send_move and black_send_move
12/10 14:00 -- finish castling implementation!    
   
12/11 09:27 -- minor changes, implemented stalemate    
12/11 09:45 -- implemented so that player can play as black     
12/11 09:54 -- implemented thing so that the board rotates when player is playing as black
12/11 09:58 -- made board color changes easier






things to consider doing:   
- deploy to lichess?   

also kinda important things:   
- figure out the half move clock (50 move rule)    
- do the inefficient material thing (e.g. KN vs K)      
- implement 3-fold repetition    
- figure out draw offers + code in resignation

    