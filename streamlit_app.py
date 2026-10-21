import streamlit as st

st.set_page_config(page_title="Nicolas Minguez Aguirre")

pg = st.navigation(
    {
        "Projects": [st.Page("blackjack_st.py", title="Blackjack Simulator"), 
                     st.Page("intro_stat_st.py", title="Random Variables")]
    }
)
pg.run()