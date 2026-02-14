import random


MAX_LINES = 3                    # global constant declared in all capitals
MAX_BET = 1000
MIN_BET = 1

ROWS = 3
COLS = 3

symbol_count = {
    "A": 2,
    "B": 4,
    "C": 6,
    "D": 8
}

symbol_value = {
    "A": 5,
    "B": 4,
    "C": 3,
    "D": 2
}


def validate_deposit(amount):
    try:
        amount = int(amount)
        if amount <= 0:
            return False, 0, "Amount must be greater than zero"
        return True, amount, None
    except:
        return False, 0, "Please enter a valid number"


def validate_lines(lines):
    try:
        lines = int(lines)
        if lines < 1 or lines > MAX_LINES:
            return False, 0, "Enter a valid number of lines"
        return True, lines, None
    except:
        return False, 0, "Please enter a valid number"


def validate_bet(bet, balance, lines):
    try:
        bet = int(bet)

        if bet < MIN_BET or bet > MAX_BET:
            return False, 0, f"Bet must be between ${MIN_BET} and ${MAX_BET}"

        if bet * lines > balance:
            return False, 0, "You don't have enough money"

        return True, bet, None
    except:
        return False, 0, "Please enter a valid number"


def check_winnings(columns, lines, bet, values):
    winnings = 0
    winning_lines = []

    for line in range(lines):
        symbol = columns[0][line]
        win = True

        for column in columns:
            if column[line] != symbol:
                win = False
                break

        if win:
            winnings += values[symbol] * bet
            winning_lines.append(line + 1)

    return winnings, winning_lines


def get_slotmachine_spin(rows, cols, symbols):
    all_symbols = []
    for symbol in symbols:
        for _ in range(symbols[symbol]):
            all_symbols.append(symbol)

    columns = []

    for _ in range(cols):
        column = []
        current = all_symbols[:]

        for _ in range(rows):
            value = random.choice(current)
            current.remove(value)
            column.append(value)

        columns.append(column)

    return columns


def spin(lines, bet, balance):
    total_bet = bet * lines

    slots = get_slotmachine_spin(ROWS, COLS, symbol_count)

    winnings, winning_lines = check_winnings(slots, lines, bet, symbol_value)

    balance += winnings - total_bet

    return {
        "slots": slots,
        "winnings": winnings,
        "winning_lines": winning_lines,
        "total_bet": total_bet,
        "net_gain": winnings - total_bet,
        "new_balance": balance
    }


def format_slots_for_display(columns):
    rows = len(columns[0])
    grid = []

    for r in range(rows):
        row = []
        for c in range(len(columns)):
            row.append(columns[c][r])
        grid.append(row)

    return grid