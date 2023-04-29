from msilib.schema import Class
import random
from classes import Player, Table
from functions import checkWinCombination, shift 

intro = """
#######################################################
#######################################################
####               ####################################
####   x | x | o   ####################################
####  ---+---+---  #####                         ######
####   o | o | x   #####  Lets Play Tic-Tac-Toe  ######
####  ---+---+---  #####                         ######
####   x | x | o   ####################################
####               ####################################
#######################################################
#######################################################
"""


#Complete Game
def play_game():
    print(intro)
    print("Number of Players:")
    # verify if the input is a valid number of players
    valid_number_of_players = False
    while (valid_number_of_players == False):
        number_of_players = input("Chose 1 or 2\n")
        if (number_of_players == "1" or number_of_players == "2"):
            valid_number_of_players = True

    #Creating players for the right input    
    table = Table()
    player_name_input = input("Enter Player1 Name:\n")
    player1 = Player(player_name_input, 1)
    if number_of_players == "1":
        player2 = Player()
    else:
        player_name_input = input("Enter Player2 Name:\n")
        player2 = Player(player_name_input)

    #using a flip coin game to ddsecide who will go first
    print("\nLet's Start the Game...")
    print("We need to decide who will start the game..")
    player1_coin = input("choose Head or Tail...\n")
    coin_side = random.choice(["head", "tail"])
    print("The coin has flipped... and the face turned up is...\n ", coin_side)

    #defining first and second player
    if player1_coin.lower() == coin_side:
        print(player1.name, " will be the first player\n")
        print(table.board.format(n1=table.n1, n2=table.n2, n3=table.n3, n4=table.n4, n5=table.n5, n6=table.n6, n7=table.n7, n8=table.n8, n9=table.n9),"\n")
        while (player1.win_status == False) or (player2.win_status ==False):
            shift(player1, table)
            if (player1.win_status == True):
                break
            shift(player2, table)
            if (player2.win_status == True):
                break
            
    else:
        print(player2.name, " will be the first player\n")
        print(table.board.format(n1=table.n1, n2=table.n2, n3=table.n3, n4=table.n4, n5=table.n5, n6=table.n6, n7=table.n7, n8=table.n8, n9=table.n9),"\n")
        while (player1.win_status == False) or (player2.win_status ==False):
            shift(player2, table)
            if (player2.win_status == True):
                break
            shift(player1, table)
            if (player1.win_status == True):
                break
            

    return 
    


    



print(play_game())








