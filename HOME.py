import streamlit as st

st.markdown("### Streamlit into your class")
st.caption(
    "2026. 01. 12. Workshop"
)


col_l, col_c, col_r = st.columns([1,2,1])
with col_c:
    st.image("https://raw.githubusercontent.com/MK316/gnu260112/main/images/bg01.png",
             caption="Teaching is one of the best ways to learn.", width=300)
    st.image("https://raw.githubusercontent.com/MK316/gnu260112/main/images/qr01.png",
             caption="Access QR", width=100)
