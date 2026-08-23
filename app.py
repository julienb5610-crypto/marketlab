"""
MarketLab - Homepage

MarketLab is an independent student-built financial research and
education platform focused on helping beginners understand markets
through data, experimentation, and transparent methodology.
"""

import streamlit as st

st.set_page_config(
    page_title="MarketLab",
    page_icon="📊",
    layout="wide",
)

# ---------------------------------------------------------------------------
# HEADER
# ---------------------------------------------------------------------------

st.title("📊 MarketLab")
st.subheader("Learn finance by exploring the markets.")

st.markdown(
    """
    **MarketLab is an independent student-built financial research and
    education platform.**

    Instead of simply telling you what a stock is doing, MarketLab helps
    you understand **why the numbers matter** by combining beginner-friendly
    explanations with real historical market data and interactive experiments.

    MarketLab is designed for people who are curious about finance but
    don't already have a finance background.
    """
)

st.divider()

# ---------------------------------------------------------------------------
# HOW IT HELPS BEGINNERS
# ---------------------------------------------------------------------------

st.header("🎓 Learn finance by doing")

st.write(
    "Finance can feel intimidating when you're first starting out. "
    "Terms like volatility, drawdown, moving averages, and returns can "
    "sound complicated when they're presented as definitions alone."
)

st.write(
    "MarketLab takes a different approach: **learn a concept, see a real "
    "example, then experiment with it yourself.**"
)

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("### 📚 Learn")
    st.write(
        "Understand fundamental finance concepts through simple explanations, "
        "examples, and interactive demonstrations."
    )

with col2:
    st.markdown("### 🔍 Explore")
    st.write(
        "Use real historical market data to see how concepts like returns, "
        "volatility, and drawdown appear in actual markets."
    )

with col3:
    st.markdown("### 🧪 Experiment")
    st.write(
        "Test simple, rule-based strategies against historical data and "
        "compare the results with a buy-and-hold approach."
    )

st.divider()

# ---------------------------------------------------------------------------
# WHAT'S INSIDE
# ---------------------------------------------------------------------------

st.header("What's inside MarketLab?")

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("#### 📚 Learn Finance")
    st.write(
        "Beginner-friendly lessons covering return, volatility, maximum "
        "drawdown, moving averages, and other concepts used throughout "
        "MarketLab."
    )

with col2:
    st.markdown("#### 🔍 Market Explorer")
    st.write(
        "Explore historical stock data and calculate statistics such as "
        "total return, annualized volatility, and maximum drawdown."
    )

with col3:
    st.markdown("#### 🧪 Strategy Lab")
    st.write(
        "Backtest a simple moving-average crossover strategy and compare "
        "its historical performance with buy-and-hold."
    )

st.divider()

# ---------------------------------------------------------------------------
# PHILOSOPHY
# ---------------------------------------------------------------------------

st.header("🔬 The MarketLab philosophy")

st.markdown(
    """
    MarketLab focuses on **research rather than prediction**.

    The platform does not try to tell users what stocks to buy or sell.
    Instead, it asks questions about historical market behavior and uses
    transparent calculations to investigate them.

    Every experiment should make it possible to understand:

    - **What question are we asking?**
    - **What data are we using?**
    - **How are we calculating the result?**
    - **What does the result actually tell us?**
    - **What are the limitations?**
    """
)

st.info(
    "Historical performance does not guarantee future results. "
    "MarketLab is an educational and research project, not financial advice.",
    icon="ℹ️",
)

st.divider()

# ---------------------------------------------------------------------------
# CREATOR
# ---------------------------------------------------------------------------

st.header("👨‍💻 About the project")

st.markdown(
    """
    **MarketLab was created by Julien Bouriakov as an independent student
    project exploring finance, programming, data analysis, and financial
    education.**

    The goal is to make financial concepts easier to understand by turning
    abstract definitions into things users can actually explore and test.
    """
)

st.caption("MarketLab • Built by Julien Bouriakov")
