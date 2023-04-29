from random import randint
from classes import Player, Table

# verificar se as escolhas do player são vencedoras - comparar com as table.win_combinations
def checkWinCombination(st, table):
    
    for i in table.win_combinations:
        count=0
        for n in i:
            if n in st:
                count += 1
                if count == 3:
                    return True
    return False


#generate random input for computer choice
def computer_input():
    return randint(1, 9)




# define a full shift for a player
def shift(player, table):
    if (len(table.picked) == len(table.table)):
        print ("The table is full")
        player.win_status=True
        return
    else:
        if (player.name == "Computer"):
            playerin = str(computer_input())
        else:
            playerin = input("{} choose: ".format(player.name))

        #check if the input is valid            
        if (playerin in table.table) and (playerin not in table.picked) and (len(playerin) == 1): 
            
            if (player.name == "Computer"):
                print("Computer choose: ", playerin)
            player.choices += playerin
            table.picked += playerin

            #actualizations of the table.n... variables for printing new board 
            if (player.number == 1):
                if (playerin == "1"):
                    table.n1 = "x"
                elif (playerin == "2"):
                    table.n2 = "x"
                elif (playerin == "3"):
                    table.n3 = "x"
                elif (playerin == "4"):
                    table.n4 = "x"
                elif (playerin == "5"):
                    table.n5 = "x"
                elif (playerin == "6"):
                    table.n6 = "x"
                elif (playerin == "7"):
                    table.n7 = "x"
                elif (playerin == "8"):
                    table.n8 = "x"
                elif (playerin == "9"):
                    table.n9 = "x"
            elif (player.number == 2):
                if (playerin == "1"):
                    table.n1 = "o"
                elif (playerin == "2"):
                    table.n2 = "o"
                elif (playerin == "3"):
                    table.n3 = "o"
                elif (playerin == "4"):
                    table.n4 = "o"
                elif (playerin == "5"):
                    table.n5 = "o"
                elif (playerin == "6"):
                    table.n6 = "o"
                elif (playerin == "7"):
                    table.n7 = "o"
                elif (playerin == "8"):
                    table.n8 = "o"
                elif (playerin == "9"):
                    table.n9 = "o"

            print (table.board.format(n1=table.n1, n2=table.n2, n3=table.n3, n4=table.n4, n5=table.n5, n6=table.n6, n7=table.n7, n8=table.n8, n9=table.n9))
            
            #check players choices against possible win combninations 
            if len(player.choices) > 2:
                check_win = checkWinCombination(player.choices, table)          
                if check_win == True:
                    player.score += 1
                    player.win_status = True
                    print(player.name, " WON the game!!!")
                    return 
                else:
                    return 
            else:
                return
        else:
            shift(player, table)



# player1 = Player()
# table1 = Table()
# # print(checkWinCombination("123", table1))
# print(type(player1.number))