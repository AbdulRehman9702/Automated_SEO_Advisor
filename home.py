import streamlit as st
from streamlit_option_menu import option_menu

# Page Configuration
st.set_page_config(page_title="SEO Advisor", page_icon="📈", layout="wide")

# Navbar
with st.sidebar:
    selected = option_menu(
        menu_title=None,
        options=["Home", "About", "Services", "Contact"],
        icons=["house", "info-circle", "briefcase", "envelope"],
        menu_icon="cast",
        default_index=0,
    )

# Logo and Header
import streamlit as st

# Use the local image path
st.image(r"C:\Users\pc care\Downloads\StreamLit\logo.png", width=100)

st.title("SEO Advisor")
st.subheader("Your trusted partner for optimizing your online presence")

# Main Content
st.write(
    """
    Welcome to **SEO Advisor**! We specialize in helping businesses increase their online visibility and attract more customers.
    Explore our services to learn how we can help you achieve your digital marketing goals.
    """
)

# Get Started Button
if st.button("Get Started"):
    st.query_params(page="main")
# Footer
st.markdown(
    """
    <hr>
    <footer>
    <p style="text-align: center;">&copy; 2024 SEO Advisor. All rights reserved.</p>
    </footer>
    """,
    unsafe_allow_html=True,
)
