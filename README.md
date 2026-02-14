# Golden Jackpot Casino

A fun and engaging slot machine game built with Python and Streamlit. Try your luck at the casino and see if you can hit the jackpot!

## Features

- **Deposit Funds**: Add money to your account to start playing
- **Flexible Betting**: Choose how many lines to bet on (1-3 lines) and set your bet amount
- **Slot Machine**: Spin a 3x3 grid of symbols and see if you win
- **Win Detection**: Automatically checks for winning combinations
- **Balance Tracking**: Keep track of your balance, total wagered, and total winnings
- **Balance History**: Visual chart showing how your balance changes over time

## Symbols

The game features four symbols with different values:
- **A** (rare) - Highest payout
- **B** - Medium-high payout
- **C** - Medium payout
- **D** (common) - Lowest payout

## Installation

1. Install the required dependencies:
```
bash
pip install -r requirements.txt
```

2. Run the game:
```
bash
streamlit run app.py
```

3. Open your browser and navigate to the URL shown (usually http://localhost:8501)

## How to Play

1. Deposit some funds using the deposit button
2. Select how many lines you want to bet on (1, 2, or 3)
3. Set your bet amount per line
4. Click "SPIN" to play
5. If you get matching symbols in a row, you win!

## Tech Stack

- **Python**: Core programming language
- **Streamlit**: Web framework for the UI
- **Plotly**: For balance history charts
- **Random**: For generating slot machine outcomes

## License

This project is for educational and entertainment purposes only. Play responsibly!
