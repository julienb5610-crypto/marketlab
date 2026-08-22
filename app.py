"""

MarketLab - Homepage



This is the main entry point for the MarketLab Streamlit app.

Streamlit automatically treats this file as the "Home" page and

builds a sidebar with links to any pages found in the pages/ folder.

"""



import streamlit as st



# st.set_page_config() must be the first Streamlit command in the app.

# It controls the browser tab title, icon, and overall page layout.

st.set_page_config(

    page_title="MarketLab",

    page_icon="📊",

    layout="wide",

)



# --- Page Header ---

st.title("📊 MarketLab")

st.subheader("An independent student financial research platform")



st.markdown(

    """

    **MarketLab is a research tool, not a source of investment advice.**



    The goal of this project is to explore questions about financial markets

    using real historical data, basic statistics, and transparent,

    rule-based backtesting — the same way you might approach a science

    fair experiment, but applied to markets.



    MarketLab will never tell you what to buy or sell, and it will never

    try to predict future prices. Instead, it focuses on **understanding

    the past**: how prices have moved, how risky different assets have

    been, and whether simple strategies would have worked historically.

    """

)



st.divider()



# --- Overview of Sections ---

st.markdown("### What you can do here")



col1, col2, col3 = st.columns(3)



with col1:

    st.markdown("#### 🔍 Market Explorer")

    st.write(

        "Look up any stock ticker and view its historical price and "

        "volume data, along with basic statistics like volatility and "

        "maximum drawdown."

    )



with col2:

    st.markdown("#### 🧪 Strategy Lab")

    st.write(

        "(Coming soon) Build simple, rule-based trading strategies and "

        "backtest them against historical data to see how they would "

        "have performed."

    )



with col3:

    st.markdown("#### 📚 Research")

    st.write(

        "(Coming soon) Read original research notes and experiments "

        "exploring specific questions about how markets behave."

    )



st.divider()



st.markdown(

    """

    ---

    *Use the sidebar on the left to navigate between sections.*

    """

) 


