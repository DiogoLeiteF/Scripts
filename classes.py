class Player:
    def __init__(self, name="Computer", number = 2):
        self.name = name
        self.number = number
        self.choices = ""
        self.score = 0
        self.win_status = False
        


    def __repr__(self) -> str:
        return "Player {}".format(self.name)

    def get_name(self):
        return self.name

    def get_choices(self):
        return self.choices
    
    def set_choices(self, choice):
        self.choices+=choice

    def get_score(self):
        return self.score

    def set_score(self, score):
        self.score = score
    


class Table:
    def __init__(self):
        self.table = "123456789"
        self.win_combinations = ["123", "456", "789", "147", "258", "369", "159", "357"]
        self.picked = ""
        self.n1 = "1"
        self.n2 = "2"
        self.n3 = "3"
        self.n4 = "4"
        self.n5 = "5"
        self.n6 = "6"
        self.n7 = "7"
        self.n8 = "8"
        self.n9 = "9"
        self.board = """        
#######################################################
#######################################################
####               ####################################
####   {n1} | {n2} | {n3}   ####################################
####  ---+---+---  #####                         ######
####   {n4} | {n5} | {n6}   #####    Pick your number:    ######
####  ---+---+---  #####                         ######
####   {n7} | {n8} | {n9}   ####################################
####               ####################################
#######################################################
#######################################################
"""
# .format(n1=self.n1, n2=self.n2, n3=self.n3, n4=self.n4, n5=self.n5, n6=self.n6, n7=self.n7, n8=self.n8, n9=self.n9)
    
    def __repr__(self):
        return "possible win combinations {}".format(", ".join(self.win_combinations))

    def set_picked(self, n):
        self.picked += n



# table = Table()

# print(table.board)