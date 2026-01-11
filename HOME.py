import streamlit as st

st.markdown("### 🐾 Streamlit into your class")
st.caption("2026. 01. 12. Workshop")


col_l, col_c, col_r = st.columns([0.5, 2, 0.5])

with col_c:
    st.markdown(
        """
        <div style="text-align: center;">
            <img src="https://raw.githubusercontent.com/MK316/gnu260112/main/images/bg01.png" width="300"><br>
            <em>Teaching is one of the best ways to learn.</em><br><br>
            <img src="https://raw.githubusercontent.com/MK316/gnu260112/main/images/qr01.png" width="100"><br>
            <em>Access QR</em>
        </div>
        """,
        unsafe_allow_html=True
    )

