import random
from colorama import Style, init, Fore

init(autoreset = True)

def display(board):
    print(" ")
     
    def color(cell):
        if cell == "O":
            return Fore.BLUE + cell + Style.reset_all
        elif cell == "X":
            return Fore.RED + cell + Style.reset_all
        else:
            return Fore.YELLOW + cell + Style.reset_all
        
    print(" " + color(board[0]) + "|" + color(board[1]) + "|" + color(board[2]))
    print(Fore.GREEN + "-----------")
    print(" " + color(board[3]) + "|" + color(board[4]) + "|" + color(board[5]))
    print(Fore.GREEN + "-----------")
    print(" " + color(board[6]) + "|" + color(board[7]) + "|" + color(board[8]))
    print()

def choice():
    symbol=""
    while symbol not in ["X", "O"]:
        symbol = input("Do you want to be X or O ?")
        
    if symbol == "X":
        return("X", "O")
    else:
        return("O", "X")
    
def moves(board, symbol):
    move = -1
    while move not in range (0, 10) or not board[move - 1].isdigit():
        try:
            move = int(input("Enter your move"))
            if move not in range(1, 10) or not board[move - 1].isdigit():
                print("invalid_move")
        except ValueError:
            print("Enter a number between 1-9")
    board [move-1] = symbol
    
def ai_move()