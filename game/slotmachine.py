import random


MAX_LINES = 3
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
    """Validate deposit amount. Returns (success: bool, value: int, error: str)"""
    try:
        amount_int = int(amount)
        if amount_int <= 0:
            return False, 0, "Amount must be greater than zero"
        return True, amount_int, None
    except ValueError:
        return False, 0, "Please enter a valid number"


def validate_lines(lines):
    """Validate number of lines. Returns (success: bool, value: int, error: str)"""
    try:
        lines_int = int(lines)
        if 1 <= lines_int <= MAX_LINES:
            return True, lines_int, None
        else:
            return False, 0, f"Enter a valid number of lines (1-{MAX_LINES})"
    except ValueError:
        return False, 0, "Please enter a valid number"


def validate_bet(bet, balance, lines):
    """Validate bet amount. Returns (success: bool, value: int, error: str)"""
    try:
        bet_int = int(bet)
        if bet_int < MIN_BET or bet_int > MAX_BET:
            return False, 0, f"Bet must be between ${MIN_BET} and ${MAX_BET}"
        
        total_bet = bet_int * lines
        if total_bet > balance:
            return False, 0, f"Insufficient balance. Your balance: ${balance}, Total bet: ${total_bet}"
        
        return True, bet_int, None
    except ValueError:
        return False, 0, "Please enter a valid number"


def check_winnings(columns, lines, bet, values):
    """
    Check winning lines and calculate total winnings.
    Returns (winnings: int, winning_lines: list)
    """
    winnings = 0
    winning_lines = []

    for line in range(lines):
        symbol = columns[0][line]
        won = True

        for column in columns:
            if column[line] != symbol:
                won = False
                break
        
        if won:
            winnings += values[symbol] * bet
            winning_lines.append(line + 1)

    return winnings, winning_lines


def get_slotmachine_spin(rows, cols, symbols):
    """
    Generate a random slot machine spin.
    Returns columns: list of lists representing the slot grid
    """
    all_symbols = []
    for symbol, count in symbols.items():
        for _ in range(count):
            all_symbols.append(symbol)

    columns = []
    for _ in range(cols):
        column = []
        current_symbols = all_symbols[:]
        for _ in range(rows):
            value = random.choice(current_symbols)
            current_symbols.remove(value)
            column.append(value)
        columns.append(column)
    
    return columns


def spin(lines, bet, balance):
    """
    Execute a spin with given parameters.
    Returns a dict with game results
    """
    total_bet = bet * lines
    
    # Generate spin results
    slots = get_slotmachine_spin(ROWS, COLS, symbol_count)
    
    # Calculate winnings
    winnings, winning_lines = check_winnings(slots, lines, bet, symbol_value)
    
    # Calculate new balance
    net_gain = winnings - total_bet
    new_balance = balance + net_gain
    
    return {
        "slots": slots,
        "winnings": winnings,
        "winning_lines": winning_lines,
        "total_bet": total_bet,
        "net_gain": net_gain,
        "new_balance": new_balance
    }


def format_slots_for_display(columns):
    """
    Convert slot columns into a grid format for display.
    Returns a list of rows (each row is a list of symbols)
    """
    rows = len(columns[0])
    grid = []
    for row in range(rows):
        row_data = [columns[col][row] for col in range(len(columns))]
        grid.append(row_data)
    return grid
