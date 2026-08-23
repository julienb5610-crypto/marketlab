"""
MarketLab - Learn Finance

This page teaches complete beginners the basic finance concepts used
throughout MarketLab: Total Return, Volatility, Maximum Drawdown, and
Moving Averages.

This is an EDUCATIONAL page only. It does not give investment advice,
recommendations, or predictions.
"""

import numpy as np
import pandas as pd
import plotly.graph_objects as go
import streamlit as st

st.set_page_config(
    page_title="Learn Finance - MarketLab",
    page_icon="📚",
    layout="wide",
)

st.title("📚 Learn Finance")
st.write(
    "MarketLab teaches finance concepts through real market data and "
    "hands-on experiments. This page walks through the core ideas used "
    "in Market Explorer and Strategy Lab — no prior finance background "
    "needed."
)

st.divider()


# ===========================================================================
# LESSON 1: TOTAL RETURN
# ===========================================================================

with st.expander("1️⃣ Total Return", expanded=True):
    st.markdown("#### What is it?")

    st.write(
        "Total return measures how much an investment's value changed "
        "over a period of time."
    )

    st.markdown("#### Why does it matter?")

    st.write(
        "It's the most basic way to answer the question: "
        "'Did this go up or down, and by how much?' "
        "It compares the beginning value with the ending value, "
        "but does not describe every movement that happened in between."
    )

    st.markdown("#### Simple example")

    ex_col1, ex_col2, ex_col3 = st.columns(3)

    ex_col1.metric("Starting Value", "$100")
    ex_col2.metric("Ending Value", "$120")
    ex_col3.metric("Total Return", "+20%")

    st.write(
        "The math: (120 − 100) ÷ 100 = 0.20, or **+20%**. "
        "If the ending value had instead been $80, the return would be "
        "(80 − 100) ÷ 100 = **−20%**."
    )

    st.markdown("#### MarketLab example")

    st.info(
        "In **Market Explorer**, the 'Total Return' metric compares the "
        "closing price on the first day of your selected date range with "
        "the closing price on the last day.",
        icon="🔍",
    )

    st.markdown("#### Key takeaway")

    st.success(
        "Total return tells you the overall change from start to end. "
        "It does not tell you how smooth or rough the path was."
    )

    st.markdown("#### 🧮 Try it yourself")

    try_col1, try_col2 = st.columns(2)

    with try_col1:
        start_value = st.number_input(
            "Starting value ($)",
            min_value=0.01,
            value=100.0,
            step=1.0,
            key="tr_start",
        )

    with try_col2:
        end_value = st.number_input(
            "Ending value ($)",
            min_value=0.0,
            value=120.0,
            step=1.0,
            key="tr_end",
        )

    user_return = (end_value - start_value) / start_value

    if user_return >= 0:
        st.success(f"Total Return: **+{user_return:.2%}**")
    else:
        st.warning(f"Total Return: **{user_return:.2%}**")


# ===========================================================================
# LESSON 2: VOLATILITY
# ===========================================================================

with st.expander("2️⃣ Volatility"):

    st.markdown("#### What is it?")

    st.write(
        "Volatility measures how much an investment's returns fluctuate "
        "over time."
    )

    st.markdown("#### Why does it matter?")

    st.write(
        "Two investments can end up with similar total returns but get "
        "there in very different ways. One might move relatively smoothly "
        "while the other experiences large swings. Volatility helps "
        "describe that difference."
    )

    st.markdown("#### Simple example")

    st.write("Compare two sequences of daily returns:")

    stable_returns = np.array(
        [0.01, -0.01, 0.01, 0.00, -0.01, 0.01, -0.01]
    )

    volatile_returns = np.array(
        [0.08, -0.10, 0.12, -0.09, 0.11, -0.08, 0.09]
    )

    comp_col1, comp_col2 = st.columns(2)

    with comp_col1:
        st.write("**Stable sequence**")
        st.write([f"{r:+.0%}" for r in stable_returns])

        st.metric(
            "Volatility (standard deviation)",
            f"{stable_returns.std():.2%}",
        )

    with comp_col2:
        st.write("**Highly variable sequence**")
        st.write([f"{r:+.0%}" for r in volatile_returns])

        st.metric(
            "Volatility (standard deviation)",
            f"{volatile_returns.std():.2%}",
        )

    st.write(
        "The second sequence has much larger daily swings, so its standard "
        "deviation — our measure of volatility — is much higher."
    )

    st.markdown("#### MarketLab example")

    st.info(
        "In **Market Explorer** and **Strategy Lab**, annualized volatility "
        "takes the standard deviation of daily returns and scales it to a "
        "yearly estimate using √252, an approximation of the number of "
        "trading days in a year.",
        icon="🔍",
    )

    st.markdown("#### Key takeaway")

    st.success(
        "Higher volatility means greater historical variation in returns. "
        "It does **not** automatically mean an investment is good or bad."
    )


# ===========================================================================
# LESSON 3: MAXIMUM DRAWDOWN
# ===========================================================================

with st.expander("3️⃣ Maximum Drawdown"):

    st.markdown("#### What is it?")

    st.write(
        "Maximum drawdown is the largest decline from a previous peak "
        "to a later low point within a selected period."
    )

    st.markdown("#### Why does it matter?")

    st.write(
        "Drawdown helps describe how severe historical downturns were. "
        "It answers a different question from total return: instead of "
        "asking how much the investment changed overall, it asks how large "
        "the worst peak-to-trough decline was."
    )

    st.markdown("#### Simple example")

    dd_prices = [100, 150, 105]

    dd_col1, dd_col2, dd_col3 = st.columns(3)

    dd_col1.metric("Day 1", f"${dd_prices[0]}")
    dd_col2.metric("Day 2 (peak)", f"${dd_prices[1]}")
    dd_col3.metric("Day 3 (low)", f"${dd_prices[2]}")

    example_drawdown = (
        (dd_prices[2] - dd_prices[1]) / dd_prices[1]
    )

    st.write(
        f"The price rises to a peak of $150 and then falls to $105. "
        f"The drawdown is measured **from the peak ($150)**: "
        f"(105 − 150) ÷ 150 = **{example_drawdown:.1%}**."
    )

    st.markdown("#### Why is this different from total return?")

    total_ret_example = (
        (dd_prices[2] - dd_prices[0]) / dd_prices[0]
    )

    st.write(
        f"The total return from Day 1 to Day 3 is "
        f"(105 − 100) ÷ 100 = **{total_ret_example:+.1%}**. "
        f"However, the price still experienced a "
        f"**{example_drawdown:.1%}** decline from its $150 peak. "
        "Total return and drawdown answer different questions."
    )

    st.markdown("#### MarketLab example")

    st.info(
        "In **Market Explorer** and **Strategy Lab**, MarketLab tracks "
        "the running peak at every point in time and then finds the "
        "largest decline from any previous peak.",
        icon="🔍",
    )

    st.markdown("#### Key takeaway")

    st.success(
        "Maximum drawdown shows the worst historical peak-to-trough "
        "decline in the selected period."
    )

    st.markdown("#### 🧮 Try it yourself")

    st.write(
        "Enter a short sequence of prices, separated by commas, "
        "to calculate its maximum drawdown:"
    )

    price_sequence_input = st.text_input(
        "Price sequence",
        value="100, 150, 105, 130, 90, 140",
        key="dd_input",
    )

    try:
        price_sequence = [
            float(p.strip())
            for p in price_sequence_input.split(",")
            if p.strip()
        ]
    except ValueError:
        price_sequence = []

        st.warning(
            "Please enter valid numbers separated by commas "
            "(for example: 100, 120, 90)."
        )

    if len(price_sequence) >= 2:

        price_series = pd.Series(price_sequence)

        running_max_series = price_series.cummax()

        drawdown_series = (
            price_series - running_max_series
        ) / running_max_series

        user_max_drawdown = drawdown_series.min()

        st.metric(
            "Maximum Drawdown",
            f"{user_max_drawdown:.2%}",
        )

        dd_fig = go.Figure()

        dd_fig.add_trace(
            go.Scatter(
                x=list(range(1, len(price_series) + 1)),
                y=price_series,
                mode="lines+markers",
                name="Price",
            )
        )

        dd_fig.update_layout(
            title="Your Price Sequence",
            xaxis_title="Day",
            yaxis_title="Price",
            height=350,
            margin=dict(
                l=40,
                r=40,
                t=60,
                b=40,
            ),
        )

        st.plotly_chart(
            dd_fig,
            use_container_width=True,
        )

    elif price_sequence_input.strip():

        st.warning(
            "Please enter at least two prices to calculate a drawdown."
        )


# ===========================================================================
# LESSON 4: MOVING AVERAGES
# ===========================================================================

with st.expander("4️⃣ Moving Averages"):

    st.markdown("#### What is it?")

    st.write(
        "A moving average is the average price over a fixed number of "
        "recent trading days. As each new trading day arrives, the oldest "
        "price drops out and the newest price enters."
    )

    st.markdown("#### Why does it matter?")

    st.write(
        "Daily prices can be noisy and jump around. A moving average "
        "smooths some of that short-term movement, making it easier to "
        "study broader patterns in historical prices."
    )

    st.markdown("#### Simple example")

    ma_prices = [10, 12, 11, 13, 14]

    st.write(
        f"Suppose the last 5 closing prices are: **{ma_prices}**"
    )

    five_day_ma = sum(ma_prices) / len(ma_prices)

    st.metric(
        "5-Day Moving Average",
        f"{five_day_ma:.2f}",
    )

    st.write(
        f"That's the average of these 5 numbers: "
        f"({' + '.join(str(p) for p in ma_prices)}) ÷ 5 = "
        f"**{five_day_ma:.2f}**."
    )

    st.write(
        "Tomorrow, the oldest price drops out and the newest price "
        "joins the calculation, so the average moves forward with time."
    )

    st.markdown("#### Why study moving averages?")

    st.write(
        "Researchers sometimes compare a **short-term** moving average "
        "with a **long-term** moving average. The short-term average "
        "reacts more quickly to recent prices, while the long-term "
        "average changes more slowly."
    )

    st.write(
        "A crossover between the two averages can be studied as a "
        "historical signal. However, a crossover by itself does not "
        "prove that future prices will move in a particular direction."
    )

    st.markdown("#### MarketLab example")

    st.info(
        "**Strategy Lab** implements a moving-average crossover strategy. "
        "The backtest assumes the strategy holds the stock when the "
        "short-term moving average is above the long-term moving average "
        "and holds cash when it is below.",
        icon="🧪",
    )

    st.markdown("#### Key takeaway")

    st.warning(
        "A historical backtest shows how a strategy would have performed "
        "using past data. It does **not** prove the strategy will work "
        "in the future."
    )


# ===========================================================================
# FOOTER
# ===========================================================================

st.divider()

st.caption(
    "MarketLab is an educational research tool. Nothing on this page or "
    "elsewhere in the app is investment advice or a recommendation to "
    "buy or sell any security."
)
