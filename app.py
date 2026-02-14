import streamlit as st
import plotly.graph_objects as go
import pandas as pd
from game.slotmachine import (
    get_slotmachine_spin,
    check_winnings,
    ROWS,
    COLS,
    symbol_count,
    symbol_value,
)


st.set_page_config(
    page_title="Golden Jackpot Casino",
    page_icon="🎰",
    layout="wide"
)

# Theme
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Bebas+Neue&family=Orbitron:wght@400;700;900&display=swap');

.stApp {
    background: linear-gradient(135deg, #1a0e0e 0%, #2d1b1b 50%, #1a0e0e 100%);
    color: #ffd700;
}

.main-title {
    font-family: 'Bebas Neue';
    font-size: 4rem;
    text-align: center;
    color: #ffd700;
    text-shadow: 0 0 20px #ff8c00;
}

.subtitle {
    text-align: center;
    color: #d4af37;
    font-family: 'Orbitron';
    letter-spacing: 3px;
    margin-bottom: 30px;
}

.balance-box {
    background: #1a0e0e;
    border: 3px solid #ffd700;
    border-radius: 15px;
    padding: 20px;
    text-align: center;
    box-shadow: 0 0 20px rgba(255,215,0,0.6);
    margin-bottom: 20px;
}

.slot-frame {
    background: #1a0e0e;
    border: 4px solid #ffd700;
    border-radius: 20px;
    padding: 20px;
    margin: 20px 0;
}

.slot-symbol {
    font-size: 3rem;
    text-align: center;
    padding: 20px;
    border: 2px solid #d4af37;
    border-radius: 10px;
    background: #2d1b1b;
}

.slot-symbol-winning {
    font-size: 3rem;
    text-align: center;
    padding: 20px;
    border: 3px solid #ffd700;
    border-radius: 10px;
    background: #3d2b2b;
    box-shadow: 0 0 25px #ffd700;
}

.stButton>button {
    background: linear-gradient(145deg, #ffd700, #d4af37);
    color: black;
    font-weight: bold;
    border-radius: 8px;
    border: 2px solid #ffd700;
}
</style>
""", unsafe_allow_html=True)


# SESSION STATE INIT

if "balance" not in st.session_state:
    st.session_state.balance = 1000

if "slots" not in st.session_state:
    st.session_state.slots = None

if "winning_lines" not in st.session_state:
    st.session_state.winning_lines = []

if "total_bet" not in st.session_state:
    st.session_state.total_bet = 0

if "winnings" not in st.session_state:
    st.session_state.winnings = 0

if "spins_count" not in st.session_state:
    st.session_state.spins_count = 0

if "total_wagered" not in st.session_state:
    st.session_state.total_wagered = 0

if "total_won" not in st.session_state:
    st.session_state.total_won = 0

if "balance_history" not in st.session_state:
    st.session_state.balance_history = [1000]


# SIDEBAR (Stats Only)

with st.sidebar:
    st.markdown("### GAME STATS")
    st.metric("Spins", st.session_state.spins_count)
    st.metric("Total Wagered", f"${st.session_state.total_wagered}")
    st.metric("Total Won", f"${st.session_state.total_won}")

    if st.button("RESET GAME"):
        for key in list(st.session_state.keys()):
            del st.session_state[key]
        st.rerun()

# MAIN TITLE
st.markdown('<div class="main-title">GOLDEN JACKPOT</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">BIG WINS AWAIT</div>', unsafe_allow_html=True)




# DEPOSIT SECTION (MAIN AREA)

st.markdown("### DEPOSIT FUNDS")

col1, col2 = st.columns([3,1])

with col1:
    deposit_amount = st.number_input(
        "Enter deposit amount",
        min_value=0,
        step=100,
        value=0
    )

with col2:
    st.write("")
    if st.button("DEPOSIT"):
        if deposit_amount > 0:
            st.session_state.balance += deposit_amount
            st.session_state.balance_history.append(st.session_state.balance)
            st.success(f"Deposited ${deposit_amount}")
            st.rerun()
        else:
            st.error("Enter valid amount")


# BALANCE DISPLAY
st.markdown(f"""
<div class="balance-box">
<h2>BALANCE: ${st.session_state.balance:,}</h2>
</div>
""", unsafe_allow_html=True)

st.divider()

#
# GAME CONTROLS

if st.session_state.balance > 0:

    col1, col2, col3, col4 = st.columns([2,2,2,2])

    with col1:
        lines = st.selectbox("Lines", [1,2,3])

    with col2:
        bet = st.number_input("Bet per line", min_value=1, value=10)

    with col3:
        total_bet = lines * bet
        st.write(f"Total Bet: ${total_bet}")

    with col4:
        spin_button = st.button("SPIN")

    if spin_button:

        if total_bet > st.session_state.balance:
            st.error("Not enough balance!")
        else:
            st.session_state.balance -= total_bet
            st.session_state.total_wagered += total_bet
            st.session_state.spins_count += 1

            st.session_state.slots = get_slotmachine_spin(
                ROWS, COLS, symbol_count
            )

            (
                st.session_state.winnings,
                st.session_state.winning_lines
            ) = check_winnings(
                st.session_state.slots,
                lines,
                bet,
                symbol_value
            )

            st.session_state.total_bet = total_bet
            st.session_state.total_won += st.session_state.winnings
            st.session_state.balance += st.session_state.winnings
            st.session_state.balance_history.append(st.session_state.balance)

            st.rerun()

else:
    st.warning("Out of money! Deposit to continue.")


# SLOT DISPLAY



if st.session_state.slots is not None:

    st.markdown('<div class="slot-frame">', unsafe_allow_html=True)

    for row in range(ROWS):
        cols = st.columns(COLS)
        for col_index in range(COLS):
            symbol = st.session_state.slots[col_index][row]
            is_winning = (row + 1) in st.session_state.winning_lines

            css_class = "slot-symbol-winning" if is_winning else "slot-symbol"

            cols[col_index].markdown(
                f'<div class="{css_class}">{symbol}</div>',
                unsafe_allow_html=True
            )

    st.markdown('</div>', unsafe_allow_html=True)

    st.write(f"Total Bet: ${st.session_state.total_bet}")
    st.write(f"Winnings: ${st.session_state.winnings}")

    if st.session_state.winning_lines:
        st.success(f"Winning Lines: {st.session_state.winning_lines}")
    else:
        st.info("No winning lines.")


# ANALYTICS
if st.session_state.spins_count > 0:

    st.divider()
    st.markdown("### BALANCE HISTORY")

    df = pd.DataFrame({
        "Spin": range(len(st.session_state.balance_history)),
        "Balance": st.session_state.balance_history
    })

    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=df["Spin"],
        y=df["Balance"],
        mode="lines+markers"
    ))

    st.plotly_chart(fig, use_container_width=True)

st.divider()
st.caption("Golden Jackpot Casino | Play Responsibly")
