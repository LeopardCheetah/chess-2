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

todolist (so i dont forget when i wake up):    
- finish up generate white candidate moves -- notably figure out how to find the legality of these moves (code white king in check probably), then also figure out castling    
- figure out send_move so that it actually records piece positions before and after etc. etc.    
- make random mover bot!    
    
    