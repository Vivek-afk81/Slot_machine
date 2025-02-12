import random


MAX_LINES=3                  # global constant declared in all capitals
MAX_BET=1000
MIN_BET=1

ROWS =3
COLS =3

symbol_count ={
    "A": 2,
    "B": 4,
    "C": 6,
    "D": 8 
}

symbol_value ={
    "A": 5,
    "B": 4,
    "C": 3,
    "D": 2 
}

def check_winnings(columns,lines,bet,values):
    winnings=0
    winning_lines=[]

    for line in range(lines):
        symbol=columns[0][line]
        won=True

        for column in columns:
            if column[line]!=symbol:
                won=False
                break
        if won:
            winnings+=values[symbol]*bet
            winning_lines.append(line+1)  
              
    return winnings,winning_lines


def get_slotmachine_spin(rows,cols,symbols):
    all_symbols=[]
    for symbol,symbol_count in symbols.items():
        for _ in range(symbol_count):    #when you want to loop something but you dont want to do anything about the counter that iterattes value we use "_" so we dont have an unused variable
            all_symbols.append(symbol)

    columns=[]          #storing columns instead of rows
    for _ in range(cols):
        column=[]
        current_symbols = all_symbols[:]  # used to make the copy of the list ote the importance of the colon
        for _ in range(rows):
            value= random.choice(current_symbols)      #here we have to make a copy oof the listr all_symbols because we do not want a symbol to come repeatdely than their count
            current_symbols.remove(value)
            column.append(value)

        columns.append(column)
    return columns            


def print_slot_machine(columns):
    for row in range(len(columns[0])):       #this assumes we have atleast one column so if we pass it without: it would crash
        for i,column in enumerate(columns):
            if i!=len(columns)-1:
                print(column[row],end=" | ")     #end the line with |
            else:
                print(column[row],end="")
        print()                


def deposit():
    while True:
        amount=input("what would you like to deposit ?")
        if amount.isdigit():        # checkig if the user entered a number (used isdigit()  function)
            amount=int(amount)     # now converting the digit into it data type
            if amount>0:
                break               # this break keyword ends the while loop
            else:
                print("amount must be greater than zero")
        else:
            print("please enter a valid number")    

    return amount

def get_number_of_lines():
    while True:
        lines=input(f"enter the number of lines you want to bet on (1-{MAX_LINES})? ")
        if lines.isdigit():        
            lines=int(lines )    
            if 1<=lines<=MAX_LINES:    #to check if the value is between the bounds
                break               
            else:
                print("enter valid number of lines")
        else:
            print("please enter a valid number")    

    return lines

def get_bet():
    while True:
        amount=input("what would you like to bet ?")
        if amount.isdigit():        
            amount=int(amount)    
            if MIN_BET<=amount<=MAX_BET:
                break              
            else:
                print(f"amount must be greater than or equalt to {MIN_BET}")
        else:
            print("please enter a valid number")
    return amount            

def spin(balance):
    lines=get_number_of_lines()
    while True:
         bet=get_bet()
         total_bet =bet * lines

         if total_bet>balance:
             print(f"you do not have enough balance to continue,if you want to conntinue add more money")
         else:
             break
        

   
    
    print(f"You are betting ${bet} on {lines} lines.Total bet is equal to $ {total_bet}")


    slots = get_slotmachine_spin(ROWS,COLS,symbol_count)
    print_slot_machine(slots)
    winnings,winning_lines=check_winnings(slots,lines,bet,symbol_value) 
    print(f"You won ${winnings}.")
    print(f"you won on lines: ", *winning_lines)
    return winnings-total_bet

def main():                             #used when the user wants to play again we can just call this function again
    balance=deposit()
    while True:
        print(f"current balance is ${balance}")
        answer=input("press enter to play (q to quit)")
        if answer=="q":
            break
        balance+=spin(balance)
    print(f"you lest with ${balance}")    



main()    

         