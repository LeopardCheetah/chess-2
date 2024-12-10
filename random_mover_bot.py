# random_mover_bot game not the actual bot that can (maybe) be deployed to lichess

import chessgame # chessgame.py
import time
import sys # for quitting
import random # for randomly selecting moves





def clear():
    print('\033[2J\033[H')
    return 

clear()
print("Note: DO NOT SCROLL thanks")
time.sleep(2)

clear()



print("Welcome! Go play Random Mover Bot, a bot that selects a random move!")
print("Note: Castling is not built in. En Passant is (but it hasn't been tested).")
print("Would you like to play as White or Black?")
player_color_in = input("> ").strip().lower()

player_color = -1
if player_color_in[0] == 'w':
    player_color = 0

# later todo -- fix this
if player_color_in[0] == 'b':
    player_color = 1
    sys.exit(f"Black is an unsupported player color. Do not choose it for now.")

if player_color_in[0] not in ['w', 'b']:
    sys.exit(f"uhhhh '{player_color_in}' is not a valid player color.")




# ok player_color is determined
# make new game

game = chessgame.ChessGame()

game_finished = False
while not game_finished:

    # check if game is finished
    white_turn = game.white_turn

    if white_turn and len(game.generate_white_candidate_moves()) == 0:
        # game is over
        game_finished = True

        clear()
        game.printboard()
        print()
        print("seems like white lost :(")
        continue

    if not white_turn and len(game.generate_black_candidate_moves()) == 0:
        # game is once again over
        game_finished = True

        clear()
        game.printboard()
        print()
        print("seems like black lost :(")
        continue



    clear()
    game.printboard() # print board





    if game.white_turn and player_color == 0:
        # player is white
        # query for move, it is player's turn
        # query in the form [start_sq] [end_sq] [promotion]
        
        print("Please enter your move in the form '[starting square] [ending square] [promotion]'. If you're move does not need promotion, leave it blank.")
        print("For example, entering in 'e2 e4' will move a piece (if it exists) from e2 to e4. Similarly, 'a7 a8 N' will move a piece from a7 to a8 and attempt to promote it to a knight.")
        print()
        print("If you want to castle, use 0-0 or 0-0-0 respectively (use zeroes).")
    
        move = input("> ")
        move_components = move.strip().split()

        # we castlign
        if move == '0-0' or move == '0-0-0':
            if move == '0-0':
                # kingside castling
                status = game.send_white_move('e1', 'g1', 'C')
                if status == 0:
                    continue
                
                # status is bad
                print("uh castling doesn't work try something else sorry")
                time.sleep(1)
                continue
            
            # move = 0-0-0
            status = game.send_white_move('e1', 'c1', 'C')
            if status == 0:
                continue
            
            print("uh queenside castling doesn't work rigth now sorry")
            time.sleep(1.1)
            continue




        if len(move_components) == 2:
            status = game.send_white_move(move_components[0], move_components[1])
            if status == 0:
                continue
            
            # status is bad
            print("That move didn't send for some reason. Please try again.")
            time.sleep(1)
            continue
        

        if len(move_components) == 3:
            status = game.send_white_move(move_components[0], move_components[1], move_components[2])
            if status == 0:
                continue
            
            print("That move didn't send for some reason. Please try again.")
            time.sleep(1)
            continue
        
        print("Your input is off somehow. Please try again.")
        time.sleep(1)
        continue
    

    if game.white_turn is False and player_color == 0:
        # it's black's move, and black is the random mover bot
        possible_moves = game.generate_black_candidate_moves()
        move_pair = random.choice(possible_moves) # randomly select one
        # play move

        if len(move_pair) == 2:
            
            game.send_black_move(move_pair[0], move_pair[1])
            continue
        
        game.send_black_move(move_pair[0], move_pair[1], move_pair[2])
        continue
        
        # randomly select one
    




    continue # haven't coded when player_color == 1




