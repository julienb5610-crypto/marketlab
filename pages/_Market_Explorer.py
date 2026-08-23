"""
MarketLab - Market Explorer

This page lets a user:
1. Enter a stock ticker and a date range
2. Download historical price data from Yahoo Finance (via yfinance)
3. View interactive price and volume charts (via Plotly)
4. See basic statistics: total return, average daily return,
   annualized volatility, and maximum drawdown

This page does NOT predict prices or recommend buying/selling anything.
It only describes what already happened, historically.
"""

import datetime as dt

import numpy as np
import pandas as pd
import plotly.graph_objects as go
import streamlit as st
import yfinance as yf
from plotly.subplots import make_subplots

st.set_page_config(
    page_title="Market Explorer - MarketLab",
    page_icon="🔍",
    layout="wide",
)

st.title("🔍 Market Explorer")
st.write(
    "Enter a ticker symbol to view its historical price and volume data, "
    "along with some basic statistics. This is historical analysis only — "
    "not a prediction or recommendation."
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
        value=dt.date.today() - dt.timedelta(days=365 * 2),
        max_value=dt.date.today(),
    )

with col3:
    end_date = st.date_input(
        "End date",
        value=dt.date.today(),
        max_value=dt.date.today(),
    )

if start_date >= end_date:
    st.error("Start date must be before end date.")
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


if not ticker_input:
    st.info(
        "Enter a ticker symbol above to get started "
        "(e.g. AAPL, MSFT, SPY)."
    )
    st.stop()

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

if len(data) < 2:
    st.warning(
        "Not enough data points in this date range to calculate statistics. "
        "Try widening the date range."
    )
    st.stop()


# ---------------------------------------------------------------------------
# 3. CALCULATIONS
# ---------------------------------------------------------------------------

daily_returns = data["Close"].pct_change().dropna()

total_return = (
    data["Close"].iloc[-1] / data["Close"].iloc[0]
) - 1

avg_daily_return = daily_returns.mean()

annualized_volatility = (
    daily_returns.std() * np.sqrt(252)
)

running_max = data["Close"].cummax()

drawdown = (
    data["Close"] - running_max
) / running_max

max_drawdown = drawdown.min()


# ---------------------------------------------------------------------------
# 4. DISPLAY STATISTICS
# ---------------------------------------------------------------------------

st.subheader(f"{ticker_input} — Key Statistics")

stat_col1, stat_col2, stat_col3, stat_col4 = st.columns(4)

stat_col1.metric(
    "Total Return",
    f"{total_return:.2%}",
)

stat_col2.metric(
    "Avg. Daily Return",
    f"{avg_daily_return:.3%}",
)

stat_col3.metric(
    "Annualized Volatility",
    f"{annualized_volatility:.2%}",
)

stat_col4.metric(
    "Max Drawdown",
    f"{max_drawdown:.2%}",
)

st.caption(
    "Total Return: overall % change from the first to the last day "
    "in this range. Volatility: a measure of how much the price swings "
    "around, scaled to a yearly figure. Max Drawdown: the largest "
    "peak-to-trough decline over this range."
)

st.divider()


# ---------------------------------------------------------------------------
# 5. CHARTS
# ---------------------------------------------------------------------------

fig = make_subplots(
    rows=2,
    cols=1,
    shared_xaxes=True,
    row_heights=[0.7, 0.3],
    vertical_spacing=0.05,
    subplot_titles=(
        f"{ticker_input} Closing Price",
        "Trading Volume",
    ),
)

fig.add_trace(
    go.Scatter(
        x=data.index,
        y=data["Close"],
        mode="lines",
        name="Close Price",
    ),
    row=1,
    col=1,
)

fig.add_trace(
    go.Bar(
        x=data.index,
        y=data["Volume"],
        name="Volume",
    ),
    row=2,
    col=1,
)

fig.update_layout(
    height=650,
    showlegend=False,
    margin=dict(
        l=40,
        r=40,
        t=60,
        b=40,
    ),
)

fig.update_yaxes(
    title_text="Price ($)",
    row=1,
    col=1,
)

fig.update_yaxes(
    title_text="Shares",
    row=2,
    col=1,
)

st.plotly_chart(
    fig,
    use_container_width=True,
)


# ---------------------------------------------------------------------------
# 6. RAW DATA
# ---------------------------------------------------------------------------

with st.expander("View raw data table"):
    st.dataframe(
        data,
        use_container_width=True,
    )
