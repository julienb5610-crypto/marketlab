"""
MarketLab - Strategy Lab

This page lets a user backtest a simple, rule-based trading strategy —
a moving-average crossover — against historical data, and compare it to
a simple buy-and-hold baseline.

This is an EDUCATIONAL HISTORICAL BACKTEST ONLY.
It does not predict future prices, does not give investment advice, and
does not generate real-time buy/sell signals for actual trading.
"""

import datetime as dt

import numpy as np
import pandas as pd
import plotly.graph_objects as go
import streamlit as st
import yfinance as yf

st.set_page_config(
    page_title="Strategy Lab - MarketLab",
    page_icon="🧪",
    layout="wide",
)

st.title("🧪 Strategy Lab")

st.write(
    "Test a simple **moving-average crossover** strategy against historical "
    "data and compare it with buy-and-hold. This is a historical backtest "
    "for educational purposes only — not a prediction or recommendation."
)

st.info(
    "**How the strategy works:** when the short-term average price is above "
    "the long-term average price, the strategy assumes you hold the stock. "
    "When the short-term average drops below the long-term average, the "
    "strategy assumes you hold cash instead.",
    icon="ℹ️",
)


# ---------------------------------------------------------------------------
# 1. USER INPUTS
# ---------------------------------------------------------------------------

col1, col2, col3 = st.columns([2, 1.5, 1.5])

with col1:
    ticker_input = st.text_input(
        "Stock ticker",
        value="AAPL",
    ).strip().upper()

with col2:
    start_date = st.date_input(
        "Start date",
        value=dt.date.today() - dt.timedelta(days=365 * 3),
        max_value=dt.date.today(),
    )

with col3:
    end_date = st.date_input(
        "End date",
        value=dt.date.today(),
        max_value=dt.date.today(),
    )

col4, col5 = st.columns(2)

with col4:
    short_window = st.number_input(
        "Short moving-average window (days)",
        min_value=2,
        max_value=200,
        value=20,
        step=1,
    )

with col5:
    long_window = st.number_input(
        "Long moving-average window (days)",
        min_value=3,
        max_value=400,
        value=50,
        step=1,
    )


# ---------------------------------------------------------------------------
# INPUT VALIDATION
# ---------------------------------------------------------------------------

if start_date >= end_date:
    st.error("Start date must be before end date.")
    st.stop()

if short_window >= long_window:
    st.error(
        "The short moving-average window must be smaller than the long window."
    )
    st.stop()

if not ticker_input:
    st.info(
        "Enter a ticker symbol above to get started "
        "(e.g. AAPL, MSFT, SPY)."
    )
    st.stop()


# ---------------------------------------------------------------------------
# 2. DATA FETCHING
# ---------------------------------------------------------------------------

@st.cache_data(ttl=3600)
def load_price_data(
    ticker: str,
    start: dt.date,
    end: dt.date,
) -> pd.DataFrame:
    """Download historical daily price data for a ticker from Yahoo Finance."""
    data = yf.download(
        ticker,
        start=start,
        end=end,
        progress=False,
    )
    return data


def flatten_columns(data: pd.DataFrame) -> pd.DataFrame:
    """Convert MultiIndex columns to simple column names if necessary."""
    if isinstance(data.columns, pd.MultiIndex):
        data.columns = data.columns.get_level_values(0)
    return data


with st.spinner(f"Fetching data for {ticker_input}..."):
    try:
        raw_data = load_price_data(
            ticker_input,
            start_date,
            end_date,
        )
    except Exception as e:
        st.error(
            f"Something went wrong while fetching data: {e}"
        )
        st.stop()

if raw_data.empty:
    st.error(
        f"No data found for ticker '{ticker_input}'. "
        "Double check the symbol and date range, then try again."
    )
    st.stop()

data = flatten_columns(raw_data).copy()

data = data.dropna(subset=["Close"])

if len(data) < long_window + 10:
    st.warning(
        f"Not enough historical data in this date range to use a "
        f"{long_window}-day moving average. Try a wider date range or a "
        f"smaller window."
    )
    st.stop()


# ---------------------------------------------------------------------------
# 3. STRATEGY LOGIC
# ---------------------------------------------------------------------------

data["Short_MA"] = (
    data["Close"]
    .rolling(window=short_window)
    .mean()
)

data["Long_MA"] = (
    data["Close"]
    .rolling(window=long_window)
    .mean()
)

# Signal:
# 1 = strategy wants to hold the stock
# 0 = strategy wants to hold cash
data["Signal"] = np.where(
    data["Short_MA"] > data["Long_MA"],
    1,
    0,
)

data = data.dropna(
    subset=["Short_MA", "Long_MA"]
).copy()

# Use yesterday's signal for today's return.
# This prevents look-ahead bias.
data["Position"] = (
    data["Signal"]
    .shift(1)
    .fillna(0)
)

# Daily return of the stock itself.
data["Daily_Return"] = (
    data["Close"]
    .pct_change()
)

# Strategy earns the stock return only while holding the stock.
data["Strategy_Return"] = (
    data["Position"] *
    data["Daily_Return"]
)

data = data.dropna(
    subset=["Daily_Return"]
).copy()


# ---------------------------------------------------------------------------
# 4. PERFORMANCE STATISTICS
# ---------------------------------------------------------------------------

def total_return(returns: pd.Series) -> float:
    """Total compounded return over the period."""
    return (1 + returns).prod() - 1


def annualized_volatility(returns: pd.Series) -> float:
    """Annualized volatility based on daily returns."""
    return returns.std() * np.sqrt(252)


def max_drawdown(returns: pd.Series) -> float:
    """Largest peak-to-trough decline."""
    cumulative = (1 + returns).cumprod()
    running_max = cumulative.cummax()
    drawdown = (
        cumulative - running_max
    ) / running_max

    return drawdown.min()


strategy_total_return = total_return(
    data["Strategy_Return"]
)

buyhold_total_return = total_return(
    data["Daily_Return"]
)

strategy_volatility = annualized_volatility(
    data["Strategy_Return"]
)

buyhold_volatility = annualized_volatility(
    data["Daily_Return"]
)

strategy_max_dd = max_drawdown(
    data["Strategy_Return"]
)

buyhold_max_dd = max_drawdown(
    data["Daily_Return"]
)

# Count position changes.
num_position_changes = int(
    (
        data["Position"]
        .diff()
        .fillna(0)
        != 0
    ).sum()
)


# ---------------------------------------------------------------------------
# 5. DISPLAY STATISTICS
# ---------------------------------------------------------------------------

st.subheader(
    f"{ticker_input} — Strategy vs. Buy-and-Hold"
)

metric_col1, metric_col2 = st.columns(2)

with metric_col1:
    st.markdown(
        "**📈 Moving-Average Strategy**"
    )

    st.metric(
        "Total Return",
        f"{strategy_total_return:.2%}",
    )

    st.metric(
        "Annualized Volatility",
        f"{strategy_volatility:.2%}",
    )

    st.metric(
        "Max Drawdown",
        f"{strategy_max_dd:.2%}",
    )

    st.metric(
        "Position Changes",
        num_position_changes,
    )


with metric_col2:
    st.markdown(
        "**🏦 Buy-and-Hold**"
    )

    st.metric(
        "Total Return",
        f"{buyhold_total_return:.2%}",
    )

    st.metric(
        "Annualized Volatility",
        f"{buyhold_volatility:.2%}",
    )

    st.metric(
        "Max Drawdown",
        f"{buyhold_max_dd:.2%}",
    )

    st.metric(
        "Position Changes",
        1,
    )


st.caption(
    "Position changes occur when the strategy switches between holding "
    "the stock and holding cash. This simplified backtest does not "
    "include transaction costs, taxes, or slippage."
)

st.divider()


# ---------------------------------------------------------------------------
# 6. PRICE + MOVING AVERAGES
# ---------------------------------------------------------------------------

price_fig = go.Figure()

price_fig.add_trace(
    go.Scatter(
        x=data.index,
        y=data["Close"],
        name="Close Price",
    )
)

price_fig.add_trace(
    go.Scatter(
        x=data.index,
        y=data["Short_MA"],
        name=f"Short MA ({short_window}-day)",
    )
)

price_fig.add_trace(
    go.Scatter(
        x=data.index,
        y=data["Long_MA"],
        name=f"Long MA ({long_window}-day)",
    )
)

price_fig.update_layout(
    title=f"{ticker_input} Price with Moving Averages",
    yaxis_title="Price ($)",
    height=450,
    margin=dict(
        l=40,
        r=40,
        t=60,
        b=40,
    ),
)

st.plotly_chart(
    price_fig,
    use_container_width=True,
)


# ---------------------------------------------------------------------------
# 7. CUMULATIVE GROWTH COMPARISON
# ---------------------------------------------------------------------------

data["Strategy_Growth"] = (
    1 + data["Strategy_Return"]
).cumprod()

data["BuyHold_Growth"] = (
    1 + data["Daily_Return"]
).cumprod()

growth_fig = go.Figure()

growth_fig.add_trace(
    go.Scatter(
        x=data.index,
        y=data["Strategy_Growth"],
        name="Strategy (MA Crossover)",
    )
)

growth_fig.add_trace(
    go.Scatter(
        x=data.index,
        y=data["BuyHold_Growth"],
        name="Buy-and-Hold",
    )
)

growth_fig.update_layout(
    title="Growth of $1 Invested",
    yaxis_title="Growth Multiple",
    height=450,
    margin=dict(
        l=40,
        r=40,
        t=60,
        b=40,
    ),
)

st.plotly_chart(
    growth_fig,
    use_container_width=True,
)


# ---------------------------------------------------------------------------
# 8. RAW DATA
# ---------------------------------------------------------------------------

with st.expander("View raw data table"):
    st.dataframe(
        data[
            [
                "Close",
                "Short_MA",
                "Long_MA",
                "Signal",
                "Position",
                "Daily_Return",
                "Strategy_Return",
            ]
        ],
        use_container_width=True,
    )
